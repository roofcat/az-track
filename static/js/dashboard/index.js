'use strict';

google.load('visualization', '1.0', {'packages': ['corechart','line','table'], 'language': 'es'});

var baseUrl = document.location.href;

var perfilUrl = 'perfiles/';
var UserProfile = null;

var urlPath = 'statistics/';

var urlGeneralExport = 'reports/general/';
var urlSendedExport = 'reports/sended/';
var urlFailureExport = 'reports/failure/';

var jsonData;

var linkGeneral = '';
var linkSended = '';
var linkFailure = '';


$( document ).ready( function () {

	baseUrl = baseUrl.split('/');
    delete baseUrl[4];
    delete baseUrl[3];
    baseUrl = baseUrl.join('/')
    baseUrl = baseUrl.substring( 0, baseUrl.length - 1 );

	// Seteo de fecha actual
	setDefaultDates();

    // obtener el perfil de usuario
    $.ajax({
        url: baseUrl + perfilUrl,
        type: 'GET',
        dataType: 'json',
        success: function ( data ) {
            UserProfile = data;
            inicializar();
        },
        error: function ( jqXHR, textStatus, errorThrown ) {
            console.log( errorThrown );
            inicializar();
        },
    });

});

function inicializar () {

	setupPageByUserProfile();
	putDownloadLink();
	setDateTimePicker( '#date_from' );
    setDateTimePicker( '#date_to' );
    // realizar carga por defecto
	//$( "#run_search" ).click();
	$( '#showMenu' ).click();

};

$( window ).on( 'resize', function () {
	
	drawJsonData();

});

$( '#showMenu' ).on( 'click', function () {
	
	$( '#menuModal' ).modal( 'show', true );

});

// Validar los campos de fecha
$( 'input:text' ).on( 'change', function () {
	
	var date_from = $( '#date_from' ).val();
	var date_to = $( '#date_to' ).val();

	date_from = moment( date_from, 'DD/MM/YYYY' ).unix();
	date_to = moment( date_to, 'DD/MM/YYYY' ).unix();

	if ( date_from > date_to ) {
		setDefaultDates();
	};
	putDownloadLink();

});

$( 'select' ).on( 'change', function () {
	
	putDownloadLink();

});

$( 'div' ).on( 'mouseover', '#spanTooltip', function () {
	
	$( this ).popover( 'show' );

});

$( 'div' ).on( 'mouseout', '#spanTooltip', function () {
	
	$( this ).popover( 'hide' );

});

function putDownloadLink () {
	
	var date_from = $( '#date_from' ).val();
	var date_to = $( '#date_to' ).val();
	var empresas = $( '#empresas' ).val();
	var tipo_receptor = $( '#tipo_receptor' ).val();
	date_from = getDateAsTimestamp( date_from );
	date_to = getDateAsTimestamp( date_to );
	
	if ( UserProfile.enable_report === true ) {
		
		linkGeneral = baseUrl + urlGeneralExport + date_from + '/';
		linkGeneral += date_to + '/' + empresas + '/' + tipo_receptor + '/';

		linkSended = baseUrl + urlSendedExport + date_from + '/';
		linkSended += date_to + '/' + empresas + '/' + tipo_receptor + '/';

		linkFailure = baseUrl + urlFailureExport + date_from + '/';
		linkFailure += date_to + '/' + empresas + '/' + tipo_receptor + '/';

	} else {

		linkGeneral = '';
		linkSended = '';
		linkFailure = '';

	};

	setupPageByUserProfile();

};

$( 'button' ).on( 'click', function () {

	var btn = $( this );
	var btnId = $( this ).attr( 'id' );

	var title = "Reporte Azurian Track";
	var body = "Se ha iniciado el proceso de generar una planilla reporte ";
	body += "cuando este proceso finalice recibirás un email con el archivo adjunto, ";
	body += "por favor espere unos minutos...";

	if ( btnId ) {
		switch ( btnId ) {
			case 'btnGeneralExport':
				btn.empty();
				btn.html( 'Generando...' );
				btn.attr( 'disabled', true );
				sendUrlToReportQueue ( linkGeneral, btn );
				notificationModal ( title, body );
				break;
			case 'btnSendedExport':
				btn.empty();
				btn.html( 'Generando...' );
				btn.attr( 'disabled', true );
				sendUrlToReportQueue ( linkSended, btn );
				notificationModal ( title, body );
				break;
			case 'btnFailedExport':
				btn.empty();
				btn.html( 'Generando...' );
				btn.attr( 'disabled', true );
				sendUrlToReportQueue ( linkFailure, btn );
				notificationModal ( title, body );
				break;
		};

	} else {
		return;
	};

});

function notificationModal ( t, b ) {

	var title = $( '#notificationTitle' );
	var body = $( '#notificationBody' );
	title.empty().append( t );
	body.empty().append( b );
	$( '#notificationModal' ).modal( 'show', true );

};

function setupPageByUserProfile() {

    var btnGeneralExport = $( '#btnGeneralExport' );
    var btnSendedExport = $( '#btnSendedExport' );
    var btnFailedExport = $( '#btnFailedExport' );

    if ( UserProfile.enable_report === true ) {

        btnGeneralExport.attr( 'disabled', false );
        btnSendedExport.attr( 'disabled', false );
        btnFailedExport.attr( 'disabled', false );

    } else {
        
        btnGeneralExport.attr( 'disabled', true );
        btnSendedExport.attr( 'disabled', true );
        btnFailedExport.attr( 'disabled', true );

    };

};

function sendUrlToReportQueue ( link, btn ) {

	if ( link != '' || link != null ) {

		$.ajax({
			url: link,
			type: 'GET',
			dataType: 'json',
			success: function ( data ) {
				btn.empty()
				btn.html( 'Generar Excel' );
				btn.attr( 'disabled', false );
				console.log( data );
			},
			error: function ( jqXHR, textStatus, errorThrown ) {
				btn.empty()
				btn.html( 'Generar Excel' );
				btn.attr( 'disabled', false );
				console.log( errorThrown );
			},
		});

	};

};

$( '#run_search' ).on( 'click', function () {
	
	$( '#closeMenuModal' ).click();

	var date_from = $( '#date_from' ).val();
	var date_to = $( '#date_to' ).val();
	var empresas = $( '#empresas' ).val();
	var tipo_receptor = $( '#tipo_receptor' ).val();
	date_from = getDateAsTimestamp( date_from );
	date_to = getDateAsTimestamp( date_to );

	putDownloadLink();
	
	$( '#loadingModal' ).modal( 'show', true );
	$.ajax({
		'type': 'GET',
		'url': urlPath,
		'dataType': 'json',
		'data': {
			'date_from': date_from,
			'date_to': date_to,
			'empresas': empresas,
			'tipo_receptor': tipo_receptor,
		},
		success: function ( data ) {
			jsonData = data;
			drawJsonData();
			$( '#closeLoadingModal' ).click();
		},
		error: function ( jqXHR, textStatus, errorThrown ) {
			$( '#closeLoadingModal' ).click();
			console.log( errorThrown );
		},
	});

});

function drawJsonData () {

	if ( jsonData.statistic ) {
		
		setLegends( jsonData.statistic );
		drawGeneralStatusPieGraph( jsonData.statistic );
		drawSendedStatusPieChart( jsonData.statistic );
		drawFailureStatusPieChart( jsonData.statistic );

	};

	if ( jsonData.results ) {
		
		drawLineGraph( jsonData.results );

	};

};

function setLegends ( data ) {

	var divResumeGeneral = $( '#divResumeGeneral' );
	var divResumeOpened = $( '#divResumeOpened' );
	var divResumeFailure = $( '#divResumeFailure' );

	var htmlGeneral = '';
	var htmlOpened = '';
	var htmlFailure = '';

	if ( data && data.total > 0 ) {
		// calcular general
		htmlGeneral += '<span class="circulo-indigo-500"></span>';
		htmlGeneral += '<label> ';
		htmlGeneral +=  data.delivered + ' enviados ';
		htmlGeneral +=  getPercentage2( data.delivered, ( data.bounced + data.dropped ) );
		htmlGeneral += '%</label><br>';
		htmlGeneral += '<span class="circulo-naranjo-500"></span>';
		htmlGeneral += '<label> ';
		htmlGeneral +=  ( data.bounced + data.dropped ) + ' fallidos ';
		htmlGeneral +=  getPercentage2( ( data.bounced + data.dropped ), data.delivered );
		htmlGeneral += '%</label><br>';

		divResumeGeneral.empty().append( htmlGeneral );

		// calcular abiertos
		htmlOpened += '<span class="circulo-indigo-700"></span>';
		htmlOpened += '<label> ';
		htmlOpened += data.opened + ' leídos ';
		htmlOpened += getPercentage2( data.opened, ( data.delivered - data.opened ) ) + '%</label><br>';
		htmlOpened += '<span class="circulo-indigo-300"></span>';
		htmlOpened += '<label> ';
		htmlOpened += ( data.delivered - data.opened ) + ' no leídos ';
		htmlOpened += getPercentage2( ( data.delivered - data.opened ), data.opened ) + '%</label><br>';

		divResumeOpened.empty().append( htmlOpened );

		// calcular fallidos
		htmlFailure += '<span class="circulo-naranjo-300"></span>';
		htmlFailure += '<label> ';
		htmlFailure += data.bounced + ' rebotados ';
		htmlFailure += getPercentage2( data.bounced, data.dropped ) + '%</label><br>';
		htmlFailure += '<span class="circulo-naranjo-700"></span>';
		htmlFailure += '<label> ';
		htmlFailure += data.dropped + ' rechazados ';
		htmlFailure += getPercentage2( data.dropped, data.bounced ) + '%</label><br>';

		divResumeFailure.empty().append( htmlFailure );

	} else {

		divResumeGeneral.empty().append( '<label>Sin datos en este período</label>' );
		divResumeOpened.empty().append( '<label>Sin datos en este período</label>' );
		divResumeFailure.empty().append( '<label>Sin datos en este período</label>' );

	};

};

function getPercentage2( val1, val2 ) {
	
	if ( val1 === 0 && val2 === 0 ) {
		return 0;
	} else {
		return parseFloat( ( val1 * 100 ) / ( val1 + val2 ) ).toFixed( 1 );
	};

};

function getPercentage3( val1, val2, val3 ) {
	
	if ( va1 === 0 && val2 === 0 && val3 === 0 ) {
		return 0;
	} else {
		return parseFloat( ( val1 * 100 ) / ( val1 + val2 + val3 ) ).toFixed( 1 );
	};

};

function drawLineGraph ( results ) {

	// opciones del grafico.
	var options = {
		'width': '87%',
		'height': '90%',
		'pointSize': 3,
		'chartArea': {
			'left': "3%",
			'top': "3%",
			'height': "83%",
			'width': "83%",
		},
		'fontSize': 11,
		'vAxis': {
			'textStyle': {
				'color': '#212121',
				'fontSize': 10,
			},
			'viewWindow': {
				'min': 0,
			},
		},
		'legend': {
			'position': 'right',
		},
		'explorer': {
			'maxZoomOut': 2,
			'keepInBounds': true,
		},
	};

	// instancia del grafico
	var chart = new google.visualization.LineChart( document.getElementById( 'divLineChart' ) );
	
	var arrayDataTable = new Array();
	arrayDataTable.push(
		[ "Fecha", "Solicitudes", "Procesados", "Enviados", "Leídos", "Rechazados", "Rebotados" ]
	);

	if ( results.length == 0 ) {

		arrayDataTable.push([0,0,0,0,0,0,0]);
		var data = new google.visualization.arrayToDataTable( arrayDataTable );
		chart.draw( data, options );
		chart.clearChart();

	} else {

		for ( var i = 0; i < results.length; i++ ) {
			var row = results[i];
			arrayDataTable.push([
				row.input_date, row.total, 
				row.processed, row.delivered, 
				row.opened, row.dropped, row.bounced
			]);
		};

		var data = new google.visualization.arrayToDataTable( arrayDataTable );
		chart.draw( data, options );

	};
	
};

function drawGeneralStatusPieGraph ( data ) {
	
	var data = google.visualization.arrayToDataTable([
		[ 'Estadísticas', 'Correos' ],
		[ 'Enviados', data.delivered ],
		[ 'Fallidos', ( data.bounced + data.dropped ) ],
		]);

	var options = {
		'pieHole': 0.65,
		'width': '100%',
		'height': '100%',
		'forceIFrame': false,
		'showLables': 'true',
		'colors': [ '#3F51B5', '#FF9800' ],
		'chartArea': {
			'left': "3%",
			'top': "3%",
			'height': "94%",
			'width': "94%",
		},
		'legend': { 'position': 'none', },
	};

	var chart = new google.visualization.PieChart( document.getElementById( 'divGeneralStatusPieChart' ) );
	chart.draw( data, options );

};

function drawSendedStatusPieChart ( data ) {
	
	var data = google.visualization.arrayToDataTable([
		[ 'Estadísticas', 'Correos' ],
		[ 'Leídos', data.opened ],
		[ 'No leídos', ( data.delivered - data.opened ) ],
	]);

	var options = {
		'pieHole': 0.65,
		'width': '100%',
		'height': '100%',
		'forceIFrame': false,
		'showLables': 'true',
		'colors': [ '#303F9F', '#7986CB' ],
		'chartArea': {
			'left': "3%",
			'top': "3%",
			'height': "94%",
			'width': "94%",
		},
		'legend': { 'position': 'none', },
	};

	var chart = new google.visualization.PieChart( document.getElementById( 'divSendedStatusPieChart' ) );
	chart.draw( data, options );

};

function drawFailureStatusPieChart ( data ) {

	var data = google.visualization.arrayToDataTable([
		[ 'Estadísticas', 'Correos' ],
		[ 'Rechazados', data.dropped ],
		[ 'Rebotados', data.bounced ],
	]);

	var options = {
		'pieHole': 0.65,
		'width': '100%',
		'height': '100%',
		'forceIFrame': false,
		'showLables': 'true',
		'colors': [ '#F57C00', '#FFB74D' ],
		'chartArea': {
			'left': "3%",
			'top': "3%",
			'height': "94%",
			'width': "94%",
		},
		'legend': { 'position': 'none', },
	};

	var chart = new google.visualization.PieChart( document.getElementById( 'divFailureStatusPieChart' ) );
	chart.draw( data, options );

};

function getDateAsTimestamp ( date ) {
	
	return moment( date, 'DD/MM/YYYY' ).unix();

};

function setDefaultDates () {
	
	var date_from = $( '#date_from' ).val( moment().subtract( 7, 'days' ).format( 'DD/MM/YYYY' ) );
	var date_to = $( '#date_to' ).val( moment().format( 'DD/MM/YYYY' ) );

};

$( 'button' ).on( "mouseover", function () {
	
	$( this ).popover( 'show' );

});

$( 'button' ).on( "mouseout", function () {
	
	$( this ).popover( 'hide' );

});
