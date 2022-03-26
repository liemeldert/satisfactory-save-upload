import psutil
import os
import pyclone
from pathlib import Path
from satisfactory_save_upload import rclone_remote, rclone_save_path, local_save_path, game_path, save_path, pyclone_obj
# somewhat needlessly OOP stuff, but it looks fancy so it's okay.


class GameSave:
    def __init__(self, path):
        self.path = path

        # extract header data from save file.
        with open(path, 'rb') as file:

            # bad solution, pattern defines length of group
            pattern = [4, 4, 4, None, None, None, 4, 8, 1, 4, None, 4]
            chunked = []
            for current_len in pattern:
                if current_len is None:
                    current_len = int.from_bytes(file.read(4), "little")
                    read_bytes = file.read(current_len).strip(b"\x00").decode()
                    if read_bytes == '':
                        chunked.append(None)
                    else:
                        chunked.append(read_bytes)
                else:
                    read_bytes = file.read(current_len)
                    if current_len == 1:
                        chunked.append(bool.from_bytes(read_bytes, "little"))
                    else:
                        chunked.append(int.from_bytes(read_bytes, "little"))

        # might make more sense to just like use json or something - especially if I read the whole file for some reason
        self.header_version = chunked[0]
        self.save_version = chunked[1]
        self.build_version = chunked[2]
        self.world_type = chunked[3]
        self.world_properties = chunked[4]
        self.session_name = chunked[5]
        self.play_time = chunked[6]
        self.save_date = chunked[7]
        self.session_visibility = chunked[8]
        self.editor_object_version = chunked[9]
        self.mod_metadata = chunked[10]
        self.mod_flags = chunked[11]

    @property
    def remote_presence(self) -> bool:
        for each in pyclone_obj.ls(rclone_remote, rclone_save_path):
            if each == self.path:
                return True
        return False

    def upload_file(self):
        pyclone_obj.copy(self.path, rclone_remote, rclone_save_path)


class Game:
    def __init__(self, process, local_save_path):
        self.process = process
        self.save_path = local_save_path

    # might not need to be a setter, but whatever
    @property
    def state(self) -> bool:
        for proc in psutil.process_iter():
            if proc.name() == self.process:
                return True
        return False

    @property
    def saves(self) -> list[GameSave]:
        saves = []
        for root, dirs, files in os.walk(self.save_path):
            for file in files:
                if file.endswith('.sav'):
                    saves.append(os.path.join(root, file))
        save_objs = []
        for each in saves:
            save_objs.append(GameSave(each))
        return save_objs

    def get_latest_save(self) -> GameSave:
        modified_time = []
        for save in self.saves:
            modified_time.append((save.save_date, save))
        # bogosort for your waiting pleasure
        modified_time.sort(key=lambda y: y[0])
        return modified_time[0][1]
