# coding=utf-8
from __future__ import absolute_import

import logging
import time
import os
import sys
import re
import string

import octoprint.plugin
import octoprint.settings

__plugin_name__ = "Terminal Response"
__plugin_version__ = "0.1"
__plugin_pythoncompat__ = ">=2.7,<4"

def __plugin_init__():
    global _plugin
    global __plugin_hooks__

    global __plugin_implementation__
    __plugin_implementation__ = TerminalResponsePlugin()

    __plugin_hooks__ = {
        "octoprint.comm.protocol.gcode.received": __plugin_implementation__.hook_terminal_response,
        "octoprint.plugin.softwareupdate.check_config": __plugin_implementation__.get_update_information
    }

class TerminalResponsePlugin(octoprint.plugin.TemplatePlugin,
              octoprint.plugin.AssetPlugin,
              octoprint.plugin.SettingsPlugin):

    def __init__(self):
        self.regex_definitions = {}

    def on_settings_initialized(self):
        self.reload_regex_definitions()

    def reload_regex_definitions(self):
        self.regex_definitions = {}

        regex_definitions_tmp = self._settings.get(["regex_definitions"])
        self._logger.debug("regex_definitions: %s" % regex_definitions_tmp)

        for definition in regex_definitions_tmp:
            self.regex_definitions[definition['regex']] = dict(type=definition['type'], command=definition['command'], enabled=definition['enabled'])
            self._logger.info("Add regex definition 'regex:%s' = %s" % (definition['regex'], definition['command']))

    def get_settings_defaults(self):
        return dict(
            regex_definitions = []
        )

    def on_settings_save(self, data):
        octoprint.plugin.SettingsPlugin.on_settings_save(self, data)
        self.reload_regex_definitions()

    def get_template_configs(self):
        return [
            dict(type="settings", name="Terminal Response", custom_bindings=True)
        ]

    def get_assets(self):
        return {
            "js": ["js/terminalresponse.js"]
        }

    def get_update_information(self):
        return dict(
        terminalresponse=dict(
        displayName="Terminal Response",
        displayVersion=self._plugin_version,

        # version check: github repository
        type="github_release",
        user="xia0",
        repo="OctoPrint-TerminalResponsePlugin",
        current=self._plugin_version,

        # update method: pip w/ dependency links
        pip="https://github.com/xia0/OctoPrint-TerminalResponsePlugin/archive/{target_version}.zip"
        )
    )

    def hook_terminal_response(self, comm, line, *args, **kwargs):
        for regex in self.regex_definitions:
            #self._logger.info(self.regex_definitions[regex])

            if self.regex_definitions[regex]["enabled"]:
                m = re.search(regex, line)
                if m:
                    command = self.regex_definitions[regex]["command"]

                    # Do replacement for numbered matches
                    for i in range(1, len(m.groups())+1):
                        command = string.replace(command, "("+str(i)+")", m.group(i))
                    for split_line in command.splitlines():
                        self._logger.info("Sending command: " + split_line)
                        self._printer.commands(split_line)

        return line
