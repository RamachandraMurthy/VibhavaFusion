from flask import Blueprint, render_template, jsonify, current_app
from flask_login import login_required
from ..services.ai_service import ai_service
from ..utils.ai_config import ai_config

bp = Blueprint('ai_console', __name__, url_prefix='/ai-console')

@bp.route('/')
@login_required
def index():
    """AI Console dashboard."""
    return render_template('ai_console/index.html',
                         api_status=ai_service.check_api_status(),
                         usage_stats=ai_service.get_usage_stats('24h'))

@bp.route('/api-status')
@login_required
def api_status():
    """Get current API status."""
    return jsonify(ai_service.check_api_status())

@bp.route('/usage-stats/<timeframe>')
@login_required
def usage_stats(timeframe):
    """Get usage statistics for the specified timeframe."""
    try:
        stats = ai_service.get_usage_stats(timeframe)
        return jsonify(stats)
    except ValueError as e:
        return jsonify({'error': str(e)}), 400

@bp.route('/model-config')
@login_required
def model_config():
    """Get current model configurations."""
    return jsonify({
        'text_model': ai_config.get_model_config('text'),
        'audio_model': ai_config.get_model_config('audio')
    })

@bp.route('/error-log')
@login_required
def error_log():
    """Get recent error logs."""
    return jsonify({
        'errors': ai_service.error_history[-50:] # Last 50 errors
    }) 