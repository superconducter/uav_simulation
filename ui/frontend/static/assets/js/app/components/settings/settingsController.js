/**
 * Manages the loading, manipulating of settings. 
 * Allows running simulations
 */

(function () {
	'use strict';

	angular.module('app.controller.settings', ['ngResource','ngAnimate','toastr', 'app.directive.settings.ui', 'app.directive.settings.sim'])

		.controller("settingsController", [ '$scope', '$resource','toastr', '$location', '$http',
			function($scope, $resource, toastr, $location, $http) {
                // Set title
                setTitle('Settings');

                $scope.config = {ui: {}};
                $scope.importConfig = function (text) {
                    if(!text){
                        text = $scope.configFromText;
                    }
                    $scope.config = JSON.parse(text);
                };
                $scope.importConfigFromUrl = function (url){
                    if (!url){
                        url = '/static/simcore_demosettings.json';
                    }
                    $http.get(url).success(function (data) {
                        $scope.config = data;
                    });
                };
                $scope.importConfigFromUrl();

                $scope.importSelectedConfig = function () {
                    $scope.config = $scope.selectedConfig;
                };


                var ConfigAPI = $resource('/api/simulations/:action', {}, {
                    run: {
                        method: 'POST',
                        params: {
                            action: 'run'
                        }
                    }
                });
                ConfigAPI.get({'limit': 1000}, function (data) {
                    $scope.simulations = data.results;
                });
                $scope.saveConfig = function () {
                    ConfigAPI.run($scope.config, function (response) {
                        toastr.success('Saved Successfully!', 'Yeah!');
                        $location.path('simulations/' + response.identifier);
                    });
                };

            }])
})();