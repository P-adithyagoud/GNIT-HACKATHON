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
    Main Intelligence Pipeline:
    Input (User Logs) -> Retrieval (KEDB + Cloud) -> Correlation -> Analysis (LLM) -> Insight.
    """
    try:
        # 1. Parse Input
        request_input = request.get_json()
        if not request_input or 'incident' not in request_input:
            return jsonify({'success': False, 'error': 'No incident payload detected.'}), 400
        
        current_query = request_input['incident'].strip()
        print(f"\n[SYSTEM] Received incident report: {current_query[:50]}...")

        # 2. Knowledge Base Retrieval (Hybrid Local KEDB + Cloud Supabase Archive)
        print("[DATABASE] Accessing Hybrid Knowledge Base (KEDB + Cloud Archive)...")
        local_kedb = KEDBService.find_known_errors()
        cloud_history = SupabaseService.fetch_historical_incidents()
        hybrid_knowledge = local_kedb + cloud_history
        
        # 3. Correlation & KEDB Matching
        print("[MATCHER] Correlating current report against KEDB entries...")
        top_matches = MatcherService.rank_correlated_knowledge(current_query, hybrid_knowledge)
        confidence_level = MatcherService.identify_confidence(len(top_matches))
        print(f"[RESULT] Match complete. KEDB Correlation: {confidence_level}")

        # 4. Expert AI Analysis (Groq Pipeline)
        print("[AI EXPERT] Consulting SRE Knowledge Engine (Mixtral 8x7B)...")
        expert_output_raw = AIService.generate_resolution_analysis(current_query, top_matches)
        
        # 5. Structure & Sanitize Response
        result_payload = ResponseParser.parse_json(expert_output_raw)
        
        if not result_payload:
            print("[WARNING] AI response format unexpected. Deploying safety fallback.")
            result_payload = Config.FALLBACK_RESPONSE.copy()
            result_payload["is_fallback"] = True
            
        # Enrich payload for Frontend
        result_payload['confidence'] = confidence_level
        result_payload['similar_incidents'] = top_matches

        # 6. Archive Discovery (Post-Analysis Learning)
        print("[LEARNING] Archiving new analysis into knowledge base for future maturity...")
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
    # Local development entry point
    app.run(debug=True, port=5000)
