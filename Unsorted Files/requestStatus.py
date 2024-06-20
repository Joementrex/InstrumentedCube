import requests
import time

url = 'http://192.168.2.10/api/printer/command'
status_url = 'http://192.168.2.10/api/printer'
headers = {'Content-Type': 'application/json', 'X-Api-Key': 'BF587631209C498EB55CD8615F12C02E'}

# payload = {
#     'commands': [
#         'G28 ; Home all axes',
#         'G1 Z15 F9000 ; Move the platform down 15mm at a speed of 9000mm/min'
#     ]
# }

# response = requests.post(url, headers=headers, json=payload)

# if response.status_code == 204:
#     print('Commands sent successfully')
# else:
#     print('Failed to send commands:', response.status_code, response.text)

# time.sleep(3)

response = requests.get(status_url, headers=headers)

if response.status_code == 200:
    printer_status = response.json()
    if printer_status['state']['text'] == 'Operational':
        print('Printer is operational')
    else:
        print('Printer is not operational')
else:
    print('Failed to get printer status:', response.status_code, response.text)

time.sleep(12)

# Tell the printer that it is printing
response = requests.post(url, headers=headers, json={'command': 'M117 Printing...'})


response = requests.get(status_url, headers=headers)
if response.status_code == 200:
    printer_status = response.json()
    if printer_status['state']['text'] == 'Operational':
        print('Printer is operational')
    else:
        print('Printer is not operational')
else:
    print('Failed to get printer status:', response.status_code, response.text)

response = requests.get(status_url, headers=headers)

if response.status_code == 200:
    printer_status = response.json()
    if printer_status['state']['flags']['printing']:
        print('Printer is currently printing')
    else:
        print('Printer is not printing')
else:
    print('Failed to get printer status:', response.status_code, response.text)