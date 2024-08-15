#timer watch function
import time
import tkinter as tk
import threading
import pywinstyles, sys
import sv_ttk

def timer_start(master, root):
    threading.Thread(target=count_down, args=(master, root)).start()
def timer_stop(master):
    pass
def stopwatch():
    pass
def count_down(master, root):
    master.minute_ui.configure(state=tk.DISABLED)
    master.second_ui.configure(state=tk.DISABLED)
    for i in range((master.minutes.get()*60)+(master.second.get())):
        minutes = master.minutes.get()
        seconds =master.second.get()
        if seconds == 0:
            minutes -=1
            master.second.set(60)
            master.minutes.set(minutes)
            root.update_idletasks()
        else:
            seconds-=1
            master.second.set(seconds)
            root.update_idletasks()
        time.sleep(1)
    master.second.set(0)
    master.minute_ui.configure(state=tk.NORMAL)
    master.second_ui.configure(state=tk.NORMAL)
    root.update_idletasks()
def apply_theme_to_titlebar(root):
    version = sys.getwindowsversion()

    if version.major == 10 and version.build >= 22000:
        # Set the title bar color to the background color on Windows 11 for better appearance
        pywinstyles.change_header_color(root, "#1c1c1c" if sv_ttk.get_theme() == "dark" else "#fafafa")
    elif version.major == 10:
        pywinstyles.apply_style(root, "dark" if sv_ttk.get_theme() == "dark" else "normal")

        # A hacky way to update the title bar's color on Windows 10 (it doesn't update instantly like on Windows 11)
        root.wm_attributes("-alpha", 0.99)
        root.wm_attributes("-alpha", 1)