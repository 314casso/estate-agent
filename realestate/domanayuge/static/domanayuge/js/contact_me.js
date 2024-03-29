// Contact Form Scripts
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

$(function() {

    $("#contactForm input,#contactForm textarea").jqBootstrapValidation({
        preventSubmit: true,
        submitError: function($form, event, errors) {
            // additional error messages or events
        },
        submitSuccess: function($form, event) {
            event.preventDefault(); // prevent default submit behaviour
            
            // try {
            //    ym(66555292,'reachGoal','forma');
            //    gtag('event', 'click');
        	// }
        	// catch (e) {
        	//    console.log(e);
        	// }
            
            // get values from FORM
            var name = $("input#name").val();
            var email = $("input#email").val();
            var phone = $("input#phone").val();
            var message = $("textarea#message").val();
            var firstName = name; // For Success/Failure Message
            var csrf_token = getCookie('csrftoken');
            // Check for white space in name for Success/Fail message
            if (firstName.indexOf(' ') >= 0) {
                firstName = name.split(' ').slice(0, -1).join(' ');
            }
            $.ajax({
                url: "/sendemail/",
                type: "POST",                                
                data: {
                    name: name,
                    phone: phone,
                    email: email,
                    message: message,
                    csrfmiddlewaretoken: csrf_token
                },
                cache: false,
                success: function() {
                    // Success message
                    $('#success').html("<div class='alert alert-success'>");
                    $('#success > .alert-success').html("<button type='button' class='close' data-dismiss='alert' aria-hidden='true'>&times;")
                        .append("</button>");
                    $('#success > .alert-success')
                        .append("<strong>Ваше сообщение было успешно отправлено. </strong>");
                    $('#success > .alert-success')
                        .append('</div>');

                    //clear all fields
                    $('#contactForm').trigger("reset");
                },
                error: function() {
                    // Fail message
                    $('#success').html("<div class='alert alert-danger'>");
                    $('#success > .alert-danger').html("<button type='button' class='close' data-dismiss='alert' aria-hidden='true'>&times;")
                        .append("</button>");
                    $('#success > .alert-danger').append("<strong>Извините " + firstName + ", в данный момент почтовый сервер недоступен. Попробуйте отправить сообщение позднее!");
                    $('#success > .alert-danger').append('</div>');
                    //clear all fields
                    $('#contactForm').trigger("reset");
                },
            });
        },
        filter: function() {
            return $(this).is(":visible");
        },
    });

    // form "More"
    $("#knowPrice input, #knowPrice textarea").jqBootstrapValidation({
        preventSubmit: true,
        submitError: function($form, event, errors) {
            // additional error messages or events
        },
        submitSuccess: function($form, event) {
            event.preventDefault(); // prevent default submit behaviour

            // try {
            //     ym(66555292,'reachGoal','forma');
            //     gtag('event', 'click');
            // }
            // catch (e) {
            //     console.log(e);
            // }

            // get values from FORM
            var name = $("input#nameUser").val();
            var email = $("input#emailUser").val();
            var phone = $("input#phoneUser").val();
            var comment = $("textarea#commentUser").val();

            // var square = $('input#square').val();
            // var floors = $('input#floors').val();
            // var walls = $('input#walls').val();
            // var roof = $('input#roof').val();

            var firstName = name; // For Success/Failure Message
            // var message = 'Комментарий: '+ comment +'; Желаемая площадь дома: '+ square + ';' +
            //     ' Этажность: '+ floors +'; Материал стен: '+ walls +'; Кровля: '+ roof +'.';
            var message = comment;
            var csrf_token = getCookie('csrftoken');
            // Check for white space in name for Success/Fail message
            if (firstName.indexOf(' ') >= 0) {
                firstName = name.split(' ').slice(0, -1).join(' ');
            }
            $.ajax({
                url: "/sendemail/",
                type: "POST",
                data: {
                    name: name,
                    phone: phone,
                    email: email,
                    message: message,
                    csrfmiddlewaretoken: csrf_token
                },
                cache: false,
                success: function() {
                    // Success message
                    $('#result-send').html("<div class='alert alert-success'>");
                    $('#result-send > .alert-success')
                        .append("<strong>Ваше сообщение было успешно отправлено. </strong>");
                    $('#result-send > .alert-success')
                        .append('</div>');

                    //clear all fields
                    $('#knowPrice').trigger("reset");
                    setTimeout(function () {
                        $('#modalMore').modal('hide');
                    }, 1500);
                },
                error: function() {
                    // Fail message
                    $('#result-send').html("<div class='alert alert-danger'>");
                    $('#result-send > .alert-danger').html("<button type='button' class='close' data-dismiss='alert' aria-hidden='true'>&times;")
                        .append("</button>");
                    $('#result-send > .alert-danger').append("<strong>Извините " + firstName + ", в данный момент почтовый сервер недоступен. Попробуйте отправить сообщение позднее!");
                    $('#result-send > .alert-danger').append('</div>');
                    //clear all fields
                    $('#contactForm').trigger("reset");
                },
            });
        },
        filter: function() {
            return $(this).is(":visible");
        },
    });

    $("a[data-toggle=\"tab\"]").click(function(e) {
        e.preventDefault();
        $(this).tab("show");
    });
});


/*When clicking on Full hide fail/success boxes */
$('#name').focus(function() {
    $('#success').html('');
});
