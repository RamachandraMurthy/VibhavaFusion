import json
import requests
from datetime import datetime, timedelta
from ..utils.ai_config import ai_config
from flask import current_app
from app.utils.log_manager import log_manager

class AIService:
    """Service class for handling AI operations and monitoring."""
    
    def __init__(self):
        self.config = ai_config
        self.request_history = []
        self.error_history = []
        
    def check_api_status(self):
        """Check the API connection and model availability."""
        try:
            # Basic API health check
            headers = self.config.headers
            response = requests.get(
                "https://api.openai.com/v1/models",
                headers=headers
            )
            
            if response.status_code == 200:
                models = response.json()
                # Verify our models are available
                available_models = [model['id'] for model in models['data']]
                required_models = [self.config.text_model, self.config.audio_model]
                
                status = {
                    'api_connected': True,
                    'models_available': all(model in available_models for model in required_models),
                    'timestamp': datetime.now().isoformat()
                }
            else:
                status = {
                    'api_connected': False,
                    'error': f"API returned status code: {response.status_code}",
                    'timestamp': datetime.now().isoformat()
                }
        except Exception as e:
            status = {
                'api_connected': False,
                'error': str(e),
                'timestamp': datetime.now().isoformat()
            }
            
        return status
    
    def get_usage_stats(self, timeframe='1h'):
        """Get usage statistics for the specified timeframe."""
        now = datetime.now()
        if timeframe == '1h':
            start_time = now - timedelta(hours=1)
        elif timeframe == '24h':
            start_time = now - timedelta(days=1)
        elif timeframe == '7d':
            start_time = now - timedelta(days=7)
        else:
            raise ValueError(f"Invalid timeframe: {timeframe}")
            
        # Filter request history by timeframe
        relevant_requests = [
            req for req in self.request_history 
            if req['timestamp'] >= start_time
        ]
        
        # Calculate statistics
        total_requests = len(relevant_requests)
        total_tokens = sum(req.get('tokens', 0) for req in relevant_requests)
        total_errors = len([
            err for err in self.error_history 
            if err['timestamp'] >= start_time
        ])
        
        return {
            'timeframe': timeframe,
            'total_requests': total_requests,
            'total_tokens': total_tokens,
            'total_errors': total_errors,
            'estimated_cost': total_tokens * self.config.cost_per_token
        }
    
    def log_request(self, request_type, tokens=0, metadata=None):
        """Log an API request for monitoring."""
        self.request_history.append({
            'timestamp': datetime.now(),
            'type': request_type,
            'tokens': tokens,
            'metadata': metadata or {}
        })
        
        # Trim history if too long
        if len(self.request_history) > 1000:
            self.request_history = self.request_history[-1000:]
    
    def log_error(self, error_type, message, metadata=None):
        """Log an error for monitoring.
        
        Args:
            error_type (str): Type of error (e.g., 'API Error', 'Validation Error')
            message (str): Error message
            metadata (dict, optional): Additional error context
        """
        error = {
            'timestamp': datetime.now(),
            'type': error_type,
            'message': message,
            'metadata': metadata or {}
        }
        
        # Add to error history
        self.error_history.append(error)
        
        # Trim history if too long
        if len(self.error_history) > 100:
            self.error_history = self.error_history[-100:]
        
        # Log to application logger
        log_manager.logger.error(
            f"AI Service Error - {error_type}: {message}",
            extra={'metadata': metadata} if metadata else None
        )

    def generate_chat_response(self, messages, context=None):
        """Generate a chat response using the OpenAI API.
        
        Args:
            messages (list): List of message dictionaries with 'role' and 'content'
            context (dict, optional): Additional context for the conversation
            
        Returns:
            dict: The API response containing the generated message
        """
        try:
            # TODO: Implement actual API call
            log_manager.logger.info(
                "Generating chat response",
                extra={
                    'message_count': len(messages),
                    'context': context
                }
            )
            return {
                'role': 'assistant',
                'content': 'This is a placeholder response.'
            }
        except Exception as e:
            self.log_error(
                'API Error',
                str(e),
                metadata={
                    'message_count': len(messages),
                    'context': context
                }
            )
            raise

# Create a singleton instance
ai_service = AIService() 