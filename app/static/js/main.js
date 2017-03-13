var app = angular.module('SpfyApp', ['vcRecaptcha','ngMessages'])

app.controller('SpfyController', [
    '$scope',
    '$log',
    '$http',
    '$timeout',
    'vcRecaptchaService',
    function($scope, $log, $http, $timeout, vcRecaptchaService) {

        $scope.loading = false;

        $scope.jobfailed = false;
        $scope.message='';

        // for table sort/search
        $scope.sortType     = 'filename'; // set the default sort type
        $scope.sortReverse  = false;  // set the default sort order

        // define form in scope
        $scope.formData={};
        // set defaults
        $scope.formData.options={};
        $scope.formData.options.vf=true
        $scope.formData.options.amr=true
        $scope.formData.options.serotype=true
        $scope.pi=90

        // check at least one of options is selected
        var calculateSomeSelected = function() {
          $scope.someSelected = Object.keys($scope.formData.options).some(function(key) {
            return $scope.formData.options[key];
          });
        };
        $scope.checkboxChanged = calculateSomeSelected;
        calculateSomeSelected();

        //recaptcha support via github.com/VividCortex/angular-recaptcha/
        $scope.submitted = false;
        $scope.response = null;
        $scope.widgetId = null;
        $scope.setResponse = function (response) {
                    console.info('Response available');
                    $scope.response = response;
                    $scope.hasResponse = true;
                };
        $scope.model = {
                    key: '6LeVYhgUAAAAAKbedEJoCcRaeFaxPh-2hZfzXfFP'
                };
        $scope.setResponse = function (response) {
                    console.info('Response available');
                    $scope.response = response;
                };
        $scope.setWidgetId = function (widgetId) {
                    console.info('Created widget ID: %s', widgetId);
                    $scope.widgetId = widgetId;
                };
        $scope.cbExpiration = function() {
            console.info('Captcha expired. Resetting response object');
            vcRecaptchaService.reload($scope.widgetId);
            $scope.response = null;
         };

        var fd = new FormData();

        $scope.getTheFiles = function ($files) {
                angular.forEach($files, function (value, key) {
                    fd.append('file', value);
                });
            };

        $scope.getResults = function() {

            // get the URL from the input
            //var userInput = $scope.myFile;

            // fire the API request




            //fd.append('file', userInput);
            fd.append('options.vf', $scope.formData.options.vf);
            fd.append('options.amr', $scope.formData.options.amr);
            fd.append('options.serotype', $scope.formData.options.serotype);
            fd.append('options.pi', $scope.pi);
            fd.append('g-recaptcha-response', $scope.response);
            $log.log($scope.response);
            $log.log($scope.formData);
            $scope.loading = true;
            $scope.submitted = true;
            $http.post('upload', fd, {
                transformRequest: angular.identity,
                headers: {
                    'Content-Type': undefined
                }
            }).success(function(results) {
                $log.log(results);
                $scope.spits = [];
                getSpfySpit(results);
                $scope.loading = true;
                $scope.urlerror = false;
                //will have to add this in server resp
                //$scope.message = data.message;
            }).error(function(error) {
                $log.log(error);
            });

        };

        function getSpfySpit(results) {

            var timeout = '';

            var poller = function(key) {
                // fire another request
                if (key !== undefined) {
                    $http.get('results/' + key).success(function(data, status, headers, config) {
                        if (status == 200) {
                            $log.log(data);
                            $scope.loading = false;
                            $scope.spits = $scope.spits.concat(data);
                            $log.log($scope.spits)
                            $timeout.cancel(timeout);
                            return false;
                        } else if (status == 202){
                          // job result not found ie. still pending
                          $scope.loading = true;
                        }
                        // continue to call the poller() function every 2 seconds
                        // until the timeout is cancelled
                        timeout = $timeout(poller(key), 2000);
                    }).error(function(error, status) {
                        $log.log(error);
                        $scope.loading = false;
                        $log.log(status);
                        $scope.uploaderror = true;
                        if (status == 415){
                          $scope.jobfailed = true;
                          $scope.message = $scope.message + "Job failed. Key: " + key + " / ";
                        }
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
                        csvString = csvString + rowData[j].textContent.trim() + ",";
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

app.directive('ngFiles', ['$parse', function ($parse) {

            function fn_link(scope, element, attrs) {
                var onChange = $parse(attrs.ngFiles);
                element.on('change', function (event) {
                    onChange(scope, { $files: event.target.files });
                });
            };

            return {
                link: fn_link
            }
        } ])
