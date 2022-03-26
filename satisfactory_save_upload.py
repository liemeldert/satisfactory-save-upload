import psutil
import os
import pyclone
from pathlib import Path
import time
import configparser
import objects
import tkinter as tk
from tkinter import ttk

config_path = Path('satisfactory_save_upload/config.ini')
process_name = 'FactoryGame-Win64-Shipping.exe'
pyclone_obj = pyclone.PyClone()
parser = configparser.ConfigParser()

global rclone_remote
global rclone_save_path
global local_save_path
global game_path
global save_path

root = tk.Tk()
root.title("Satisfactory save manager")
root.geometry('600x400+50+50')
root.resizable(False, False)


def update_loop(save_path: Path) -> None:
    game = objects.Game(process_name, save_path)
    while True:
        time.sleep(10)


def play_alert():
    root.attributes('-topmost', 1)


def display_saves():
    


def confirm():
    root.attributes('-topmost', 0)


def main(run=False) -> None:
    if not os.path.isfile(config_path):
        if run:
            raise SystemExit('Something went wrong when trying to save the file... '
                             'Make sure the folder can be writen to.')
        # collect config file information
        # TODO: Convert to a menu in tkinter
        print("Config.ini not found!")
        print(pyclone_obj.remotes())
        print("Which remote would you like to use? (enter remote's name)\n"
              "If there are none, please create one from rclone first.")
        remote = input()
        print("Please enter the path to the directory you want your saves to upload to.")
        directory = input()
        print("Please enter the path to where your saves are located, or leave blank for me to try to find them for "
              "you.")
        saves_path = input()
        if saves_path is None: 
            saves_path = str(Path.home()) + r"\AppData\Local\FactoryGame\Saved\SaveGames"
            for root, dirs, files in os.walk(saves_path):
                for file in files:
                    if file.endswith('.sav'):
                        break
            saves_path = Path(root)
            if root is None:
                print("I could not find the save directory, please enter it manually.")
                saves_path = Path(input())
        print(r"Please enter the path to your game files (leave blank for default: "
              r"'C:\Program Files (x86)\Steam\steamapps\common\Satisfactory'")
        game_path = input()
        
        # generate config file
        parser.add_section('Satisfactory_upload')
        parser.set('Satisfactory_upload', 'remote', remote)
        parser.set('Satisfactory_upload', 'directory', directory)
        parser.set('Satisfactory_upload', 'saves_path', saves_path)
        parser.set('Satisfactory_upload', 'game_path', game_path)
        
        # save config file
        fp = open(config_path, 'w')
        parser.write(fp)
        fp.close()
        main(run=True)
    
    else:
        parser.read(config_path)
        rclone_remote = parser.get('Satisfactory_upload', 'remote')
        rclone_save_path = parser.get('Satisfactory_upload', 'directory')
        local_save_path = parser.get('Satisfactory_upload', 'saves_path')
        game_path = parser.get('Satisfactory_upload', 'game_path')
        save_path = Path(parser.get('Satisfactory_upload', 'saves_path'))

        update_loop(save_path)

try:
    from ctypes import windll

    windll.shcore.SetProcessDpiAwareness(1)
finally:
    root.mainloop()

if __name__ == '__main__':
    main()
