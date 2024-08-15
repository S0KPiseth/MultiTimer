from tkinter import *
from tkinter import ttk
from Function import timer_start,timer_stop, stopwatch,apply_theme_to_titlebar
from PIL import Image, ImageTk
import sv_ttk

# create interface



class UI:
    def __init__(self, root):

        root.geometry("800x300")
        global timer_icon, stop_watch
        self.minutes = IntVar()
        self.second = IntVar()   
        timer_icon = self.get_img("Assets\\hourglass.png", 25, 25)
        stop_watch = self.get_img("Assets\\stopwatch.png", 30, 30)

        notebook = ttk.Notebook(root)
        notebook.pack(fill=BOTH, expand=True)
        # create timer tab
        tab1 = Frame(notebook)
        notebook.add(tab1, text="Timer", image=timer_icon, compound=LEFT)

        # create stopwatch tab
        tab2 = Frame(notebook)
        notebook.add(tab2, text="Stop Watch", image=stop_watch, compound=LEFT)

        # first half frame
        tab1_firstFm = Frame(tab1)
        tab1_firstFm.pack(fill="both", expand=True)

        # second half frame
        tab1_secondFm = Frame(tab1)
        tab1_secondFm.pack(fill="both", expand=True)

        # timer frame(minute + second)
        timer_frame = Frame(tab1_firstFm)
        timer_frame.pack(side="bottom")

        # minute frame
        minute_frame = Frame(timer_frame)
        minute_frame.grid(row=1, column=1)

        # second frame
        second_frame = Frame(timer_frame)
        second_frame.grid(row=1, column=2)

        # minute UI that allow user to input minute
        self.minute_ui = ttk.Entry(
            minute_frame,
            font=("Roboto mono", 50),
            width=5,
            #relief="solid",
            justify=RIGHT,
            textvariable=self.minutes
        )
        self.minute_ui.grid(row=0, column=0)
        Label(minute_frame, text="m", font=("Roboto mono", 20)).grid(
            row=0, column=1, sticky=S
        )

        # second UI that allow user to input second
        self.second_ui = ttk.Entry(
            second_frame,
            font=("Roboto mono", 50),
            width=5,
            #relief="solid",
            justify=RIGHT,
            textvariable=self.second,
            
        )
        self.second_ui.grid(row=0, column=0)
        Label(second_frame, text="s", font=("Roboto mono", 20)).grid(
            row=0, column=1, sticky=S
        )

        # get icons
        start_icon = self.get_img(img="Assets\\play-button_724963.png")
        stop_icon = self.get_img(img="Assets\\pause _icon.png")

        # control frame(start + stop)
        control_frame = Frame(tab1_secondFm)
        control_frame.pack(side="bottom", anchor="w")

        start_button = ttk.Button(
            control_frame, text="Start", width=15, image=start_icon, compound=LEFT,
            command=lambda: timer_start(self,root),#style="Accent.TButton",
            padding= (1,1)
        )
        start_button.grid(row=0, column=0)

        stop_button = ttk.Button(
            control_frame, text="Stop", width=15, image=stop_icon, compound=LEFT, 
            command=lambda: timer_stop(self),
            padding= (1,1)
        )
        stop_button.grid(row=0, column=1)
        start_button.image = start_icon
        stop_button.image = stop_icon

    def get_img(self, img, width=20, height=20):
        start_img = Image.open(img)
        start_resize = start_img.resize((width, height))
        final = ImageTk.PhotoImage(start_resize)
        return final


if __name__ == "__main__":
    window = Tk()
    
    # window.call("source", "Azure/azure.tcl")
    # window.call("set_theme", "light")
    sv_ttk.set_theme("dark")
    apply_theme_to_titlebar(window)
    style = ttk.Style(window)
    
    style.configure(
        "TNotebook.Tab", width=window.winfo_screenwidth(), font=("Roboto mono", 20),
        background="#3B1A4F"
        
    )
    style.map("TNotebook.Tab",  background=[("selected", '#BC32C3')])
    style.configure("TButton", font=("Roboto mono", 12))
    
    ui= UI(window)
    ui.minutes.set(00)
    ui.second.set(00)
    
    window.mainloop()