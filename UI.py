from tkinter import *
from tkinter import ttk
from Function import *
from PIL import Image, ImageTk
from Function import minimize_window

# create interface



class UI:
    def __init__(self, root):
        root.title("Clock")
        
        root.geometry("900x400")
        global timer_icon, stop_watch,start_icon,stop_icon,close,minimize, maximize
        self.minutes = IntVar()
        self.second = IntVar()
        self.theme_value = BooleanVar()   
        timer_icon = self.get_img("Assets\\hourglass.png", 25, 25)
        stop_watch = self.get_img("Assets\\stopwatch.png", 30, 30)
        close = self.get_img("Assets\\pause _icon.png", 25,25)
        minimize = self.get_img("Assets\\minus.png",25,25)
        maximize = self.get_img("Assets\\maximize-2.png",25,25)

        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill=BOTH, expand=True)
        #custom title bar
        self.title_frame = Frame(self.notebook,relief="flat", border=0)
        self.title_frame.pack(side=TOP, anchor=E,pady=8)
        self.close =Button(self.title_frame, text='',
                               image=close,
                               
                               relief='flat',
                               activebackground="#e7e7e7",
                               border=0,
                               width=30,
                               command=lambda: close_win(root))
        self.close.grid(row=0, column=2)
        self.minimize = Button(self.title_frame, text='', image=minimize,
                               
                               relief='flat',
                               activebackground="#e7e7e7",
                               border=0,width=30,
                               command=lambda: minimize_window(root))
        self.minimize.grid(row=0, column=0)
        self.maximize=Button(self.title_frame, text='', image=maximize,
                               
                               relief='flat',
                               activebackground="#e7e7e7",
                               border=0,width=30,
                               command=lambda: maximize_win(root))
        self.maximize.grid(row=0, column=1)
        # create timer tab
        tab1 = Frame(self.notebook)
        self.notebook.add(tab1, text="Timer", image=timer_icon, compound=LEFT)

        # create stopwatch tab
        tab2 = Frame(self.notebook)
        self.notebook.add(tab2, text="Stop Watch", image=stop_watch, compound=LEFT)

        # first half frame
        tab1_firstFm = Frame(tab1)
        tab1_firstFm.pack(fill="both", expand=True)

        # second half frame
        tab1_secondFm = Frame(tab1)
        tab1_secondFm.pack(fill="both", expand=True)

        # timer frame(minute + second)
        timer_frame = Frame(tab1_firstFm)
        timer_frame.pack(side="bottom")

        #switch theme
        theme = ttk.Checkbutton(tab1_firstFm, text="Dark Mode", style="Switch.TCheckbutton", variable=self.theme_value,
                                command=lambda: change_theme(self, root))
        theme.pack(side= RIGHT, padx=5)
        
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

        # get icons
        
        start_icon = self.get_img(img="Assets\\play-button_724963.png")
        stop_icon = self.get_img(img="Assets\\pause _icon.png")

        # control frame(start + stop)
        control_frame = Frame(tab1_secondFm)
        control_frame.pack(side="bottom", anchor="w", padx=10, pady=20)
        #create Timer_object
        timer_obj = Timer(self, root)

        self.start_button = ttk.Button(
            control_frame, text="Start", width=15, image=start_icon, compound=LEFT,
            command=lambda: timer_obj.start(),#style="Accent.TButton",
            padding= (1,1)
        )
        self.start_button.grid(row=0, column=0)

        self.stop_button = ttk.Button(
            control_frame, text="Stop", width=15, image=stop_icon, compound=LEFT, 
            command=lambda: timer_obj.stop(),
            padding= (1,1)
        )
        self.stop_button.grid(row=0, column=1)
        self.notebook.bind('<<NotebookTabChanged>>', lambda e: change_theme(self, root))
        

    def get_img(self, img, width=20, height=20):
        start_img = Image.open(img)
        start_resize = start_img.resize((width, height))
        final = ImageTk.PhotoImage(start_resize)
        return final


if __name__ == "__main__":
    window = Tk()
    #move window without title bar
    def move(event):
        
        x= window.winfo_x()-window.startX + event.x
        y = window.winfo_y()-window.startY + event.y
        window.geometry(f'+{x}+{y}')
    
    def origin_cords(event):
        window.startX= event.x
        window.startY= event.y
    
    window.overrideredirect(True)

    window.bind('<Button-1>', origin_cords)
    window.bind('<B1-Motion>',move)
    ui= UI(window)
    
    ui.minutes.set(00)
    ui.second.set(00)
    change_theme(ui,window)
    
    
    window.mainloop()