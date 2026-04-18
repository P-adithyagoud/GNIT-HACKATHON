from flask import Flask, render_template, request, jsonify
import json
import os
from dotenv import load_dotenv
import httpx

load_dotenv()

app = Flask(__name__, template_folder='templates', static_folder='static')

GROQ_API_KEY = os.getenv('GROQ_API_KEY')
GROQ_API_URL = 'https://api.groq.com/openai/v1/chat/completions'

SYSTEM_PROMPT = """You are a senior Site Reliability Engineer with deep experience in production outages.
Analyze the following incident and return ONLY valid JSON. No markdown, no explanations outside JSON.
Each list must contain concise, actionable items. Avoid generic advice.

Return this exact JSON format:
{
  "root_causes": ["cause1", "cause2"],
  "resolution_steps": ["step1", "step2"],
  "priority_actions": {
    "immediate": ["action1", "action2"],
    "short_term": ["action1", "action2"],
    "long_term": ["action1", "action2"]
  },
  "confidence": "High"
}

confidence must be: "High", "Medium", or "Low"
All lists must have at least 2 items.
Be specific, not generic."""

FALLBACK_RESPONSE = {
    "root_causes": [
        "Unable to determine from provided information",
        "Retry analysis with more detailed logs"
    ],
    "resolution_steps": [
        "Review application logs for error patterns",
        "Check system resource usage (CPU, memory, disk)",
        "Inspect recent deployment changes",
        "Verify external service dependencies"
    ],
    "priority_actions": {
        "immediate": [
            "Stabilize affected services",
            "Alert incident response team"
        ],
        "short_term": [
            "Root cause analysis",
            "Temporary mitigation if needed"
        ],
        "long_term": [
            "Implement monitoring for this issue",
            "Post-incident review and documentation"
        ]
    },
    "confidence": "Low"
}


def validate_input(incident):
    """Validate incident input."""
    if not incident or not isinstance(incident, str):
        return False, "Incident must be a non-empty string"
    
    incident = incident.strip()
    
    if len(incident) < 10:
        return False, "Incident description too short (min 10 characters)"
    
    if len(incident) > 3000:
        return False, "Incident description too long (max 3000 characters)"
    
    return True, None


def parse_json_response(response_text):
    """Attempt to parse JSON from response."""
    try:
        data = json.loads(response_text)
        
        if not isinstance(data, dict):
            return None
        
        required_keys = ['root_causes', 'resolution_steps', 'priority_actions', 'confidence']
        if not all(key in data for key in required_keys):
            return None
        
        if not isinstance(data['root_causes'], list) or len(data['root_causes']) < 1:
            return None
        
        if not isinstance(data['resolution_steps'], list) or len(data['resolution_steps']) < 1:
            return None
        
        if not isinstance(data['priority_actions'], dict):
            return None
        
        if data['confidence'] not in ['High', 'Medium', 'Low']:
            return None
        
        return data
    
    except (json.JSONDecodeError, ValueError, TypeError):
        return None


def call_groq_api(incident):
    """Call Groq API with incident."""
    if not GROQ_API_KEY:
        return None
    
    try:
        with httpx.Client(timeout=5.0) as client:
            response = client.post(
                GROQ_API_URL,
                headers={
                    'Authorization': f'Bearer {GROQ_API_KEY}',
                    'Content-Type': 'application/json'
                },
                json={
                    'model': 'mixtral-8x7b-32768',
                    'messages': [
                        {
                            'role': 'system',
                            'content': SYSTEM_PROMPT
                        },
                        {
                            'role': 'user',
                            'content': f"Incident:\n{incident}"
                        }
                    ],
                    'temperature': 0.2,
                    'max_tokens': 500
                }
            )
            
            if response.status_code == 200:
                data = response.json()
                if 'choices' in data and len(data['choices']) > 0:
                    return data['choices'][0]['message']['content']
            
            return None
    
    except Exception as e:
        print(f"API Error: {str(e)}")
        return None


@app.route('/')
def index():
    """Serve the frontend."""
    return render_template('index.html')


@app.route('/analyze', methods=['POST'])
def analyze():
    """Analyze incident using Groq API."""
    data = request.get_json()
    
    if not data or 'incident' not in data:
        return jsonify({'error': 'Missing incident description'}), 400
    
    incident = data['incident'].strip()
    
    valid, error_msg = validate_input(incident)
    if not valid:
        return jsonify({'error': error_msg}), 400
    
    api_response = call_groq_api(incident)
    
    if api_response:
        parsed = parse_json_response(api_response)
        if parsed:
            return jsonify({
                'success': True,
                'data': parsed
            })
    
    return jsonify({
        'success': True,
        'data': FALLBACK_RESPONSE,
        'fallback': True
    })


@app.errorhandler(404)
def not_found(e):
    return jsonify({'error': 'Not found'}), 404


@app.errorhandler(500)
def server_error(e):
    return jsonify({'error': 'Server error'}), 500


if __name__ == '__main__':
    app.run(debug=True, port=5000)
