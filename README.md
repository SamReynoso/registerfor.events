# This is a README


## Backend Notes.
- [ ] Rename notifications app to mailbox.
- [ ] Handle team deletion with existing registrations.
- [ ] Do a full ownership check audit on every view in every app.
- [ ] Think about removing or moving events hosts and teams views from base views.
- [ ] Rename create app to 'app' and create two views pages.
- [ ] Create three views files in app. (user_views, host_view, participant_views)
- [ ] Move all crude endpoint to the 'app' app.

## List of things I think I should do tomorrow. (on day 4)
### Status related
- [ ] Add withdraw logic to registration view.
- [ ] Add registration status to event host view.
- [ ] Add a event host registration management view.
- [ ] Add event status update view.
- [ ] Add event cacelation view, and logical ramifications of such an action.
- [ ] Add team deleat view, and handle logic for its registrations.
### Alert related
- [ ] Add new registration alert.
- [ ] Add new registration withdraw alert.
- [ ] Add event cancellation alert.
- [ ] Add registration cancellation alert from the host side.
- [ ] Add new message alert.
- [ ] Add new announcement alert.
### Media related
- [ ] Add profile picture upload feature.
- [ ] Add event post upload feature. 
### Message related
- [ ] Add host/event announcement creation view.
- [ ] Add participant announcement mailbox view.
- [ ] Remove notifications in favor of alerts.

## Possible must have features that will need to be added.
- [ ] Add additional contact information requirements to registration.
- [ ] Host options for registration contact information requirements.
- [ ] Email notifications and control page.
- [ ] Host email remiders and update features.
- [ ] Host and participant email confirmation at time of registration.
- [ ] Email confirmation at time of event creation.
- [ ] Registration withdrawal email notification.
- [ ] Event cancellation email notification.

## Clean up before first test deploy.
- [ ] Poster/other image sizing.
- [ ] Sports ball thumbnail images.
- [ ] Links from details pages to edit pages for asset owners.
- [ ] Proper page level heading and descriptions. Or atleast remove placeholder text.
- [ ] Add checkmark icon to registration page.

## Possible nice touches if free.
- [ ] Optional fine grain address for events.
- [ ] Map support on event details page.

## Frontend notes.
- [ ] Minimal search bar on landing page.
- [ ] Division details is bare.
- [ ] Team details is very very bare.
- [ ] Registration page needs to be nicer. (probably create a tournent overview card snippet)
- [ ] add link to host on registration page.
- [ ] make it clear that you are looking at your registrations on the "my events" page.
- [ ] Fix links on "my events" page.
- [ ] Participant Registration page is bare.
- [ ] Finish Upcoming Event/Past Events table on team account view.
- [ ] Delete on other options for account control to the profile account page.
- [ ] Add footer to all pages except for in messaging.
### Messageing
- [ ] Create mailbox root page for direct messages, announecments, and alerts.
- [ ] Create conversations list card for direct messages.
- [ ] Create alerts list with simple details/summary elements.
- [ ] Finish cool announcements page.
- [ ] Add scrolling message box in direct messaging.
- [ ] Create message cards with links to user profile and profile picture.

## Styling notes.
- [ ] Add styling to login and register pages.
- [ ] Clickable card on landing page.
- [ ] Fix width of search results.
- [ ] Add event creation form styling.
- [ ] Add event details styling.
- [ ] Fix width of event details page tables. (possibly just setting globally)
- [ ] Add styling to team account view.
- [ ] Add styling to profile update form.

## Possible data integrity concernes.
- [ ] Creating an event without enough contact information in profile.
- [ ] Registering for an event without enough contact information in profile.
