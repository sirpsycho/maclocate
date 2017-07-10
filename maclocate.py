#!/usr/bin/python

import sys
import optparse
import subprocess
import shlex
import json

##### ENTER GOOGLE API KEY HERE: #####

apikey = ''

######################################

if apikey == '':
	print "Error - edit this script and enter Google API key"
	sys.exit()

url = 'https://www.googleapis.com/geolocation/v1/geolocate?key=%s' % apikey
maclist = []
j = ''
lat = ''
lng = ''
acc = ''
output = ''

# Get Options
parser = optparse.OptionParser()

parser.add_option('-i', '--iface',
                  dest="iface",
                  default='',
                  help='Wireless interface to scan nearby APs',
                 )
parser.add_option('-m', '--mac',
                  dest="macinput",
                  default='',
                  help='MAC address(s) - define a single address or comma-separated list',
                 )
parser.set_usage("Usage: ./maclocate.py [options]\n\nExample: ./maclocate.py -i wlan0\nExample: ./maclocate.py -m 00:00:00:aa:bb:cc")

options, remainder = parser.parse_args()

macinput = options.macinput
iface = options.iface

if not macinput == '':
	# Use manual MAC entries
	print "Using defined MAC address(es)."
	maclist = macinput.split(',')
	macstring = '{"macAddress": "%s"}' % maclist[0]
	if len(maclist) > 1:
	        for mac in maclist[1:]:
	                macstring += ',{"macAddress": "%s"}' % mac
elif not iface == '':
	# Use auto MAC discovery
	datalist = []
	print 'Scanning for APs using interface %s...' % iface
	try:
		iwlistOut = subprocess.check_output(('sudo iwlist %s scan' % iface).split(' '))
	except:
		print "Error (1): iwlist command failed."
		sys.exit()

	ssidData = iwlistOut.split('          Cell ')

	if 'No scan results' in iwlistOut:
		print "Error (2): No scan results."
		sys.exit()
	elif not 'Scan completed :' in ssidData[0]:
		print "Error (3): Access point scan failed."
		sys.exit()
	else:
		ssidData.pop(0)

	for item in ssidData:
		lines = item.split("\n")
		mac = '[none]'
		essid = '[none]'
		for line in lines:
			if 'Address: ' in line:
				mac = line.split('Address: ')[1]
			if 'ESSID:' in line:
				essid = line.split('ESSID:')[1]
		datalist.append([mac, essid])

	print "\nFound nearby BSSIDs:"
	print "#\tMac Address\t\tSSID"
	for item in datalist:
		print "%s\t%s\t%s" % (datalist.index(item) + 1, item[0], item[1])
		maclist.append(item[0])
else:
        print 'Please enter MAC address(s). use -h option for help menu'
        sys.exit()


macstring = '{"macAddress": "%s"}' % maclist[0]
if len(maclist) > 1:
	for mac in maclist[1:]:
		macstring += ',{"macAddress": "%s"}' % mac

jsondata = '{"wifiAccessPoints": [%s]}' % macstring
command = '''curl -sS -H "Content-Type: application/json" -d '%s' "%s"''' % (jsondata, url)
#print "\nRunning command:\n%s" % command
print "\nQuerying Google API..."

try:
	output = subprocess.check_output(shlex.split(command)).strip("\n")
except:
	print "Error: curl command failed."
	sys.exit()

try:
	j = json.loads(output)
	lat = j['location']['lat']
	lng = j['location']['lng']
	acc = j['accuracy']

	print "Found Location!\n"
	print "latitude, longitude: %s, %s" % (lat, lng)
	print "Accuracy radius (m): %s" % acc
except:
	print "Error: Invalid HTTP response"
	sys.exit()
