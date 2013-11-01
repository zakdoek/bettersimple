$.ajax({
    url: 'http://127.0.0.1:8000/clients/1/',
    dataType: "html",
    type: "GET",
    success: function(d){ alert(d); }
    });

$.post({
    url: 'http://127.0.0.1:8000/reservation/create/1/',
    dataType: "json",
    data: {pickup_datetime:'2012-04-18 21:06:41', dropoff_datetime:'2012-04-20 21:07:49', name:'Timbo slice', phone:'23423443', email:'schilling711@gmail.com'},
    success: function(d){ alert(d); }
});

var newReservation = {
    pickup_datetime:'2012-04-18 21:06:41',
    dropoff_datetime:'2012-04-28 21:06:41',
    name: 'jsonUser',
    phone: 'Fuckoff',
    email: 'fuckoff@fucking.fuck',
    pickup-landmark: 'Your arse',
    pickup-address: '12345',
    pickup-city: 'Jackass',
    pickup-state: 'WI',
    pickup-zipcode: '12345',
    dropoff-landmark: 'Junk',
    dropoff-address: 'Junk2',
    dropoff-city: 'Junk3',
    dropoff-state: 'AL',
    dropoff-zipcode: '67890'
};

    $.ajax({
        type: 'POST',
        url: 'http://127.0.0.1:8000/reservation/create/1/',
        contentType: "application/json; charset=utf-8",
        dataType: "html",
        data: newReservation,
        success: function(d)
        { 
            alert('success');
        },
        failure: function(x)
        {
            alert('fail motherfucker');
        }
    });
