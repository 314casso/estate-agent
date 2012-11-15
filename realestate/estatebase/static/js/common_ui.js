$(document).ready(function() {
	$('a.inline-button').parent().addClass('ui-state-default ui-corner-all');
	$('a.icon-plus').addClass('ui-icon ui-icon-plus');
	$('input:submit, input:button, a, button', '.button').button();
	$('.btn-add').button( "option", "icons", { primary: "ui-icon-plusthick"});
	$('.btn-filter-add').button( "option", "icons", { primary: "ui-icon-search"});
	$('.btn-filter-remove').button( "option", "icons", { primary: "ui-icon-cancel"});
	$('.btn-back').button( "option", "icons", { primary: "ui-icon-circle-arrow-w"});
	$('.btn-bind').button( "option", "icons", { primary: "ui-icon-circle-plus"});
	$('.btn-unbind').button( "option", "icons", { primary: "ui-icon-circle-minus"});
	$('.btn-delete').button( "option", "icons", { primary: "ui-icon-minusthick"});
	
	$('.btn-add,.btn-filter-add,.btn-filter-remove,.btn-back,.btn-bind,.btn-unbind,.btn-delete').button("option", "text", false);	
	// $( ".date-time-input" ).datepicker();
	$('input:text, textarea, input:password, .topbar').addClass('ui-widget ui-widget-content ui-corner-all');
	$('select').addClass('ui-corner-left')	
	$('.date-input').datepicker({
		dateFormat : "dd.mm.yy"
	});

	$(".base-table-list").find("tr").live('mouseover mouseout', function(event) {
		if (event.type == 'mouseover') {
			$(this).children("td").addClass("ui-state-hover");
		} else {
			$(this).children("td").removeClass("ui-state-hover");
		}
	});

	$('.active').addClass('ui-state-highlight');
	$('.local-int').autoNumeric({
		aSep : String.fromCharCode(160),
		aDec : ',',
		mDec : 0
	});
	$('.local-decimal').autoNumeric({
		aSep : String.fromCharCode(160),
		aDec : ',',
		mDec : 2
	});
	$('#loadingMask').fadeOut();
	
	$(".errorlist a").click(function(){
		$(this).parent().fadeOut();
	});
	
});

function getIndex(id, item) {
	estateId = parseInt(localStorage.getItem('estate_id'));
	if (parseInt(id) == parseInt(estateId)) {
		return parseInt(localStorage.getItem(item));
	} else {
		return 0;
	}
}

function html_unescape(text) {
	text = text.replace(/</g, '');
	text = text.replace(/"/g, '"');
	text = text.replace(/'/g, "'");
	text = text.replace(/&/g, '&');
	return text;
}

function dismissAddAnotherPopup(win, newId, newRepr) {
    newId = html_unescape(newId);
    newRepr = html_unescape(newRepr);
    var name = win.name;	    
    var elem_repr = $('#'+ name + '_0');	
    var elem_id = $('#'+ name + '_1');
    elem_repr.val(newRepr);
    elem_id.val(newId);	
    win.close();
}

(function($) {
	$.fn.addAnother = function(options) {

		defaults = {
			url : null,
			width : 500,
			height : 800,
			object_id : null
		};

		var opts = $.extend(defaults, options);

		var a = document.createElement('a');
		a.title = "Добавить нового заказчика";
		a.innerHTML = "Добавить";
		a.href = opts.url;
		$(a).click(function() {
			popupWin = window.open(this.href, opts.object_id, 'height=' + opts.height + ', width=' + opts.width + ', resizable=yes, scrollbars=yes');
			popupWin.focus();
			return false;
		})
		this.after(' ', a);
	};
})(jQuery);

$(document).ajaxSend(function(event, xhr, settings) {
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

	function sameOrigin(url) {
		// url could be relative or scheme relative or absolute
		var host = document.location.host;
		// host + port
		var protocol = document.location.protocol;
		var sr_origin = '//' + host;
		var origin = protocol + sr_origin;
		// Allow absolute or scheme relative URLs to same origin
		return (url == origin || url.slice(0, origin.length + 1) == origin + '/') || (url == sr_origin || url.slice(0, sr_origin.length + 1) == sr_origin + '/') ||
		// or any other URL that isn't scheme relative or absolute i.e relative.
		!(/^(\/\/|http:|https:).*/.test(url));
	}

	function safeMethod(method) {
		return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
	}

	if (!safeMethod(settings.type) && sameOrigin(settings.url)) {
		xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
	}
});

(function($) {
	$.widget("ui.combobox", {
		_create : function() {
			var input, self = this, select = this.element.hide(), selected = select.children(":selected"), value = selected.val() ? selected.text() : "", wrapper = this.wrapper = $("<span>").addClass("ui-combobox").insertAfter(select);

			input = $("<input>").appendTo(wrapper).val(value).addClass("ui-combobox-input").autocomplete({
				delay : 0,
				minLength : 0,
				source : function(request, response) {
					var matcher = new RegExp($.ui.autocomplete.escapeRegex(request.term), "i");
					response(select.children("option").map(function() {
						var text = $(this).text();
						if (this.value && (!request.term || matcher.test(text) ))
							return {
								label : text.replace(new RegExp("(?![^&;]+;)(?!<[^<>]*)(" + $.ui.autocomplete.escapeRegex(request.term) + ")(?![^<>]*>)(?![^&;]+;)", "gi"), "<strong>$1</strong>"),
								value : text,
								option : this
							};
					}));
				},
				select : function(event, ui) {
					ui.item.option.selected = true;
					self._trigger("selected", event, {
						item : ui.item.option
					});
				},
				change : function(event, ui) {
					if (!ui.item) {
						var matcher = new RegExp("^" + $.ui.autocomplete.escapeRegex($(this).val()) + "$", "i"), valid = false;
						select.children("option").each(function() {
							if ($(this).text().match(matcher)) {
								this.selected = valid = true;
								return false;
							}
						});
						if (!valid) {
							// remove invalid value, as it didn't match anything
							$(this).val("");
							select.val("");
							input.data("autocomplete").term = "";
							return false;
						}
					}
				}
			}).addClass("ui-widget ui-widget-content ui-corner-left");

			input.data("autocomplete")._renderItem = function(ul, item) {
				return $("<li></li>").data("item.autocomplete", item).append("<a>" + item.label + "</a>").appendTo(ul);
			};

			$("<a>").attr("tabIndex", -1).attr("title", "Show All Items").appendTo(wrapper).button({
				icons : {
					primary : "ui-icon-triangle-1-s"
				},
				text : false
			}).removeClass("ui-corner-all").addClass("ui-corner-right ui-combobox-toggle").click(function() {
				// close if already visible
				if (input.autocomplete("widget").is(":visible")) {
					input.autocomplete("close");
					return;
				}

				// work around a bug (likely same cause as #5265)
				$(this).blur();

				// pass empty string as value to search for, displaying all results
				input.autocomplete("search", "");
				input.focus();
			});
		},

		destroy : function() {
			this.wrapper.remove();
			this.element.show();
			$.Widget.prototype.destroy.call(this);
		}
	});
})(jQuery);

function showFilter(id) {
	$(id).dialog('open');
}

