# timer watch function
import time
import tkinter as tk
import threading
import sv_ttk # type: ignore
from tkinter import ttk, messagebox
not_full_screen= False
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
    
    
    global timer_icon, stop_watch, start_icon, stop_icon, timer_icon_white, stop_watch_white, timer_notst, stop_watch_notst
    
    #identify tab id
    tab_index = int(master.notebook.index(master.notebook.select()))

    #get icon as photoimage
    timer_icon_white = master.get_img("Assets\\hourglass_white.png", 25, 25)
    stop_watch_white = master.get_img("Assets\\stopwatch_white.png", 25, 25)
    timer_icon = master.get_img("Assets\\hourglass.png", 25, 25)
    stop_watch = master.get_img("Assets\\stopwatch.png", 25, 25)
    timer_notst=master.get_img("Assets\\hourglass_notst.png", 25, 25)
    stop_watch_notst=master.get_img("Assets\\stopwatch_notst.png", 25, 25)
    
    #apply theme
    if master.theme_value.get():
        start_icon = master.get_img(img="Assets\\play_icon_white.png")
        stop_icon = master.get_img(img="Assets\\x.png")
        sv_ttk.set_theme("dark")
        color = '#2f2f2f'
        #config title bar button
        master.close.config(bg=color)
        master.minimize.config(bg=color)
        master.maximize.config(bg=color)
        
        customize_style(root,master.theme_value.get())
        
        if tab_index ==0:
            timer_icon=timer_icon_white
            stop_watch=stop_watch_notst
        elif tab_index ==1:
            stop_watch=stop_watch_white
            timer_icon=timer_notst
    else:
        sv_ttk.set_theme("light")
        color = '#e7e7e7'
        #config title bar button
        master.close.config(bg=color)
        master.minimize.config(bg=color)
        master.maximize.config(bg=color)
        customize_style(root,master.theme_value.get())
        start_icon = master.get_img(img="Assets\\play-button_724963.png")
        stop_icon = master.get_img(img="Assets\\pause _icon.png")
        if tab_index ==0:
            stop_watch=stop_watch_notst
        elif tab_index ==1:
            timer_icon=timer_notst
    

    master.notebook.tab(0, image=timer_icon)
    master.notebook.tab(1, image=stop_watch)

    master.start_button.configure(image=start_icon)
    master.stop_button.configure(image=stop_icon)

def customize_style(window, theme):
    style = ttk.Style(window)
    style.map("TNotebook.Tab",font=[("selected", ("Roboto mono", 15, "bold")), ("!selected", ("Roboto mono", 15))])
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
    if theme:
        style.map("TNotebook.Tab",  foreground=[("selected", 'white'), ("!selected", '#8b8b8b')],
                  font=[("selected", ("Roboto mono", 15, "bold")), ("!selected", ("Roboto mono", 15))])
    else:
        style.map("TNotebook.Tab",  foreground=[("selected", 'black'), ("!selected", '#8b8b8b')])
    style.configure("TButton", font=("Roboto mono", 12))
    style.configure("Switch.TCheckbutton", font=("Roboto mono", 12))
def close_win(root):
    root.after(300, root.destroy())
def maximize_win(root):
    global not_full_screen
    if not_full_screen:
        root.geometry('900x400')
        not_full_screen=False
    else:
        root.geometry(f'{root.winfo_screenwidth()}x{root.winfo_screenheight()}+0+0')
        not_full_screen=True
def minimize_window(root):
   messagebox.showwarning("Sorry!", "You cannot iconify the window")