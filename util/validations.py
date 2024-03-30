import bcrypt
import re
from util.db import Users, Assignments
class Validation():
    @staticmethod
    def isAssignDataValid(data):
        message=""
        name = data.get("name")
        points = data.get("points")
        num_of_attempts = data.get("num_of_attempts")
        deadline = data.get("deadline")
        mandatory = ["name","points","num_of_attempts","deadline"]
        if any(k not in data.keys() for k in mandatory):
            message = "Mandatory fields : name, points, num_of_attempts, deadline"
        elif len(data)>4:
            message = "Restricted : Only name, points, num_of_attempts, deadline are allowed"
        elif name == "" or points == "" or  num_of_attempts== "" or deadline == "":
            message = "Values cannot be Null : name, points, num_of_attempts, deadline"
        elif not isinstance(name, str):
            message = "Type error: Name should be string"
        for field in ['points', 'num_of_attempts']:
            value = data.get(field)
            if not isinstance(value, int):
                return f"Invalid type: {field} must be an integer"
            if not (1 <= value <= 100):
                return f"Invalid value: {field} must be between 1 and 100"
        return message
    
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
        if not user or not Validation.isValidPassword(password, user.password):
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
    
    @staticmethod
    def isSubDataValid(data):
        message=""
        pattern = r'/^(http|https):\/\/.*\.zip$/'
        submission_url = data.get("submission_url")
        mandatory = ["submission_url"]
        if any(k not in data.keys() for k in mandatory):
            message = "Mandatory field : submission_url"
        elif len(data)>1:
            message = "Restricted : Only Submission URL is allowed"
        elif not re.match(pattern, submission_url):
            message = "Submission URL is not in correct format"
        elif submission_url == "":
            message = "Value cannot be Null in submission_url"
        elif not isinstance(submission_url, str):
            message = "Type error: Submission URL should be string"
        return message