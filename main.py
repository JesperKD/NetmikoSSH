from datetime import datetime
from netmiko import Netmiko

my_device = {
    'host': "10.0.3.24",
    'username': "ciscoclass",
    'password': "kage",
    'secret': "class",
    'device_type': 'cisco_ios'
}


def show_running_config():
    net_conn = Netmiko(**my_device)
    print("Connected to device\n")
    print(net_conn.send_command_timing("show running-config"))


def show_vlan_br():
    net_conn = Netmiko(**my_device)
    print("Connected to device\n")
    print(net_conn.send_command_timing("show vlan brief"))


def show_ip_int():
    net_conn = Netmiko(**my_device)
    print("Connected to device\n")
    print(net_conn.send_command_timing("show ip int br"))


def create_vlan():
    number = input("Type your preferred vlan number: ")
    ip = input("Type your preferred vlan Ip: ")
    mask = input("Type the fitting Subnet mask: ")

    start_time = datetime.now()

    net_conn = Netmiko(**my_device)
    print("Connected to device\n")

    net_conn.enable()

    print("creating vlan {}".format(num))

    config_commands = [
        f"interface vlan {number}",
        f"ip address {ip} {mask}",
        "no shutdown"
    ]
    output = net_conn.send_config_set(config_commands)
    print(output + "\n creation of vlan had concluded.")

    end_time = datetime.now()
    print("Time elapsed: {}".format(end_time - start_time))


def main_switch_case(choice):
    if choice == 'a':
        show_switch_case()
    elif choice == 'b':
        change_switch_case()


def show_switch_case():
    print("What do you wish to see?:\n")
    choice = input("A. Show the entire running-config.\n"
                   "B. Show the VLANs.\n"
                   "C. Show the IP setup.\n")

    if choice.lower() == 'a':
        show_running_config()
    elif choice == 'b':
        show_vlan_br()
    elif choice == 'c':
        show_ip_int()


def change_switch_case():
    if choice == 'a':
        print("bruh")
    elif choice == 'b':
        print("bruh")


print("What do you wish to do?: \n")
userChoice = input("A. Show device info.\n"
                   "B. Change the device config.\n")

main_switch_case(userChoice)

