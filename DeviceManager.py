import os
from pysnmp.hlapi import *
from netmiko import Netmiko
import pysnmp.entity.engine
from datetime import datetime

device_ip = "10.0.3.24"
client_ip = "10.0.3.15"

my_device = {
    'host': f"{device_ip}",
    'username': "ciscoclass",
    'password': "kage",
    'secret': "class",
    'device_type': 'cisco_ios'
}


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


def show_running_config():
    net_conn = Netmiko(**my_device)
    net_conn.enable()
    print("Connected to device\n Getting sh run\n")
    return net_conn.send_command_timing("show running-config")


def show_vlan_br():
    net_conn = Netmiko(**my_device)
    net_conn.enable()
    print("Connected to device\n Getting sh vlan br\n")
    return net_conn.send_command_timing("show vlan brief")


def show_ip_int():
    net_conn = Netmiko(**my_device)
    net_conn.enable()
    print("Connected to device\n Getting ip int br\n")
    return net_conn.send_command_timing("show ip int br")


def cb_fun(snmp_engine, send_request_handle, error_indication, error_status, error_index, var_binds, cb_ctx):
    print(error_indication, error_status, error_index, var_binds)


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


def catch_traps():
    os.system('python SNMPTrapReceiver.py')


"""
def main_switch_case():
    print("What do you wish to do?: \n")
    choice = input("A. Show device info.\n"
                   "B. Change the device config.\n"
                   "C. Catch traps.\n")

    if choice == 'a':
        show_switch_case()
    elif choice == 'b':
        change_switch_case()
    elif choice == 'c':
        catch_traps()


def show_switch_case():
    print("What do you wish to see?:\n")
    choice = input("A. Show the entire running-config.\n"
                   "B. Show the VLANs.\n"
                   "C. Show the IP setup.\n"
                   "D. show the mib Interface Table.\n")

    if choice.lower() == 'a':
        show_running_config()
    elif choice == 'b':
        show_vlan_br()
    elif choice == 'c':
        show_ip_int()
    elif choice == 'd':
        mib_interface_table()


def change_switch_case():
    print("What do you wish to configure?:\n")
    choice = input("A. create a new vlan\n"
                   "B. Add SNMP to device\n")

    if choice == 'a':
        print(create_vlan())
    elif choice == 'b':
        print(setup_snmp())
"""