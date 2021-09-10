'use-strict';

// TODO: adds an event item to the event details ordered list
$('#event-adder').on('click', () => {
    if($('#event-item').val().length>0) {
        $('#event-list').append(`<li>${$('#event-item').val()}</li>`)
    }
})


//gets the like button to communicate with server.py's function
$('.like-button').on('click', (evt) => {
    const formInputs = { eventId : evt.target.value }; //gets the button's value aka -> eventId : event.event_id
    $.post("/handle-likes", formInputs, (res) => {
        console.log(res) //prints out whatever the route returns on server.py 
        $('.liked-response').html("Thanks for the like!")
        let currentLike = parseInt($('#like-counter').html())
        $('#like-counter').html(currentLike+1)
        $('.like-button').attr("disabled", "disabled"); // disable button
    })
})


//allow user to hide/show event overview details editor
$("input[name=btnEditOverview]").on('click', () => {
    if ($("#dvEditOverview").hasClass("hide")) {
        $("#dvEditOverview").removeClass("hide");
    } else {
        $("#dvEditOverview").addClass("hide")
    }
     
});


//allow user to target which event they'd like to delete from their current plan
$('.del-event-from-plan-btn').on('click', (evt) => {
    const plan_id = $('#plan_id').html();
    const event_id = evt.target.value; //gets the button's value aka -> eventId : event.event_id
    $.get(`/plan/${plan_id}/delete/${event_id}`, (res) => {
        console.log(res) //prints out whatever the route returns on server.py 
        $(`#li${event_id}`).remove();
    })
})

//guides user to create/search for events if none found for current city
if ($('#dropdown-event')[0].length < 1 ) {
    $('#relevant-events').remove();
    $('#no-relevant-events').removeClass("hide");
}