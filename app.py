from flask import Flask, render_template, request, jsonify
from config import Config
from services.supabase_service import SupabaseService
from services.matcher_service import MatcherService
from services.ai_service import AIService
from services.parser import ResponseParser
import json

app = Flask(__name__, template_folder='templates', static_folder='static')

@app.route('/')
def index():
    """Serve the frontend."""
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    """
    STRICT SYSTEM FLOW:
    1. Receive user input
    2. Fetch incidents from Supabase
    3. Similarity matching in backend
    4. Select top 3 matched incidents
    5. Determine confidence level
    6. Send query + matches to LLM
    7. LLM generates structured response
    8. Store new incident in Supabase
    9. Return response to user
    """
    try:
        data = request.get_json()
        if not data or 'incident' not in data:
            return jsonify({'error': 'Missing incident description'}), 400
        
        user_query = data['incident'].strip()
        
        # 2. Fetch incidents from Supabase
        all_past_incidents = SupabaseService.get_all_incidents()
        
        # 3 & 4. Similarity matching & Select top 3
        top_matches = MatcherService.rank_incidents(user_query, all_past_incidents, top_n=3)
        
        # 5. Determine confidence level
        confidence = MatcherService.determine_confidence(len(top_matches))
        
        # 6 & 7. Send to LLM & Generate structured response
        api_response = AIService.analyze_incident(user_query, top_matches)
        
        if api_response:
            parsed_result = ResponseParser.parse_json(api_response)
            if parsed_result:
                # Inject similarity matching results into the final response
                parsed_result['confidence'] = confidence
                parsed_result['similar_incidents'] = [
                    {
                        "issue": inc.get('issue'),
                        "root_cause": inc.get('root_cause'),
                        "resolution": inc.get('resolution')
                    } for inc in top_matches
                ]
                
                # 8. Store new incident in Supabase (async-like or post-analysis)
                # Using data from AI analysis for future learning
                SupabaseService.store_incident(
                    issue=user_query,
                    root_cause=parsed_result.get('root_cause', 'Unknown'),
                    resolution=parsed_result.get('resolution_steps', ['N/A'])[0] if parsed_result.get('resolution_steps') else 'N/A'
                )
                
                # 9. Return response to user
                return jsonify({
                    'success': True,
                    'data': parsed_result
                })

        # Fallback if anything fails
        fallback = Config.FALLBACK_RESPONSE.copy()
        fallback['confidence'] = confidence
        return jsonify({
            'success': True,
            'data': fallback,
            'fallback': True
        })

    except Exception as e:
        print(f"System Error: {str(e)}")
        return jsonify({'error': 'Internal system error', 'details': str(e)}), 500

@app.errorhandler(404)
def not_found(e):
    return jsonify({'error': 'Not found'}), 404

@app.errorhandler(500)
def server_error(e):
    return jsonify({'error': 'Server error'}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
