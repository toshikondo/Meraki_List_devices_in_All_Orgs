import requests
import json
import pandas as pd
import os
import pathlib
from datetime import date


DATE_FOLDER = './' + str(date.today())
pathlib.Path(DATE_FOLDER).mkdir(exist_ok=True)

url_org = "https://api.meraki.com/api/v1/organizations"
api_key = os.environ.get('MERAKI_DASHBOARD_API_KEY')  #<= Getting Meraki API-Key value from environment variable. 
                                                      #   You need to set MERAKI_DASHBOARD_API_KEY as an environment variable                           

payload={}
headers = {
  'X-Cisco-Meraki-API-Key': api_key  
}

response_org = requests.request("GET", url_org, headers=headers, data=payload)

json_data_org_list = response_org.text
json_object_org_list = json.loads(json_data_org_list)
#json_formatted_str_org_list = json.dumps(json_object_org_list, indent=2)
#print(json_data_org_list)
#print(json_formatted_str_org_list)

print('You can access to these Organizations')

for org in json_object_org_list:
  print(' -' + org['name'] + ',  OrganizationId: ' + org['id'])

for org_info in json_object_org_list:
  print()
  print("##### " + 'OrganizationID = ' + org_info['id'] + " #####")
  print('Getting Device information from Organization: ' + org_info['name']  +'\n')
  organizationId = org_info['id']

  url_dev = f"https://api.meraki.com/api/v1/organizations/{organizationId}/devices"

  response_dev = requests.request("GET", url_dev, headers=headers, data=payload)

  dev_list = json.loads(response_dev.text)
  #print(type(dev_list))

  df = pd.json_normalize(dev_list)
  #print(df)
  df.index += 1 #<== Index start from 1 instead of 0.
  #print(df)

  df.to_csv(DATE_FOLDER + '/' + org_info['name'] + '_OrgID_' + org_info['id'] + '.csv')
  
