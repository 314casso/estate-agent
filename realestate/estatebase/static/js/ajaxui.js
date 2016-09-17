$( "#globalsearchdialog" ).dialog({
	      autoOpen: false,
	      height: 250,
	      width: 500,
	      modal: true,
	      buttons: {	         
	          "Закрыть": function() {
	            $( this ).dialog( "close" );
	          }
	        }
});
	
var search = $( "#globalsearch" );

var callback = function() {	
	var next = search.data( "next" );
	var q = search.val();
	if (!q) {
		return;
	}	
	var dialog = $( "#globalsearchdialog" ); 
	params = $.param({q: q, next: next});
	dialog.dialog('option', 'title', 'Поиск: ' + q);
	dialog.load('/estatebase/globalsearch/?'+params).dialog('open');
}

//search.focusout(callback);

search.keypress(function(e){
    if(e.which == 13){
    	callback();
        $(this).blur();    
    }
});