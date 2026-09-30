from utils import load_data
from inspect_world import load_world

world = load_world()
init_state = load_data("init_player_state.json")
def deliver_herbs(player_state, npc_id):
    if(npc_id == "mira"):
        if "earn_miras_trust" not in player_state["completed_quests"]:
            herb_amt = player_state["inventory"].get("healing_herb", 0)
            if(herb_amt >= 3):
                player_state["inventory"]["healing_herb"] = herb_amt - 3
                player_state["completed_quests"].append("earn_miras_trust")
                return{
                    "success": True,
                    "reason": "completed"
                }
            else:
                return{
                    "success": False,
                    "reason": "insufficient_items"
                }
        else:
            return{
                "success": False,
                "reason": "duplicate_submission"
                }
    else:
        return{
            "success": False,
            "reason": "wrong_npc"
        }

def get_inventory(player_state):
    return player_state["inventory"].copy()

def get_quest_status(player_state):
    return {
    "quest_id": "earn_miras_trust",
    "completed": "earn_miras_trust" in player_state["completed_quests"],
    "required_item": "healing_herb",
    "required_amount": 3,
    "target_npc": "mira"
}

def execute_tool(tool_name, player_state, npc_id):
    if tool_name == "deliver_herbs":
        return deliver_herbs(player_state, npc_id)
    if tool_name == "get_inventory":
        return get_inventory(player_state)
    if tool_name == "get_quest_status":
        return get_quest_status(player_state)
    else:
        return{
            "success": False,
            "reason": "unknown_tool"
        }

if __name__ == "__main__":
    result = execute_tool("deliver_herbs", init_state, "mira")
    print(result)