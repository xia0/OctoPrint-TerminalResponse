$(function() {
    function TerminalResponseViewModel(parameters) {
        var self = this;

        self.global_settings = parameters[0];

        self.regex_definitions = ko.observableArray();

        self.addCommandDefinition = function() {
            self.regex_definitions.push({regex:"", type:"", command:"", enabled: true});
        };

        self.removeCommandDefinition = function(definition) {
            self.regex_definitions.remove(definition);
        };

        self.onBeforeBinding = function () {
            self.settings = self.global_settings.settings.plugins.terminalresponse;
            self.regex_definitions(self.settings.regex_definitions.slice(0));
        };

        self.onSettingsBeforeSave = function () {
            self.global_settings.settings.plugins.terminalresponse.regex_definitions(self.regex_definitions.slice(0));
        }
    }

    ADDITIONAL_VIEWMODELS.push([
        TerminalResponseViewModel,
        ["settingsViewModel"],
        ["#settings_plugin_terminalresponse"]
    ]);
});
