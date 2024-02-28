import os
import requests

api_key = os.environ.get('API_TOKEN')
url = "https://scheduling.interviews.brevium.com/api/Scheduling"

api = "?token=" + api_key
response = requests.post(url + "/Start" + api) # resetting the test system
print(response.status_code)
# GET /api/Scheduling/Schedule request the inital state of the schedule 
response = requests.get(url + "/Schedule" + api)
print(response.status_code)

# call the api/Scheduling/AppointmnetRequest until no more appointments requests left (return code 204)
response = requests.get(url + "/AppointmentRequest" + api)
print(response.status_code)

# once done hit the /api/Scheduling/stop endpoint to stop the test system
response = requests.post(url + "/Stop" + api) # stop test system and returns the final state of the schedule
print(response.status_code)
