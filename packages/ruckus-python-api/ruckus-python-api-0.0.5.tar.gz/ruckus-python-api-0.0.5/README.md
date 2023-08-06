# ruckus_python_client

#Install and configure ambiance
$python3 -m venv env
$pip install -e .
$pip install ipython

#Start Project
$ipython
$from ruckus_api import SmartZoneClient, VSpotClient
$SmartZoneClient(url, username, password)
$VSpotClient(url, api_key)
