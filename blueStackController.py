import pyautogui
import win32gui
import win32com.client
import pythoncom
import os
from datetime import datetime
from PIL import Image, ImageGrab
import imageRecognition
import time
from dotenv import load_dotenv
load_dotenv()
import json

class BlueStackController():
    toplist, winlist = [], []
    def enum_cb(self, hwnd, results):
        self.winlist.append((hwnd, win32gui.GetWindowText(hwnd)))
   
    bluestacksHandle = None
    screenshotPath = None
    def __init__(self) -> None:
        self.screenshotPath = os.path.join(os.path.dirname(__file__), os.environ.get("screenshot"))
        self.macros = json.load(open(os.path.join(os.path.dirname(__file__), os.environ.get("bluestacksMacros"))))
        
        
    def setForeGround(self):
        win32gui.EnumWindows(self.enum_cb, self.toplist)
        bluestack = [(hwnd, title) for hwnd, title in self.winlist if 'bluestacks' in title.lower()]
        # just grab the hwnd for first window matching bluestack
        bluestack = bluestack[0]
        hwnd = bluestack[0]
        xl=win32com.client.Dispatch("Excel.Application",pythoncom.CoInitialize())
        shell = win32com.client.Dispatch("WScript.Shell")
        shell.SendKeys('%')
        win32gui.SetForegroundWindow(hwnd)
    
    def getBBox(self):
        win32gui.EnumWindows(self.enum_cb, self.toplist)
        bluestack = [(hwnd, title) for hwnd, title in self.winlist if 'bluestacks' in title.lower()]
        # just grab the hwnd for first window matching bluestack
        bluestack = bluestack[0]
        hwnd = bluestack[0]
        xl=win32com.client.Dispatch("Excel.Application",pythoncom.CoInitialize())
        shell = win32com.client.Dispatch("WScript.Shell")
        shell.SendKeys('%')
        return win32gui.GetWindowRect(hwnd)

    def screenshot(self):
        self.deleteScreenshot()
        self.setForeGround()
        pyautogui.hotkey('ctrl','shift','s')
        self.renameScreenshot("screenshot.png")
        return Image.open(os.path.join(os.path.dirname(__file__), "data", "screenshot", "screenshot.png"))

    def screenshotPIL(self):
        self.setForeGround()
        bbox = self.getBBox()
        return ImageGrab.grab(bbox)

    def clearScreenshots(self):
        for file in os.listdir(self.screenshotPath):
            os.remove(file)
    
    def renameScreenshot(self, name, timeout=5):
        startTimestamp = datetime.now()
        renamed = False
        while not renamed:
            try:
                for file in os.listdir(self.screenshotPath):
                    if file.endswith(".png"):
                        try:
                            os.rename(os.path.join(self.screenshotPath, file), os.path.join(self.screenshotPath, name))
                            renamed = True
                        except FileExistsError:
                            self.deleteScreenshot()
                            self.renameScreenshot(name)
                            renamed = True
            except FileNotFoundError:
                currentTimestamp = datetime.now()
                delta = startTimestamp - currentTimestamp
                if delta.seconds > timeout:
                    return False
        return True

    def deleteScreenshot(self):
        try:
            os.remove(os.path.join(self.screenshotPath, "screenshot.png"))
        except FileNotFoundError:
            print("screenshot wasn't deleted, becaus it doesnt exist")

    def closeAll(self):
        self.runMacro(self.macros["CloseAll"])
        time.sleep(3)    
    def executePythonScript(self):
        self.runMacro(self.macros["ExecutePythonScript"])

    def openHome(self):
        self.runMacro(self.macros["OpenHome"])

    def pressStart(self):
        self.runMacro(self.macros["PressStart"])
    
    def closeScript(self):
        self.runMacro(self.macros["CloseScript"])
        time.sleep(2.5)

    def runMacro(self, macro):
        keys = macro.split(";")
        self.setForeGround()
        pyautogui.hotkey(*keys)

    def sendSaveData(self):
        self.executePythonScript()
        time.sleep(2)
        timeout = 10
        starttime = datetime.now()
        executed = False
        while not executed:
            img = self.screenshotPIL()
            onscreentext = imageRecognition.readAll(img)
            if "done!" in onscreentext:
                executed = True
            if (datetime.now() - starttime).total_seconds() > timeout:
                print("sending data timed out!")
                break
            time.sleep(1)
        self.closeScript()
        self.closeAll()
        print("script executed", executed)
        if executed:
            return True
        return False
    
    def reloadSaveData(self) -> bool:
        self.setForeGround()
        self.openHome()
        ready = False
        timeout = 13
        starttime = datetime.now()
        while not ready:
            time.sleep(2)
            img:Image = self.screenshotPIL()
            text = imageRecognition.readAll(img)
            if "TAP TO START" in text:
                ready = True
            if (datetime.now() - starttime).total_seconds() > timeout:
                print("opening pokemon home timed out!")
                break
        if not ready:
            return False
        self.pressStart()
        ready = False
        timeout = 13
        starttime = datetime.now()
        while not ready:
            time.sleep(2)
            img:Image = self.screenshotPIL()
            text = imageRecognition.readAll(img)
            if "Trade" in text:
                ready = True
                break
            if (datetime.now() - starttime).total_seconds() > timeout:
                print("opening pokemon home timed out!")
                break
        if not ready:
            return False
        self.closeAll()
        return True
        
        
if __name__=="__main__":
    controller = BlueStackController()
    controller.closeAll()
    if controller.reloadSaveData():
        controller.sendSaveData()