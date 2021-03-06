'use strict';

$( document ).ready( function () {

	$( '.datePicker' ).datetimepicker ({
		'dayOfWeekStart': 1,
		'lang': 'es',
		'timepicker': false,
		'format': 'd/m/Y',
		'formatDate': 'Y/m/d',
	});

	setDefaultDates();

});


function setDefaultDates () {
	$( '#date_from' ).val( moment().subtract( 7, 'days' ).format( 'DD/MM/YYYY' ) );
	$( '#date_to' ).val( moment().format( 'DD/MM/YYYY' ) );
};
