from __future__ import annotations

import datetime
import os

import requests
from flask import Blueprint
from flask import jsonify
from flask import send_from_directory
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

models_blueprint = Blueprint('models', __name__)
limiter = Limiter(key_func=get_remote_address)

# Define the directory where the model files are stored
MODELS_DIRECTORY = 'models/pt/'
# Define the allowed models
ALLOWED_MODELS = {'yolov8n', 'yolov8s', 'yolov8m', 'yolov8l', 'yolov8x'}


@models_blueprint.route('/models/<model_name>', methods=['GET'])
@limiter.limit('10 per minute')
def download_model(model_name):
    """
    Endpoint to download model files.

    Args:
        model_name (str): The name of the model file to download.

    Returns:
        Response: A Flask response object that downloads the model file.
    """
    # Ensure the model name is valid
    if model_name not in ALLOWED_MODELS:
        return jsonify({'error': 'Model not found.'}), 404

    file_name = f"best_{model_name}.pt"

    try:
        # Define the external URL for model files
        MODEL_URL = (
            f"http://changdar-server.mooo.com:28000/models/{file_name}"
        )

        # Check last modified time via a HEAD request to the external server
        response = requests.head(MODEL_URL)
        if response.status_code == 200 and 'Last-Modified' in response.headers:
            server_last_modified = datetime.datetime.strptime(
                response.headers['Last-Modified'],
                '%a, %d %b %Y %H:%M:%S GMT',
            )

            # Use os.path.join to safely construct the file path
            local_file_path = os.path.join(
                MODELS_DIRECTORY, file_name,
            )

            # Ensure the constructed path is within the expected directory
            common_path = os.path.commonpath(
                [local_file_path, MODELS_DIRECTORY],
            )
            if common_path != MODELS_DIRECTORY:
                return jsonify({'error': 'Invalid model name.'}), 400

            # Check local file's last modified time
            if os.path.exists(local_file_path):
                local_last_modified = datetime.datetime.fromtimestamp(
                    os.path.getmtime(local_file_path),
                )
                if local_last_modified >= server_last_modified:
                    return jsonify(
                        {
                            'message': 'Local model is up-to-date.',
                        },
                    ), 304

        # If not up-to-date, fetch the file and return it
        return send_from_directory(
            MODELS_DIRECTORY,
            model_name,
            as_attachment=True,
        )

    except FileNotFoundError:
        return jsonify(
            {
                'error': 'Model not found.',
            },
        ), 404

    except requests.RequestException as e:
        return jsonify(
            {
                'error': 'Failed to fetch model information.',
                'details': str(e),
            },
        ), 500
