$(function() {

    var dropbox = $('#dropbox'),
        message = $('.message', dropbox);

    dropbox.filedrop({
        paramname: 'file',
        maxfiles: 10,
        maxfilesize: 5,
        url: '/upload',
        uploadFinished: function(i, file, response, time) {
						var status_url = respose.location
            check_job_status(status_url);
        },

        error: function(err, file) {
            switch (err) {
                case 'BrowserNotSupported':
                    showMessage('Your browser does not support HTML5 file uploads!');
                    break;
                case 'TooManyFiles':
                    alert('Too many files! Please select ' + this.maxfiles + ' at most!');
                    break;
                case 'FileTooLarge':
                    alert(file.name + ' is too large! The size is limited to ' + this.maxfilesize + 'MB.');
                    break;
                default:
                    break;
            }
        },


    });





    function showMessage(msg) {
        message.html(msg);
    }

    function flash_alert(message, category, clean) {
        if (typeof(clean) === "undefined")
            clean = true;
        if (clean) {
            remove_alerts();
        }
        var htmlString = '<div class="alert alert-' + category + ' alert-dismissible" role="alert">'
        htmlString += '<button type="button" class="close" data-dismiss="alert" aria-label="Close">'
        htmlString += '<span aria-hidden="true">&times;</span></button>' + message + '</div>'
        $(htmlString).prependTo("#mainContent").hide().slideDown();
    }

    function remove_alerts() {
        $(".alert").slideUp("normal", function() {
            $(this).remove();
        });
    }

    function check_job_status(status_url) {
        $.getJSON(status_url, function(data) {
            console.log(data);
            switch (data.status) {
                case "unknown":
                    flash_alert("Unknown job id", "danger");
                    $("#submit").removeAttr("disabled");
                    break;
                case "finished":
                    flash_alert(data.result, "success");
                    $("#submit").removeAttr("disabled");
                    break;
                case "failed":
                    flash_alert("Job failed: " + data.message, "danger");
                    $("#submit").removeAttr("disabled");
                    break;
                default:
                    // queued/started/deferred
                    setTimeout(function() {
                        check_job_status(status_url);
                    }, 500);
            }
        });
    }

});
