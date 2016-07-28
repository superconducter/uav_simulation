/**
 * Created by Niels-Ole Kühl
 * This router manages the navigation on the page
 */
(function () {

    'use strict';

    angular
        .module('app.router',
        [
            'app.controller.agent.list',
            'app.controller.round.list',
            'app.controller.map',
            'app.directive.map',
            'app.controller.settings',
            'app.controller.statistic',
            'app.controller.simulation.list',
            'app.controller.home.controller',
            'ngRoute'
        ]
    )
        .config(config);

    function config($routeProvider) {
        $routeProvider.
               when('/drones', {
                templateUrl: '/static/assets/js/app/components/agentList/agentListView.html',
                controller: 'agentListController'
            }).when('/rounds', {
                templateUrl: '/static/assets/js/app/components/roundList/roundListView.html',
                controller: 'roundListController'
             }).when('/simulations', {
                templateUrl: '/static/assets/js/app/components/simulationList/simulationListView.html',
                controller: 'simulationListController'
            }).when('/simulations/:simulationId', {
                redirectTo: '/simulations/:simulationId/map',
            }).when('/simulations/:simulationId/map', {
                templateUrl: '/static/assets/js/app/components/map/mapView.html'
            }).when('/simulations/:simulationId/statistic', {
                templateUrl: '/static/assets/js/app/components/statistic/statisticView.html',
                controller: 'statisticsController'
            }).when('/settings', {
                templateUrl: '/static/assets/js/app/components/settings/settingsView.html',
                controller: 'settingsController'
            }).when('/statistic', {
                templateUrl: '/static/assets/js/app/components/statistic/statisticView.html',
                controller: 'statisticsController'
            }).when('/', {
                templateUrl: '/static/assets/js/app/components/home/homeView.html',
                controller: 'homeController'
            }).
            otherwise({
                redirectTo: '/'
            });
    }
})();