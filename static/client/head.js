var DefaultOrInitialRide = 0;
var RideBack = 1;
var Reservation = 2;
var baseUrl = 'https://www.better-simple.com';//'https://www.better-simple.com'; //'https://127.0.0.1:8000';
jQuery.support.cors = true;

function SetupEvents(id, uuid) {
	$('head').append('<!DOCTYPE html><meta name="viewport" content="width=device-width, initial-scale=1.0"><link href="https://s3.amazonaws.com/better-simple/bootstrap/css/namespace.css" rel="stylesheet"><link href="https://s3.amazonaws.com/better-simple/jquery-ui-1.8.20.custom.css" rel="stylesheet"><link href="https://s3.amazonaws.com/better-simple/client/css/common.css" rel="stylesheet"><!-- Le HTML5 shim, for IE6-8 support of HTML5 elements --><!--[if lt IE 9]><script src="http://html5shim.googlecode.com/svn/trunk/html5.js"></script><link href="https://s3.amazonaws.com/better-simple/client/css/badie.css" rel="stylesheet"><![endif]--><!--[if gt IE 6]><link href="https://s3.amazonaws.com/better-simple/client/css/badie.css" rel="stylesheet"><![endif]-->');
    $('#better-simple-link').click(function(){
		//if($.browser.msie && 
		if($('#bsContent').length === 0) {
			if ($.browser.msie && window.XDomainRequest) {
				var xdr = new XDomainRequest();
				xdr.onload = function() {
					// XDomainRequest doesn't provide responseXml, so if you need it:
					getSuccess(xdr.responseText);
				};
				xdr.open("get", 'http://www.better-simple.com/reservation/create/'+id.toString()+'/'+uuid+'/');
				xdr.send(); 

			}
			else {
				$.ajax({
					url: baseUrl+'/reservation/create/'+id.toString()+'/'+uuid+'/',
					dataType: "html",
					type: "GET",
					crossDomain: true,
					success: getSuccess
				});
			}
		}
		else {
			$('#bsContent').css('display', '');
		}
    });
}

function getSuccess(d) {
	$('body').prepend('<div style="position:relative; width:99% %;z-index:1000;"><div style="margin:0px auto; width:700px;z-index:1000;"><div id="bsContent" class="bsbt" style="height:600px; width:700px; position: absolute; display:none; top:100px;z-index:1000;"></div></div></div>');
	// console.log(d);
	$('#bsContent').html(d);
	PageIsReady();
	// set page so that future clicks on the link don't cause other event.
	$('#bsContent').css('display', '');
	$('#reserveride').click(function () {
		// remove the errors
		UpdatePageWithErrors(new Object(), new Object(),new Object(),new Object());
		$('#bsbterror').css('display', 'none');
		// display the submitting button.
		$('#submitting').siblings().css('display', 'none');
		$('#submitting').css('display', '');
		
		var pageState = GetPageState();
		pageState = UpdatePageState(pageState);
		UpdatePage(pageState);
		SavePageState(pageState);
		var newReservation = CreateReservationJSON(pageState);
		if ($.browser.msie && window.XDomainRequest) {
	        var xdr = new XDomainRequest();
			xdr.onload = function() {
				// XDomainRequest doesn't provide responseXml, so if you need it:
				postSuccess(xdr.responseText);
			};
			xdr.open("post", 'http://www.better-simple.com/reservation/create/'+id.toString()+'/'+uuid+'/');
			xdr.send(JSON.stringify(newReservation).split('"').join('').split(',').join('&').split("{").join("").split("}").join("").split(":").join("=")); 
	    }
	    else {
		    $.ajax({
			    type: 'POST',
			    url: baseUrl+'/reservation/create/' + id.toString() + '/' + uuid + '/',
			    contentType: "application/json; charset=utf-8",
			    dataType: "json", // With datatype as json, it's already parsed.
			    data: newReservation,
			    crossDomain: true,
			    success: postSuccess,
			    failure: function(x)
			    {
				    alert(x);
			    }
		    });
	    }
		// hack so that clicking back the first time doesn't refresh the page.
		return false;
			
	});
}

function postSuccess(d) {
    // set the reservation buttons back to normal
    $('#submitting').siblings().css('display', '');
    $('#submitting').css('display', 'none');
	var jsonD = null;
	if ($.browser.msie && window.XDomainRequest) {
		jsonD = JSON.parse(d);
	}
	else {
		jsonD = d; // With datatype as json, it's already parsed.
	}
    if(jsonD.created) {
	    // reset the page state cookie so that none of the fileds are populated.
	    DeletePageState();
	    $('.better-simple-close').click();
    }
    else {
	    // update the page and state with the errors
	    var pageState = GetPageState();
	    pageState.CurrentState = UpdatePageWithErrors(jsonD.reservation_form, jsonD.contact_form, jsonD.pickup_address_form, jsonD.dropoff_address_form);
	    SavePageState(pageState);
	    UpdatePage(pageState);
    }
}

function PageIsReady() {
    
    // setup all the jQuery UI date pickers
    $( ".datepicker" ).datepicker();
    
    var landmarks = $('#client_landmarks').length > 0 ? JSON.parse($('#client_landmarks').text()) : [];
    $('.landmark-select').change(function () {
        for( var i = 0; i < landmarks.length; i++) {
            if(landmarks[i].landmark_name === $(this).find(':selected').text()) {
                //alert('found it');
                if($(this).closest('.pickup').length === 1) {
                    $('#id_pickup-address').val(landmarks[i].address);
                    $('#id_pickup-city').val(landmarks[i].city);
                    $('#id_pickup-state').val(landmarks[i].state);
                    $('#id_pickup-zipcode').val(landmarks[i].zipcode);
                }
                else {
                    $('#id_dropoff-address').val(landmarks[i].address);
                    $('#id_dropoff-city').val(landmarks[i].city);
                    $('#id_dropoff-state').val(landmarks[i].state);
                    $('#id_dropoff-zipcode').val(landmarks[i].zipcode);
                }
                break;
            }
        }
    });
    
    $('.address-field').change(function () {
        if($(this).parent().parent().parent().find('#id_pickup-landmarks').length === 1) {
            $(this).parent().parent().parent().find('#id_pickup-landmarks').val(0);
        }
        else if($(this).parent().parent().parent().find('#id_dropoff-landmarks').length === 1) {
            $(this).parent().parent().parent().find('#id_dropoff-landmarks').val(0);
        }
    });
    
	var pageState = GetPageState();
	// Set the page to open up the first page.
    pageState.CurrentState = DefaultOrInitialRide;
	// Setup the default values for the tables
	UpdatePage(pageState);
	
	$('.gotoprevious').click(goToPrevious_Click);
	$('#oneWayTripBtn').click(isOneWayTrip_Click);
	
	$('.better-simple-close').click(function () {
	    $('#bsContent').css('display', 'none');
	    var pageState = GetPageState();
	    pageState = UpdatePageState(pageState);
        pageState.CurrentState = DefaultOrInitialRide;
	    SavePageState(pageState);
	    // hack so that clicking back the first time doesn't refresh the page.
	    return false;
	});
}

function DeletePageState() {
    eraseCookie("PageState");
    // will reset the page
	var pageState = GetPageState();
	UpdatePage(pageState);
}

function CreateReservationJSON(pageState) {
    var time = ConvertToLocalString(pageState.PickupFirstTime);
    var newReservation = {
        reservation_datetime_0:pageState.PickupFirstTime.getMonth()+1 + "/" + pageState.PickupFirstTime.getDate() + "/" + pageState.PickupFirstTime.getFullYear(),
        reservation_datetime_1_hour: time[0],
        reservation_datetime_1_minute: time[1],
        reservation_datetime_1_meridiem:time[2],
        dropoff_datetime_0:pageState.PickupFirstTime.getMonth()+1 + "/" + pageState.PickupFirstTime.getDate() + "/" + pageState.PickupFirstTime.getFullYear(),
        dropoff_datetime_1_hour: time[0],
        dropoff_datetime_1_minute: time[1],
        dropoff_datetime_1_meridiem:time[2],
        name: pageState.Contact.Name,
        phone: pageState.Contact.Phone,
        email: pageState.Contact.Email,
        passengers: pageState.Passengers ? pageState.Passengers : 1,
        special_instructions: pageState.SpecialInstructions,
        'pickup-landmarks': pageState.PickupFirstLocation.Landmark,
        'pickup-address': pageState.PickupFirstLocation.Address,
        'pickup-city': pageState.PickupFirstLocation.City,
        'pickup-state': pageState.PickupFirstLocation.State,
        'pickup-zipcode': pageState.PickupFirstLocation.Zipcode,
        'dropoff-landmarks': pageState.DropoffFirstLocation.Landmark,
        'dropoff-address': pageState.DropoffFirstLocation.Address,
        'dropoff-city': pageState.DropoffFirstLocation.City,
        'dropoff-state': pageState.DropoffFirstLocation.State,
        'dropoff-zipcode': pageState.DropoffFirstLocation.Zipcode
    };
    return newReservation;
}

function UpdatePageWithErrors(reservation_form, contact_form, pickup_form, dropoff_form) {
    //if(reservation_form.reservation_datetime)
    var return_val = Reservation;
    $('#id_name').siblings('.help-inline').html('');
    $('#id_phone').siblings('.help-inline').html('');
    $('#id_email').siblings('.help-inline').html('');
    $('#id_passengers').siblings('.help-inline').html('');
    $('#id_special_instructions').siblings('.help-inline').html('');
    $('#id_pickup-address').siblings('.help-inline').html('');
    $('#id_pickup-landmarks').siblings('.help-inline').html('');
    $('#id_pickup-city').siblings('.help-inline').html('');
    $('#id_pickup-zipcode').siblings('.help-inline').html('');
    $('#id_dropoff-address').siblings('.help-inline').html('');
    $('#id_dropoff-landmarks').siblings('.help-inline').html('');
    $('#id_dropoff-city').siblings('.help-inline').html('');
    $('#id_dropoff-zipcode').siblings('.help-inline').html('');
    $('#id_reservation_datetime_0').siblings('.help-inline').html('');
    $('#bsbterror').css('display', '');
    if(contact_form.name) {
        $.each(contact_form.name, function(index, value) {
            $('#id_name').siblings('.help-inline').append(value + "<br>");
        });
        $('#id_name').parent().parent().addClass('error');
    }
    else {
        $('#id_name').parent().parent().removeClass('error');
    }
        
    if(contact_form.phone) {
        $.each(contact_form.phone, function(index, value) {
            $('#id_phone').siblings('.help-inline').append(value + "<br>");
        });
        $('#id_phone').parent().parent().addClass('error');
    }
    else {
        $('#id_phone').parent().parent().removeClass('error');
    }
        
    if(contact_form.email) {
        $.each(contact_form.email, function(index, value) {
            $('#id_email').siblings('.help-inline').append(value + "<br>");
        });
        $('#id_email').parent().parent().addClass('error');
    }
    else {
        $('#id_email').parent().parent().removeClass('error');
    }
        
    if(reservation_form.passengers) {
        $.each(reservation_form.passengers, function(index, value) {
            $('#id_passengers').siblings('.help-inline').append(value + "<br>");
        });
        $('#id_passengers').parent().parent().addClass('error');
    }
    else {
        $('#id_passengers').parent().parent().removeClass('error');
    }
    
    if(reservation_form.special_instructions) {
        $.each(reservation_form.special_instructions, function(index, value) {
            $('#id_special_instructions').siblings('.help-inline').append(value + "<br>");
        });
        $('#id_special_instructions').parent().parent().addClass('error');
    }
    else {
        $('#id_special_instructions').parent().parent().removeClass('error');
    }
    
    if(pickup_form.address) {
        $.each(pickup_form.address, function(index, value) {
            $('#id_pickup-address').siblings('.help-inline').append(value + "<br>");
        });
        $('#id_pickup-address').parent().parent().addClass('error');
        return_val = DefaultOrInitialRide;
    }
    else {
        $('#id_pickup-address').parent().parent().removeClass('error');
    }
    if(pickup_form.landmarks) {
        $.each(pickup_form.landmarks, function(index, value) {
            $('#id_pickup-landmarks').siblings('.help-inline').append(value + "<br>");
        });
        $('#id_pickup-landmarks').parent().parent().addClass('error');
        return_val = DefaultOrInitialRide;
    }
    else {
        $('#id_pickup-landmarks').parent().parent().removeClass('error');
    }
    if(pickup_form.city) {
        $.each(pickup_form.city, function(index, value) {
            $('#id_pickup-city').siblings('.help-inline').append(value + "<br>");
        });
        $('#id_pickup-city').parent().parent().addClass('error');
        return_val = DefaultOrInitialRide;
    }
    else {
        $('#id_pickup-city').parent().parent().removeClass('error');
    }
    if(pickup_form.zipcode) {
        $.each(pickup_form.zipcode, function(index, value) {
            $('#id_pickup-zipcode').siblings('.help-inline').append(value + "<br>");
        });
        $('#id_pickup-zipcode').parent().parent().addClass('error');
        return_val = DefaultOrInitialRide;
    }
    else {
        $('#id_pickup-zipcode').parent().parent().removeClass('error');
    }
    
    if(dropoff_form.address) {
        $.each(dropoff_form.address, function(index, value) {
            $('#id_dropoff-address').siblings('.help-inline').append(value + "<br>");
        });
        $('#id_dropoff-address').parent().parent().addClass('error');
        return_val = DefaultOrInitialRide;
    }
    else {
        $('#id_dropoff-address').parent().parent().removeClass('error');
    }
    if(dropoff_form.landmarks) {
        $.each(dropoff_form.landmarks, function(index, value) {
            $('#id_dropoff-landmarks').siblings('.help-inline').append(value + "<br>");
        });
        $('#id_dropoff-landmarks').parent().parent().addClass('error');
        return_val = DefaultOrInitialRide;
    }
    else {
        $('#id_dropoff-landmarks').parent().parent().removeClass('error');
    }
    if(dropoff_form.city) {
        $.each(dropoff_form.city, function(index, value) {
            $('#id_dropoff-city').siblings('.help-inline').append(value + "<br>");
        });
        $('#id_dropoff-city').parent().parent().addClass('error');
        return_val = DefaultOrInitialRide;
    }
    else {
        $('#id_dropoff-city').parent().parent().removeClass('error');
    }
    if(dropoff_form.zipcode) {
        $.each(dropoff_form.zipcode, function(index, value) {
            $('#id_dropoff-zipcode').siblings('.help-inline').append(value + "<br>");
        });
        $('#id_dropoff-zipcode').parent().parent().addClass('error');
        return_val = DefaultOrInitialRide;
    }
    else {
        $('#id_dropoff-zipcode').parent().parent().removeClass('error');
    }
    
    if(reservation_form.reservation_datetime) {
        $.each(reservation_form.reservation_datetime, function(index, value) {
            $('#id_reservation_datetime_0').siblings('.help-inline').append(value + "<br>");
        });
        $('#id_reservation_datetime_0').parent().parent().addClass('error');
        return_val = DefaultOrInitialRide;
    }
    else {
        $('#id_reservation_datetime_0').parent().parent().removeClass('error');
    }
    
    // Hack for re-directing back to the initial screen for non-trip reservations
    return_val = $('.reservation').length > 0 ? return_val : DefaultOrInitialRide;

    return return_val;       
}
    
function AjaxWrapper (type, url, data, successCallback) {
       $.ajax({
        type: type,
        url: url,
        contentType: "application/json; charset=utf-8",
        dataType: "html",
        data: data,
        success: successCallback
    });
}
    



function ConvertToLocalString(time) {
	var timeArray = new Array(3);
	var hours = time.getHours();
	if(hours - 12 >= 0) {
		timeArray[0] =  hours - 12;
		timeArray[2] = "PM";
	}
	else {
		timeArray[0] = hours;
		timeArray[2] = "AM"
	}
	timeArray[0] = PrependZeroToTime(timeArray[0] == 0 ? timeArray[0]+12 : timeArray[0]);
	timeArray[1] = PrependZeroToTime(time.getMinutes());
	return timeArray;
}

function PrependZeroToTime(time){
	return (time / 10 < 1 && time.toString().length < 2 ? "0" + time : time);
}

function UpdatePage(pageState){
	$('#reservationIndicator').css('display','none');
	$('#ridebackIndicator').css('display','none');
	if(pageState.CurrentState == DefaultOrInitialRide) {
		var time = ConvertToLocalString(pageState.PickupFirstTime);
		$('#id_reservation_datetime_0').val(pageState.PickupFirstTime.getMonth()+1 + "/" + pageState.PickupFirstTime.getDate() + "/" + pageState.PickupFirstTime.getFullYear());
		$('#id_reservation_datetime_1_hour').val(time[0]);
		$('#id_reservation_datetime_1_minute').val(time[1]);
		$('#id_reservation_datetime_1_meridiem').val(time[2]);
		
		$('#id_pickup-landmarks').val(pageState.PickupFirstLocation.Landmark);
		$('#id_pickup-address').val(pageState.PickupFirstLocation.Address);
		$('#id_pickup-city').val(pageState.PickupFirstLocation.City);
		$('#id_pickup-zipcode').val(pageState.PickupFirstLocation.Zipcode);
		$('#id_pickup-state').val(pageState.PickupFirstLocation.State);
		
		$('#id_dropoff-landmarks').val(pageState.DropoffFirstLocation.Landmark);
		$('#id_dropoff-address').val(pageState.DropoffFirstLocation.Address);
		$('#id_dropoff-city').val(pageState.DropoffFirstLocation.City);
		$('#id_dropoff-zipcode').val(pageState.DropoffFirstLocation.Zipcode);
		$('#id_dropoff-state').val(pageState.DropoffFirstLocation.State);
		$('.rideback').css('display', 'none');
		$('div.reservation').css('display', 'none');
		$('div.location').css('display', '');
		$('.initialride').css('display', '');
	}
	else if(pageState.CurrentState == RideBack) {
		var time = ConvertToLocalString(pageState.PickupSecondTime);
		$('#id_reservation_datetime_0').val(pageState.PickupSecondTime.getMonth()+1 + "/" + pageState.PickupSecondTime.getDate() + "/" + pageState.PickupSecondTime.getFullYear());
		$('#id_reservation_datetime_1_hour').val(time[0]);
		$('#id_reservation_datetime_1_minute').val(time[1]);
		$('#id_reservation_datetime_1_meridiem').val(time[2]);
		
		$('#id_pickup-landmarks').val(pageState.PickupSecondLocation.Landmark);
		$('#id_pickup-address').val(pageState.PickupSecondLocation.Address);
		$('#id_pickup-city').val(pageState.PickupSecondLocation.City);
		$('#id_pickup-zipcode').val(pageState.PickupSecondLocation.Zipcode);
		$('#id_pickup-state').val(pageState.PickupSecondLocation.State);
		
		$('#id_dropoff-landmarks').val(pageState.DropoffSecondLocation.Landmark);
		$('#id_dropoff-address').val(pageState.DropoffSecondLocation.Address);
		$('#id_dropoff-city').val(pageState.DropoffSecondLocation.City);
		$('#id_dropoff-zipcode').val(pageState.DropoffSecondLocation.Zipcode);
		$('#id_dropoff-state').val(pageState.DropoffSecondLocation.State);
		$('.initialride').css('display', 'none');
		$('div.reservation').css('display', 'none');
		$('.rideback').css('display', '');
		$('div.location').css('display', '');
		$('#ridebackIndicator').css('display','');
	}
	else if(pageState.CurrentState == Reservation) {
		$('#reservationIndicator').css('display','');
		$('div.location').css('display', 'none');
		$('.initialride').css('display', 'none');
		$('.rideback').css('display', 'none');
		$('div.reservation').css('display', '');
	}
    $('#id_name').val(pageState.Contact.Name);
    $('#id_email').val(pageState.Contact.Email);
    $('#id_phone').val(pageState.Contact.Phone);
    $('#id_passengers').val(pageState.Passengers);
    $('#id_special_instructions').val(pageState.SpecialInstructions);
	return pageState;
}

function UpdatePageState(pageState) {
	if(pageState.CurrentState == DefaultOrInitialRide) {
		pageState.PickupFirstTime = new Date($('#id_reservation_datetime_0').val() + " " + $('#id_reservation_datetime_1_hour').val()+":"+$('#id_reservation_datetime_1_minute').val() + " " + $('#id_reservation_datetime_1_meridiem').val());
		
		pageState.PickupFirstLocation.Landmark = $('#id_pickup-landmarks').val();
		pageState.PickupFirstLocation.Address = $('#id_pickup-address').val();
		pageState.PickupFirstLocation.City = $('#id_pickup-city').val();
		pageState.PickupFirstLocation.Zipcode = $('#id_pickup-zipcode').val();
		pageState.PickupFirstLocation.State = $('#id_pickup-state').val();
		
		pageState.DropoffFirstLocation.Landmark = $('#id_dropoff-landmarks').val();
		pageState.DropoffFirstLocation.Address = $('#id_dropoff-address').val();
		pageState.DropoffFirstLocation.City = $('#id_dropoff-city').val();
		pageState.DropoffFirstLocation.Zipcode = $('#id_dropoff-zipcode').val();
		pageState.DropoffFirstLocation.State = $('#id_dropoff-state').val();
	}
	else if(pageState.CurrentState == RideBack) {
		pageState.PickupSecondTime = new Date($('#id_reservation_datetime_0').val() + " " + $('#id_reservation_datetime_1_hour').val()+":"+$('#id_reservation_datetime_1_minute').val() + " " + $('#id_reservation_datetime_1_meridiem').val());
		
		pageState.PickupSecondLocation.Landmark = $('#id_pickup-landmarks').val();
		pageState.PickupSecondLocation.Address = $('#id_pickup-address').val();
		pageState.PickupSecondLocation.City = $('#id_pickup-city').val();
		pageState.PickupSecondLocation.Zipcode = $('#id_pickup-zipcode').val();
		pageState.PickupSecondLocation.State = $('#id_pickup-state').val();
		
		pageState.DropoffSecondLocation.Landmark = $('#id_dropoff-landmarks').val();
		pageState.DropoffSecondLocation.Address = $('#id_dropoff-address').val();
		pageState.DropoffSecondLocation.City = $('#id_dropoff-city').val();
		pageState.DropoffSecondLocation.Zipcode = $('#id_dropoff-zipcode').val();
		pageState.DropoffSecondLocation.State = $('#id_dropoff-state').val();
	}
    pageState.Contact.Name = $("#id_name").val();
    pageState.Contact.Email = $("#id_email").val();
    pageState.Contact.Phone = $("#id_phone").val();
    pageState.Passengers = $("#id_passengers").val();
    pageState.SpecialInstructions = $('#id_special_instructions').val();
	return pageState;
}

function isRoundTrip_Click() {
	var pageState = GetPageState();
	pageState = UpdatePageState(pageState);
	pageState.IsRoundTrip = true;
	pageState.CurrentState = RideBack;
	UpdatePage(pageState);
	SavePageState(pageState);
}

function isOneWayTrip_Click() {
	var pageState = GetPageState();
	pageState = UpdatePageState(pageState);
	pageState.IsRoundTrip = false;
	pageState.CurrentState = Reservation;
	UpdatePage(pageState);
	SavePageState(pageState);
}

function ridebackNext_Click() {
	var pageState = GetPageState();
	pageState = UpdatePageState(pageState);
	pageState.CurrentState = Reservation;
	UpdatePage(pageState);
	SavePageState(pageState);
}

function goToPrevious_Click() {
	var pageState = GetPageState();
	pageState = UpdatePageState(pageState);
	if(pageState.CurrentState == RideBack) {
		pageState.CurrentState = DefaultOrInitialRide;
	}
	else if(pageState.CurrentState == Reservation) {
		pageState.CurrentState = (pageState.IsRoundTrip ? RideBack : DefaultOrInitialRide);
	}
	else {
		pageState.CurrentState = DefaultOrInitialRide;
	}
	UpdatePage(pageState);
	SavePageState(pageState);
	// hack so that clicking back the first time doesn't refresh the page.
	return false;
}


function DefaultAddress() {
	var address = new Address("", "", "", "", "", "");
	address.Landmark = "";
	address.Address = "";
	address.City = "";
	address.State = "";
	address.Zipcode = "";
	return address;
}

function Address(landmark, Address, city, state, zipcode) {
	this.Landmark = landmark;
	this.Address = Address;
	this.City = city;
	this.State = state;
	this.Zipcode = zipcode;
}

function DefaultContact() {
    return new Contact("", "", "");
}

function Contact(name, email, phone) {
    this.Name = name;
    this.Email = email;
    this.Phone = phone; 
}

function SavePageState(pageState) {
	pageState.PickupFirstTime = pageState.PickupFirstTime.toJSON();
	pageState.PickupSecondTime = pageState.PickupSecondTime.toJSON();
	createCookie("PageState", JSON.stringify(pageState), 1);
	// Check invalid date for Chrome, NaN for older versions of IE
	pageState.PickupFirstTime = ( new Date(pageState.PickupFirstTime) == 'Invalid Date'  || new Date(pageState.PickupFirstTime) == 'NaN') ? dateFromString(pageState.PickupFirstTime) : new Date(pageState.PickupFirstTime);
	pageState.PickupSecondTime = ( new Date(pageState.PickupSecondTime) == 'Invalid Date' || new Date(pageState.PickupSecondTime) == 'NaN') ? dateFromString(pageState.PickupSecondTime) : new Date(pageState.PickupSecondTime);
}

function GetPageState() {
	
	var pageStateString = readCookie("PageState");
	
	if(pageStateString != null && pageStateString.length > 0 && pageStateString != "undefined")
	{
		// Check invalid date for Chrome, NaN for older versions of IE
		var returnValue = JSON.parse(pageStateString);
		returnValue.PickupFirstTime = ( new Date(returnValue.PickupFirstTime) == 'Invalid Date' || new Date(returnValue.PickupFirstTime) == 'NaN') ? dateFromString(returnValue.PickupFirstTime) : new Date(returnValue.PickupFirstTime);
		
		if(returnValue.PickupFirstTime == null || returnValue.PickupFirstTime == "Invalid Date"  || new Date(returnValue.PickupFirstTime) == 'NaN' ||  returnValue.PickupFirstTime < new Date()) {
			returnValue.PickupFirstTime = new Date();
		}
		returnValue.PickupSecondTime = ( new Date(returnValue.PickupSecondTime) == 'Invalid Date'  || new Date(returnValue.PickupSecondTime) == 'NaN') ? dateFromString(returnValue.PickupSecondTime) : new Date(returnValue.PickupSecondTime);
		if(returnValue.PickupSecondTime == null || returnValue.PickupSecondTime == "Invalid Date"  || new Date(returnValue.PickupSecondTime) == 'NaN' ||  returnValue.PickupSecondTime < new Date()) {
			returnValue.PickupSecondTime = new Date();
		}
		return returnValue;
	}
	else
	{
		return new function() {
			this.CurrentState = DefaultOrInitialRide;
			this.IsRoundTrip = false;
			this.Passengers = "1";
			this.SpecialInstructions="";
			this.PickupFirstLocation = DefaultAddress();
			this.PickupFirstTime = new Date();
			this.DropoffFirstLocation = DefaultAddress();
			this.PickupSecondLocation = DefaultAddress();
			this.PickupSecondTime = new Date();
			this.DropoffSecondLocation = DefaultAddress();
			this.UsePreviousAddress = readCookie("UsePreviousAddress") || true;
			this.Contact = DefaultContact();
		};
	}
}

function createCookie(name,value,days) {
	if (days) {
		var date = new Date();
		date.setTime(date.getTime()+(days*24*60*60*1000));
		var expires = "; expires="+date.toGMTString();
	}
	else var expires = "";
	document.cookie = name+"="+value+expires+"; path=/";
}

function readCookie(name) {
	var nameEQ = name + "=";
	var ca = document.cookie.split(';');
	for(var i=0;i < ca.length;i++) {
		var c = ca[i];
		while (c.charAt(0)==' ') c = c.substring(1,c.length);
		if (c.indexOf(nameEQ) == 0) return c.substring(nameEQ.length,c.length);
	}
	return null;
}

function eraseCookie(name) {
	createCookie(name,"",-1);
}

function dateFromString(s) {
  var bits = s.split(/[-T:Z]/g);
  var d = new Date(bits[0], bits[1]-1, bits[2]);
  d.setUTCHours(bits[3], bits[4], bits[5]);

  return d;
}
