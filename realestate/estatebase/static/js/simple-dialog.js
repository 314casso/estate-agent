$(function() {
	$('a.ajax-dialog').live('click', function() {
		var url = this.href;
		var title = this.title;
		var width = this.dataset.width;
		var uniq = 'dialog' + (new Date()).getTime();

		var dialog = $('<div id="' + uniq + '" style="display:hidden"></div>').appendTo('body');

		// load remote content
		dialog.load(url, function(responseText, textStatus, XMLHttpRequest) {
			dialog.dialog({
				modal : true,
				close : function(event, ui) {
					dialog.remove();
				},
				buttons : {
					Отмена : function() {
						dialog.dialog("close");
					}
				},
				width : width,
				title : title,
				position: ['center',170]
			});
		});
		//prevent the browser to follow the link
		return false;
	});
});
