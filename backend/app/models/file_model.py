import datetime

class FileModel:
    """Defining the file model/schem"""
    
    def __init__(self, filename, recipient_name, operation):
        self.filename = filename
        self.recipient_name = recipient_name
        self.operation = operation
        self.timestamp = datetime.datetime.utcnow()

    def to_dict(self):
        return {
            "filename": self.filename,
            "recipient_name": self.recipient_name,
            "operation": self.operation,
            "timestamp": self.timestamp.strftime("%Y-%m-%d %H:%M:%S")
        }
