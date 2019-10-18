from jsondb import JsonDB




def add_new_arena_log(data):
    db = JsonDB.DB('arena')
    db.append(data)

