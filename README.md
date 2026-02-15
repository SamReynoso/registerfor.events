# This is a README


## Backend Notes.
- [x] Rename notifications app to mailbox.
- [x] Handle team deletion with existing registrations.
- [x] Think about removing or moving events hosts and teams views from base views.
- [x] Rename create app to 'app' and create two views pages.
- [x] Create three views files in app. (user_views, host_view, participant_views)
- [x] Move all crude endpoint to the 'app' app.
- [ ] Do a full ownership check audit ~~on every view in every app~~.
- [x] Add redirect after updating event divisions.
- [ ] Add unique constraints to models.

## List of things I think I should do tomorrow. (on day 4)
### Status related
- [x] ~~Add withdraw logic to registration view.~~ Just delete the registrations for now.
- [x] ~~Add registration status to event host view.~~
- [x] Add a event host registration management view.
- [x] Add event status update view.
- [x] Add event cacelation view, and logical ramifications of such an action.
- [x] Add team deleat view, and handle logic for its registrations.
### Media related
- [x] Add profile picture upload feature.
- [x] Add event poster upload feature. 
### Alert related
- [x] Add new registration alert.
- [x] Add new registration withdraw alert.
- [x] Add event cancellation alert.
- [x] Add registration cancellation alert from the host side.
- [x] ~~Add new message alert.~~
- [x] ~~Add new announcement alert.~~
### Message related
- [x] Add host/event announcement creation view.
- [x] Add participant announcement mailbox view.
- [x] Remove notifications in favor of alerts.

## Priority
- [ ] Add additional contact information requirements to registration.
- [x] Email notifications
- [ ] Email control page.
- [x] Host and participant email confirmation at time of registration.
- [x] Event cancellation email notification.
- [x] Proper page level heading and descriptions. Or atleast remove placeholder text.
- [x] Change text input to dropdown in create event form.
- [ ] Finish cool announcements page.
- [x] Add styling to login and register pages.


## Possible must have features that will need to be added.
- [ ] Host options for registration contact information requirements.
- [ ] Host email remiders and update features.
- [x] ~~Email confirmation at time of event creation.~~
- [x] Registration withdrawal email notification.

## Clean up before first test deploy.
- [x] Poster/other image sizing.
- [x] Sports ball thumbnail images.
- [x] ~~Links from details pages to edit pages for asset owners.~~
- [ ] Add checkmark icon to registration page.

## Possible nice touches if free.
- [x] Optional fine grain address for events.
- [ ] Map support on event details page.
- [ ] Request a division be added to an event.

## Frontend notes.
- [x] Fix all links from create app refactor.
- [x] Division details is bare.
- [x] Team details is very very bare.
- [x] Registration page needs to be nicer. (probably create a event overview card snippet)
- [x] add link to host on registration page.
- [x] make it clear that you are looking at your registrations on the "my events" page.
- [x] Fix links on "my events" page.
- [ ] Add a sport photo to the header in details if you sport is known.
- [ ] Minimal search bar on landing page.
- [x] Participant Registration page is bare.
- [ ] Finish Upcoming Event/Past Events table on team account view.
- [ ] Delete and other options for account control to the profile account page.
- [ ] Add footer to all pages except for in messaging.
- [ ] Add links from owner detail view to public detail view. i.e. events.
### Messageing
- [x] Create mailbox root page for direct messages, announecments, and alerts.
- [x] Create conversations list card for direct messages.
- [x] Create alerts list with simple details/summary elements.
- [ ] Add scrolling message box in direct messaging.
- [ ] Create message cards with links to user profile and profile picture.

## Styling notes.
- [x] Clickable card on landing page.
- [x] Fix width of search results.
- [x] Add event details styling.
- [x] Fix width of event details page tables. (possibly just setting globally)
- [x] Add styling to profile update form.
- [ ] Add event creation form styling.
- [ ] Add styling to team create form.
- [ ] Add styling to team account view.

## Possible data integrity concernes.
- [ ] Creating an event without enough contact information in profile.
- [ ] Registering for an event without enough contact information in profile.
