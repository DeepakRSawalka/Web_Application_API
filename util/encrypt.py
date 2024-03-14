import bcrypt,base64

class Encryption():
    @staticmethod
    def encrypt(password):
        encrypted_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        return encrypted_password

    @staticmethod
    def decode(auth_header):
        key = base64.b64decode(auth_header.split(" ")[1])
        user_data = key.decode().split(":")
        email, password = user_data[0], user_data[1]
        return email,password

    
    
