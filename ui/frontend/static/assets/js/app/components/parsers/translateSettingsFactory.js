/**
 * Created by nkuehl on 04/07/16.
 * This class translates the settings from the server into a usable format for the map. 
 * Ideally they should match very closely and thus this class very small.
 */

(function () {
    'use strict';

    angular.module('app.factory.settingsParser', [])
        .factory('settingsParser', [
            function () {
                var demoSettings = {
                    objectTypes: {
                        default: {
                            type: "awesome",
                            length: 10,
                            options: {
                                fillColor: "#ff0000"
                            },
                            status: {
                                "primary": {},
                                "warning": {
                                    fillColor: "#00ffff",
                                    weight: 10
                                },
                                "danger": {
                                    fillColor: "#ff0000",
                                    weight: 20
                                },
                                "success": {
                                    fillColor: "#00ff00",
                                    weight: 5
                                }
                            }
                        }
                    },
                    eventTypes: [],
                    events: [],
                    groups: []
                };
                var arrayToObjectByKey = function(someArr, key){
                    /**
                     * This function transforms an array into an object and uses @key to retrieve names for the properties
                     * @type {{}}
                     */
                    var ret = {};
                    someArr.forEach(function(element){
                        ret[element[key]] = element;
                        delete ret[element[key]][key];
                    });
                    return ret;
                };
                var parser = function (raw_settings, movingArr, events) {
                    // var raw_settings = raw_settings || { "objectTypes": [] };
                    // console.log('DEMO: ', demoSettings.objectTypes);
                    var settings = $.extend({}, raw_settings);

                    $.extend(settings, {
                        objectTypes: arrayToObjectByKey(raw_settings.objectTypes, "name") || demoSettings.objectTypes,
                        //objectTypes: demoSettings.objectTypes,

                        // eventTypes: raw_settings.eventTypes || [],
                        eventTypes: arrayToObjectByKey(raw_settings.eventTypes, "name") || demoSettings.eventTypes,
                        moving: movingArr || [],
                        events: events || [],
                        groups: []
                    });

                    return settings;
                };
                return parser;
    }])
})();
