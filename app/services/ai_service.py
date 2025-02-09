import json
import requests
from datetime import datetime, timedelta
from ..utils.ai_config import ai_config
from flask import current_app
import logging

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
        """Log an error for monitoring."""
        self.error_history.append({
            'timestamp': datetime.now(),
            'type': error_type,
            'message': message,
            'metadata': metadata or {}
        })
        
        # Trim history if too long
        if len(self.error_history) > 100:
            self.error_history = self.error_history[-100:]
        
        # Log to application logger as well
        logging.error(f"AI Service Error - {error_type}: {message}")

    def generate_chat_response(self, messages, context=None):
        """Generate a chat response using the OpenAI API.
        
        Args:
            messages (list): List of message dictionaries with 'role' and 'content'
            context (dict, optional): Additional context for the conversation
            
        Returns:
            dict: The API response containing the generated message
        """
        try:
            # Prepare the API request
            headers = self.config.headers
            data = {
                'model': self.config.text_model,
                'messages': messages,
                'max_tokens': self.config.max_output_tokens,
                'temperature': 0.7,
                'top_p': 1.0,
                'frequency_penalty': 0.0,
                'presence_penalty': 0.0
            }
            
            # Add context if provided
            if context:
                system_message = messages[0] if messages and messages[0]['role'] == 'system' else None
                if system_message:
                    system_message['content'] += f"\nContext: {json.dumps(context)}"
                else:
                    messages.insert(0, {
                        'role': 'system',
                        'content': f"Context: {json.dumps(context)}"
                    })
                data['messages'] = messages
            
            # Make the API call
            response = requests.post(
                'https://api.openai.com/v1/chat/completions',
                headers=headers,
                json=data
            )
            
            if response.status_code == 200:
                result = response.json()
                # Log the request
                self.log_request(
                    'chat_completion',
                    tokens=result.get('usage', {}).get('total_tokens', 0),
                    metadata={'model': self.config.text_model}
                )
                return result
            else:
                error_msg = f"OpenAI API error: {response.status_code} - {response.text}"
                self.log_error('api_error', error_msg)
                raise Exception(error_msg)
                
        except Exception as e:
            error_msg = f"Error generating chat response: {str(e)}"
            self.log_error('chat_error', error_msg)
            raise

# Create a singleton instance
ai_service = AIService() 