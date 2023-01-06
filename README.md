# satisfactory-save-upload

### Very much WIP at the moment

Python script to automatically handle uploading satisfactory saves to a remote location on rclone as an alternative for dedicated servers.
Since this is based on rclone, you can use products like google drive to easily share the save files with others.
I created this because servers do not currently support mods.
If I really wanted to sound like a bozo, I would call this a decentralized save management solution, but I don't think I'm a bozo, so I'll only say that satirically.

## Directions to set up
  - clone the repo: `git clone https://github.com/chbeomjunn/satisfactory-save-upload.git`
    - make sure git is installed first
  - install requirements.txt
    - `cd satisfactory-save-upload`
    - `python3 -m pip install -r requirements.txt`
  - install and create an rclone remote
    - Here's how: https://rclone.org/docs/
  - run the script
    - `python3 main.py`
  - follow the amazing built in set up guide (most of the defaults should be sensible for most people)
  - share your remote with friends and get them to also install and set up this script. 
  - Enjoy - the script will automatically notify you when starting the game as to who is using the save file (stored in a lock file on the remote)
