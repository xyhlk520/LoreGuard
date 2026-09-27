from google import genai
from google.genai import types
from action import execute_tool
from utils import load_data
import os

init_state = load_data("init_player_state.json")
agent_tools = types.Tool(
    function_declarations=[
        types.FunctionDeclaration(
            name="get_inventory",
            description=(
                "Return the player's current items and quantities. "
                "Does not change state."
            ),
        ),
        types.FunctionDeclaration(
            name="get_quest_status",
            description=(
                "Return whether Mira's herb quest is completed, "
                "the required item and amount, and the target NPC. "
                "Does not change state."
            ),
        ),
        types.FunctionDeclaration(
            name="deliver_herbs",
            description=(
                "Attempt to deliver three healing herbs to the current NPC. "
                "On success, consume the herbs and complete Mira's trust quest. "
                "Use only when the player requests delivery. "
                "Do not use for questions or hypothetical statements."
            ),
        ),
    ]
)

def inspect_tool_choice(client, query, model_name="gemini-3.8-flash"):
        response = client.models.generate_content(
        model=model_name,
        contents=[genai.types.Content(role="user", parts=[genai.types.Part(text=query)])],
        config = genai.types.GenerateContentConfig(
            max_output_tokens=512,
            tools=[agent_tools]
        )
    )
        if response.function_calls:
            for call in response.function_calls:
                print("Tool name:", call.name)
                print("Arguments:", call.args)
        else:
            print("reply:", response.text)

def run_agent(client, query, player_state, npc_id, model_name="gemini-3.8-flash"):
        contents = [types.Content(
             role = "user",
             parts = [types.Part(text=query)]
        )]

        for step in range(5):
            response = client.models.generate_content(
            model=model_name,
            contents=contents,
            config = genai.types.GenerateContentConfig(
                max_output_tokens=512,
                tools=[agent_tools]
            ))
            if response.function_calls:
                contents.append(response.candidates[0].content)
                response_parts = []
                for call in response.function_calls:
                    result = execute_tool(call.name, player_state, npc_id)
                    response_part = types.Part(
                        function_response=types.FunctionResponse(
                            id=call.id,
                            name=call.name,
                            response=result
                        )
                    )
                    response_parts.append(response_part)
                contents.append(types.Content(
                    role="user",
                    parts=response_parts
                ))
            else:
                 return response.text or "No valid response received"
            
        return "Step limit reached; no final reply was generated."
                  

if __name__ == "__main__":
    api_key = os.environ.get("GEMINI_API_KEY")

    if not api_key:
        raise RuntimeError(
            "Set GEMINI_API_KEY in this terminal before running."
        )

    npc_id = "rowan"
    state_id = "before_trust"

    with genai.Client(api_key=api_key) as client:
         result = run_agent(client, "what quest do I have, what do I need to complete the quest, what do I have now in my bag", init_state, "mira")
         print(result)

