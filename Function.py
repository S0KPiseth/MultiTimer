# timer watch function
import multiprocessing.process
import time
import tkinter as tk
import threading
import sv_ttk  # type: ignore
from tkinter import ttk, messagebox
import math
from PIL import Image, ImageTk
from pygame import mixer  # type: ignore


#set up flags
not_full_screen = False
sw_stop_flag = False
#set up lap count
lap_count = 0
function_call = 0

new_lap=False
lap_variable =[]

#lap default variable
minute_lap = 0
second_lap = 0
centi_lap = 0

#get photoimage
def get_img(img, width=20, height=20):
    start_img = Image.open(img)
    start_resize = start_img.resize((width, height))
    final = ImageTk.PhotoImage(start_resize)
    return final
#timer class that allow user to start and stop the timer
class Timer:
    def __init__(self, master, root):
        self.master = master
        self.root = root

    def count_down(self):
        # create mixer(add sound)
        mixer.init()
        mixer.music.load("Assets\\short-beep-countdown-81121.mp3")
        mixer.music.set_volume(0.8)

        if self.master.minutes.get() == '':
            self.master.minutes.set("00")
        elif self.master.second.get() == '':
            self.master.second.set("00")

        if self.master.minutes.get().isdigit() and self.master.second.get().isdigit():
            self.master.minute_ui.configure(state=tk.DISABLED)
            self.master.second_ui.configure(state=tk.DISABLED)

            for i in range((int(self.master.minutes.get())*60)+int(self.master.second.get())):
                minutes = int(self.master.minutes.get())
                seconds = int(self.master.second.get())
                if seconds == 0:
                    minutes -= 1
                    self.master.second.set("59")
                    self.master.minutes.set((f"0{str(minutes)}") if len(
                        str(minutes)) == 1 else str(minutes))
                    self.root.update_idletasks()
                else:
                    seconds -= 1
                    self.master.second.set((f"0{str(seconds)}") if len(
                        str(seconds)) == 1 else str(seconds))
                    self.root.update_idletasks()
                if int(self.master.second.get()) == 3 and int(self.master.minutes.get()) == 0:
                    mixer.music.play()
                time.sleep(1)
                if self.master.stop_timer:
                    break
            if not self.master.stop_flag:
                self.master.second.set("00")
                self.master.minute_ui.configure(state=tk.NORMAL)
                self.master.second_ui.configure(state=tk.NORMAL)
                self.root.update_idletasks()
        else:
            self.master.minutes.set("00")
            self.master.second.set("00")
            messagebox.showerror('Error!', 'Please enter only integer')
        self.master.is_starting = False

    def start(self):
        if not self.master.is_starting:
            self.master.is_starting = True
            if self.master.stop_timer:
                self.master.stop_timer = False
            self.master.stop_flag = False
            change_theme(self.master, self.root)
            threading.Thread(target=self.count_down).start()

    def stop(self):
        if not self.master.stop_timer:
            self.master.stop_timer = True
        if self.master.is_starting and not self.master.stop_flag:
            self.master.stop_flag = True
            change_theme(self.master, self.root)
#option to reset timer to 00:00 is the stop button is press             
def reset_timer(master, root):
    if master.stop_flag:
        master.stop_flag = False
        master.minutes.set("00")
        master.second.set("00")
        
        master.minute_ui.configure(state=tk.NORMAL)
        master.second_ui.configure(state=tk.NORMAL)
        change_theme(master, root)

def change_theme(master, root):
    global timer_icon, stop_watch, start_icon, stop_icon, timer_icon_white, \
        stop_watch_white, timer_notst, stop_watch_notst, pause_sp, pause_sp_white, reset, reset_white,\
        close, minimize,maximize, logo_img,un_maximize

    # identify tab id
    tab_index = int(master.notebook.index(master.notebook.select()))

    # get icon as photoimage
    timer_icon_white = get_img("Assets\\hourglass_white.png", )
    stop_watch_white = get_img("Assets\\stopwatch_white.png", )
    timer_icon = get_img("Assets\\hourglass.png", )
    stop_watch = get_img("Assets\\stopwatch.png", )
    timer_notst = get_img("Assets\\hourglass_notst.png", )
    stop_watch_notst = get_img("Assets\\stopwatch_notst.png", )

    close = get_img("Assets\\pause _icon.png", 25, 25)
    minimize = get_img("Assets\\minus.png", 25, 25)
    maximize = get_img("Assets\\maximize-2.png", 25, 25)
    un_maximize = get_img("Assets\\un_maximize.png",25,25)

    pause_sp = get_img("Assets\\pause_sp.png", 20, 20)
    pause_sp_white = get_img("Assets\\pause_sp_white.png", 20, 20)
    reset = get_img("Assets\\reset.png", 20, 20)
    reset_white = get_img("Assets\\reset_white.png", 20, 20)

    logo_img = get_img('Assets\\my_logo.png',25,25)
    # apply theme
    if master.theme_value.get():
        color = '#2f2f2f'
        start_icon = get_img(img="Assets\\play_icon_white.png")
        stop_icon = get_img(img="Assets\\x.png")

        close = get_img("Assets\\x.png", 25, 25)
        minimize = get_img("Assets\\minus_white.png", 25, 25)
        maximize = get_img("Assets\\maximize-2_white.png", 25, 25)
        un_maximize = get_img("Assets\\un_maximize_white.png",25,25)

        master.close.config(activebackground=color, image=close)
        master.minimize.config(activebackground=color,image=minimize)
        master.maximize.config(activebackground=color,image=maximize)
        if not_full_screen:
            master.maximize.config(image=un_maximize)

        sv_ttk.set_theme("dark")
        
        # config title bar button
        master.close.config(bg=color)
        master.minimize.config(bg=color)
        master.maximize.config(bg=color)
        master.logo.config(bg=color,image=logo_img)
        customize_style(root, master.theme_value.get())
        # config stopwatch buttons
        master.stop_watchBtn.config(image=start_icon)
        if master.sp_start_flag:
            master.stop_watchBtn.config(image=pause_sp_white)
        reset = reset_white
        if master.stop_flag:
            stop_icon = reset_white

        if tab_index == 1:
            timer_icon = timer_icon_white
            stop_watch = stop_watch_notst
        elif tab_index == 2:
            stop_watch = stop_watch_white
            timer_icon = timer_notst
    else:
        color = '#e7e7e7'
        master.close.config(activebackground=color,image=close)
        master.minimize.config(activebackground=color,image=minimize)
        master.maximize.config(activebackground=color,image=maximize)
        if not_full_screen:
            master.maximize.config(image=un_maximize)
        sv_ttk.set_theme("light")
        
        # config title bar button
        master.close.config(bg=color)
        master.minimize.config(bg=color)
        master.maximize.config(bg=color)
        master.logo.config(bg=color, image=logo_img)
        customize_style(root, master.theme_value.get())
        start_icon = get_img(img="Assets\\play-button_724963.png")
        stop_icon = get_img(img="Assets\\pause _icon.png")
        # config stopwatch buttons
        master.stop_watchBtn.config(image=start_icon)
        if master.sp_start_flag:
            master.stop_watchBtn.config(image=pause_sp)
        if master.stop_flag:
            stop_icon = reset
        if tab_index == 1:
            stop_watch = stop_watch_notst
        elif tab_index == 2:
            timer_icon = timer_notst

    master.notebook.tab(1, image=timer_icon)
    master.notebook.tab(2, image=stop_watch)

    master.start_button.configure(image=start_icon)
    master.stop_button.configure(
        image=stop_icon, text="Reset"if master.stop_flag else "Stop")
    if sw_stop_flag:
        master.reset_button.configure(image=reset, text = "", command = lambda: reset_sw(master, root))
    else:
        master.reset_button.configure(text="Add Lap", command= lambda: add_lap(master, root),image="")


def customize_style(window, theme):
    style = ttk.Style(window)
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
        style.map("TNotebook.Tab",  foreground=[
                  ("selected", 'black'), ("!selected", '#8b8b8b')],
                  font=[("selected", ("Roboto mono", 15, "bold")), ("!selected", ("Roboto mono", 15))])
    style.configure("TButton", font=("Roboto mono", 12))
    style.configure("Switch.TCheckbutton", font=("Roboto mono", 12))

#enter window full screen function for custom maximize button
def maximize_win(master,root):
    global not_full_screen
    if not_full_screen:
        root.geometry('900x450')
        not_full_screen = False
    else:
        root.geometry(f'{root.winfo_screenwidth()}x{
                      root.winfo_screenheight()}+0+0')
        not_full_screen = True
    change_theme(master,root)

def minimize_window(root, minimize_helper):
    # messagebox.showwarning("Sorry!", "You cannot iconify the window")
    minimize_helper.iconify()
    root.withdraw()


def limit_digit(master, box, second=False):
    # customize input to only two digit
    if len(box.get()) == 2:
        value = box.get()
        out_value = value[0]
        box.set(value[1:len(value)])
        if second:
            master.minute_ui.insert(tk.END, out_value)

            if len(master.minutes.get()) > 2:
                master.minute_ui.delete(0)


def calculate_path_details(master):
    # Get the coordinates of the bounding box of the oval path
    x1, y1, x2, y2 = master.canvas.coords(master.path)
    # Calculate the center of the circle
    center_x = (x1 + x2) / 2
    center_y = (y1 + y2) / 2
    # Calculate the radius of the circle
    radius = (x2 - x1) / 2
    return center_x, center_y, radius

def move_circle(master):
    if master.is_moving:
        # Calculate the new position of the circle
        x = master.center_x + master.radius * math.cos(master.angle)
        y = master.center_y + master.radius * math.sin(master.angle)

        # Move the circle to the new position
        circle_radius = 15
        master.canvas.coords(master.circle, x - circle_radius,
                             y - circle_radius, x + circle_radius, y + circle_radius)
        # Increment the angle for the next update
        master.angle += master.speed
        # Keep the angle within the range [0, 2*pi]
        master.angle = master.angle % (2 * math.pi)
        # Schedule the next update
        master.canvas.after(20, lambda: move_circle(master))

def start_stopwatch(master, root):
    global sw_stop_flag, new_lap, lap_variable
    #prevent from set the default lap variable to 0 when after start the stopwatch again
    new_lap=False

    if not master.sp_start_flag:
        master.sp_start_flag = True
    if sw_stop_flag:
        sw_stop_flag = False
        threading.Thread(target=lap_value, args=(lap_count, lap_variable, root,master), daemon=True).start()

    master.reset_button.grid(row=0, column=1)
    master.stop_watchBtn.config(width=15)
    change_theme(master, root)
    if not master.is_moving:
        master.is_moving = True
    threading.Thread(target=stopwatch, args=(
        master, root), daemon=True).start()


def stop_stopwatch(master, root):
    master.is_moving = False
    global sw_stop_flag
    if master.sp_start_flag:
        master.sp_start_flag = False
    if not sw_stop_flag:
        sw_stop_flag = True
    change_theme(master, root)


def stopwatch(master, root):

    move_circle(master)
    while not sw_stop_flag:
        master.sw_centi.set(("0"+str(int(master.sw_centi.get())+1))if len(
            str(int(master.sw_centi.get())+1)) == 1 else str(int(master.sw_centi.get())+1))
        time.sleep(0.014)
        if int(master.sw_centi.get()) == 60:
            master.sw_second.set(("0"+str(int(master.sw_second.get())+1))if len(
                str(int(master.sw_second.get())+1)) == 1 else str(int(master.sw_second.get())+1))
            master.sw_centi.set("00")
            if int(master.sw_second.get()) == 60:
                master.sw_second.set("00")
                master.sw_minute.set(("0"+str(int(master.sw_minute.get())+1))if len(
                    str(int(master.sw_minute.get())+1)) == 1 else str(int(master.sw_minute.get())+1))
        root.update_idletasks()


def reset_sw(master,root):
    stop_stopwatch(master, root)
    master.sw_centi.set("00")
    master.sw_second.set("00")
    master.sw_minute.set("00")
    master.lap_frame.place_forget()
def add_lap(master, root):
    global lap_count, new_lap,lap_variable

    new_lap = True

    lap_labels=[master.lap1,master.lap2,master.lap3,master.lap4,master.lap5]
    lap_name = [master.lap_name1,master.lap_name2,master.lap_name3,master.lap_name4,master.lap_name5]
    lap_separator =[master.lap_spt1,master.lap_spt2,master.lap_spt3,master.lap_spt4,master.lap_spt5]
    lap_variable= [master.lap_1,master.lap_2,master.lap_3,master.lap_4,master.lap_5]
    if lap_count<5:
        lap_labels[lap_count].grid(row = 10-(2*lap_count), column = 1)
        lap_name[lap_count].grid(row = 10-(2*lap_count), column = 0)

    if lap_count<4:
        lap_separator[lap_count].grid(row=9-(2*lap_count), column = 0, columnspan=2)
    lap_count+=1
    threading.Thread(target=display_rs, args=(lap_variable, sw_stop_flag, master,root), daemon=True).start()
    
    

def move(event, window):

        x = window.winfo_x()-window.startX + event.x
        y = window.winfo_y()-window.startY + event.y
        window.geometry(f'+{x}+{y}')

def origin_cords(event, window):
    window.startX = event.x
    window.startY = event.y

def display_rs(variable, flag, master,root):
    global lap_count
    if not(lap_count>5):
        while lap_count==1:
            variable[0].set(f"{master.sw_minute.get()}:{master.sw_second.get()}:{master.sw_centi.get()}")
        if lap_count==2:
            lap_value(2, variable,root,master)
        if lap_count==3:
            lap_value(3, variable,root, master)
        if lap_count==4:
            lap_value(4, variable,root, master)
        if lap_count==5:
            lap_value(5,variable,root, master)
    else:
        messagebox.showwarning("Warning!", "You can only add five labs.")

        
def lap_value(lap_iden, variable, root,master):
    global lap_count,sw_stop_flag,minute_lap,second_lap,centi_lap
    if new_lap:
        minute_lap = int(master.sw_minute.get())
        second_lap = int(master.sw_second.get())
        centi_lap = int(master.sw_centi.get())
        
    while lap_count==lap_iden:
        if not sw_stop_flag:
            minute=abs(int(master.sw_minute.get())-minute_lap)
            second = abs(int(master.sw_second.get())-second_lap)
            centi=abs(int(master.sw_centi.get())-centi_lap)
            display_minute = str(minute) if len(str(minute)) ==2 else f"0{minute}"
            display_second = str(second) if len(str(second)) ==2 else f"0{second}"
            display_centi = str(centi) if len(str(centi)) ==2 else f"0{centi}"
            variable[lap_count-1].set(f"{display_minute}:{display_second}:{display_centi}")
            time.sleep(0.01)
            root.update_idletasks()
        else:
            break
        