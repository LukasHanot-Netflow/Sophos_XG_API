# Import necessary modules
from sophosfirewall_python.firewallapi import SophosFirewall
import re

var_username = "api-administrator"
var_password = "EnterPasswordHere"
hostnames = ["xxx.xxx.xxx.xxx", ]


def get_vlans(student_vlans, zone_name = "STUDENT"):
    """Populates the student_vlans list with vlans who have given Zone assigned"""
    try:
        response = sfos.get_vlan()
        vlans = response["Response"]["VLAN"]
        for vlan in vlans:
                if vlan['Zone'] == zone_name:
                    #print(vlan)
                    student_vlans.append(vlan)

    except SophosFirewall.SophosFirewallAuthFailure as e:
        print(f"Authentication error: {e}")

def create_host(student_vlans):
    """Creates host objects for every network in given list of vlans"""
    try:
        for student_vlan in student_vlans:
            vlan_ipaddress = student_vlan['IPAddress']
            vlan_ipaddress_formated = re.sub(r'\b(\d+\.\d+\.\d+)\.\d+\b', r'\1.0', vlan_ipaddress)
            vlan_name = "vlan_" + student_vlan['VLANID'].zfill(3)
            #print("name=" + vlan_name + " , ip_address=" + vlan_ipaddress_formated + ", mask=" + student_vlan['Netmask'])
            response = sfos.create_ip_network(name=vlan_name, ip_network=vlan_ipaddress_formated, mask=student_vlan['Netmask'])
            print(response)

    except SophosFirewall.SophosFirewallAuthFailure as e:
        print(f"Authentication error: {e}")


def create_firewall_rules(student_vlans):
    """Creates a firewall rule for each vlan"""
    try:
        for student_vlan in student_vlans:
            vlan_rulename = "allow v" + student_vlan['VLANID'].zfill(3) + " WAN"
            vlan_source_net = "vlan_" + student_vlan['VLANID'].zfill(3)
            rule_params = dict(
                rulename=vlan_rulename,
                position="Before",
                before_rulename='Allow Student WAN',
                description="allows outbound traffic for vlan v" + student_vlan['VLANID'].zfill(3),
                action="Accept",
                log="Enable",
                src_zones=["STUDENT"],
                dst_zones=["WAN"],
                src_networks=[vlan_source_net],
                dst_networks=["Internet IPv4 group"],
                service_list=["HTTPS", "HTTP", "NTP", "DNS"],
                traffic_shaping='XIOR_default_guarantee'
            )

            response = sfos.submit_template(filename="FirewallRule.xml", template_vars=rule_params, template_dir="")
            print(response)

    except SophosFirewall.SophosFirewallAuthFailure as e:
        print(f"Authentication error: {e}")

## Main
for var_hostname in hostnames:
    student_vlans = []
    sfos = SophosFirewall(
        username=var_username,
        password=var_password,
        hostname=var_hostname,
        port=8282,
        verify=False
    )

    get_vlans(student_vlans)
    create_host(student_vlans)
    create_firewall_rules(student_vlans)

