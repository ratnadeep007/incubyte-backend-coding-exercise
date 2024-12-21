# Solution

I started with exploring how things are implemented in the repo previously and started laying ground for schdule and appointment models. Added seed data to the schedule and appointment models. Create basic routes to `GET` schedules and appointments. After `GET` routes, I started to add `POST` routes for creating schedules and appointments. While creating the apppointment, I added a check to see if the doctor is available at the given time and location and there is no appointment at the same time. If the doctor is available, the appointment is created. If the doctor is not available, a `404` is returned and if there is an appointment at the same time, a `409` is returned. I also added a `DELETE` route for cancelling an appointment which is soft delete that changes the `is_active` field to `False`.

I have added tests cases for availability service but run as its giving error in sqlite3 and due to time constraints I didn't get time to fix it.

## What can be improved

- First of all appointment can be improved by adding a max time limit for each appointment. This will help in avoiding the situation where a doctor is available for a long time and the appointment is created for a short time.
- Schedule can be `active` or `inactive` as doctor can be available or not. This will help to avoid situations where schedule is there but doctor is not available.