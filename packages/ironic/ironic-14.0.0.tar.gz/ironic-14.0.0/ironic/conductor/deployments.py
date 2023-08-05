#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

"""Functionality related to deploying and undeploying."""

import tempfile

from ironic_lib import metrics_utils
from oslo_db import exception as db_exception
from oslo_log import log
from oslo_utils import excutils
from oslo_utils import versionutils

from ironic.common import exception
from ironic.common.i18n import _
from ironic.common import release_mappings as versions
from ironic.common import states
from ironic.common import swift
from ironic.conductor import notification_utils as notify_utils
from ironic.conductor import steps as conductor_steps
from ironic.conductor import task_manager
from ironic.conductor import utils
from ironic.conf import CONF
from ironic.objects import fields

LOG = log.getLogger(__name__)

METRICS = metrics_utils.get_metrics_logger(__name__)

# NOTE(rloo) This is used to keep track of deprecation warnings that have
# already been issued for deploy drivers that do not use deploy steps.
_SEEN_NO_DEPLOY_STEP_DEPRECATIONS = set()


@METRICS.timer('do_node_deploy')
@task_manager.require_exclusive_lock
def do_node_deploy(task, conductor_id=None, configdrive=None):
    """Prepare the environment and deploy a node."""
    node = task.node

    try:
        if configdrive:
            if isinstance(configdrive, dict):
                configdrive = utils.build_configdrive(node, configdrive)
            _store_configdrive(node, configdrive)
    except (exception.SwiftOperationError, exception.ConfigInvalid) as e:
        with excutils.save_and_reraise_exception():
            utils.deploying_error_handler(
                task,
                ('Error while uploading the configdrive for %(node)s '
                 'to Swift') % {'node': node.uuid},
                _('Failed to upload the configdrive to Swift. '
                  'Error: %s') % e,
                clean_up=False)
    except db_exception.DBDataError as e:
        with excutils.save_and_reraise_exception():
            # NOTE(hshiina): This error happens when the configdrive is
            #                too large. Remove the configdrive from the
            #                object to update DB successfully in handling
            #                the failure.
            node.obj_reset_changes()
            utils.deploying_error_handler(
                task,
                ('Error while storing the configdrive for %(node)s into '
                 'the database: %(err)s') % {'node': node.uuid, 'err': e},
                _("Failed to store the configdrive in the database. "
                  "%s") % e,
                clean_up=False)
    except Exception as e:
        with excutils.save_and_reraise_exception():
            utils.deploying_error_handler(
                task,
                ('Unexpected error while preparing the configdrive for '
                 'node %(node)s') % {'node': node.uuid},
                _("Failed to prepare the configdrive. Exception: %s") % e,
                traceback=True, clean_up=False)

    try:
        task.driver.deploy.prepare(task)
    except exception.IronicException as e:
        with excutils.save_and_reraise_exception():
            utils.deploying_error_handler(
                task,
                ('Error while preparing to deploy to node %(node)s: '
                 '%(err)s') % {'node': node.uuid, 'err': e},
                _("Failed to prepare to deploy: %s") % e,
                clean_up=False)
    except Exception as e:
        with excutils.save_and_reraise_exception():
            utils.deploying_error_handler(
                task,
                ('Unexpected error while preparing to deploy to node '
                 '%(node)s') % {'node': node.uuid},
                _("Failed to prepare to deploy. Exception: %s") % e,
                traceback=True, clean_up=False)

    try:
        # This gets the deploy steps (if any) and puts them in the node's
        # driver_internal_info['deploy_steps'].
        conductor_steps.set_node_deployment_steps(task)
    except exception.InstanceDeployFailure as e:
        with excutils.save_and_reraise_exception():
            utils.deploying_error_handler(
                task,
                'Error while getting deploy steps; cannot deploy to node '
                '%(node)s. Error: %(err)s' % {'node': node.uuid, 'err': e},
                _("Cannot get deploy steps; failed to deploy: %s") % e)

    steps = node.driver_internal_info.get('deploy_steps', [])

    new_rpc_version = True
    release_ver = versions.RELEASE_MAPPING.get(CONF.pin_release_version)
    if release_ver:
        new_rpc_version = versionutils.is_compatible('1.45',
                                                     release_ver['rpc'])

    if not steps or not new_rpc_version:
        # TODO(rloo): This if.. (and the above code wrt rpc version)
        # can be deleted after the deprecation period when we no
        # longer support drivers with no deploy steps.
        # Note that after the deprecation period, there needs to be at least
        # one deploy step. If none, the deployment fails.

        if steps:
            info = node.driver_internal_info
            info.pop('deploy_steps')
            node.driver_internal_info = info
            node.save()

        # We go back to using the old way, if:
        # - out-of-tree driver hasn't yet converted to using deploy steps, or
        # - we're in the middle of a rolling upgrade. This is to prevent the
        #   corner case of having new conductors with old conductors, and
        #   a node is deployed with a new conductor (via deploy steps), but
        #   after the deploy_wait, the node gets handled by an old conductor.
        #   To avoid this, we need to wait until all the conductors are new,
        # signalled by the RPC API version being '1.45'.
        _old_rest_of_do_node_deploy(task, conductor_id, not steps)
    else:
        do_next_deploy_step(task, 0, conductor_id)


def _old_rest_of_do_node_deploy(task, conductor_id, no_deploy_steps):
    """The rest of the do_node_deploy() if not using deploy steps.

    To support out-of-tree drivers that have not yet migrated to using
    deploy steps.

    :param no_deploy_steps: Boolean; True if there are no deploy steps.
    """
    # TODO(rloo): This method can be deleted after the deprecation period
    #             for supporting drivers with no deploy steps.

    if no_deploy_steps:
        deploy_driver_name = task.driver.deploy.__class__.__name__
        if deploy_driver_name not in _SEEN_NO_DEPLOY_STEP_DEPRECATIONS:
            LOG.warning('Deploy driver %s does not support deploy steps; this '
                        'will be required starting with the Stein release.',
                        deploy_driver_name)
            _SEEN_NO_DEPLOY_STEP_DEPRECATIONS.add(deploy_driver_name)

    node = task.node
    try:
        new_state = task.driver.deploy.deploy(task)
    except exception.IronicException as e:
        with excutils.save_and_reraise_exception():
            utils.deploying_error_handler(
                task,
                ('Error in deploy of node %(node)s: %(err)s' %
                 {'node': node.uuid, 'err': e}),
                _("Failed to deploy: %s") % e)
    except Exception as e:
        with excutils.save_and_reraise_exception():
            utils.deploying_error_handler(
                task,
                ('Unexpected error while deploying node %(node)s' %
                 {'node': node.uuid}),
                _("Failed to deploy. Exception: %s") % e,
                traceback=True)

    # Update conductor_affinity to reference this conductor's ID
    # since there may be local persistent state
    node.conductor_affinity = conductor_id

    # NOTE(deva): Some drivers may return states.DEPLOYWAIT
    #             eg. if they are waiting for a callback
    if new_state == states.DEPLOYDONE:
        _start_console_in_deploy(task)
        task.process_event('done')
        LOG.info('Successfully deployed node %(node)s with '
                 'instance %(instance)s.',
                 {'node': node.uuid, 'instance': node.instance_uuid})
    elif new_state == states.DEPLOYWAIT:
        task.process_event('wait')
    else:
        LOG.error('Unexpected state %(state)s returned while '
                  'deploying node %(node)s.',
                  {'state': new_state, 'node': node.uuid})
    node.save()


@task_manager.require_exclusive_lock
def do_next_deploy_step(task, step_index, conductor_id):
    """Do deployment, starting from the specified deploy step.

    :param task: a TaskManager instance with an exclusive lock
    :param step_index: The first deploy step in the list to execute. This
        is the index (from 0) into the list of deploy steps in the node's
        driver_internal_info['deploy_steps']. Is None if there are no steps
        to execute.
    """
    node = task.node
    if step_index is None:
        steps = []
    else:
        steps = node.driver_internal_info['deploy_steps'][step_index:]

    LOG.info('Executing %(state)s on node %(node)s, remaining steps: '
             '%(steps)s', {'node': node.uuid, 'steps': steps,
                           'state': node.provision_state})

    # Execute each step until we hit an async step or run out of steps
    for ind, step in enumerate(steps):
        # Save which step we're about to start so we can restart
        # if necessary
        node.deploy_step = step
        driver_internal_info = node.driver_internal_info
        driver_internal_info['deploy_step_index'] = step_index + ind
        node.driver_internal_info = driver_internal_info
        node.save()
        interface = getattr(task.driver, step.get('interface'))
        LOG.info('Executing %(step)s on node %(node)s',
                 {'step': step, 'node': node.uuid})
        try:
            result = interface.execute_deploy_step(task, step)
        except exception.IronicException as e:
            if isinstance(e, exception.AgentConnectionFailed):
                if task.node.driver_internal_info.get('deployment_reboot'):
                    LOG.info('Agent is not yet running on node %(node)s after '
                             'deployment reboot, waiting for agent to come up '
                             'to run next deploy step %(step)s.',
                             {'node': node.uuid, 'step': step})
                    driver_internal_info['skip_current_deploy_step'] = False
                    node.driver_internal_info = driver_internal_info
                    task.process_event('wait')
                    return
            log_msg = ('Node %(node)s failed deploy step %(step)s. Error: '
                       '%(err)s' %
                       {'node': node.uuid, 'step': node.deploy_step, 'err': e})
            utils.deploying_error_handler(
                task, log_msg,
                _("Failed to deploy: %s") % node.deploy_step)
            return
        except Exception as e:
            log_msg = ('Node %(node)s failed deploy step %(step)s with '
                       'unexpected error: %(err)s' %
                       {'node': node.uuid, 'step': node.deploy_step, 'err': e})
            utils.deploying_error_handler(
                task, log_msg,
                _("Failed to deploy. Exception: %s") % e, traceback=True)
            return

        if ind == 0:
            # We've done the very first deploy step.
            # Update conductor_affinity to reference this conductor's ID
            # since there may be local persistent state
            node.conductor_affinity = conductor_id
            node.save()

        # Check if the step is done or not. The step should return
        # states.DEPLOYWAIT if the step is still being executed, or
        # None if the step is done.
        # NOTE(deva): Some drivers may return states.DEPLOYWAIT
        #             eg. if they are waiting for a callback
        if result == states.DEPLOYWAIT:
            # Kill this worker, the async step will make an RPC call to
            # continue_node_deploy() to continue deploying
            LOG.info('Deploy step %(step)s on node %(node)s being '
                     'executed asynchronously, waiting for driver.',
                     {'node': node.uuid, 'step': step})
            task.process_event('wait')
            return
        elif result is not None:
            # NOTE(rloo): This is an internal/dev error; shouldn't happen.
            log_msg = (_('While executing deploy step %(step)s on node '
                       '%(node)s, step returned unexpected state: %(val)s')
                       % {'step': step, 'node': node.uuid, 'val': result})
            utils.deploying_error_handler(
                task, log_msg,
                _("Failed to deploy: %s") % node.deploy_step)
            return

        LOG.info('Node %(node)s finished deploy step %(step)s',
                 {'node': node.uuid, 'step': step})

    # Finished executing the steps. Clear deploy_step.
    node.deploy_step = None
    driver_internal_info = node.driver_internal_info
    driver_internal_info['deploy_steps'] = None
    driver_internal_info.pop('deploy_step_index', None)
    driver_internal_info.pop('deployment_reboot', None)
    driver_internal_info.pop('deployment_polling', None)
    # Remove the agent_url cached from the deployment.
    driver_internal_info.pop('agent_url', None)
    node.driver_internal_info = driver_internal_info
    node.save()

    _start_console_in_deploy(task)

    task.process_event('done')
    LOG.info('Successfully deployed node %(node)s with '
             'instance %(instance)s.',
             {'node': node.uuid, 'instance': node.instance_uuid})


def _get_configdrive_obj_name(node):
    """Generate the object name for the config drive."""
    return 'configdrive-%s' % node.uuid


def _store_configdrive(node, configdrive):
    """Handle the storage of the config drive.

    If configured, the config drive data are uploaded to a swift endpoint.
    The Node's instance_info is updated to include either the temporary
    Swift URL from the upload, or if no upload, the actual config drive data.

    :param node: an Ironic node object.
    :param configdrive: A gzipped and base64 encoded configdrive.
    :raises: SwiftOperationError if an error occur when uploading the
             config drive to the swift endpoint.
    :raises: ConfigInvalid if required keystone authorization credentials
             with swift are missing.


    """
    if CONF.deploy.configdrive_use_object_store:
        # NOTE(lucasagomes): No reason to use a different timeout than
        # the one used for deploying the node
        timeout = (CONF.conductor.configdrive_swift_temp_url_duration
                   or CONF.conductor.deploy_callback_timeout
                   # The documented default in ironic.conf.conductor
                   or 1800)
        container = CONF.conductor.configdrive_swift_container
        object_name = _get_configdrive_obj_name(node)

        object_headers = {'X-Delete-After': str(timeout)}

        with tempfile.NamedTemporaryFile(dir=CONF.tempdir) as fileobj:
            fileobj.write(configdrive)
            fileobj.flush()

            swift_api = swift.SwiftAPI()
            swift_api.create_object(container, object_name, fileobj.name,
                                    object_headers=object_headers)
            configdrive = swift_api.get_temp_url(container, object_name,
                                                 timeout)

    i_info = node.instance_info
    i_info['configdrive'] = configdrive
    node.instance_info = i_info
    node.save()


def _start_console_in_deploy(task):
    """Start console at the end of deployment.

    Console is stopped at tearing down not to be exposed to an instance user.
    Then, restart at deployment.

    :param task: a TaskManager instance with an exclusive lock
    """

    if not task.node.console_enabled:
        return

    notify_utils.emit_console_notification(
        task, 'console_restore', fields.NotificationStatus.START)
    try:
        task.driver.console.start_console(task)
    except Exception as err:
        msg = (_('Failed to start console while deploying the '
                 'node %(node)s: %(err)s.') % {'node': task.node.uuid,
                                               'err': err})
        LOG.error(msg)
        task.node.last_error = msg
        task.node.console_enabled = False
        task.node.save()
        notify_utils.emit_console_notification(
            task, 'console_restore', fields.NotificationStatus.ERROR)
    else:
        notify_utils.emit_console_notification(
            task, 'console_restore', fields.NotificationStatus.END)
