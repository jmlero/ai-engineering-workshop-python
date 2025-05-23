from flask import Blueprint, request, jsonify, current_app
from .request_models import CurlChatRequest

curl_bp = Blueprint('curl_bp', __name__, url_prefix='/curl')

@curl_bp.route('/chat', methods=['POST'])
def chat_request():
    data = request.get_json()
    if not data or 'message' not in data:
        return jsonify({"error": "Missing message"}), 400
    
    try:
        # Assuming CurlChatRequest can be instantiated directly from the dict
        # if its fields match the keys in `data`.
        # For more complex validation or transformation, you might use a library
        # or manual checks.
        chat_req = CurlChatRequest(message=data['message'])
    except TypeError as e:
        # This might happen if 'message' key is present but other unexpected keys are also there
        # and CurlChatRequest is strict about its fields.
        # Or if data['message'] is not a string.
        return jsonify({"error": f"Invalid request format: {str(e)}"}), 400

    orchestrator = current_app.config['LLM_ORCHESTRATOR']
    reply = orchestrator.call(chat_req.message)
    return jsonify({"reply": reply})
