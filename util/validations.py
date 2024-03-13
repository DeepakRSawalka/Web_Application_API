
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