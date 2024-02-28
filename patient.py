from datetime import datetime

class Patient:
	def __init__(self, patient_id):
		self.patient_id = patient_id
		self.schedule = [] # list of appointment dates ( strip the date since we dont care about the time, just the day)

	def addAppointment(self, apptTime):
		# strip the apptTime to just the date
		apptDate = datetime.strptime(apptTime, '%Y-%m-%dT%H:%M:%SZ').date()  # Parse date and time, then extract date
		self.schedule.append(apptDate)
		self.schedule.sort() # TODO: come up with a better sorting logic then just sorting every time. 
		return self.schedule
	
	def isValidDate(self, apptTime):
		# TODO: since the schedule is already sorted change it to a binary search to improve efficiency when searching throught the list 
		apptTime_date = datetime.strptime(apptTime, '%Y-%m-%dT%H:%M:%SZ').date()
		for date in self.schedule:
			if abs((date - apptTime_date).days) < 7:
				return False	
		return True 
	
