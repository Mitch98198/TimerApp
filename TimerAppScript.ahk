<<<<<<< HEAD
﻿; ACTUAL SCRIPT FOR TIMERAPP/TOPMOSTFRIEND
; Not the best, I need to implement a "fool-proof" method of opening TopMostFriend

#SingleInstance Force ;Circumvents pop-up window by confirming this is the ONLY task running.
#Persistent

^!t:: ; Ctrl + Alt + t to execute the script

	Run, C:\Users\mitch\Desktop\Python\Projects\Timer\dist\TimerApp.exe, , Hide
	
	Sleep, 500
	
	; The following moves the mouse to right click on TopMostFriend
	CoordMode, Mouse, Screen
	MouseMove, 1630, 1079
	Sleep, 5
	MouseMove, 1630, 1040, 0
	Sleep, 500
	MouseClick, Right
	Sleep, 50
	Send, {Down}
	Sleep, 50
	Send, {Enter}

=======
﻿;One version of chatGPT's script
;^!t::  ; Ctrl + Alt + T
;   Run "C:\Users\mitch\Desktop\Python\Scripts\dist\TimerApp.exe"
;return

^!t::  ; Ctrl + Alt + T
    Run, C:\Users\mitch\Desktop\Python\Timer\dist\TimerApp\TimerApp.exe, , Hide
>>>>>>> 7605b1296685c481ac893cda55304a91782cd3e1
return