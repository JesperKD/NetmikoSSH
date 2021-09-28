import tkinter as tk
from tkinter import messagebox
from DeviceManager import setup_snmp
from DeviceManager import create_vlan
from DeviceManager import show_ip_int
from DeviceManager import show_vlan_br
from DeviceManager import show_running_config


LARGE_FONT = ("Verdana", 12)


class WindowControl(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        container = tk.Frame(self)

        container.pack(side="top", fill="both", expand=True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for F in (StartPage, InfoPage, ConfigPage, ShowRunConfigPage, ShowIPConfigPage, ShowVlanConfigPage,
                  CreateVlanPage, SetupSNMPPage):
            frame = F(container, self)

            self.frames[F] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(StartPage)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()


class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Start Page", font=LARGE_FONT)
        label.pack(pady=10, padx=10)

        button = tk.Button(self, text="Information Page",
                           command=lambda: controller.show_frame(InfoPage))
        button.pack()

        button2 = tk.Button(self, text="Configuration Page",
                            command=lambda: controller.show_frame(ConfigPage))
        button2.pack()


class InfoPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Information Page", font=LARGE_FONT)
        label.pack(pady=10, padx=10)

        button1 = tk.Button(self, text="Back to Home",
                            command=lambda: controller.show_frame(StartPage))
        button1.pack()

        button2 = tk.Button(self, text="Show Running Config",
                            command=lambda: controller.show_frame(ShowRunConfigPage))
        button2.pack()

        button3 = tk.Button(self, text="Show IP Config",
                            command=lambda: controller.show_frame(ShowIPConfigPage))
        button3.pack()

        button4 = tk.Button(self, text="Show VLAN Config",
                            command=lambda: controller.show_frame(ShowVlanConfigPage))
        button4.pack()


class ConfigPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Configuration page", font=LARGE_FONT)
        label.pack(pady=10, padx=10)

        button1 = tk.Button(self, text="Back to Home",
                            command=lambda: controller.show_frame(StartPage))
        button1.pack()

        button2 = tk.Button(self, text="Create Vlan",
                            command=lambda: controller.show_frame(CreateVlanPage))
        button2.pack()

        button3 = tk.Button(self, text="Setup SNMP",
                            command=lambda: controller.show_frame(SetupSNMPPage))
        button3.pack()


class ShowRunConfigPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Running Configuration", font=LARGE_FONT)
        label.pack(pady=10, padx=10)

        txt_box = tk.Text(self)
        txt_box.config(state="normal")
        txt_box.pack()

        update_btn = tk.Button(self, text="Update",
                               command=lambda: update_txt_box(txt_box, 1))
        update_btn.pack()

        button1 = tk.Button(self, text="Back",
                            command=lambda: controller.show_frame(InfoPage))
        button1.pack()


def update_txt_box(txt_box, conf_type):
    txt_box.delete('1.0', tk.END)
    if conf_type == 1:
        txt_box.insert(1.0, show_running_config())
    elif conf_type == 2:
        txt_box.insert(1.0, show_ip_int())
    elif conf_type == 3:
        txt_box.insert(1.0, show_vlan_br())


class ShowIPConfigPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="IP Configuration", font=LARGE_FONT)
        label.pack(pady=10, padx=10)

        txt_box = tk.Text(self)
        txt_box.config(state="normal")
        txt_box.pack()

        update_btn = tk.Button(self, text="Update",
                               command=lambda: update_txt_box(txt_box, 2))
        update_btn.pack()

        button1 = tk.Button(self, text="Back",
                            command=lambda: controller.show_frame(InfoPage))
        button1.pack()


class ShowVlanConfigPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="IP Configuration", font=LARGE_FONT)
        label.pack(pady=10, padx=10)

        txt_box = tk.Text(self)
        txt_box.config(state="normal")
        txt_box.pack()

        update_btn = tk.Button(self, text="Update",
                               command=lambda: update_txt_box(txt_box, 3))
        update_btn.pack()

        button1 = tk.Button(self, text="Back",
                            command=lambda: controller.show_frame(InfoPage))
        button1.pack()


class CreateVlanPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="IP Configuration", font=LARGE_FONT)
        label.pack(pady=10, padx=10)

        lbl_vlan_num = tk.Label(self, text="Vlan Number")
        ent_vlan_num = tk.Entry(self)
        lbl_vlan_num.pack()
        ent_vlan_num.pack()

        lbl_vlan_ip = tk.Label(self, text="Vlan IP")
        ent_vlan_ip = tk.Entry(self)
        lbl_vlan_ip.pack()
        ent_vlan_ip.pack()

        lbl_vlan_mask = tk.Label(self, text="Vlan Mask")
        ent_vlan_mask = tk.Entry(self)
        lbl_vlan_mask.pack()
        ent_vlan_mask.pack()

        submit_btn = tk.Button(self, text="submit",
                               command=lambda: submit_vlan_data(
                                  ent_vlan_num.get(),
                                  ent_vlan_ip.get(),
                                  ent_vlan_mask.get())
                               )
        submit_btn.pack()

        back_btn = tk.Button(self, text="Back",
                             command=lambda: controller.show_frame(ConfigPage))
        back_btn.pack()


def submit_vlan_data(vlan_num, vlan_ip, vlan_mask):
    if create_vlan(vlan_num, vlan_ip, vlan_mask):
        return messagebox.showinfo('message', f'Vlan {vlan_num} has been created.')
    else:
        print("Vlan creation Error")


class SetupSNMPPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="SNMP Setup", font=LARGE_FONT)
        label.pack(pady=10, padx=10)

        lbl_com_ro = tk.Label(self, text="Read Only Community key:")
        ent_com_ro = tk.Entry(self)
        lbl_com_ro.pack()
        ent_com_ro.pack()

        lbl_com_rw = tk.Label(self, text="Read and Write Community key:")
        ent_com_rw = tk.Entry(self)
        lbl_com_rw.pack()
        ent_com_rw.pack()

        submit_btn = tk.Button(self, text="Submit",
                               command=lambda: submit_snmp_data(ent_com_ro.get(), ent_com_rw.get()))
        submit_btn.pack()

        back_btn = tk.Button(self, text="Back",
                             command=lambda: controller.show_frame(ConfigPage))
        back_btn.pack()


def submit_snmp_data(ro_name, rw_name):
    if setup_snmp(ro_name, rw_name):
        return messagebox.showinfo('message', f'Snmp has been configured.')
    else:
        print("Vlan creation Error")


app = WindowControl()
app.mainloop()
