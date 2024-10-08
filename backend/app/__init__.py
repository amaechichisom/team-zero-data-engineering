from flask import Flask
from app.controllers import file_controller
from flasgger import Swagger

def create_app():
    app = Flask(__name__)

    swagger_template = {
        "swagger": "2.0",
        "info": {
            "title": "Team Zero API",
            "description": "API for uploading, downloading, and deleting files from S3 bucket",
            "version": "1.0.0"
        },
        "host": "localhost:5000",
        "basePath": "/",
        "schemes": ["http"],
        "consumes": ["application/json"],
        "produces": ["application/json"]
    }
    
    swagger = Swagger(app, template=swagger_template)

    app.add_url_rule('/upload', view_func=file_controller.upload_file, methods=['POST'])
    app.add_url_rule('/download/<filename>', view_func=file_controller.get_file, methods=['GET'])
    app.add_url_rule('/delete/<filename>', view_func=file_controller.delete_file, methods=['DELETE'])

    return app
