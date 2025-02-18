# Sophos XG API Python

This python application communicates directly to Sophos XG(S) devices through it's API.

Requirements
* Python Module: sophosfirewall-python (pip install sophosfirewall-python)
* "XIOR_default_guarantee traffic" shaping rule on firewall
* Activate API access on firewall (Backup & Firmware > API)

Manual:
1. Set var_username, var_password in script.py
2. Add ip-adresses of firewalls to hostnames list
3. Run script