/**
 * Created by nkuehl on 29/06/16.
 * Directive for displaying the map. This is useful if we want to use the map on multiple pages.
 */


(function () {
    angular.module('app.directive.map', ['app.controller.map'])
        .directive('mapdirective', function () {
                return {
                    restrict: 'E',
                    scope: {settings: '=settings', name: '=name'},
                    templateUrl: function (_, attrs) {
                        return '/static/assets/js/app/directives/map/views/mapView.html';
                    },
                    controller: 'mapController'
                }
            }
        );
})();