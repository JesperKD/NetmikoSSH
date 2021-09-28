import tkinter as tk
from DeviceManager import show_ip_int
from DeviceManager import show_vlan_br
from DeviceManager import show_running_config


LARGE_FONT = ("Verdana", 12)


def mirror_text(text):
    mirror_point = int(len(text) / 2)
    if mirror_point % 2 == 0:
        res = text[:mirror_point]
    else:
        res = text[:mirror_point + 1]
    return res + res[::-1]


class WindowControl(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        container = tk.Frame(self)

        container.pack(side="top", fill="both", expand=True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for F in (StartPage, InfoPage, ConfigPage, ShowRunConfigPage, ShowIPConfigPage, ShowVlanConfigPage):
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

        button2 = tk.Button(self, text="Info Page",
                            command=lambda: controller.show_frame(InfoPage))
        button2.pack()


class ShowRunConfigPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Running Configuration", font=LARGE_FONT)
        label.pack(pady=10, padx=10)

        conf_string = show_running_config()

        txt_box = tk.Text(self)
        txt_box.insert(1.0, conf_string)
        txt_box.pack()

        button1 = tk.Button(self, text="Back",
                            command=lambda: controller.show_frame(InfoPage))
        button1.pack()


class ShowIPConfigPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="IP Configuration", font=LARGE_FONT)
        label.pack(pady=10, padx=10)

        conf_string = show_ip_int()

        txt_box = tk.Text(self)
        txt_box.insert(1.0, conf_string)
        txt_box.pack()

        button1 = tk.Button(self, text="Back",
                            command=lambda: controller.show_frame(InfoPage))
        button1.pack()


class ShowVlanConfigPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="IP Configuration", font=LARGE_FONT)
        label.pack(pady=10, padx=10)

        conf_string = show_vlan_br()

        txt_box = tk.Text(self)
        txt_box.insert(1.0, conf_string)
        txt_box.pack()

        button1 = tk.Button(self, text="Back",
                            command=lambda: controller.show_frame(InfoPage))
        button1.pack()


app = WindowControl()
app.mainloop()
