# THIS FILE IS INDEPENDENT OF THE MAIN APP AND CAN BE RUN SEPARATELY.
# THIS FILE ONLY SENDS REQUESTS TO THE SERVER FOR UP.

import requests,time,datetime
print('========== REQUEST SENDING MODULE ==========')
request_urls={
"LOGIN PAGE":"https://dpsjalesar.onrender.com",
"DASHBOARD":"https://dpsjalesar.onrender.com/dashboard",
"ADMISSION PAGE":"https://dpsjalesar.onrender.com/DPSADMISSION_FORM",}
set_time = 10 #every 10 seconds
fail = 0
i = 0
while True:
	if fail >= 3:
		break
	for item in request_urls.keys():
		t = datetime.datetime.now().strftime("%H:%M:%S")
		d = datetime.date.today()
		if int(requests.head(request_urls[item],headers={"User-Agent": "Chrome/5.0"}).status_code) == 200:
			print(f'SUCCESS!!! [{d},{t}] --> {item}\n{request_urls[item]}')
			fail = 0
			time.sleep(set_time)
		else:
			print(f'FAILED!! [{d},{t}] --> {item}\n{request_urls[item]}')
			fail += 1
			time.sleep(set_time)
			
if fail >= 3:
	while True:
		i+=1
		print(f'{i}. SYSTEM GOT AN ERROR !!!\n[{d},{t}]')
		time.sleep(0.1)