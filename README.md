# meet-me2

One of the problems with existing applications like when2meet, doodle, etc. that help users to coordinate meeting times is that they are so tedious to use repeatedly - users have to put in virtually the same information each time they want to use the app to meet with a new person. I want to create an application that will allow users to co-ordinate meeting times by uploading their ical calendars, and/or maybe create some 'default' times they're free that they can edit each time as needed.

This is an [extension](https://github.com/angelinahli/meet-me) of a project created during [Sister Hacks 2018](http://sisterhacks.co/).

I am incredibly indebted to [Miguel Grinberg](https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world)'s excellent introduction to the Flask framework.

## done
* Learn how to properly manage user sessions and implement that
    * added login and sign up pages
* Have the app running such that you can log in and logout
* Write out your uml diagram - users, schedules, events.
* Create responsive navbar
* Make the search bar look nicer
* Create test dataset of users
* Create user settings pages - update user information, change password, change email, delete account
* Create user profile pages
* update validation functions
* figure out some other way of doing the multiple submit button stuff
* create form allowing users to set up events with each other
* add validators for new event page
* Create better way of managing username and password validation (get rid of the ugly program_info module or make it better)
* Load in and load out user dataset
* Create a schedule page where people can view a representation of their schedule
* (Eventually) update the spaces between input fields in the login form to make everything look more standardized
* allow users to set up events with one another and return the possible dates of the event
* added custom error pages for 404 and 500 errors
* Create a search feature to search for users by username, first name, last name, email
    * if match one person, return that person
    * if match multiple people, return all results that match
* (Eventually) update the front page to make it look nicer
* display the possible event times to the user better

## backlog

### front end
* make search bar width expand to fill page
* update the sign up page validation text
* Rethink the user page - what needs to be on there?

### somewhere in between?
* organize searches with pages, perhaps sort search results
* Allow users to add each other?
* add ability to specify event duration by hour : min
* make it easier to find users to hold events with

### back end
* allow user to create and add an event to their google calendar from the new_event page
* create testing units for all of this
* add validator to ensure that event is not more than 24 hours long
* add validator to ensure that start and end times are different
* Allow users to update their schedule with different events
* research potential methods possible to have scheduling data.
    * work first on ability to modify your schedule from scratch (create "templates"?)
* rethink algorithm on finding matching free times - probably a better one out there
* send yourself an email whenever an error occurs https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-vii-error-handling
