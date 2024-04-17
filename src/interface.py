import tkinter as tk
import tkinter.ttk as ttk
from .sniffer import PacketSniffer
from .pcap import Pcap
import sys, threading

widgets = {
    "label": tk.Label,
    "entry": tk.Entry,
    "button": tk.Button,
    "checkbutton": tk.Checkbutton,
    "radiobutton": tk.Radiobutton
}

valid_arguments = {
    "widget": ["text", "value", "width", "command"],
    "grid": ["row", "column", "sticky", "padx", "pady", "columnspan"]
}


class StopThread(StopIteration):
    pass


threading.SystemExit = SystemExit, StopThread


class Thread2(threading.Thread):

    def stop(self):
        self.__stop = True

    def _bootstrap(self):
        if threading._trace_hook is not None:
            raise ValueError('Cannot run thread with tracing!')
        self.__stop = False
        sys.settrace(self.__trace)
        super()._bootstrap()

    def __trace(self, frame, event, arg):
        if self.__stop:
            raise StopThread()
        return self.__trace


class WidgetMenu(tk.Menu):

    def __init__(self, **kwargs):
        self.menu_settings = None
        self.__dict__.update(kwargs)
        super(WidgetMenu, self).__init__(master=self.master)
        self.update_menubar()
        self.master.config(menu=self)

    def update_menubar(self):
        for m in self.menu_settings:
            menu = tk.Menu(self, tearoff=0)
            for option in self.menu_settings[m]:
                if option["label"] == "Capture":
                    option["command"] = self.master.capture
                elif option["label"] == "Stop":
                    option["command"] = self.master.stop
                elif option["label"] == "Exit":
                    option["command"] = self.master.quit
                elif option["label"] == "Save":
                    option["command"] = self.master.save

                menu.add_command(**option)
            self.add_cascade(label=m, menu=menu)


class WidgetFrame(tk.Frame):
    def __init__(self, **kwargs):
        self.settings = None
        self.__dict__.update(kwargs)
        super(WidgetFrame, self).__init__(master=self.master)

        self.lambda_functions()
        self.update_interface()
        self.configure(**self.filter_args(self.settings["frame"], "widget") if "frame" in self.settings else None)

        self.grid(**self.filter_args(self.settings["frame"], "grid") if "frame" in self.settings else None)

    def lambda_functions(self):
        self.filter_args = lambda s, f: {k: s[k] for k in s if k in valid_arguments[f]}
        self.widget = lambda w, s: w(master=self, **self.filter_args(s, "widget")).grid(**self.filter_args(s, "grid"))

    def set_widget(self, w, s):
        if "name" in s:
            if s["name"] == "capture":
                s["command"] = self.master.capture
            elif s["name"] == "stop":
                s["command"] = self.master.stop
            elif s["name"] == "save":
                s["command"] = self.master.save

        widget = w(master=self, **self.filter_args(s, "widget"))

        if "image" in s:
            pi = tk.PhotoImage(file=s["image"][0]).subsample(s["image"][1], s["image"][2])
            widget.config(image=pi)
            widget.photo = pi
        widget.grid(**self.filter_args(s, "grid"))

        return widget

    def update_interface(self):
        self.update_widgets()

    def update_widgets(self):
        for w in self.settings:
            for s in self.settings[w]:
                if w in widgets:
                    self.set_widget(widgets[w], s)
            if w == "textbox":
                self.add_textbox(self.settings[w])

    def add_textbox(self, settings):
        S = tk.Scrollbar(master=self)
        T = tk.Text(master=self, height=30, width=200)
        S.pack(side="right", fill="y")
        T.pack(side="left", fill="y")
        S.config(command=T.yview)
        T.config(yscrollcommand=S.set)

        # T.insert("end", quote)
        self.master.textbox = T


class Interface(tk.Tk):
    def __init__(self, **kwargs):
        self.win_title = "Main Window"
        self.frame_settings = None
        self.menu = None
        self.selected_item = None

        self.__dict__.update(kwargs)
        super(Interface, self).__init__()

        self.update_interface()
        self.packet_list = {}
        self.update_packet = lambda n, p: self.packet_list.update({n: p})
        self.mainloop()

    def update_interface(self):
        self.title(self.win_title)
        if self.menu:
            WidgetMenu(master=self, menu_settings=self.menu)
        if self.frame_settings:
            for frame in self.frame_settings:
                if "treeview" in frame:
                    self.add_treeview(settings=frame["treeview"])
                else:
                    WidgetFrame(master=self, settings=frame)

    def add_treeview(self, settings):
        tv = ttk.Treeview(self)
        tv['columns'] = settings

        tv.heading("#0", text='No.', anchor='w')
        tv.column("#0", anchor="w", width=50)

        for c in settings:
            tv.heading(c, text=c.title(), anchor='center')
            tv.column(c, anchor='center', width=100)

        tv.grid(sticky='nswe')
        self.treeview = tv
        self.insert_data = lambda n, v: self.treeview.insert('', 'end', text=n, values=v)
        self.treeview.bind("<Double-1>", self.on_double_click)
        self.treeview.bind("<Button-1>", self.on_single_click)
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

    def on_double_click(self, event):
        item = self.treeview.identify('item', event.x, event.y)
        citem = self.treeview.item(item, "text")
        self.selected_item = citem

        packet = self.packet_list[citem]
        msg = packet.get_packet_info()
        self.textbox.delete(1.0, "end")
        self.textbox.insert("end", msg)

    def on_single_click(self, event):
        item = self.treeview.identify('item', event.x, event.y)
        self.selected_item = self.treeview.item(item, "text")

    def capture(self):
        ps = PacketSniffer()
        tv = lambda n, v: self.insert_data(n, v)
        self.capture_status = True
        packet_no_list = list(self.packet_list.keys())
        packet_no_list.sort()
        packet_no = packet_no_list[-1] + 1 if len(packet_no_list) else 1
        self.instance = Thread2(target=ps.capture_packets, args=(tv, self.update_packet, packet_no,))
        self.instance.start()

    def stop(self):
        try:
            self.instance.stop()
            print("Stopped")
        except:
            pass

    def save(self):
        if self.selected_item:
            packet = self.packet_list[self.selected_item]
            Pcap(filename="data/{}.pcap".format(self.selected_item)).write(packet.bytes_data)


if __name__ == "__main__":
    Interface()
