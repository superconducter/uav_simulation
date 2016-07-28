/**
 * Created by nokadmin on 06.07.16.
 */
/**
 * Created by nkuehl on 29/06/16.
 * This factory contains the UI part of the settings creator
 */


(function () {
    angular.module('app.directive.settings.ui', [])
        .directive('settingsUi', function () {
                return {
                    restrict: 'E',
                    scope: {settings: '=settings', name: '=name'},
                    templateUrl: function (_, attrs) {
                        return '/static/assets/js/app/components/settings/settingsUi/view.html';
                    },
                    controller: 'settingsUiController'
                }
            }
        ).controller('settingsUiController', ['$scope', function ($scope) {
        $scope.view = {
            objectTypes: [
                {
                    label: 'Rectangle',
                    value: 'rectangle'
                },
                {
                    label: 'Circle',
                    value: 'circle'
                },
                {
                    label: 'Awesome Marker',
                    value: 'awesome'
                },
                {
                    label: 'Icon(Experimental)',
                    value: 'icon'
                }
            ]
        };
        $scope.addEvent = function () {
            if (Array.isArray($scope.settings.eventTypes)) {
                $scope.settings.eventTypes.push({})
            } else {
                $scope.settings.eventTypes = [{}];
            }
        };
        $scope.addObjectType = function () {
            emptyObjectType = function () {
                return {
                    status: {},
                    options: {shadowSize: [10,10],
                        iconSize: [10,10]}
                }
            };
            if (Array.isArray($scope.settings.objectTypes)) {
                $scope.settings.objectTypes.push(emptyObjectType())
            } else {
                $scope.settings.objectTypes = [emptyObjectType()];
            }
        };

        $scope.removeItem = function (obj, item) {
            delete obj[item]
        };

        $scope.addStatus = function (objectType, statusName) {
            objectType.status[$scope.view.status] = {};
            $scope.view.status = '';
        };

        $scope.updateBackgroundPosition = function () {
            try{
                $scope.settings.backgroundPosition = [[$scope.view.background.start.x, $scope.view.background.start.y],[$scope.view.background.end.x, $scope.view.background.end.y]]
            }catch(TypeError){
            }
        };


        $scope.isEmpty = function (obj) {
            return !obj || Object.keys(obj).length == 0;
        };

        $scope.icons = ["automobile", "ban", "bank", "battery-0", "blind", "bomb", "bullseye", "cab", "camera", "child", "cloud", "comment", "diamond", "dot-circle-o", "envelope", "envelope-o", "exclamation", "eye", "fighter-jet", "fire", "flash", "gift", "glass", "home", "hourglass", "industry", "life-saver", "location-arrow", "money", "plane", "power-off", "rocket", "star", "truck", "warning", "wrench"]
    }]);
})();