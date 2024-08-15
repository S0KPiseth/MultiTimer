# timer watch function
import time
import tkinter as tk
import threading
import pywinstyles
import sys
import sv_ttk
from tkinter import ttk

class Timer:
    def __init__(self, master, root):
        self.master=master
        self.root=root
        self.stop_flag = False
        
    def count_down(self):
        self.master.minute_ui.configure(state=tk.DISABLED)
        self.master.second_ui.configure(state=tk.DISABLED)
        for i in range((self.master.minutes.get()*60)+(self.master.second.get())):
            minutes = self.master.minutes.get()
            seconds = self.master.second.get()
            if seconds == 0:
                minutes -= 1
                self.master.second.set(60)
                self.master.minutes.set(minutes)
                self.root.update_idletasks()
            else:
                seconds -= 1
                self.master.second.set(seconds)
                self.root.update_idletasks()
            time.sleep(1)
            if self.stop_flag:
                break
        if not self.stop_flag:
            self.master.second.set(0)
            self.master.minute_ui.configure(state=tk.NORMAL)
            self.master.second_ui.configure(state=tk.NORMAL)
            self.root.update_idletasks()
        
    def start(self):
        if self.stop_flag:
            self.stop_flag=False
        threading.Thread(target=self.count_down).start()
    def stop(self):
        if not self.stop_flag:
            self.stop_flag=True
    
    

def stopwatch():
    pass


def change_theme(master, root):
    global timer_icon, stop_watch, start_icon, stop_icon

    if master.theme_value.get():
        timer_icon = master.get_img("Assets\\hourglass_white.png", 25, 25)
        stop_watch = master.get_img("Assets\\stopwatch_white.png", 30, 30)
        start_icon = master.get_img(img="Assets\\play_icon_white.png")
        stop_icon = master.get_img(img="Assets\\x.png")
        sv_ttk.set_theme("dark")
        apply_theme_to_titlebar(root)
        customize_style(root)

    else:
        sv_ttk.set_theme("light")
        apply_theme_to_titlebar(root)
        customize_style(root)
        timer_icon = master.get_img("Assets\\hourglass.png", 25, 25)
        stop_watch = master.get_img("Assets\\stopwatch.png", 30, 30)
        start_icon = master.get_img(img="Assets\\play-button_724963.png")
        stop_icon = master.get_img(img="Assets\\pause _icon.png")
    master.notebook.tab(0, image=timer_icon)
    master.notebook.tab(1, image=stop_watch)
    master.start_button.configure(image=start_icon)
    master.stop_button.configure(image=stop_icon)

# https://github.com/rdbende/Sun-Valley-ttk-theme


def apply_theme_to_titlebar(root):
    version = sys.getwindowsversion()

    if version.major == 10 and version.build >= 22000:
        # Set the title bar color to the background color on Windows 11 for better appearance
        pywinstyles.change_header_color(
            root, "#1c1c1c" if sv_ttk.get_theme() == "dark" else "#fafafa")
    elif version.major == 10:
        pywinstyles.apply_style(
            root, "dark" if sv_ttk.get_theme() == "dark" else "normal")

        # A hacky way to update the title bar's color on Windows 10 (it doesn't update instantly like on Windows 11)
        root.wm_attributes("-alpha", 0.99)
        root.wm_attributes("-alpha", 1)


def customize_style(window):
    style = ttk.Style(window)
    style.configure(
        "TNotebook.Tab", width=window.winfo_screenwidth(), font=("Roboto mono", 18, "bold"),
    )
    # remove dotted line around notebook tabs(https://stackoverflow.com/questions/23354303/removing-ttk-notebook-tab-dashed-line?rq=4)
    style.layout("Tab",
                 [('Notebook.tab', {'sticky': 'nswe', 'children':
                                    [('Notebook.padding', {'side': 'top', 'sticky': 'nswe', 'children':
                                                           # [('Notebook.focus', {'side': 'top', 'sticky': 'nswe', 'children':
                                                           [('Notebook.label', {
                                                             'side': 'top', 'sticky': ''})],
                                                           # })],
                                                           })],
                                    })]
                 )
    style.map("TNotebook.Tab",  background=[("selected", '#BC32C3')])
    style.configure("TButton", font=("Roboto mono", 12))
    style.configure("Switch.TCheckbutton", font=("Roboto mono", 12))
