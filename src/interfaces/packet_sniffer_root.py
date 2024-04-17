from ..interface import Interface
from ..sniffer import PacketSniffer as ps

menu_settings = {"File": [{"label": "Save"}, {"label": "Exit"}],
                 "Edit": [{"label": "Capture"}, {"label": "Stop"}]
                 }

b = 20

frame_settings = [
    {
        "frame": {"row": 0, "width": 500, "padx": 5, "pady": 5, "sticky": "w"},
        "button": [{"name": "capture", "image": ("src/interfaces/icons/capture.png", b, b), "row": 0, "column": 0},
                   {"name": "stop", "image": ("src/interfaces/icons/stop.png", b, b), "row": 0, "column": 1},
                   {"image": ("src/interfaces/icons/settings.png", b, b), "row": 0, "column": 2},
                   {"name": "save", "image": ("src/interfaces/icons/folder.png", b, b), "row": 0, "column": 3},
                   {"image": ("src/interfaces/icons/search.png", b, b), "row": 0, "column": 4}],
    },
    {
        "frame": {"row": 1, "width": 500, "padx": 5, "pady": 5, "columnspan": 20},
        "treeview": ('time', 'source', 'destination', 'protocol', 'length')
    },
    {
        "frame": {"row": 2, "width": 500, "padx": 5, "pady": 5, "columnspan": 20},
        "textbox": ()
    }

]


def packet_sniffer_root():
    interface = Interface(win_title="Packet Sniffer", frame_settings=frame_settings, menu=menu_settings)
