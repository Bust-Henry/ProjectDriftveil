import pyautogui
import win32gui
import os
from datetime import datetime
from dotenv import load_dotenv
load_dotenv()

class BlueStackController():
    toplist, winlist = [], []
    def enum_cb(self, hwnd, results):
        self.winlist.append((hwnd, win32gui.GetWindowText(hwnd)))
   
    bluestacksHandle = None
    screenshotPath = None
    def __init__(self) -> None:
        self.screenshotPath = os.path.join(os.path.dirname(__file__), os.environ.get("screenshot"))
        
        
    def setForeGround(self):
        win32gui.EnumWindows(self.enum_cb, self.toplist)
        bluestack = [(hwnd, title) for hwnd, title in self.winlist if 'bluestacks' in title.lower()]
        # just grab the hwnd for first window matching bluestack
        bluestack = bluestack[0]
        hwnd = bluestack[0]
        win32gui.SetForegroundWindow(hwnd)

    def screenshot(self):
        pyautogui.hotkey('ctrl','shift','s')

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

    def nextPokemon(self):
        pyautogui.press('A')
    
    def countPokemon(self):
        lastPokemonStats = None
        currentPokemonStats = None
        # get current pokemon

        # move to next pokemon

        # check if same pokemon
    
        # if same pokemon twice in a row, counting completed

if __name__=="__main__":
    controller = BlueStackController()

    controller.nextPokemon()