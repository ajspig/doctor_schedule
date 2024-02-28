import os
import requests
from patient import Patient
from doctor import Doctor
from datetime import datetime

api_key = os.environ.get('API_TOKEN')
url = "https://scheduling.interviews.brevium.com/api/Scheduling"

api = "?token=" + api_key
response = requests.post(url + "/Start" + api) # resetting the test system

# GET /api/Scheduling/Schedule request the inital state of the schedule 
response = requests.get(url + "/Schedule" + api)
if response.status_code != 200: 
	print("Error in getting the schedule")
	exit()

patients = {} # key is the personId and the value is the patient object
doctor_schedule = {} # key is the doctorId and the value is doctor object
for appointment in response.json():
	# update the patient schedule
	person_Id = appointment['personId']
	appt_time = appointment['appointmentTime']
	if person_Id not in patients:
		new_patient = Patient(person_Id)
		new_patient.addAppointment(appt_time) 
		patients[person_Id] = Patient(person_Id)
	else:
		patients[person_Id].addAppointment(appt_time)
	if appointment['doctorId'] not in doctor_schedule:
		doctor_schedule[appointment['doctorId']] = Doctor(appointment['doctorId'])
	doctor_schedule[appointment['doctorId']].add_appointment(appt_time)

# loop through all the AppointmentRequests 
response = requests.get(url + "/AppointmentRequest" + api)
appointment = response.json()
while response.status_code != 204:
	# TODO: make this its own class? store the appointment data better
	new_appointment = {
		"doctorId": None,
		"personId": appointment['personId'],
		"appointmentTime": None,
		"isNewPatientAppointment": appointment['isNew'], # TODO: update the API so this naming convention is consistent 
		"requestId": appointment['requestId'],
	}
	# TODO: assumes that preferredDays is in order of preference 
	preferredDays = [day for day in appointment['preferredDays'] if patients[appointment['personId']].isValidDate(day)]

	# according to the specs this shouldn't happen
	if len(preferredDays) == 0: 
		print("No valid days for the patient")
		exit()
	# loop through all the appointments preferedDocs and for each one check if the doc has availability on that day 
	# TODO: this assumes the patient wants to have thier preferred doctor over the preferred days. I did this becuase I would much rather have the doctor I like on an more inconvient day then vice versa
	# TODO: this also assumes that preferredDocs is in order of preference 
	for doctor in appointment['preferredDocs']:
		# check if the doctor has availability for each of the preferredDays
		for day in preferredDays:
			# strip day so its just YYYY-MM-DD
			day = datetime.strptime(day, '%Y-%m-%dT%H:%M:%SZ').date()
			time = doctor_schedule[doctor].next_available_appointment(day)
			if time is not None:
				# if they do then schedule the appointment 
				new_appointment['appointmentTime'] = day.strftime('%Y-%m-%d') + "T" + time
				new_appointment['doctorId'] = doctor
				appointment_scheduled = True
				break 
		if appointment_scheduled: break
	if not appointment_scheduled:
		# if the loop finishes and the appointment is not scheduled this is a problem 
		# according to the specs this should not happen
		print("No valid doctors for the patient")
		exit()
	# now the new_appointment is built we can schedule it
	# POST /api/Scheduling/AppointmnetRequest request to schedule an appointment
	print ("appointment to be scheduled:" , appointment)
	print("Scheduling appointment: ", new_appointment)
	response = requests.post(url + "/Schedule" + api, json=new_appointment)
	if response.status_code != 200: 
		print("Error in scheduling the AppointmentRequest. Error code: ", response.status_code)
		exit()
	# update the doctor schedule
	doctor_schedule[doctor].add_appointment(new_appointment['appointmentTime'])
	#update the patient schedule
	patients[appointment['personId']].addAppointment(new_appointment['appointmentTime'])
	response = requests.get(url + "/AppointmentRequest" + api)
	appointment = response.json()
		

# once done hit the /api/Scheduling/stop endpoint to stop the test system
response = requests.post(url + "/Stop" + api) # stop test system and returns the final state of the schedule
print(response.status_code)
print("FINAL RESULT: ", response.json())
