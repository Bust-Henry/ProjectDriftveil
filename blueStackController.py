import imageRecognition
import pyautogui
import win32gui
import os

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

    def renameScreenshot(self, name):
        for file in os.listdir(self.screenshotPath):
            if file.endswith(".png"):
                try:
                    os.rename(os.path.join(self.screenshotPath, file), os.path.join(self.screenshotPath, name))
                except FileExistsError:
                    self.deleteScreenshot()
                    self.renameScreenshot(name)

    def deleteScreenshot(self):
        try:
            os.remove(os.path.join(self.screenshotPath, "screenshot.png"))
        except FileNotFoundError:
            print("screenshot wasn't deleted, becaus it doesnt exist")


    def countPokemon(self):
        lastPokemonStats = None
        currentPokemonStats = None
        # get current pokemon

        # move to next pokemon

        # check if same pokemon
    
        # if same pokemon twice in a row, counting completed

if __name__=="__main__":
    controller = BlueStackController()
    controller.setForeGround()
    controller.deleteScreenshot()