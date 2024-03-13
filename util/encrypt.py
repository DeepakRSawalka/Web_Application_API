import bcrypt,base64
import re
from util.db import Users, Assignments
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

    @staticmethod 
    def isValidPassword(userpassword,dbpassword):
        isValid = bcrypt.checkpw(userpassword.encode('utf-8'),dbpassword.encode('utf-8'))
        return isValid
    
    @staticmethod
    def validate_email(email):
        # Validate the email using a regex pattern
        pattern = r'^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$'
        if re.match(pattern, email):
            return True
        return False
    
    @staticmethod
    def validate_user(email, password):
        user = Users.query.filter_by(email=email).first()
        if not user or not Encryption.isValidPassword(password, user.password):
            return None
        return user
    
    @staticmethod
    def validate_assign_access(email, assignment_id):
        user = Users.query.filter_by(email=email).first()
        if not user:
            return 'Not Found'

        assignment = Assignments.query.filter_by(id=assignment_id).first()
        if not assignment:
            return 'Not Found'
        
        if user.id != assignment.owner_user_id:
            return 'Forbidden'

        return ''
    
