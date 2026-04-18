from flask import Flask, render_template, request, jsonify
from config import Config
from services.supabase_service import SupabaseService
from services.matcher_service import MatcherService
from services.ai_service import AIService
from services.parser import ResponseParser
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    try:
        data = request.get_json()
        if not data or 'incident' not in data:
            return jsonify({'success': False, 'error': 'Missing input'}), 400
        
        user_query = data['incident'].strip()
        
        # 1. Fetch
        history = SupabaseService.get_all_incidents()
        # 2. Match
        matches = MatcherService.rank_incidents(user_query, history)
        confidence = MatcherService.determine_confidence(len(matches))
        # 3. AI Analysis
        raw_res = AIService.analyze_incident(user_query, matches)
        # 4. Parse
        result = ResponseParser.parse_json(raw_res)
        
        if not result:
            result = Config.FALLBACK_RESPONSE.copy()
            result["is_fallback"] = True
            
        result['confidence'] = confidence
        result['similar_incidents'] = matches

        # 5. Store
        SupabaseService.store_incident(
            issue=user_query,
            root_cause=result.get('root_cause', 'N/A'),
            resolution=result.get('resolution_steps', ['N/A'])[0] if result.get('resolution_steps') else 'N/A'
        )

        return jsonify({'success': True, 'data': result})

    except Exception as e:
        print(f"Server Error: {str(e)}")
        return jsonify({'success': False, 'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
