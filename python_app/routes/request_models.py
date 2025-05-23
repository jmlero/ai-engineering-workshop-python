from dataclasses import dataclass, field
from typing import Optional, List, Dict, Any
from datetime import datetime

@dataclass
class CurlChatRequest:
    message: str

@dataclass
class OllamaToolCallFunction:
    name: str
    arguments: Dict[str, Any]

@dataclass
class OllamaToolCall:
    function: OllamaToolCallFunction

@dataclass
class OllamaMessage:
    role: str
    content: str
    images: Optional[List[str]] = None
    tool_calls: Optional[List[OllamaToolCall]] = field(default_factory=list)

@dataclass
class OllamaChatOptions:
    temperature: Optional[float] = None # Changed to float for temperature

@dataclass
class OllamaChatRequest:
    model: str # model is usually required
    messages: List[OllamaMessage] = field(default_factory=list)
    stream: Optional[bool] = False
    options: Optional[OllamaChatOptions] = None
    # Added format and keep_alive based on Ollama docs for more complete request
    format: Optional[str] = None # e.g., "json"
    keep_alive: Optional[str] = None # e.g., "5m"


@dataclass
class OllamaChatResponse:
    model: str
    created_at: str # Changed to string for easier JSON serialization
    message: OllamaMessage
    done: bool
    done_reason: Optional[str] = None # Added based on common API patterns, can be null
    total_duration: Optional[int] = None
    load_duration: Optional[int] = None
    prompt_eval_count: Optional[int] = None
    prompt_eval_duration: Optional[int] = None
    eval_count: Optional[int] = None
    eval_duration: Optional[int] = None

@dataclass
class ModelDetails:
    format: str
    family: str
    families: Optional[List[str]] = None # Added based on Ollama /tags response
    parameter_size: str
    quantization_level: str

@dataclass
class ModelInfo:
    name: str
    model: str # This is often same as name, or more specific model id
    modified_at: str # Changed to string for easier JSON serialization
    size: int
    digest: str
    details: ModelDetails
    # Added based on Ollama /tags response
    expires_at: Optional[datetime] = None
    size_vram: Optional[int] = None


@dataclass
class TagsResponse:
    models: List[ModelInfo]
