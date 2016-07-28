(function () {
    'use strict';

    angular.module('app.controller.map', ['ngFlash', 'app.factory.settingsParser', 'app.factory.dataParser', 'app.factory.demoData', 'app.factory.mapWrapper'])
        .controller('mapController', ['$scope', '$http', '$routeParams', 'dataParser', 'demoData', 'mapWrapperFactory',


            function ($scope, $http, $routeParams, dataParser, demoData, MapWrapper) {

                // Load details from selected simulation
                $http.get('/api/simulations/' + $routeParams.simulationId + '/').success(function (simulation) {
                        $scope.simulation = simulation;

                        // Set title
                        setTitle(simulation.name);

                        console.log(simulation);

                        var old_simulation = simulation;
                        var checkDataTimeout = 1000;
                        var checkData = function () {
                            console.log('Completed?', old_simulation.rounds_count);

                            $http.get('/api/simulations/' + $routeParams.simulationId + '/').success(function (new_simulation) {
                                console.log('new simulation: ', new_simulation);
                                if (old_simulation.rounds_count < new_simulation.rounds_count) {
                                    console.log('New data avaiable');
                                    $('#newdata').show();
                                    $('#loading').hide();

                                } else {
                                    // No new data
                                    if (new_simulation.completed) {
                                        $('#loading').hide();
                                    } else {
                                        console.log('No new data, but yet not completed,.. try again');
                                        checkDataTimeout *= 1.5;
                                        window.setTimeout(checkData, checkDataTimeout);
                                    }
                                }
                            });
                        };

                        if (simulation.completed == false) {
                            // loadingButton = true;
                            $('#loading').show();
                            window.setTimeout(checkData, checkDataTimeout);
                        }

                        console.log('Settings from API: ', simulation.settings);

                        // Load object (drone) details
                        $http.get('/api/agents2/?simulation=' + simulation.id).success(function (dronesOfSimulation) {
                            // Load Events
                            var translatedData = dataParser(simulation.settings.ui, dronesOfSimulation);

                            $http.get('/api/events2/?simulation=' + simulation.id).success(function (events) {
                                // Prepare map
                                var map = new MapWrapper('map');

                                var translatedEvents = {};
                                var last_round = 0;
                                events.forEach(function (round) {
                                    translatedEvents[round.round_number] = round.events;
                                });

                                translatedData.events = translatedEvents;
                                // translatedData.static = demoStatic;

                                map.setData(translatedData);
                                $scope.data = translatedData;

                                $scope.toggleGroup = function ($event, group) {
                                    $('.group-' + group.id).toggle();
                                    if ($($event.currentTarget).text() == 'show') {
                                        $($event.currentTarget).text('hide');
                                    } else {
                                        $($event.currentTarget).text('show');
                                    }
                                };

                                // Draw map
                                map.init();
                            });

                        });

                    }
                )
            }

        ])
})
();