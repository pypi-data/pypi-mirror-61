#
# Copyright (c) Dell Inc., or its subsidiaries. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#

from __future__ import division

import datetime
import json
import logging
import os
import re

# P3 Libraries
from p3_test_driver import p3_plugin_manager
from p3_test_driver.p3_test import TimeoutException, StorageTest
from p3_test_driver.p3_util import record_result
from p3_test_driver.system_command import system_command, time_duration_to_seconds

_default_configs = {
    'simple': {
        'print_output': True,
        },
    }


class PluginInfo(p3_plugin_manager.IP3Plugin):
    def get_plugin_info(self):
        return [
            {
            'class_type': 'test', 
            'class_name': 'simple',
            'class': SimpleTest,
            },
        ]


class SimpleTest(StorageTest):
    """P3 generic test class that can be used to run tests consisting of a single command."""

    def __init__(self, test_config, default_configs=_default_configs):
        super(SimpleTest, self).__init__(test_config, default_configs=default_configs)

    def configure_environment(self):
        self.configure_storage()

    def run_test(self):
        rec = self.test_config

        self.configure_environment()

        # Build environment for commands.
        env = None
        command_env = rec.get('command_env')
        if command_env:
            env = dict(os.environ)
            env.update(command_env)

        # Run pre-commands.
        for pre_command in rec.get('pre_commands', []):
            pre_command_template = pre_command['command_template']
            if isinstance(pre_command_template, list):
                cmd = [x % rec for x in pre_command_template]
            else:
                cmd = pre_command_template % rec
            return_code, output, errors = system_command(cmd,
                print_command=True,
                print_output=True,
                timeout=rec.get('command_timeout_sec',None),
                raise_on_error=True,
                shell=not isinstance(cmd, list),
                noop=False,
                env=env)
            if 'key' in pre_command:
                rec[pre_command['key']] = output.rstrip()

        # Build command from command template.
        if 'command' not in rec and 'command_template' in rec:
            if isinstance(rec['command_template'], list):
                rec['command'] = [x % rec for x in rec['command_template']]
            else:
                rec['command'] = rec['command_template'] % rec
        cmd = rec['command']

        if 'command_shell' not in rec:
            rec['command_shell'] = not isinstance(cmd, list)

        rec['_status_node'].set_status('Running command: %s' % str(cmd))

        with self.metrics_collector_context():
            self.start_metrics()

            t0 = datetime.datetime.utcnow()
            
            return_code, output, errors = system_command(cmd, 
                print_command=True, 
                print_output=rec['print_output'], 
                timeout=rec.get('command_timeout_sec',None), 
                raise_on_error=False,
                shell=rec['command_shell'],
                noop=rec['noop'], 
                env=env)

            t1 = datetime.datetime.utcnow()
            td = t1 - t0

            logging.info('exit_code=%d' % return_code)

            # Parse any output matching a regex pattern in the json_regex list.
            for json_regex in rec.get('json_regex', []):
                m = re.search(json_regex, output, flags=re.MULTILINE)
                if m:
                    json_str = m.groups()[0]
                    d = json.loads(json_str)
                    rec.update(d)

            rec['utc_begin'] = t0.isoformat()
            rec['utc_end'] = t1.isoformat()
            rec['elapsed_sec'] = time_duration_to_seconds(td)
            rec['error'] = (return_code != 0)
            rec['exit_code'] = return_code
            rec['command_timed_out'] = (return_code == -1)
            rec['output'] = output
            rec['errors'] = errors            
            rec['run_as_test'] = rec['test']
            if 'record_as_test' in rec:
                rec['test'] = rec['record_as_test']

        if 'result_filename' in rec:
            record_result(rec, rec['result_filename'])

        if rec['command_timed_out']:
            raise TimeoutException()
        if rec['error']:
            raise Exception('Command failed')
