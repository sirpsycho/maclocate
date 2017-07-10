# maclocate
Locate a device using surrounding wireless access points

# Description
This script uses the Google Geolocation API to accurately map a device's location based on MAC addresses of surrounding wireless routers. Location info is output in lat/long coordinates that are normally accurate down to a particular street address. Currently, this script is designed for linux-based operating systems (tested in Kali Linux).



Note: This requires an API key from Google, which can be aquired for free [here](https://developers.google.com/maps/documentation/geolocation/get-api-key) (requires a Google account).

```
Usage: maclocate.py [options]

Example: ./maclocate.py -i wlan0
Example: ./maclocate.py -m 00:00:00:aa:bb:cc

Options:
  -h, --help                    show this help message and exit
  -i IFACE, --iface=IFACE       Wireless interface to scan nearby APs
  -m MACINPUT, --mac=MACINPUT   MAC address(s) - define a single address or comma-separated list
```
