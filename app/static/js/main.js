var jsonldVis = require('jsonld-vis.js')

var app = angular.module('WordcountApp', [])

app.controller('WordcountController', [
    '$scope',
    '$log',
    '$http',
    '$timeout',
    function($scope, $log, $http, $timeout) {

        $scope.submitButtonText = 'Submit';
        $scope.loading = false;
        $scope.urlerror = false;

        $scope.getResults = function() {

            $log.log('test');

            // get the URL from the input
            var userInput = $scope.myFile;

            // fire the API request
            var fd = new FormData();
            fd.append('file', userInput);
            $http.post('/upload', fd, {
                transformRequest: angular.identity,
                headers: {
                    'Content-Type': undefined
                }
            }).success(function(results) {
                $log.log(results);
                $scope.wordcounts = [];
                getWordCount(results);
                $scope.loading = true;
                $scope.submitButtonText = 'Loading...';
                $scope.urlerror = false;
            }).error(function(error) {
                $log.log(error);
            });

        };

        function getWordCount(results) {

            var timeout = '';

            var poller = function(key) {
                // fire another request
                if (key !== undefined) {
                    $http.get('/results/' + key).success(function(data, status, headers, config) {
                        if (status === 202) {} else if (status === 200) {
                            $log.log(data);
                            $scope.loading = false;
                            $scope.submitButtonText = "Submit";
                            $scope.wordcounts.push(data);
                            $log.log($scope.wordcounts)
                            $timeout.cancel(timeout);
                            return false;
                        }
                        // continue to call the poller() function every 2 seconds
                        // until the timeout is cancelled
                        timeout = $timeout(poller(key), 2000);
                    }).error(function(error) {
                        $log.log(error);
                        $scope.loading = false;
                        $scope.submitButtonText = "Submit";
                        $scope.urlerror = true;
                    });
                };
            }

            angular.forEach(results, function(value, key) {
                $log.log(value, key);
                poller(key)
            });

        }

    }
])

app.directive('fileModel', [
    '$parse',
    function($parse) {
        return {
            restrict: 'A',
            link: function(scope, element, attrs) {
                var model = $parse(attrs.fileModel);
                var modelSetter = model.assign;

                element.bind('change', function() {
                    scope.$apply(function() {
                        modelSetter(scope, element[0].files[0]);
                    });
                });
            }
        };
    }
]);

app.directive('graph', [
    '$parse',
    function($parse) {
        return {
            restrict: 'E',
            replace: true,
            template: '<div id="graph"></div>',
            link: function(scope) {
                scope.$watch('wordcounts', function() {
                    d3.select('#graph').selectAll('*').remove();
                    var res = scope.wordcounts;
                    d3.json(res, (err, data) => {
                        if (err)
                            return console.warn(err);
                        d3.jsonldVis(data, '#graph', {
                            w: 800,
                            h: 600,
                            maxLabelWidth: 250
                        });
                    });
                }, true);
            }
        };
    }
]);
