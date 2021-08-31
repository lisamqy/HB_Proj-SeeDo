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


//gets the like button to communicate with server.py's function
$('.like-button').on('click', (evt) => {
    const formInputs = { eventId : evt.target.value }; //gets the button's value aka -> eventId : event.event_id
    $.post("/handle-likes", formInputs, (res) => {
        console.log(res) //prints out whatever the route returns on server.py 
        $('.liked-response').html("Thanks for the like!")
    })
})