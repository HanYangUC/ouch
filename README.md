# ouch - Barber Management System
- This is a backend system for user to book appointment for hair grooming.
- Barber can register and login into the system, select the available timeslot for each day of week, and system will automatically allocate timeslot for them instead of entering each available date-time.
- Customer can search available barber using `get-timeslots` api with the query param `date`, they can filter it based on area too.
- Customer can search specific barber using `get-timeslots/<barber-id>` api with the query param `date`.
> Timeslot will look like `1111100000xx111000001111`, index 0 = slot 00:00-01:00,  `1` indicates available, `0` indicates not available, `x` indicates slot is booked.

- Appointment can be created by providing customer-id, barber-id, start-time, and date.
> start-time is using 24 Hours format, if user want to book on 9am, start-time should be 9.

- After appointment is made, both parties will receive a confirmation email about the appointment and the details of customer (phone number, email, name).
- Booked slot cannot be booked by another customer.
- Both parties will also receive an email if either one cancel the booking.

- Barber cannot update the hour slot if there is an active booking.

## How to run
1. Clone the project
2. Run `docker compose up --build` to re-initialize database and run server. Run `docker compose up` to run server.
3. Interact using the [Postman collection](https://github.com/HanYangUC/ouch/blob/main/Ouch%20Postman.postman_collection.json)
