/**
 * Created by nokadmin on 24.05.16.
 * This controller displays a list of all agents
 */
(function () {
    'use strict';

    angular.module('app.controller.agent.list', [])
        .controller('agentListController', ['$scope', '$http', '$resource',
            function ($scope, $http, $resource) {
                var AgentAPI = $resource('/api/agents/:sim_id', {}, {
                });
                $scope.view = {
                    offset: 0,
                    limit: 15

                };

                $scope.load = function (offset) {
                    if (offset == null){
                        offset = $scope.view.offset;
                    }
                    AgentAPI.get({
                        'offset': offset,
                        'limit': $scope.view.limit
                    }, function (result) {
                        console.log(result);
                        $scope.response = result;
                        $scope.view.offset = offset;
                        $scope.view.upperLimit = offset + $scope.view.limit > result.count ? result.count: offset + $scope.view.limit;
                        $scope.drones = result.results.map(function (drone) {
                            drone.layer = "drones";
                            return drone
                        });
                    });
                };
                $scope.drones = [];
                $scope.load();
                /*$http.get('/api/agents/?limit=300').success(function(result) {
                    $scope.results = result;
                    $scope.drones = result.results.map(function (drone) {
                        drone.layer = "drones";
                        return drone
                    });
                });*/
            }]);
            })();