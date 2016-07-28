/**
 * Created by nokadmin on 24.05.16.
 * Loads and Lists all rounds
 */
(function () {
    'use strict';

    angular.module('app.controller.round.list', [])
        .controller('roundListController', ['$scope', '$http',
            function ($scope, $http) {
                $http.get('/api/rounds/').success(function(result){
                    $scope.rounds = result.results;
                })
            }]);
})();