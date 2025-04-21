import tkinter as tk
from playsound import playsound #for the ending audio
import threading #some issues with the window freezing when playsound is executed

class TimerApp:

    def __init__(self, root):

        self.root = root
        self.root.overrideredirect(True) #Remove annoying max/min/X buttons

        #Setting up the ET (enter time) size, and position
        screenW = self.root.winfo_screenwidth()
        screenH = self.root.winfo_screenheight()
        
        self.ET_width = 60 #hand picked values
        self.ET_height = 76
        self.AT_width = 140
        self.AT_height = 70
       
        self.globalX = screenW - self.ET_width - 80 #offset bc next window is slightly longer
        self.globalY = screenH - self.ET_height
        
        #Initializing some things
        self.ogTime = 0
        self.remainingSecs = 0
        self.timerRunning = False
        self.timerID = None

        self.CreateETScreen()
        self.MakeWindowMovable()

    #create the ET (entertime screen)
    def CreateETScreen(self):
        self.ClearRoot() #clear previous widgets
        self.timerRunning = False
        self.root.geometry(F"{self.ET_width}x{self.ET_height}+{self.globalX}+{self.globalY}")
        self.ETframe = tk.Frame(self.root)
        self.ETframe.pack()

        tk.Label(self.ETframe, text = " ").pack()
        self.timeEntry = tk.Entry(self.ETframe, width = 5, font = ("Helvetica", 12))
        self.timeEntry.pack()

        #frame setup
        buttonFrame = tk.Frame(self.ETframe)
        buttonFrame.pack(pady = 3)

        #button setup
        tk.Button(buttonFrame, text = "Set", command = self.SetTimer).pack(side = "left", padx = 1)
        tk.Button(buttonFrame, text = "X", command = self.root.quit).pack(side = "left", padx = 1)

        self.root.bind("<Return>", self.SetAndStartTimer)

    #create the AT (actual time) screen
    def CreateTimerScreen(self):
        self.ClearRoot()
        self.timerFrame = tk.Frame(self.root)
        self.timerFrame.pack()

        self.timeLabel = tk.Label(self.timerFrame, text = self.FormatTime(), font = ("Helvetica", 24))
        self.timeLabel.pack(pady = 0)

        buttonFrame = tk.Frame(self.timerFrame)
        buttonFrame.pack()

        self.startStopButton = tk.Button(buttonFrame, text = "Start", command = self.ToggleTimer)
        self.startStopButton.pack(side = "left", padx = 1)

        #Button setup
        tk.Button(buttonFrame, text = "Reset", command = self.ResetTimer).pack(side = "left", padx = 1)
        tk.Button(buttonFrame, text = "Redo", command = self.CreateETScreen).pack(side = "left", padx = 1)
        tk.Button(buttonFrame, text = "X", command = self.root.quit).pack(side = "left", padx = 1)

        #change the geometry to AT
        self.root.geometry(f"{self.AT_width}x{self.AT_height}")

    #"clears" the window
    def ClearRoot(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    #Used for enter key
    def SetTimerEvent(self, event):
        self.SetTimer()

    def ResetTimer(self):
        self.timerRunning = False
        self.remainingSecs = self.ogTime
        self.timeLabel.config(text = self.FormatTime())
        self.startStopButton.config(text = "Start")

    def PlaySound(self):
        playsound("theGoblins.mp3")

    def SetTimer(self):
        try:
            minutes = int(self.timeEntry.get())
            self.ogTime = self.remainingSecs = minutes * 60
            self.CreateTimerScreen()
            #self.StartTimer()
        except ValueError:
            pass

    #specific func for the enter key
    def SetAndStartTimer(self, event = None):
        self.SetTimer()
        self.root.after(10, self.StartTimer)
        self.startStopButton.config(text = "Stop")

    
    def StartTimer(self):
        self.timerRunning = True
        self.UpdateTimer()

    def UpdateTimer(self):
        self.timeLabel.config(text = self.FormatTime())
        
        if self.timerRunning and self.remainingSecs > 0:
            self.remainingSecs -= 1
            self.timerID = self.root.after(1000, self.UpdateTimer)
        
        elif self.remainingSecs == 0:
            self.timerRunning = False
            self.timeLabel.config(text = "DONE!")

            soundThread = threading.Thread(target = self.PlaySound)
            soundThread.start()

    def ToggleTimer(self):
        if self.timerRunning:
            self.timerRunning = False
            self.startStopButton.config(text = "Start")
            
            if self.timerID:
                self.root.after_cancel(self.timerID)
            
        else:
            self.timerRunning = True
            self.startStopButton.config(text = "Stop")
            self.UpdateTimer()

    def FormatTime(self):
        hours = self.remainingSecs // 3600
        minutes = (self.remainingSecs % 3600) // 60
        seconds = self.remainingSecs % 60

        if hours > 0:
            return f"{hours:02}:{minutes:02}:{seconds:02}"
        else:
            return f"{minutes:02}:{seconds:02}"
        
    #quick/easy func for making the window movable, as overrideredirect(True) removes it!
    def MakeWindowMovable(self):
        def StartMove(event):
            self.xOffset = event.x
            self.yOffset = event.y

        def OnMove(event):
            self.globalX = self.root.winfo_x() + (event.x - self.xOffset)
            self.globalY = self.root.winfo_y() + (event.y - self.yOffset)
            self.root.geometry(f"+{self.globalX}+{self.globalY}")

        self.root.bind("<Button-1>", StartMove)
        self.root.bind("<B1-Motion>", OnMove)


root = tk.Tk()
app = TimerApp(root)
root.mainloop()