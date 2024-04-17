from ..interface import Interface

menu_settings = {"File": [{"label": "New", "command": lambda: print("a")},
                          {"label": "New", "command": lambda: print("a")},
                          {"label": "New", "command": lambda: print("a")}],
                 "Edit": [{"label": "New", "command": lambda: print("a")},
                          {"label": "New", "command": lambda: print("a")},
                          {"label": "New", "command": lambda: print("a")}],
                 "Help": [{"label": "New", "command": lambda: print("a")},
                          {"label": "New", "command": lambda: print("a")},
                          {"label": "New", "command": lambda: print("a")}],
                 }

frame_settings = [{
    "label": [{"text": "Find:", "row": 0, "column": 0, "sticky": "e"},
              {"text": "Replace:", "row": 1, "column": 0, "sticky": "e"},
              {"text": "Direction:", "row": 2, "column": 6, "sticky": "w"}],
    "button": [{"text": "Find", "row": 0, "column": 10, "sticky": "ew", "padx": 2, "pady": 2},
               {"text": "Find All", "row": 1, "column": 10, "sticky": "ew", "padx": 2},
               {"text": "Replace", "row": 2, "column": 10, "sticky": "ew", "padx": 2},
               {"text": "Replace All", "row": 3, "column": 10, "sticky": "ew", "padx": 2}],
    "entry": [{"width": 60, "row": 0, "column": 1, "sticky": "we", "padx": 2, "pady": 2, "columnspan": 9},
              {"row": 1, "column": 1, "sticky": "we", "padx": 2, "pady": 2, "columnspan": 9}],
    "checkbutton": [{"text": "Match whole word only", "row": 2, "column": 1, "sticky": "w", "columnspan": 4},
                    {"text": "Match Case", "row": 3, "column": 1, "sticky": "w", "columnspan": 4},
                    {"text": "Wrap around", "row": 4, "column": 1, "sticky": "w", "columnspan": 4}],
    "radiobutton": [{"text": "Up", "value": 1, "row": 3, "column": 6, "sticky": "w", "columnspan": 6},
                    {"text": "Down", "value": 2, "row": 3, "column": 7, "sticky": "e", "columnspan": 2}]
}]


def find_n_replace():
    Interface(win_title="Find & Replace", frame_settings=frame_settings, menu=menu_settings)
