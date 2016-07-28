/**
 * Created by nokadmin on 06.07.16.
 */
/**
 * Created by nkuehl on 29/06/16.
 * This directive is used in the settings view to configure the simcore settings
 */


(function () {
    angular.module('app.directive.settings.sim', [])
        .directive('settingsSim', function () {
                return {
                    restrict: 'E',
                    scope: {settings: '=settings'},
                    templateUrl: function (_, attrs) {
                        return '/static/assets/js/app/components/settings/settingsSim/view.html';
                    },
                    controller: 'settingsSimController'
                }
            }
        ).controller('settingsSimController', [ '$scope', function ($scope) {
        //TODO
        $scope.settings = {
            UseCase: []
        };
        $scope.addUseCase = function(){
            $scope.settings.UseCase.push({
                ChargingStation: [],
                Building: [],
                Wind: [],
                UAV: []
            })
        }
        $scope.addItTo = function(item, arr){
            arr.push(item);
        }
    }]);
})();