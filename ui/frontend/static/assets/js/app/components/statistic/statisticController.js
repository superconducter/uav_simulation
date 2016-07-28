/**
 * Created by J.D. on 12.06.16 Sedat will adapt it to work with real events.
 *
 * This class will handles the statistics data and defines the x & y axis.
 * As Sedat Koca suggested: there are 6 Events with different types. Per type one diagram in sum 6 diagrams.
 */
(function () {
    'use strict';


    angular.module('app.controller.statistic', ['angular.morris-chart'])

        .controller('statisticsController', ['$scope', '$http', '$routeParams',
            function ($scope, $http, $routeParams) {
            $http.get('/api/events2/?simulation=' + $routeParams.simulationId).success(function (data) {

                var ctrl = this;
                var jsonObject = data;

                $scope.data=[{a:0,b:0,c:0, x:0}];
                for(var i=0; i< jsonObject.length;i++){
                    var round=0;
                    for(var o in jsonObject[i]){
                        var e1=0,e2=0,e3=0;

                        if(o == "round_number"){
                            // console.log("i : "+ i +"  "+jsonObject[i][o]);
                            round = jsonObject[i][o];
                        }
                        if(o == "events"){

                            for(var event in jsonObject[i][o]){


                                var e = jsonObject[i][o][event].type ;

                                if(e=="PackagesLost"){
                                    e1++;

                                }
                                if(e=="PackagesDelivered"){
                                    e2++;

                                }
                                if(e=="PackagesNotFound"){
                                    e3++;

                                }
                            }
                            if(round == 1){
                                $scope.data=[{a:e1,b:e2,c:e3, x:i+1}];
                            }else{

                                $scope.data.push({a:e1,b:e2,c:e3, x:i+1});
                            }
                        }
                    }
                }
            });
        }])

        .controller('settingsControllerDonutPackages', ['$scope', '$http', '$routeParams',
            function ($scope, $http, $routeParams) {
            $http.get('/api/events2/?simulation=' + $routeParams.simulationId).success(function (data3) {
                var ctrl = this;
                var jsonObject = data3;
                var d1= 0;
                var d2= 0;
                var d3= 0;

                for(var i=0; i< jsonObject.length;i++){
                    for(var o in jsonObject[i]){

                        if(o == "events"){

                            for(var event in jsonObject[i][o]){
                                var e = jsonObject[i][o][event].type ;
                                if(e=="PackagesLost"){
                                    d1++;
                                }
                                if(e=="PackagesDelivered"){
                                    d2++;
                                }
                                if(e=="PackagesNotFound"){
                                    d3++;
                                }
                            }
                        }
                    }
                }
                $scope.data3=[{a:d1,b:d2,c:d3, x:0}];


            });
        }])
         .controller('statisticsController2', ['$scope', '$http', '$routeParams',
            function ($scope, $http, $routeParams) {
            $http.get('/api/events2/?simulation=' + $routeParams.simulationId).success(function (data2) {
                var ctrl = this;
                var jsonObject = data2;
                $scope.data2=[{a:0,b:0,c:0, x:0}];
                for(var i=0; i< jsonObject.length;i++){
                    var round=0;
                    for(var o in jsonObject[i]){
                        var e1=0,e2=0,e3=0;

                        if(o == "round_number"){
                            // console.log("i : "+ i +"  "+jsonObject[i][o]);
                            round = jsonObject[i][o];
                        }
                        if(o == "events"){

                            for(var event in jsonObject[i][o]){
                                var e = jsonObject[i][o][event].type ;
                                if(e=="DroneActive"){
                                    e1++;

                                }
                                if(e=="DroneInactive"){
                                    e2++;

                                }
                                if(e=="DroneCrashed"){
                                    e3++;

                                }
                            }
                            if(round == 1){
                                $scope.data2=[{a:e1,b:e2,c:e3, x:i+1}];
                            }else{
                                $scope.data2.push({a:e1,b:e2,c:e3, x:i+1});
                            }
                        }
                    }
                }

            });
        }])

         .controller('settingsControllerDonutDrone', ['$scope', '$http', '$routeParams',
            function ($scope, $http, $routeParams) {
            $http.get('/api/events2/?simulation=' + $routeParams.simulationId).success(function (data3) {
                var ctrl = this;
                var jsonObject = data3;
                var d1= 0;
                var d2= 0;
                var d3= 0;

                for(var i=0; i< jsonObject.length;i++){
                    for(var o in jsonObject[i]){

                        if(o == "events"){

                            for(var event in jsonObject[i][o]){
                                var e = jsonObject[i][o][event].type ;
                                if(e=="DroneActive"){
                                    d1++;
                                }
                                if(e=="DroneInactive"){
                                    d2++;
                                }
                                if(e=="DroneCrashed"){
                                    d3++;
                                }
                            }
                        }
                    }
                }
                $scope.data3=[{a:d1,b:d2,c:d3, x:0}];


            });
        }])
})();

