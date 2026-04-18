from flask import Blueprint, render_template, request, jsonify
from services.pipeline import IncidentPipeline

# Define the main blueprint for the application using the 'core' package
main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    """EntryPoint: Serve the main AI Analyzer UI."""
    return render_template('index.html')

@main_bp.route('/analyze', methods=['POST'])
def analyze():
    """
    Intelligence Portal: Receives incoming incident data and 
    pipes it through the Expert Analysis Pipeline.
    """
    try:
        data = request.get_json()
        if not data or 'incident' not in data:
            return jsonify({'success': False, 'error': 'No incident data provided'}), 400
        
        user_query = data['incident'].strip()
        
        # Hand off to the Unified Pipeline
        result = IncidentPipeline.analyze(user_query)
        
        return jsonify({
            'success': True,
            'data': result
        })

    except Exception as e:
        print(f"Route Execution Error: {str(e)}")
        return jsonify({
            'success': False, 
            'error': 'The system encountered an unexpected bottleneck.',
            'details': str(e)
        }), 500
