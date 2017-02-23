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

        // for table sort/search
        $scope.sortType     = 'filename'; // set the default sort type
        $scope.sortReverse  = false;  // set the default sort order
        $scope.searchFish   = '';     // set the default search/filter term

        $scope.getResults = function() {

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
                            $scope.wordcounts = $scope.wordcounts.concat(data);
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

app.directive('exportToCsv', function() {
    return {
        restrict: 'A',
        link: function(scope, element, attrs) {
            var el = element[0];
            element.bind('click', function(e) {
                var table = e.target.nextElementSibling;
                var csvString = '';
                for (var i = 0; i < table.rows.length; i++) {
                    var rowData = table.rows[i].cells;
                    for (var j = 0; j < rowData.length; j++) {
                        csvString = csvString + rowData[j].innerHTML + ",";
                    }
                    csvString = csvString.substring(0, csvString.length - 1);
                    csvString = csvString + "\n";
                }
                csvString = csvString.substring(0, csvString.length - 1);
                var a = $('<a/>', {
                    style: 'display:none',
                    href: 'data:application/octet-stream;base64,' + btoa(csvString),
                    download: 'results.csv'
                }).appendTo('body')
                a[0].click()
                a.remove();
            });
        }
    }
});
