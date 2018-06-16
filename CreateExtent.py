import json
import requests

FREENAS = "FREENAS_NAME/IP_Address"
USERNAME = "FREE_USERNAME"
PASSWORD = "FREE_PASSWORD"

r = requests.post(
	'http://' + FREENAS '/api/v1.0/services/iscsi/portal/',
	auth=(USERNAME, PASSWORD),
	headers={'Content-Type': 'application/json'},
	verify=False,
	data=json.dumps({
		"iscsi_target_portal_tag": 1,
        "id": 1,
        "iscsi_target_portal_discoveryauthmethod": "None",
        "iscsi_target_portal_discoveryauthgroup": "",
        "iscsi_target_portal_ips": [
                  "0.0.0.0:3260"
        ],
        "iscsi_target_portal_comment": ""
	})
)
print r.text

for x in range (0, 48):

	NUMBER = x
	NUMBER_PLUS1 = x + 1
	NUMBER_2D = str(x).zfill(2)
	NUMBER_PLUS1_2D = str(NUMBER_PLUS1).zfill(2)
	
	EXTENT = "LUN" + NUMBER_PLUS1_2D
	PATH = "/mnt/VMware-WE/" + EXTENT

	GROUP = NUMBER / 6 
	GROUP += 1

	if GROUP == 1:
		TARGET = "b01-b02"
	elif GROUP == 2:
		TARGET = "b03-b04"
	elif GROUP == 3:
		TARGET = "b05-b06"
	elif GROUP == 4:
		TARGET = "b07-b08"
	elif GROUP == 5:
		TARGET = "b09-b10"
	elif GROUP == 6:
		TARGET = "b11-b12"
	elif GROUP == 7:
		TARGET = "b13-b14"
 	elif GROUP == 8:
		TARGET = "b15-b16"

	LUN = NUMBER_PLUS1 % 6
	if LUN == 0:
		LUN = 6
	
	if (LUN == 3) or (LUN == 6):
		SIZE = "16MB"
	else:
		SIZE = "22GB"

	SERIAL = "08002724ab56" + NUMBER_PLUS1_2D

	INI_IP = NUMBER_PLUS1 % 6

	if INI_IP == 1:

		LAST_IP1 = 170 + (GROUP*2) - 1
		IPADDRESS1 = "10.15.27." + str(LAST_IP1)

		LAST_IP2 = 170 + (GROUP*2)
		IPADDRESS2 = "10.15.27." + str(LAST_IP2)

		AUTH_NET = IPADDRESS1 + "/32\n" + IPADDRESS2 + "/32"

		r = requests.post(
			'http://' + FREENAS '/api/v1.0/services/iscsi/authorizedinitiator/',
			auth=(USERNAME, PASSWORD),
			headers={'Content-Type': 'application/json'},
			verify=False,
			data=json.dumps({
				"iscsi_target_initiator_initiators": "ALL",
         		"iscsi_target_initiator_auth_network": AUTH_NET,
			})
 		)
		print r.text

		r = requests.post(
			'http://' + FREENAS '/api/v1.0/services/iscsi/target/',
			auth=(USERNAME, PASSWORD),
			headers={'Content-Type': 'application/json'},
			verify=False,
			data=json.dumps({
				"iscsi_target_name": TARGET,
			    "iscsi_extent_alias": TARGET,
			    "iscsi_lunid_id": GROUP
	   		})
	 	)
		print r.text

		r = requests.post(
			'http://' + FREENAS '/pi/v1.0/services/iscsi/targetgroup/',
			auth=(USERNAME, PASSWORD),
			headers={'Content-Type': 'application/json'},
			verify=False,
			data=json.dumps({
				"id": GROUP,
	          	"iscsi_target": GROUP,
	          	"iscsi_target_authgroup": "",
	          	"iscsi_target_authtype": "None",
	          	"iscsi_target_portalgroup": "1",
	          	"iscsi_target_initiatorgroup": GROUP,
	          	"iscsi_target_initialdigest": "Auto"
	   		})
	 	)
		print r.text

	r = requests.post(
		'http://' + FREENAS '/api/v1.0/services/iscsi/extent/',
		auth=(USERNAME, PASSWORD),
		headers={'Content-Type': 'application/json'},
		verify=False,
		data=json.dumps({
			"iscsi_target_extent_type": "File",
      		"iscsi_target_extent_name": EXTENT,
      		"iscsi_target_extent_filesize": SIZE,
      		"iscsi_target_extent_path": PATH,
      		"iscsi_target_extent_serial": SERIAL
   		})
 	)
	print r.text

	r = requests.post(
		'http://' + FREENAS '/api/v1.0/services/iscsi/targettoextent/',
		auth=(USERNAME, PASSWORD),
		headers={'Content-Type': 'application/json'},
		verify=False,
		data=json.dumps({
			"iscsi_target": GROUP,
          	"iscsi_extent": NUMBER_PLUS1,
          	"iscsi_lunid": LUN
   		})
 	)
	print r.text

	print GROUP
	print NUMBER_PLUS1
	print LUN

r = requests.post(
	'http://' + FREENAS '/api/v1.0/services/iscsi/authorizedinitiator/',
	auth=(USERNAME, PASSWORD),
	headers={'Content-Type': 'application/json'},
	verify=False,
	data=json.dumps({
		"iscsi_target_initiator_initiators": "ALL",
 		"iscsi_target_initiator_auth_network": "ALL",
	})
	)
print r.text
