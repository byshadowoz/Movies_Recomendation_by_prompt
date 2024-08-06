import bcrypt
def encryptPassword(password):
    pwd = password.encode('utf-8')
    sal = bcrypt.gensalt()
    encrypt = bcrypt.hashpw(pwd, sal)
    return encrypt

def uncryptPassword(Password, hash):
    return bcrypt.checkpw(Password.encode('utf-8'), hash)
