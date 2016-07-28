/**
 * Created by nkuehl on 04/07/16.
 * This Service translates the drones from the server into a good format for the Playback framework.
 */

(function () {
    'use strict';

    angular.module('app.factory.dataParser', ['app.factory.settingsParser', 'app.factory.demoData'])
        .factory('dataParser', ['settingsParser', 'Flash', 'demoData',
            function (settingsParser, Flash, demoData) {
                function translateData(settings, agentsOfSimulation) {
                    var moving = [];
                    var statics = [];

                    // Playback requires array
                    // Convert the data from the backend into a usable format for the frontend
                    var raw_agent;
                    var agent;
                    var translatedData = settingsParser(settings, []); // translate settings first

                    Object.keys(agentsOfSimulation).forEach(
                        function (key) {
                            raw_agent = agentsOfSimulation[key];
                            agent = demoData.emptyTrack();
                            agent.title = "Agent #" + key;
                            agent.visualType = raw_agent.type;

                            agent.geometry.coordinates = raw_agent.coordinates;
                            agent.properties.changes = raw_agent.status.map(function (obj) {
                                return {'status': obj};
                            });
                            agent.properties.time = raw_agent.round.map(function (obj) {
                                return obj * 1000;
                            });

                            if (isStaticType(translatedData, raw_agent.type)) {
                                statics.push(agent);
                            } else {
                                moving.push(agent);
                            }

                        }
                    );

                    translatedData.static = statics;
                    translatedData.moving = moving; // Add agents to data

                    return translatedData;
                }

                function isStaticType(settings, typeName) {
                    var typeInfo = L.Sim.getTypeInfo(settings, typeName);
                    return typeInfo.static || false;

                    // console.log('isStatic: ', typeName, ' --> ', L); //.ui.objectTypes);
                }

                return function (settings, dronesOfSimulation) {
                    console.log('SETTINGS in dataFactory >>', settings);

                    if (Object.keys(dronesOfSimulation).length > 0) {
                        return translateData(settings, dronesOfSimulation);
                    }
                    Flash.create('warning', 'Simulation is empty. Using demo data');
                    return demoData.trackData();
                };
            }])
})();

