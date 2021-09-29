import tkinter as tk
from tkinter import messagebox
from DeviceManager import setup_snmp
from DeviceManager import create_vlan
from DeviceManager import show_ip_int
from DeviceManager import show_vlan_br
from DeviceManager import check_connection
from DeviceManager import show_running_config

# Style properties
LARGE_FONT = ("Verdana", 16)
BG_COLOR = "#382B5C"
BTN_COLOR = "#271E40"
TXT_COLOR = "#F3F6F4"


class WindowControl(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        container = tk.Frame(self)

        container.pack(side="top", fill="both", expand=True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        # Preloads all frames/pages
        for F in (StartPage, MenuPage, InfoPage, ConfigPage, ShowRunConfigPage, ShowIPConfigPage, ShowVlanConfigPage,
                  CreateVlanPage, SetupSNMPPage):
            frame = F(container, self)

            self.frames[F] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(StartPage)

    # function to display a given frame/page
    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()


class StartPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg=BG_COLOR)
        label = tk.Label(self, text="Start Page", font=LARGE_FONT, fg=TXT_COLOR, bg=BG_COLOR)
        label.pack(pady=10, padx=10)

        connection_works = False

        # entry widget with fitting label to indicate the expected data
        lbl_client_ip = tk.Label(self, text="Client IP", bg=BG_COLOR, fg=TXT_COLOR)
        ent_client_ip = tk.Entry(self)
        lbl_client_ip.pack()
        ent_client_ip.pack()

        lbl_device_ip = tk.Label(self, text="Device IP", bg=BG_COLOR, fg=TXT_COLOR)
        ent_device_ip = tk.Entry(self)
        lbl_device_ip.pack()
        ent_device_ip.pack()

        confirm_btn = tk.Button(self, fg=TXT_COLOR, bg=BTN_COLOR, border=0, text="Confirm",
                                command=lambda: confirm_connection(confirm_btn, continue_btn, ent_client_ip.get(),
                                                                   ent_device_ip.get()))
        confirm_btn.pack()

        continue_btn = tk.Button(self, fg=TXT_COLOR, bg=BTN_COLOR, border=0, text="Continue",
                                 command=lambda: controller.show_frame(MenuPage))


class MenuPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg=BG_COLOR)
        label = tk.Label(self, text="Menu", font=LARGE_FONT, fg=TXT_COLOR, bg=BG_COLOR)
        label.pack(pady=10, padx=10)

        button = tk.Button(self, fg=TXT_COLOR, bg=BTN_COLOR, border=0, text="Information Page",
                           command=lambda: controller.show_frame(InfoPage))
        button.pack()

        button2 = tk.Button(self, fg=TXT_COLOR, bg=BTN_COLOR, border=0, text="Configuration Page",
                            command=lambda: controller.show_frame(ConfigPage))
        button2.pack()


class InfoPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg=BG_COLOR)
        label = tk.Label(self, text="Information Page", font=LARGE_FONT, fg=TXT_COLOR, bg=BG_COLOR)
        label.pack(pady=10, padx=10)

        button1 = tk.Button(self, fg=TXT_COLOR, bg=BTN_COLOR, border=0, text="Back to Home",
                            command=lambda: controller.show_frame(MenuPage))
        button1.pack()

        button2 = tk.Button(self, fg=TXT_COLOR, bg=BTN_COLOR, border=0, text="Show Running Config",
                            command=lambda: controller.show_frame(ShowRunConfigPage))
        button2.pack()

        button3 = tk.Button(self, fg=TXT_COLOR, bg=BTN_COLOR, border=0, text="Show IP Config",
                            command=lambda: controller.show_frame(ShowIPConfigPage))
        button3.pack()

        button4 = tk.Button(self, fg=TXT_COLOR, bg=BTN_COLOR, border=0, text="Show VLAN Config",
                            command=lambda: controller.show_frame(ShowVlanConfigPage))
        button4.pack()


class ConfigPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg=BG_COLOR)
        label = tk.Label(self, text="Configuration page", font=LARGE_FONT, fg=TXT_COLOR, bg=BG_COLOR)
        label.pack(pady=10, padx=10)

        button1 = tk.Button(self, fg=TXT_COLOR, bg=BTN_COLOR, border=0, text="Back to Home",
                            command=lambda: controller.show_frame(MenuPage))
        button1.pack()

        button2 = tk.Button(self, fg=TXT_COLOR, bg=BTN_COLOR, border=0, text="Create Vlan",
                            command=lambda: controller.show_frame(CreateVlanPage))
        button2.pack()

        button3 = tk.Button(self, fg=TXT_COLOR, bg=BTN_COLOR, border=0, text="Setup SNMP",
                            command=lambda: controller.show_frame(SetupSNMPPage))
        button3.pack()


class ShowRunConfigPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg=BG_COLOR)
        label = tk.Label(self, text="Running Configuration", font=LARGE_FONT, fg=TXT_COLOR, bg=BG_COLOR)
        label.pack(pady=10, padx=10)

        txt_box = tk.Text(self, bg=TXT_COLOR)
        txt_box.config(state="normal")
        txt_box.pack()

        update_btn = tk.Button(self, fg=TXT_COLOR, bg=BTN_COLOR, text="Update",
                               command=lambda: update_txt_box(txt_box, 1))
        update_btn.pack()

        button1 = tk.Button(self, fg=TXT_COLOR, bg=BTN_COLOR, border=0, text="Back",
                            command=lambda: controller.show_frame(InfoPage))
        button1.pack()


class ShowIPConfigPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg=BG_COLOR)
        label = tk.Label(self, text="IP Configuration", font=LARGE_FONT, fg=TXT_COLOR, bg=BG_COLOR)
        label.pack(pady=10, padx=10)

        txt_box = tk.Text(self, bg=TXT_COLOR)
        txt_box.config(state="normal")
        txt_box.pack()

        update_btn = tk.Button(self, fg=TXT_COLOR, bg=BTN_COLOR, text="Update",
                               command=lambda: update_txt_box(txt_box, 2))
        update_btn.pack()

        button1 = tk.Button(self, fg=TXT_COLOR, bg=BTN_COLOR, border=0, text="Back",
                            command=lambda: controller.show_frame(InfoPage))
        button1.pack()


class ShowVlanConfigPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg=BG_COLOR)
        label = tk.Label(self, text="IP Configuration", font=LARGE_FONT, fg=TXT_COLOR, bg=BG_COLOR)
        label.pack(pady=10, padx=10)

        txt_box = tk.Text(self, bg=TXT_COLOR)
        txt_box.config(state="normal")
        txt_box.pack()

        update_btn = tk.Button(self, fg=TXT_COLOR, bg=BTN_COLOR, text="Update",
                               command=lambda: update_txt_box(txt_box, 3))
        update_btn.pack()

        button1 = tk.Button(self, fg=TXT_COLOR, bg=BTN_COLOR, border=0, text="Back",
                            command=lambda: controller.show_frame(InfoPage))
        button1.pack()


class CreateVlanPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg=BG_COLOR)
        label = tk.Label(self, text="Create Vlan", font=LARGE_FONT, fg=TXT_COLOR, bg=BG_COLOR)
        label.pack(pady=10, padx=10)

        lbl_vlan_num = tk.Label(self, text="Vlan Number", bg=BG_COLOR, border=0, fg=TXT_COLOR)
        ent_vlan_num = tk.Entry(self)
        lbl_vlan_num.pack()
        ent_vlan_num.pack()

        lbl_vlan_ip = tk.Label(self, text="Vlan IP", bg=BG_COLOR, border=0, fg=TXT_COLOR)
        ent_vlan_ip = tk.Entry(self)
        lbl_vlan_ip.pack()
        ent_vlan_ip.pack()

        lbl_vlan_mask = tk.Label(self, text="Vlan Mask", bg=BG_COLOR, border=0, fg=TXT_COLOR)
        ent_vlan_mask = tk.Entry(self)
        lbl_vlan_mask.pack()
        ent_vlan_mask.pack()

        submit_btn = tk.Button(self, fg=TXT_COLOR, bg=BTN_COLOR, text="submit",
                               command=lambda: submit_vlan_data(
                                  ent_vlan_num.get(),
                                  ent_vlan_ip.get(),
                                  ent_vlan_mask.get())
                               )
        submit_btn.pack()

        back_btn = tk.Button(self, fg=TXT_COLOR, bg=BTN_COLOR, border=0, text="Back",
                             command=lambda: controller.show_frame(ConfigPage))
        back_btn.pack()


class SetupSNMPPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg=BG_COLOR)
        label = tk.Label(self, text="SNMP Setup", font=LARGE_FONT, fg=TXT_COLOR, bg=BG_COLOR)
        label.pack(pady=10, padx=10)

        lbl_com_ro = tk.Label(self, text="Read Only Community key:", bg=BG_COLOR, fg=TXT_COLOR)
        ent_com_ro = tk.Entry(self)
        lbl_com_ro.pack()
        ent_com_ro.pack()

        lbl_com_rw = tk.Label(self, text="Read and Write Community key:", bg=BG_COLOR, fg=TXT_COLOR)
        ent_com_rw = tk.Entry(self)
        lbl_com_rw.pack()
        ent_com_rw.pack()

        submit_btn = tk.Button(self, fg=TXT_COLOR, bg=BTN_COLOR, text="Submit",
                               command=lambda: submit_snmp_data(ent_com_ro.get(), ent_com_rw.get()))
        submit_btn.pack()

        back_btn = tk.Button(self, fg=TXT_COLOR, bg=BTN_COLOR, border=0, text="Back",
                             command=lambda: controller.show_frame(ConfigPage))
        back_btn.pack()


# Checks if connection is valid
def confirm_connection(confirm_btn, continue_btn, cli_ip, dev_ip):
    if check_connection(dev_ip, cli_ip):
        show_btn(continue_btn)
        hide_btn(confirm_btn)
        return messagebox.showinfo('message', f'Connection confirmed!')
    else:
        return messagebox.showinfo('Error', f'Connection failed, make sure the info is correct.')


# hides a given button
def hide_btn(btn):
    btn.pack_forget()


# shows a given button
def show_btn(btn):
    btn.pack()


# Clears a given textbox and inserts newly gathered data depending on type
def update_txt_box(txt_box, conf_type):
    txt_box.delete('1.0', tk.END)
    if conf_type == 1:
        txt_box.insert(1.0, show_running_config())
    elif conf_type == 2:
        txt_box.insert(1.0, show_ip_int())
    elif conf_type == 3:
        txt_box.insert(1.0, show_vlan_br())


# Submit given data for vlan creation
def submit_vlan_data(vlan_num, vlan_ip, vlan_mask):
    if create_vlan(vlan_num, vlan_ip, vlan_mask):
        return messagebox.showinfo('message', f'Vlan {vlan_num} has been created.')
    else:
        print("Vlan creation Error")


# Submit given data for SNMP setup
def submit_snmp_data(ro_name, rw_name):
    if setup_snmp(ro_name, rw_name):
        return messagebox.showinfo('message', f'Snmp has been configured.')
    else:
        print("Vlan creation Error")


# Runs the GUI
app = WindowControl()
app.mainloop()
