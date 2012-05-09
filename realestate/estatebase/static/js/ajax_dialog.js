$(function() {		
		$('a.ajax-dialog').live('click', function() {
			var url = this.href;
			var uniq = 'dialog' + (new Date()).getTime();						
			
			var dialog = $('<div id="'+ uniq +'" style="display:hidden"></div>').appendTo('body');
			
			// load remote content
			dialog.load(url, function(responseText, textStatus, XMLHttpRequest) {
				dialog.dialog({
					modal : true,
					close : function(event, ui) {
						dialog.remove();
					},
					buttons : {
						OK : function() {
							var form =  dialog.find('form');
							$.post(url, form.serialize(), function(data) {
								if(data.result != 'success') {
									form.html(data.form);
									// Re-bind selectables
									if( typeof (rebindDialog) != 'undefined') {
										rebindDialog();
									}
								} else {
									dialog.dialog("close");
								}
							}, 'json')

						},
						Cancel : function() {
							dialog.dialog("close");
						}
					}
				});
				if( typeof (setDialogTitle) != 'undefined') {
					setDialogTitle(dialog);
				}
			});
			//prevent the browser to follow the link
			return false;
		});
	});