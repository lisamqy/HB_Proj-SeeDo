'use-strict';

// TODO: adds an event item to the event details ordered list
$('#event-adder').on('click', () => {
    $('#event-list').append(`<li>${$('#event-item').val()}</li>`)
})

// TODO: adds an event item from homepage to a user's plan
$('#event-box-adder').on('click', () => {
    $('#event-list').append(`<li>${$('#event-overview')}</li>`)
    $('#event-list').html('Added!')
})