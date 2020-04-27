# OctoPrint-TerminalResponse

Monitors OctoPrint terminal for your defined regular expressions. When it detects a match, it will send your commands. Code is based off [OctoPrint-ActionCommandsPlugin by benlye](https://github.com/benlye/OctoPrint-ActionCommandsPlugin).

## Setup

Install via the bundled [Plugin Manager](https://docs.octoprint.org/en/master/bundledplugins/pluginmanager.html)
or manually using this URL:

    https://github.com/xia0/OctoPrint-TerminalResponse/archive/master.zip

## Configuration

![Plugin settings](https://raw.githubusercontent.com/xia0/OctoPrint-TerminalResponse/master/screenshots/01.png)

Enter your regular expression on the left. Place values you would like to extract in parentheses. Enter your commands on the right with a new line for each command. Enter `(1)`, `(2)`, etc... to substitute your values.
