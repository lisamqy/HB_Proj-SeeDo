# all_events = {
#   'Van Gogh': {
#       'venue': 'blah blah',
#       'events': [
#                   {'id': 12345, 'start_time': '2021-11-01 12:00', 'end_time': '2021-11-01 12:30'},
#                   {'id': 56789, 'start_time': '2021-11-01 12:30', 'end_time': '2021-11-01 1:00'}
#               ]
#         }
# }

def clean_search_results(tm_response):
    #parse through the event search results 

    events = {}

    for tm_event in tm_response: 
        # set a name key
        name = tm_event['name']
        venue = tm_event['_embedded']['venues'][0]['name'] 
        start_date = tm_event['dates']['start']['localDate']
        # start_time = tm_event['dates']['start']['localTime'] #NOTE shows have multiple show times so might cause user confusion if i add
        #TODO add in a date and time key
        if name not in events: #if name doesnt exist then we add url
            events[name] = [tm_event['url'], venue, start_date]

    return events
   