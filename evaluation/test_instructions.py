import unittest
from inspect_world import inspect_knowledge, load_world
from generation import build_messages

disclosure_instruction = (
    "Answer using the supplied evidence. "
    "If it does not support an answer, express uncertainty."
)

class TestInspectKnowledge(unittest.TestCase):
    def setUp(self):
        self.world = load_world()
        self.query = "Why are the village gates sealed?"
        
    def get_fact_ids(self, result, category):
        return{
            entry["fact_id"] for entry in result[category]
        }

    def test_mira_before_trust(self):
        result = inspect_knowledge(self.world,
                                   "mira",
                                   "before_trust")
        
        evidence = result["disclosable"][0:2]  # Use the first two disclosable facts as evidence
        messages = build_messages(self.world, "mira", "before_trust", self.query, evidence)
        system_content = None

        for message in messages:
            if message["role"] == "system":
                system_content = message["content"]
                break

       #Assure special instruction is not included
        self.assertIsNotNone(system_content)
        self.assertIn(self.world["characters"]["mira"]["disclosure_rules"][0]["instruction"], 
        system_content)
        self.assertIn(disclosure_instruction, system_content)
        

    def test_mira_after_trust(self):
        result = inspect_knowledge(self.world,
                                   "mira",
                                   "after_trust")
        
        evidence = result["disclosable"][0:2]  # Use the first two disclosable facts as evidence
        messages = build_messages(self.world, "mira", "after_trust", self.query, evidence)
        system_content = None

        for message in messages:
            if message["role"] == "system":
                system_content = message["content"]
                break

       # Check that the system prompt includes the disclosure instruction and does not include the specific disclosure rule for Mira
        self.assertIsNotNone(system_content)
        self.assertNotIn(self.world["characters"]["mira"]["disclosure_rules"][0]["instruction"], 
        system_content)
        self.assertIn(disclosure_instruction, system_content)


    def test_rowan_before_trust(self):
        result = inspect_knowledge(self.world,
                                   "rowan",
                                   "before_trust")
        
        evidence = result["disclosable"][0:2]  # Use the first two disclosable facts as evidence
        messages = build_messages(self.world, "rowan", "before_trust", self.query, evidence)
        system_content = None

        for message in messages:
            if message["role"] == "system":
                system_content = message["content"]
                break

       #Assure common instruction is included and mira's instruction won't appear
        self.assertIsNotNone(system_content)
        self.assertIn(disclosure_instruction, system_content)
        self.assertNotIn(self.worldself.world["characters"]["mira"]["disclosure_rules"][0]["instruction"],
                         system_content)
      

    def test_rowan_after_trust(self):
        pass

if __name__ == "__main__":
    unittest.main()