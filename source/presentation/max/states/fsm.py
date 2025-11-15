from enum import Enum
from typing import Dict, Any, Optional

class UserState(Enum):
    IDLE = "idle"
    CHOOSING_CATEGORY = "choosing_category"
    ENTERING_FREQUENCY = "entering_frequency"
    EDITING_PROFILE = "editing_profile"
    DONATING_CATEGORY = "donating_category"
    SELECTING_ADVERT = "selecting_advert"
    ENTERED_ADVERT = "entered_advert"
    DONATION_ENTERING_AMOUNT = "donation_entering_amount"
    FUND_CHOOSING_CATEGORY = "fund_choosing_category"
    FUND_ENTERING_AMOUNT = "fund_entering_amount" 
    FUND_ENTERING_FREQUENCY = "fund_entering_frequency"
    EDITING_BIRTH_DATE = "editing_birth_date"
    EDITING_INTERESTS = "editing_interests"

class FSM:
    def __init__(self):
        self.states: Dict[int, Dict[str, Any]] = {}
    
    async def get_state(self, user_id: int) -> Optional[UserState]:
        return self.states.get(user_id, {}).get("state")
    
    async def set_state(self, user_id: int, state: UserState, data: Optional[Dict] = None):
        self.states[user_id] = {"state": state, "data": data or {}}
    
    async def clear_state(self, user_id: int):
        self.states.pop(user_id, None)

fsm = FSM()