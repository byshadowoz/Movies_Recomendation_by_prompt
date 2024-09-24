import bcrypt

def encryptPassword(password):
    pwd = password.encode('utf-8')
    sal = bcrypt.gensalt()
    encrypt = bcrypt.hashpw(pwd, sal)
    return encrypt

def uncryptPassword(Password, hash):
    return bcrypt.checkpw(Password.encode('utf-8'), hash)

def checkPassword(password, username):
    import sqlite3
    database = sqlite3.connect('database/usersAndMovie')
    cursor = database.cursor()
    cursor.execute(f'SELECT password FROM user WHERE name = ?', (username, ))
    hashs = cursor.fetchone()[0]
    if uncryptPassword(password, hashs) == True:
        return True
    else:
        return False
