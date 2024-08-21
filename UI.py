from tkinter import *
from tkinter import ttk
from Function import *
from tkextrafont import Font


# create interface


class UI:
    def __init__(self, root, minimize_helper):
        root.title("Clock")
        root.geometry("900x450")
        self.root = root,
        
        #define flag
        self.is_starting = False
        self.stop_timer = False
        self.stop_flag = False
        self.sp_start_flag = False
        self.is_moving = False

        # define font
        self.roboto_mono = Font(file="Assets\\RobotoMono-Regular.ttf", family="Roboto Mono")

        # Timer Tab_UI
        
        self.minutes = StringVar()
        self.second = StringVar()
        self.sw_minute = StringVar()
        self.sw_second = StringVar()
        self.sw_centi = StringVar()
        self.theme_value = BooleanVar()

        #create notebook
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill=BOTH, expand=True)
        # custom title bar

        logo_frame = Frame()
        self.notebook.add(logo_frame, text="    ")
        self.logo =Label(self.notebook, compound=LEFT)
        self.logo.place(x=10, y=10)

        self.title_frame = Frame(self.notebook, relief="flat", border=0)
        self.title_frame.pack(side=TOP, anchor=E, pady=8)
        self.close = Button(self.title_frame, text='',
                            
                            relief='flat',
                            border=0,
                            width=30,
                            command=lambda: self.close_win(root))
        self.close.grid(row=0, column=2)
        self.minimize = Button(self.title_frame, text='',

                               relief='flat',
                               border=0, width=30,
                               command=lambda: minimize_window(root, minimize_helper))
        self.minimize.grid(row=0, column=0)
        self.maximize = Button(self.title_frame, text='',

                               relief='flat',
                               border=0, width=30,
                               command=lambda: maximize_win(self,root))
        self.maximize.grid(row=0, column=1)

        # create notebook tab
        tab1 = Frame(self.notebook)
        self.notebook.add(tab1, text="Timer", compound=LEFT)

        # create stopwatch tab
        self.tab2 = Frame(self.notebook)
        self.notebook.add(self.tab2, text="Stop Watch",
                          compound=LEFT)
        self.notebook.select(tab1)
        self.notebook.tab(0, state="disabled")
        # first half frame
        tab1_firstFm = Frame(tab1)
        tab1_firstFm.pack(fill="both", expand=True)

        # second half frame
        tab1_secondFm = Frame(tab1)
        tab1_secondFm.pack(fill="both", expand=True)

        # timer frame(minute + second)
        timer_frame = Frame(tab1_firstFm)
        timer_frame.pack(side="bottom")

        # switch theme
        theme = ttk.Checkbutton(tab1_firstFm, text="Dark Mode", style="Switch.TCheckbutton", variable=self.theme_value,
                                command=lambda: change_theme(self, root))
        theme.pack(side=RIGHT, padx=5)

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

            justify=RIGHT,
            textvariable=self.minutes
        )
        self.minute_ui.grid(row=0, column=0)
        Label(minute_frame, text="m", font=("Roboto mono", 20)).grid(
            row=0, column=1, sticky=S
        )
        self.minute_ui.bind(
            "<Button-1>", lambda e: self.minute_ui.delete(0, tk.END))
        self.minute_ui.bind("<Key>", lambda e: limit_digit(self, self.minutes))

        # second UI that allow user to input second
        self.second_ui = ttk.Entry(
            second_frame,
            font=("Roboto mono", 50),
            width=5,

            justify=RIGHT,
            textvariable=self.second,

        )
        self.second_ui.grid(row=0, column=0)
        Label(second_frame, text="s", font=("Roboto mono", 20)).grid(
            row=0, column=1, sticky=S
        )
        self.second_ui.bind(
            "<Button-1>", lambda e: self.second_ui.delete(0, tk.END))
        self.second_ui.bind(
            "<Key>", lambda e: limit_digit(self, self.second, True))
        
        #set initial value to minute and second
        self.minutes.set("00")
        self.second.set("00")

        # control frame(start + stop)
        control_frame = Frame(tab1_secondFm)
        control_frame.pack(side="bottom", anchor="w", padx=10, pady=20)
        # create Timer_object
        self.timer_obj = Timer(self, root)

        self.start_button = ttk.Button(
            control_frame, text="Start", width=15, compound=LEFT,
            command=lambda: self.timer_obj.start(),
            padding=(1, 1)
        )
        self.start_button.grid(row=0, column=0)

        self.stop_button = ttk.Button(
            control_frame, width=15, compound=LEFT,
            command=lambda: (
                self.timer_obj.stop()) if not self.stop_flag else reset_timer(self, root),
            padding=(1, 1)
        )
        self.stop_button.grid(row=0, column=1)
        self.notebook.bind('<<NotebookTabChanged>>',
                           lambda e: change_theme(self, root))

        # Timer Stopwatch Tab_UI
        self.canvas = Canvas(self.tab2, width=900, height=350)
        self.canvas.pack(expand=True)

        #draw a circle path and circle
        self.path = self.canvas.create_oval(
            296, 329, 604, 21, outline="grey", width=5)
        self.circle = self.canvas.create_oval(
            434.6, 344.4, 465.4, 313.6, fill='light grey', outline='light grey')
        
        # Extract the center and radius of the path
        self.center_x, self.center_y, self.radius = calculate_path_details(
            self)
        
        # Set the initial angle for the circle
        self.angle = 0

        # Define the speed of the circle
        self.speed = 0.035

        # add control
        self.sp_control = Frame(self.tab2)
        self.sp_control.pack(pady=5)

        self.stop_watchBtn = ttk.Button(self.sp_control,
                                        text='',
                                        compound='center',
                                        width=30,
                                        command=lambda: start_stopwatch(self, root) if not self.sp_start_flag else stop_stopwatch(self, root))
        self.stop_watchBtn.grid(row=0, column=0)

        self.reset_button = ttk.Button(
            self.sp_control,
            
            compound='center',
            width=15,
            command=lambda: reset_sw(self, root))

        # stop watch label
        stop_watch_frame = Frame(self.canvas)
        stop_watch_frame.place(relx=0.37, rely=0.4)
        self.minute_label = Label(stop_watch_frame, font=(
            "Roboto mono", 35), textvariable=self.sw_minute)
        self.minute_label.grid(row=0, column=0)

        self.second_label = Label(stop_watch_frame, font=(
            "Roboto mono", 35), textvariable=self.sw_second)
        self.second_label.grid(row=0, column=2)

        self.centisecond = Label(stop_watch_frame, font=(
            "Roboto mono", 35), textvariable=self.sw_centi)
        self.centisecond.grid(row=0, column=4)
        # insert (:)
        for i in range(2):
            Label(stop_watch_frame, text=":", font=(
                "Roboto mono", 35)).grid(row=0, column=(i*2)+1)
        #set the initial value
        self.sw_centi.set("00")
        self.sw_second.set("00")
        self.sw_minute.set("00")
    def close_win(self, root):
        stop_stopwatch(self, root)
        self.timer_obj.stop()
        root.after(300, root.destroy())


def main():
    # Reference: https://stackoverflow.com/questions/4066027/making-tkinter-windows-show-up-in-the-taskbar
    window = Tk()
    minimize_helper = Toplevel(window)    # add a taskbar icon
    minimize_helper.iconbitmap("Assets\\my_logo.ico")
    minimize_helper.title("Multi Timer")
    #remove title bar for custom title bar
    window.overrideredirect(True)

    minimize_helper.attributes("-alpha", 0.0)

    # move window without title bar
    window.bind('<Button-1>', lambda e: origin_cords(e, window))
    window.bind('<B1-Motion>', lambda e: move(e, window))

    #add ui
    ui = UI(window, minimize_helper)

    #apply change to buttons when theme change
    change_theme(ui, window)

    # toplevel follows root taskbar events (minimize, restore)
    def onRootIconify(event): window.withdraw()
    minimize_helper.bind("<Unmap>", onRootIconify)
    def onRootDeiconify(event): window.deiconify()
    minimize_helper.bind("<Map>", onRootDeiconify)

    window_ = Frame(master=window)
    window_.mainloop()


if __name__ == "__main__":
    main()
