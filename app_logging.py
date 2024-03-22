import logging
import os
from datetime import datetime, timezone
import json

class CustomFormatter(logging.Formatter):
    def format(self, record):
        # Construct log message as object
        log_message = {
            "timestamp": datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z',
            "level": record.levelname,
            "message": record.getMessage()
        }

        # Conditionally add properties if they exist
        if hasattr(record, 'method'):
            log_message["method"] = record.method
        if hasattr(record, 'uri'):
            log_message["uri"] = record.uri
        if hasattr(record, 'statusCode'):
            log_message["statusCode"] = record.statusCode

        # Convert log message to a single line string
        return f"{log_message['timestamp']} {log_message['level']}: {json.dumps(log_message)}"

# Get application root path 
app_root = os.path.dirname(os.path.abspath(__file__))

# Create logger
logger = logging.getLogger('csye6225Logger')
logger.setLevel(logging.INFO)  # Set default log level

# Create file handler
file_handler = logging.FileHandler(os.path.join(app_root,'csye6225.log'))
file_handler.setFormatter(CustomFormatter())

# Add file handler to logger
logger.addHandler(file_handler)

logger.info('This is a test log message.', extra={'method': 'GET', 'uri': '/api/test', 'statusCode': 200})
