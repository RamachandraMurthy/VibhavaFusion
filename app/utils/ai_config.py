import os
from dotenv import load_dotenv

class AIConfig:
    """Configuration class for AI-related settings and validation."""
    
    def __init__(self):
        load_dotenv()
        self.api_key = os.getenv('OPENAI_API_KEY')
        self.validate_config()
        
        # Model configurations
        self.text_model = "gpt-4o-mini-2024-07-18"
        self.audio_model = "gpt-4o-mini-audio-preview-2024-12-17"
        
        # Context window settings
        self.max_context_tokens = 128000
        self.max_output_tokens = 16384
        
        # Rate limiting and monitoring
        self.requests_per_minute = 50  # Adjustable based on API limits
        self.cost_per_token = 0.0001  # Update with actual cost
        
    def validate_config(self):
        """Validate the configuration settings."""
        if not self.api_key:
            raise ValueError("OpenAI API key not found in environment variables")
        
        if not self.api_key.startswith('sk-proj-'):
            raise ValueError("Invalid OpenAI API key format")
    
    @property
    def headers(self):
        """Get the headers for API requests."""
        return {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
    
    def get_model_config(self, model_type='text'):
        """Get configuration for specific model type."""
        if model_type == 'text':
            return {
                'model': self.text_model,
                'max_tokens': self.max_output_tokens,
                'context_window': self.max_context_tokens
            }
        elif model_type == 'audio':
            return {
                'model': self.audio_model,
                'max_tokens': self.max_output_tokens,
                'context_window': self.max_context_tokens
            }
        else:
            raise ValueError(f"Unknown model type: {model_type}")

# Create a singleton instance
ai_config = AIConfig() 