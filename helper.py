
def clean_search_results(tm_response):
    #parse through the event search results 

    events = {}

    for tm_event in tm_response: 
        # set a name key
        name = tm_event['name']
        image = tm_event['images'][0]['url']
        venue = tm_event['_embedded']['venues'][0]['name'] 
        city = tm_event['_embedded']['venues'][0]['city']['name'] 
        start_date = tm_event['dates']['start']['localDate']
        # start_time = tm_event['dates']['start']['localTime'] #NOTE shows have multiple show times so might cause user confusion if i add
        if name not in events: #if name doesnt exist then we add url
            events[name] = [tm_event['url'], image, venue, city, start_date]

    return events
   