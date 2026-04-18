from flask import Flask, render_template, request, jsonify
from config import Config
from services.supabase_service import SupabaseService
from services.matcher_service import MatcherService
from services.ai_service import AIService
from services.parser import ResponseParser
from services.kedb_service import KEDBService
import os

# Application Entry Point
app = Flask(__name__)

@app.route('/')
def index():
    """Serves the SRE AI Analysis Dashboard."""
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    """
    Intelligence Pipeline:
    Input -> Retrieval (3 KEDB + 3 Supabase) -> AI Re-ranking -> Insight.
    """
    try:
        # 1. Parse Input
        request_input = request.get_json()
        if not request_input or 'incident' not in request_input:
            return jsonify({'success': False, 'error': 'No incident payload detected.'}), 400
        
        current_query = request_input['incident'].strip()
        print(f"\n[SYSTEM] Received incident report: {current_query[:50]}...")

        # 2. Hybrid Retrieval (3 Local KEDB + 3 Cloud Archive)
        print("[DATABASE] Fetching candidates from KEDB and Cloud Archive...")
        local_db = KEDBService.find_known_errors()
        cloud_db = SupabaseService.fetch_historical_incidents()
        
        # Get top 3 from each source to give AI a rich but manageable candidate pool
        local_candidates = MatcherService.rank_correlated_knowledge(current_query, local_db, top_n=3)
        cloud_candidates = MatcherService.rank_correlated_knowledge(current_query, cloud_db, top_n=3)
        candidate_pool = local_candidates + cloud_candidates

        # 3. AI Analysis & Re-ranking
        print(f"[AI EXPERT] Analyzing {len(candidate_pool)} candidate cases for best fit...")
        expert_output_raw = AIService.generate_resolution_analysis(current_query, candidate_pool)
        
        # 4. Structure & Sanitize Response
        result_payload = ResponseParser.parse_json(expert_output_raw)
        
        if not result_payload:
            print("[WARNING] AI response format failed. Triggering recovery fallback.")
            result_payload = Config.FALLBACK_RESPONSE.copy()
            result_payload["is_fallback"] = True
            
        # Ensure confidence level is calculated based on AI determination or local counts
        if 'confidence' not in result_payload:
            result_payload['confidence'] = MatcherService.identify_confidence(len(candidate_pool))

        # 5. Archive Discovery
        print("[LEARNING] Archiving session to cloud for continuous maturity...")
        SupabaseService.archive_new_discovery(
            issue=current_query,
            root_cause=result_payload.get('root_cause', 'Under Investigation'),
            resolution=result_payload.get('resolution_steps', ['N/A'])[0] if result_payload.get('resolution_steps') else 'N/A'
        )

        print("[SUCCESS] Intelligence delivery successful.\n")
        return jsonify({'success': True, 'data': result_payload})

    except Exception as e:
        print(f"[ERROR] Pipeline Exception: {str(e)}")
        return jsonify({'success': False, 'error': 'Internal pipeline encountered a bottleneck.'}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
