/*
Lists all simulations
 */

(function () {
    'use strict';

    angular.module('app.controller.simulation.list', [])
        .controller('simulationListController', ['$scope', '$http', '$resource',
            function ($scope, $http, $resource) {
                var SimulationAPI = $resource('/api/simulations/:sim_id', {}, {
                });
                $scope.view = {};
                $scope.load = function (offset) {
                    if (offset == null){
                        offset = $scope.view.offset;
                    }
                    SimulationAPI.get({
                        'name__icontains': $scope.view.search,
                        'offset': offset,
                        'limit': 15
                    }, function (result) {
                        $scope.response = result;
                        $scope.view.offset = offset;
                    });
                };
                $scope.delete = function(sim_id){
                    $http.delete('/api/simulations/'+ sim_id).success(function (result) {
                        $scope.load();
                    });
                };
                $scope.load();

            }]);
            })();