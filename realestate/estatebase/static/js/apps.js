$(document).ready(function() {

	var appEvents = new Vue({
		el : '#app-events',
		delimiters : [ "<%", "%>" ],		
		data : {
			events : [],
		},
		methods : {
			open : function(url) {
				window.location.href = url;
			},
			
			getUrl : function() {				
				return $(this.$el).data('url');
			},
			getTriggerUrl : function() {				
				return $(this.$el).data('triggerevent');
			},			
			openDialog : function() {				
				eventDlg.open();
			},
			fetchData : function() {
				var xhr = new XMLHttpRequest();
				var self = this;
				xhr.open('GET', this.getUrl());
				xhr.onload = function() {
					var data = JSON.parse(xhr.responseText)
					self.events = data.events;
				}				
				xhr.send()				
			},
			trigger : function(event) {
				event.preventDefault();
				var url = this.getTriggerUrl();
				var self = this;
				$.ajax({
		            type: 'POST',
		            url: url,
		            data: {'pk': $(event.target).data('pk')},
		            success: function(data) {
		            	self.fetchData();
		            },
		            error: function (jqXHR, textStatus, errorThrown) {		            	
		            	$('#eventerrors').text(errorThrown).show().delay(2000).fadeOut();		            	
		            	console.log(errorThrown);
		            }
		          });
			}
		}
	})	
		
	var eventDlg = {
		dlg : $("#event-form"),
		open : function() {
			this.dlg.dialog('open');
		},
		init : function() {
			var dlg = this.dlg;
			dlg.dialog({
				modal : true,
				width : 500,
				height : 'auto',
				title : 'Добавление события',
				autoOpen : false,
				open : function(event, ui) {
					dlg.css('overflow', 'hidden');
				},
				close : function(event, ui) {
					dlg.find('.error').text('');
				}
			});
		
			var dlg = this.dlg;
			dlg.find('form').submit(function(event) {
				event.preventDefault();
		        var frm = $(this);      		        
		        $.ajax({
		            type: 'POST',
		            url: frm.attr('action'),
		            data: frm.serialize(),
		            success: function(data) {
		            	if (data.errors) {
			            	dlg.find('.error').text(data.errors);
			            } else {
			            	frm.trigger('reset');
				            dlg.dialog('close');
				            appEvents.fetchData();
			            }
		            },
		            error: function (jqXHR, textStatus, errorThrown) {
		            	dlg.find('.error').text(errorThrown);
		            }
		          });
		    });	
		}
	}
	
	eventDlg.init();
	appEvents.fetchData();
	
});
