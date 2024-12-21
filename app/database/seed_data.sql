DELETE FROM doctor_locations;
DELETE FROM doctors;
DELETE FROM locations;

INSERT INTO doctors(id, first_name, last_name) VALUES (0, 'Jane', 'Wright');
INSERT INTO doctors(id, first_name, last_name) VALUES (1, 'Joseph', 'Lister');

INSERT INTO locations(id, address) VALUES (0, '1 Park St');
INSERT INTO locations(id, address) VALUES (1, '2 University Ave');

INSERT INTO doctor_locations(id, doctor_id, location_id) VALUES (0, 0, 0);
INSERT INTO doctor_locations(id, doctor_id, location_id) VALUES (1, 1, 0);
INSERT INTO doctor_locations(id, doctor_id, location_id) VALUES (2, 1, 1);

INSERT INTO doctor_schedules(id, doctor_id, location_id, start_time, end_time) VALUES (0, 0, 0, '09:00', '10:00');
INSERT INTO doctor_schedules(id, doctor_id, location_id, start_time, end_time) VALUES (1, 1, 0, '09:00', '10:00');
INSERT INTO doctor_schedules(id, doctor_id, location_id, start_time, end_time) VALUES (2, 1, 1, '09:00', '10:00');

INSERT INTO doctor_appointments (id, doctor_id, location_id, time, patient_name, is_active) VALUES (0, 0, 0, '09:00', 'Jane', 1);
INSERT INTO doctor_appointments (id, doctor_id, location_id, time, patient_name, is_active) VALUES (2, 1, 1, '10:00', 'Joseph', 1);
INSERT INTO doctor_appointments (id, doctor_id, location_id, time, patient_name, is_active) VALUES (3, 1, 2, '10:00', 'Joseph', 1);