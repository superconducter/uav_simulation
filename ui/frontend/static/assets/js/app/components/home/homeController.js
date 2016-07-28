/**
 * Created by J.D. on 11.07.16.
 *
 * This class provides the landing main navigation menu.
 * It provides the data for all occuring stats.
 */
(function () {
    'use strict';

    angular.module('app.controller.home.controller', [])
        .controller('homeController', ['$scope', '$http',
            function ($scope, $http) {
                $http.get('/api/statistics/').success(function (data) {
                    $scope.statistics = data;

                  //  console.log('Statistics : ', data);

                });
            }]);
})();