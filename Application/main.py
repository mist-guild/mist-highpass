from gui import HighpassGUI
from dotenv import load_dotenv

load_dotenv('.env')

if __name__ == "__main__":
    gui = HighpassGUI()
    gui.run()
