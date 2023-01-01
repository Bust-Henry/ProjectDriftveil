from subprocess import Popen, CREATE_NEW_CONSOLE
import os
from dotenv import load_dotenv
load_dotenv()

if __name__ == "__main__":
    api_path=os.environ.get("api_path")
    homeConnector_path=os.environ.get("homeConnector_path")
    discordBot_path=os.environ.get("discordBot_path")
    if not os.path.exists(api_path):
        print("Missing file:", api_path)
        print("Press enter to continue...")
        input()
        exit()
    if not os.path.exists(homeConnector_path):
        print("Missing file:", homeConnector_path)
        print("Press enter to continue...")
        input()
        exit()
    if not os.path.exists(discordBot_path):
        print("Missing file:", discordBot_path)
        print("Press enter to continue...")
        input()
        exit()
    Popen(f"cmd /K python3 {api_path}", creationflags=CREATE_NEW_CONSOLE)
    Popen(f"cmd /K python3 {homeConnector_path}", creationflags=CREATE_NEW_CONSOLE)
    Popen(f"cmd /K python3 {discordBot_path}", creationflags=CREATE_NEW_CONSOLE)
