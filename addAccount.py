from app import db, models
from io import BytesIO
import hashlib, binascii

def main(args):
    salt = b'MuchSecure'
    bytePassword = bytes(args[2], 'utf-8')
    hashedPassword = hashlib.pbkdf2_hmac('sha256', bytePassword, salt, 100000)
    account = models.Account(surname=args[5], username=args[1], firstname=args[4], password=hashedPassword, account_type=args[3])
    db.session.add(account)
    db.session.commit()

    return 0

if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))
