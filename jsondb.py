import os
import threading
import json
import shutil
import sys
import time

class JsonDB():
    
    DB_DIRECTORY = 'database'

    __global_lock = threading.Lock()
    __db_instance = {}

    @classmethod
    def DB(cls, dbname):
        with cls.__global_lock:
            if dbname in cls.__db_instance:
                return cls.__db_instance[dbname]
            else:
                db = cls(dbname)
                db.save_cron()
                cls.__db_instance[dbname] = db
                return db

    def __init__(self, dbname):
        if not os.path.isdir(self.DB_DIRECTORY):
            os.mkdir(self.DB_DIRECTORY)
        
        self.__dbname = dbname
        self.__dbfile = os.path.join(self.DB_DIRECTORY, dbname + '.json')
        self.__backupfile = os.path.join(self.DB_DIRECTORY, dbname + '.bak.json')
        self.__lock = threading.Lock()
        self.__data = []

        if os.path.isfile(self.__backupfile):
            shutil.copy(self.__backupfile, self.__dbfile)
            os.remove(self.__backupfile)

        if os.path.isfile(self.__dbfile):
            with open(self.__dbfile, 'r') as f:
                self.__data = json.loads(f.read())
        else:
            with open(self.__dbfile, 'w') as f:
                f.write(json.dumps(self.__data, ensure_ascii=False, separators=(',', ':')))

    def save_cron(self, time_gap = 60):
        thread = threading.Thread(target=self._save_cron, args=(time_gap, ))
        thread.daemon=True
        thread.start()

    def _save_cron(self, time_gap):
        while True:
            time.sleep(time_gap)
            self.savefile()

    def __getitem__(self, key):
        with self.__lock:
            if type(key) is not int:
                raise ValueError('key must be integer')
            if key < 0 or key >= len(self.__data):
                raise ValueError(f'Invalid index {key} of array size {len(self.__data)}')
            return self.__data[key]

    def copy(self):
        with self.__lock:
            return self.__data[:]
    
    def append(self, value):
        with self.__lock:
            self.__data.append(value)
    
    def __len__(self):
        with self.__lock:
            return len(self.__data)

    def savefile(self):
        with self.__lock:
            shutil.copy(self.__dbfile, self.__backupfile)
            with open(self.__dbfile, 'w') as f:
                f.write(json.dumps(self.__data, ensure_ascii=False, separators=(',', ':')))
            os.remove(self.__backupfile)