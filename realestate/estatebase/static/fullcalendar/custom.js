$(document).ready(function() {

    // page is now ready, initialize the calendar...

    $('#calendar').fullCalendar({
    	header: {
			left: 'prev,next today',
			center: 'title',
			right: 'month,agendaWeek,agendaDay,listWeek'
		},
    	events: '/estatebase/bidcalendarevents/',
    	eventClick: function(event) {
            if (event.url) {
                window.open(event.url);
                return false;
            }
        }
    })

});