## Features added:

* triggerbot + magnet.

* abilities triggerbot + magnet. (previous releases)

* a much faster screengrab.

* better smoothing.


## Installation:

I have made changes to the dll so to use this you' ll have to recompile it from the source uploaded here plus having: 

* InputInterceptor.dll (https://github.com/0x2E757/InputInterceptor) 

* interception.dll (https://github.com/oblitum/Interception YOU ALSO NEED TO INSTALL THIS)

* ClassLibrary1.dll

All in the same folder. 

Once thats done edit grabber.py line 14 to the location of the ClassLibrary dll.

**Example:**
```
clr.AddReference('C:\\Users\\You\\Desktop\\New folder (3)\\DLL\\ClassLibrary1\\ClassLibrary1.dll')
```
Then install the required packages by using this command with your python interpreter (opened inside the folder):
```
pip install -r requirements.txt
```
In case you dont know how to run a python script: https://pythonbasics.org/execute-python-scripts/




## Settings:
All the settings are in main.py but I dont really use anything else other then the aim key so 

the they arent tuned well, try messing around with the sleeps and stuff till you find a good balance.






If you are experiencing frame drops you can try restarting the application every game.

I am not sure whats causing it, probably something with dxcam



## Credits: 

https://www.unknowncheats.me/forum/members/3853446.html (what this is pasted from)

https://www.unknowncheats.me/forum/valorant/414206-implementing-speed-color-aimbot.html (part of the smooth)




I dont really code/ know what I am doing and the code is incredibly lazy but still this works fairly well imo.
