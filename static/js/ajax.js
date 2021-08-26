'use-strict';

// TODO: adds an event item to the event details ordered list
$('#event-adder').on('click', () => {
    if($('#event-item').val().length>0) {
        $('#event-list').append(`<li>${$('#event-item').val()}</li>`)
    }
})

// TODO: adds an event item from homepage to a user's plan
// $('#dropdown-event-adder').on('click', () => {
//     $('#event-list').append(`<li>${$('option').html()}</li>`)
// })