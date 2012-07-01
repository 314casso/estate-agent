$(document).ready(function() {
	$('a.inline-button').parent().addClass('ui-state-default ui-corner-all');
	$('a.icon-plus').addClass('ui-icon ui-icon-plus');
	$('input:submit, a, button', '.button').button();
	// $( ".date-time-input" ).datepicker();
	//$("select").combobox();
	$('input:text, textarea').addClass('ui-widget ui-widget-content ui-corner-all');
});

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

			input = $("<input>").appendTo(wrapper).val(value).addClass("ui-state-default ui-combobox-input").autocomplete({
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