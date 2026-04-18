import time
import json
import os
from .supabase_service import SupabaseService
from .matcher_service import MatcherService
from config import Config

class LearningService:
    """
    KEDB Auto-Learning Interface: Implements production-safe knowledge maturation.
    State is managed locally to ensure high-fidelity pattern tracking before KEDB promotion.
    """

    _STATE_PATH = os.path.join(os.path.dirname(__file__), '..', 'data', 'learning_state.json')
    _KEDB_PATH = os.path.join(os.path.dirname(__file__), '..', 'data', 'kedb.json')

    @classmethod
    def _load_state(cls):
        if not os.path.exists(cls._STATE_PATH): return {}
        try:
            with open(cls._STATE_PATH, 'r') as f: return json.load(f)
        except: return {}

    @classmethod
    def _save_state(cls, state):
        os.makedirs(os.path.dirname(cls._STATE_PATH), exist_ok=True)
        with open(cls._STATE_PATH, 'w') as f: json.dump(state, f, indent=2)

    @classmethod
    def process_incident(cls, query, analysis_result):
        """
        Orchestrates the lifecycle of an incident from discovery to KEDB promotion.
        """
        if not analysis_result or not isinstance(analysis_result, dict):
            return {"status": "skipped", "reason": "invalid_analysis"}

        # Step 1: Normalize & Sign
        signature = MatcherService.generate_incident_signature(query)
        
        # Step 4: Validate Output (STRICT)
        confidence = analysis_result.get('confidence_score')
        if confidence is None:
            conf_str = str(analysis_result.get('confidence', 'Low')).lower()
            mapping = {'high': 90, 'medium': 70, 'low': 40}
            confidence = mapping.get(conf_str, 40)

        root_cause = analysis_result.get('root_cause', '')
        actions = analysis_result.get('immediate_actions', [])
        
        is_valid = (
            confidence >= (Config.LEARNING_THRESHOLD_CONFIDENCE * 100) and 
            len(root_cause) >= Config.LEARNING_MIN_ROOT_CAUSE_LENGTH and
            len(actions) >= Config.LEARNING_MIN_ACTIONS_COUNT
        )

        # Step 2: Global Archive (Cloud Discovery) - Always archive to Supabase
        SupabaseService.archive_new_discovery(
            issue=query,
            root_cause=root_cause,
            resolution=analysis_result.get('resolution_steps', ["N/A"])[0] if analysis_result.get('resolution_steps') else "N/A",
            tags=list(MatcherService.extract_keywords(query))[:5]
        )

        if not is_valid:
            return {"status": "archived", "reason": "quality_threshold_not_met", "signature": signature}

        # Step 5: Frequency Tracking (Local State Management)
        state = cls._load_state()
        entry = state.get(signature, {
            "frequency": 0,
            "root_cause": root_cause,
            "promoted": False,
            "first_seen": time.strftime('%Y-%m-%dT%H:%M:%SZ')
        })
        
        entry["frequency"] += 1
        entry["last_seen"] = time.strftime('%Y-%m-%dT%H:%M:%SZ')
        
        # Step 8: Duplicate Protection (Minimal version: update existing pattern)
        entry["root_cause"] = root_cause 
        state[signature] = entry
        cls._save_state(state)

        # Step 6 & 7: Promotion to KEDB (Local Gold Standard)
        if entry["frequency"] >= Config.LEARNING_THRESHOLD_FREQUENCY and not entry["promoted"]:
            cls._promote_to_local_kedb(query, analysis_result)
            entry["promoted"] = True
            cls._save_state(state)
            return {"status": "promoted", "signature": signature, "frequency": entry["frequency"]}

        return {"status": "tracked", "signature": signature, "frequency": entry["frequency"]}

    @classmethod
    def _promote_to_local_kedb(cls, query, analysis):
        """Appends high-quality resolution to the local Gold Standard KEDB."""
        if not os.path.exists(cls._KEDB_PATH):
            kedb = []
        else:
            try:
                with open(cls._KEDB_PATH, 'r') as f: kedb = json.load(f)
            except: kedb = []

        new_entry = {
            "issue": query,
            "root_cause": analysis.get('root_cause', ''),
            "resolution": analysis.get('resolution_steps', ["N/A"])[0] if analysis.get('resolution_steps') else "N/A",
            "tags": list(MatcherService.extract_keywords(query))[:5]
        }
        
        # Avoid exact duplicates in KEDB
        if not any(e.get('root_cause') == new_entry['root_cause'] for e in kedb):
            kedb.append(new_entry)
            with open(cls._KEDB_PATH, 'w') as f: json.dump(kedb, f, indent=2)
