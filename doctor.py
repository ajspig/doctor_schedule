from datetime import datetime, timedelta

class Doctor:
	def __init__(self, doctor_id):
		self.doctor_id = doctor_id
		# TODO: come up with a better datasctructure of the schedule (likely an additonal class)
		self.schedule = {} # key is the date and the value is the list of appointment times for that day 
		# key is the date and the value is the list of open times for that day. prepoulated with the times 8am-4pm UTC
		self.open_times = {}
		# Iterate over dates in November and December 2021
		current_date = datetime(2021, 11, 1).date()
		end_date = datetime(2021, 12, 31).date()
		while current_date <= end_date:
			# Check if the current date is a weekday (Monday to Friday)
			if current_date.weekday() < 5:  # Monday is 0, Sunday is 6
				# Generate available appointment times from 8 am to 4 pm UTC
				available_times = [f"{hour:02}:00" for hour in range(8, 17)]  # 8 am to 4 pm UTC
				self.open_times[current_date.strftime("%Y-%m-%d")] = available_times
			
			# Move to the next day
			current_date += timedelta(days=1)
	
	# find the next available appointment for the doctor on that day (take in optional parameter of new patient (they can only be scheduled between 3-4pm))
	# will return the next available appointment time on that day if there is one. does not update the schedule 
	def next_available_appointment(self, apptDay, newPatient=False):
		apptDay_str = apptDay.strftime('%Y-%m-%d')
		if len(self.open_times[apptDay_str]) == 0: return None # the doctor is booked for the day 
		if newPatient: return self.is_new_patient(apptDay_str) # checking if they are new 
		return self.open_times[apptDay_str][0] # return the first open time in the list, if the doctor is open all day this will be 8:00am 

		
	# add an appointment 
	def add_appointment(self, apptTime):
		# Parse the datetime string including both date and time components
		apptDateTime = datetime.strptime(apptTime, '%Y-%m-%dT%H:%M:%SZ')

		# Extract date and time separately
		apptDate = apptDateTime.date()  # Date component
		apptTime = apptDateTime.strftime('%H:%M') 

		if apptDate in self.schedule:
			self.schedule[apptDate].append(apptTime)
		else:
			self.schedule[apptDate] = [apptTime]		
		self.open_times[apptDate.strftime('%Y-%m-%d')].remove(apptTime)

	def is_new_patient(self, date):
		# check if the date is in the schedule
		if date in self.schedule:
			# check if the time is in the schedule 
			if '15:00' in self.open_times[date]:
				return '15:00'
			if '16:00' in self.open_times[date]:
				return '16:00'
		else:
			# the doctor's schedule is open on the date so they can be scheduled at 3pm UTC
			return '15:00'

