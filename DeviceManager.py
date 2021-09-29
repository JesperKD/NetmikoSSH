import os
from pysnmp.hlapi import *
from netmiko import Netmiko
import pysnmp.entity.engine
from datetime import datetime

device_ip = "10.0.3.24"
client_ip = "10.0.3.15"

# Properties for the network device in question
my_device = {
    'host': f"{device_ip}",
    'username': "ciscoclass",
    'password': "kage",
    'secret': "class",
    'device_type': 'cisco_ios'
}


# Returns true if a connection can be established
def check_connection(dev_ip, cli_ip):
    try:
        global device_ip
        global client_ip
        device_ip = dev_ip
        client_ip = cli_ip
        net_conn = Netmiko(**my_device)
        net_conn.enable()
        return True
    except:
        return False


# Returns the running configuration of the given device
def show_running_config():
    net_conn = Netmiko(**my_device)
    net_conn.enable()
    print("Connected to device\n Getting sh run\n")
    return net_conn.send_command_timing("show running-config")


# Returns the VLAN configuration of the given device
def show_vlan_br():
    net_conn = Netmiko(**my_device)
    net_conn.enable()
    print("Connected to device\n Getting sh vlan br\n")
    return net_conn.send_command_timing("show vlan brief")


# Returns the IP configuration of the given device
def show_ip_int():
    net_conn = Netmiko(**my_device)
    net_conn.enable()
    print("Connected to device\n Getting ip int br\n")
    return net_conn.send_command_timing("show ip int br")


# Returns the mib interface table of the given device
def mib_interface_table():
    start_time = datetime.now()
    error_indication, error_status, error_index, var_bind_table = cmdGen.bulkCmd(
        cmdgen.CommunityData('private'),
        cmdgen.UdpTransportTarget(("10.0.3.24", 161)),
        0, 25,
        '1.3.6.1.2.1.2.2.1.2'
    )

    for var_bind_table_row in var_bind_table:
        for name, val in var_bind_table_row:
            print('%s = Interface Name: %s' % (name.prettyPrint(), val.prettyPrint()))

    end_time = datetime.now()
    print("Time elapsed: {}".format(end_time - start_time))


# Creates a vlan with given parameters
def create_vlan(number, ip, mask):
    try:
        net_conn = Netmiko(**my_device)
        net_conn.enable()

        print("creating vlan {}".format(number))

        config_commands = [
            f"interface vlan {number}",
            f"ip address {ip} {mask}",
            "no shutdown"
        ]
        output = net_conn.send_config_set(config_commands)
        print(output + "\n creation of vlan has concluded.")
        return True
    except:
        print("Creation of VLAN failed")
        return False


# Sets up SNMP with the given parameters
def setup_snmp(ro_name, rw_name):
    try:
        net_conn = Netmiko(**my_device)
        net_conn.enable()
        config_commands = [
            f"snmp-server community {ro_name} RO",
            f"snmp-server community {rw_name} RW",
            f"snmp-server host {client_ip} informs version 2c public",
            f"snmp-server host {client_ip} traps version 2c public",
            f"snmp-server enable traps bgp",
            f"logging trap 7"
        ]

        output = net_conn.send_config_set(config_commands)
        print(output + "\n SNMP has now been configured.")
        return True
    except:
        print("Setting up SNMP failed.")
        return False


# Continuously checks on a port for SNMP Trap messages
def catch_traps():
    os.system('python SNMPTrapReceiver.py')
