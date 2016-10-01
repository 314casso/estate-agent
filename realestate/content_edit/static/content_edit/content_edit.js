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

function save_cms_content() {
	var tagname = $('#editable-tagname').val()
    var content = $('#editable-content').val()    
    var csrf_token = getCookie('csrftoken');
    $.post(
        '/content_edit/ajax_save_content/',
        {
            content: content, 
            content_name: tagname,
            csrfmiddlewaretoken: csrf_token
        },
        function(data) {
            if (data == "SUCCESS") {            	
            	$("#content_" + tagname).text(content)
            	$('#content-edit-modal').modal('toggle');
            }
        }
    );
}

$('#content-edit-modal').on('show.bs.modal', function (event) {
	  var button = $(event.relatedTarget)
	  var tagname = button.data('tagname')
	  var content = $("#content_" + tagname).text()
	  var modal = $(this)
	  modal.find('.modal-title').text(tagname)
	  modal.find('#editable-tagname').val(tagname)
	  modal.find('#editable-content').val(content)	  
})
