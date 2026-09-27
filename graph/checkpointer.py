import time
from typing import Dict, Any, Optional, List
from graph.state import PollutionState

class MemoryCheckpointer:
    """In-memory state checkpointer for agent session history and memory persistence."""

    def __init__(self):
        self.sessions: Dict[str, PollutionState] = {}
        self.history: Dict[str, List[Dict[str, Any]]] = {}

    def save_checkpoint(self, state: PollutionState):
        self.sessions[state.session_id] = state.model_copy(deep=True)
        if state.session_id not in self.history:
            self.history[state.session_id] = []
        
        self.history[state.session_id].append({
            "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ"),
            "user_query": state.user_query,
            "location": state.location,
            "aqi": state.aqi,
            "category": state.category,
            "answer": state.final_response.get("answer", "")
        })

    def get_checkpoint(self, session_id: str) -> Optional[PollutionState]:
        return self.sessions.get(session_id)

    def get_history(self, session_id: str) -> List[Dict[str, Any]]:
        return self.history.get(session_id, [])
