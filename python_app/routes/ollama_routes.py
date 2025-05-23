from flask import Blueprint, request, jsonify, current_app
from datetime import datetime, timezone
from .request_models import (
    OllamaChatRequest, OllamaChatResponse, OllamaMessage, 
    TagsResponse, ModelInfo, ModelDetails, 
    OllamaToolCall, OllamaToolCallFunction # Ensure these are imported if used by request structure
)
from dataclasses import asdict # For converting dataclasses to dict for jsonify

ollama_bp = Blueprint('ollama_bp', __name__, url_prefix='/ollama')

@ollama_bp.route('/api/chat', methods=['POST'])
def chat_request():
    data = request.get_json()
    if not data or not data.get('messages'):
        return jsonify({"error": "Invalid request structure for Ollama chat"}), 400
    
    try:
        # Basic parsing, assuming structure largely matches.
        # For a production app, consider using a library like Pydantic for robust validation.
        
        # Assuming OllamaChatRequest can be constructed if data matches its structure.
        # This is a simplified approach. Direct instantiation from a complex nested dict 
        # might require a more sophisticated parsing mechanism (e.g. a library or a custom parser).
        
        # For placeholder, let's just extract some info to form a reply
        last_msg_data = data['messages'][-1] # Get the last message
        last_message_content = last_msg_data.get('content', '')

        orchestrator = current_app.config['LLM_ORCHESTRATOR']
        reply_content = orchestrator.call(last_message_content)
        
        response_message = OllamaMessage(role="assistant", content=reply_content)
        
        # Using datetime.now(timezone.utc).isoformat() to get a string, as dataclass field is str
        chat_response = OllamaChatResponse(
            model="workshop_py_converted", 
            created_at=datetime.now(timezone.utc).isoformat(), 
            message=response_message, 
            done=True,
            done_reason="stop" # Added done_reason as per dataclass definition
        )
        return jsonify(asdict(chat_response))
        
    except (TypeError, KeyError, IndexError) as e:
        current_app.logger.error(f"Ollama chat request parsing error: {str(e)}")
        return jsonify({"error": f"Request parsing error: {str(e)}"}), 400

@ollama_bp.route('/api/tags', methods=['GET'])
def get_tags():
    mock_details = ModelDetails(
        format="gguf", 
        family="mock_family_py", 
        families=["mock_family_py", "another_family_py"], # Example with families list
        parameter_size="7B", 
        quantization_level="Q4_0"
    )
    mock_model_info = ModelInfo(
        name="workshop_py:latest", 
        model="workshop_py:latest", 
        modified_at=datetime.now(timezone.utc).isoformat(), # Ensure this is string
        size=123456789, 
        digest="sha256:mock_digest_py", 
        details=mock_details,
        expires_at=None, # Optional field
        size_vram=None    # Optional field
    )
    response = TagsResponse(models=[mock_model_info])
    return jsonify(asdict(response))

@ollama_bp.route('/api/version', methods=['GET'])
def get_version():
    return jsonify({"version": "0.1.0_py_converted"})

@ollama_bp.route('/', methods=['GET'])
def get_heartbeat():
    current_app.logger.info("OLLAMA_HEARTBEAT_PY")
    return jsonify({"status": "ok_py"}), 200

@ollama_bp.route('/<path:subpath>', methods=['GET', 'POST', 'PUT', 'DELETE'])
def handle_undefined_request(subpath):
    current_app.logger.warning(f"Ollama undefined path accessed: {subpath} with method {request.method}")
    return jsonify({"error": "Ollama Unprocessable Entity Py"}), 422
