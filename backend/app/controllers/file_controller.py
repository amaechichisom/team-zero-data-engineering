from flask import request, jsonify
from app.services.s3_service import S3Service
from app.models.file_model import FileModel
from app.utils.logger import log_operation
from flasgger.utils import swag_from


s3_service = S3Service()

@swag_from({
    'responses': {
        200: {
            'description': 'File successfully uploaded',
            'examples': {
                'application/json': {
                    'message': 'File uploaded successfully'
                }
            }
        }
    },
    'parameters': [
        {
            'name': 'file',
            'in': 'formData',
            'type': 'file',
            'required': True,
            'description': 'The file to upload'
        }
    ]
})
def upload_file():
    """Handle file uploads to S3."""
    
    recipient_name = request.form.get("recipient_name")
    file = request.files.get("file")

    if not file or not recipient_name:
        return jsonify({"error": "File or recipient name is missing"}), 400

    filename = file.filename
    file_model = FileModel(filename, recipient_name, "upload")

    try:
        s3_service.upload_file(file, filename)
        log_operation(file_model.to_dict())
        return jsonify({"message": "File uploaded successfully", "file": filename}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@swag_from({
    'responses': {
        200: {
            'description': 'Successfully retrieved file content'
        },
        404: {
            'description': 'File not found'
        }
    },
    'parameters': [
        {
            'name': 'filename',
            'in': 'path',
            'type': 'string',
            'required': True,
            'description': 'The name of the file to retrieve'
        }
    ]
})
def get_file(filename):
    """Handle get file from S3."""
    
    recipient_name = request.args.get("recipient_name")

    if not recipient_name:
        return jsonify({"error": "Recipient name is missing"}), 400

    file_model = FileModel(filename, recipient_name, "retrieve")

    try:
        file_url = s3_service.generate_file_url(filename)
        log_operation(file_model.to_dict())
        return jsonify({"file_url": file_url}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@swag_from({
    'responses': {
        200: {
            'description': 'File successfully deleted',
            'examples': {
                'application/json': {
                    'message': 'File deleted successfully'
                }
            }
        },
        404: {
            'description': 'File not found'
        }
    },
    'parameters': [
        {
            'name': 'filename',
            'in': 'path',
            'type': 'string',
            'required': True,
            'description': 'The name of the file to delete'
        }
    ]
})
def delete_file(filename):
    """Handle file deletion from S3."""
    
    recipient_name = request.args.get("recipient_name")

    if not recipient_name:
        return jsonify({"error": "Recipient name is missing"}), 400

    file_model = FileModel(filename, recipient_name, "delete")

    try:
        s3_service.delete_file(filename)
        log_operation(file_model.to_dict())
        return jsonify({"message": "File deleted successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
