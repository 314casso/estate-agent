$(document).ready(function() {

	
	var extra = {'p': '0909'};
	var $calendar = $('#calendar'); 

	$calendar.fullCalendar({
    	header: {
			left: 'prev,next today',
			center: 'title',
			right: 'month,agendaWeek,agendaDay,listWeek'
		},
		
		eventSources: [

	        {
	            url: $calendar.data('bidcalendarevents'),
	            type: 'GET',
	            data: extra,
	            error: function() {
	                alert('there was an error while fetching events!');
	            },	            
	        },
	        
	        {
	            url: $calendar.data('estatecalendarevents'),
	            type: 'GET',
	            data: extra,
	            error: function() {
	                alert('there was an error while fetching events!');
	            },	            
	        }


	    ],
	    
    	eventClick: function(event) {
            if (event.url) {
                window.open(event.url);
                return false;
            }
        },
        eventRender: function(event, element) {
        	if (event.description) {
	            element.qtip({
	                content: event.description
	            });
        	}
        }
    })

    
    $.fn.select2.defaults.set( "theme", "bootstrap" );
    $.fn.select2.defaults.set( "width", '100%' );
    var elem = $('#id_users');
    elem.on('change', function (e) {
    	var obj = elem.select2('data');
    	var ids = [];
        for (let e of obj) {
        	ids.push(e.id);
        }
        extra.ids = ids;
        $('#calendar').fullCalendar( 'refetchEvents' );
    });
    
    
    
});