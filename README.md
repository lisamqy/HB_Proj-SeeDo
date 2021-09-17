# SeeDo

## Table of Contents

*   [Description](#description)
*   [Tech Stack](#tech-stack)
*   [Features](#features)
*   [Running](#running)
*   [About the Developer](#developer)

## <a name="description"></a>Description
**SeeDo** is a full stack web app that allows users to find and plan events to do either now or later. It is for anyone to use, especially those who enjoy planning trips, going to shows or even just browsing for events. Once logged in, a user can create their own plans for different cities within the US and then search for events to add to their existing plans. If they find events that catch their eyes, users can choose to give it a like--which will then displayed the event on their account page. After staying home for a long period, SeeDo can be the tool to help one find something fun to do!

## <a name="tech-stack"></a>Tech Stack
__Front End:__ JavaScript, Jinja2, AJAX, jQuery, HTML5, CSS, Bootstrap<br/>
__Back End:__ Python, Flask, PostgreSQL, SQLAlchemy <br/>

## <a name="features"></a>Features

Search for events within a city with the keyword or date of your choosing:
    ![Event Search](/static/gif-demo/event-search.gif)

<br/>

Logged-in users can create/edit plans, add events to their plans, and give likes to events:
    ![Edit User Plan](/static/gif-demo/edit-plan.gif)
    <ul>⬆️ Shown in gif above ⬆️
        <li> user deleting selected event from the plan </li>
        <li> adding selected event from the dropdown to the plan </li>
        <li> updating the plan's name/overview </li>
    </ul>
    ![Create Plan](/static/gif-demo/create-plan.gif)
    <ul>⬆️ Shown in gif above ⬆️
        <li> user creating a plan based in Las Vegas </li>
        <li> choosing an event located in Las Vegas to add to the current plan </li>
    </ul>
    ![Like Event](/static/gif-demo/liked-event.gif)
    <ul>⬆️ Shown in gif above ⬆️
        <li> user liking an event </li>
        <li> the event will then be displayed on their liked list on their account page </li>
    </ul>

## <a name="setup"></a>Setup/Installation

To run SeeDo on your local machine:

#### Requirements:
- blinker==1.4
- click==7.1.2
- Flask==1.1.4
- Flask-DebugToolbar==0.11.0
- Flask-SQLAlchemy==2.5.1
- greenlet==1.1.1
- itsdangerous==1.1.0
- Jinja2==2.11.3
- MarkupSafe==2.0.1
- requests==2.22.0
- psycopg2-binary==2.8.6
- SQLAlchemy==1.4.22
- Werkzeug==1.0.1

Clone repository:
```
$ git clone https://github.com/lisamqy/HB-Proj
```

Create and activate a virtual environment:
```
$ virtualenv env
$ source env/bin/activate
```

Install the dependencies:
```
$ pip3 install -r requirements.txt
```

Register to use the [Ticketmaster API] (https://developer.ticketmaster.com/products-and-docs/apis/getting-started/)

Save your API keys in a file called <kbd>secrets.sh</kbd> using this format:

```
$ export TICKETMASTERKEY="YOUR_KEY_HERE"
```

Source your keys from your secrets.sh file into your virtual environment:

```
$ source secrets.sh
```

Set up the database:

```
$ createdb project
$ python3 model.py
```

Seed database with data (optional):
```
$ python3 seed.py
```

Run the app:

```
$ python3 server.py
```

You can now navigate to 'localhost:5000/' 

## <a name="developer"></a>About the Developer

Lisa Ma is a new software engineer excited to put her skills to the test and just learn and build stuff!
Learn more on her <a href="https://www.linkedin.com/in/lisa-ma77/">LinkedIn.</a>