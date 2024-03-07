import re
class Validation():
    def isUserDataValid(data):
        message=""
        first_name = data.get("first_name")
        last_name = data.get("last_name")
        email = data.get("email")
        password = data.get("password")
        is_email_valid = r'^(?i)([a-z0-9]+([/.][a-z0-9]+)?[@][a-z0-9]+[/.][a-z]+)$'
        is_name_valid = r'^(?i)[a-z]+$'
        mandatory = ["first_name","last_name","email","password"]
        if any(k not in data.keys() for k in mandatory):
            message = "Mandatory fields : first_name, last_name, email, password"
        elif len(data)>4:
            message = "Restricted : Only first_name, last_name, email, password fields are allowed"
        elif first_name == "" or last_name == "" or email == "" or password == "":
            message = "Values cannot be Null : first_name, last_name, username, password"
        elif any(not isinstance("Temp",type(k)) for k in data.values()):
            message = "first_name, last_name, email, password should contain string"
        elif not(re.match(is_name_valid,first_name)) or not(re.match(is_name_valid,last_name)):
            message = "first_name and last_name should can only contain characters and should be of one word without spaces"
        elif not(re.match(is_email_valid,email)):
            message = "Username should contain email address in correction format (example: demo@domain.com)"
        return message