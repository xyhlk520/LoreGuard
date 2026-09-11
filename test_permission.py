import unittest
from inspect_world import inspect_knowledge, load_world

SECRET_FACTS = {"devil_pact", "lockdown_purpose"}
MIRA_ORDINARY_KNOWLEDGE = {"gates_sealed"}
ROWAN_ORDINARY_KNOWLEDGE = {
                            "gates_sealed", 
                            "sickness_claim", 
                            "rowan_guard_shift",
                            "village_well",
                            "food_distribution",
                            "mira_clinic",
                            "village_market",
                            }

class TestInspectKnowledge(unittest.TestCase):
    def setUp(self):
        self.world = load_world()
        
    def get_fact_ids(self, result, category):
        return{
            entry["fact_id"] for entry in result[category]
        }

    def test_mira_before_trust(self):
        result = inspect_knowledge(self.world, 
                                   "mira", 
                                   "before_trust")

        disclosable = self.get_fact_ids(result, "disclosable")
        withheld = self.get_fact_ids(result, "withheld")

        self.assertEqual(MIRA_ORDINARY_KNOWLEDGE, disclosable)
        self.assertTrue(SECRET_FACTS.isdisjoint(disclosable))
        self.assertEqual(SECRET_FACTS, withheld)
        

    def test_mira_after_trust(self):
        result = inspect_knowledge(self.world,
                                   "mira",
                                   "after_trust")
        
        disclosable = self.get_fact_ids(result, "disclosable")
        withheld = self.get_fact_ids(result, "withheld")
        
        self.assertEqual(MIRA_ORDINARY_KNOWLEDGE|SECRET_FACTS
                         , disclosable)
        self.assertFalse(withheld)  # No withheld facts after trust

    def test_rowan_before_trust(self):
        result = inspect_knowledge(self.world,
                                   "rowan",
                                   "before_trust")
        disclosable = self.get_fact_ids(result, "disclosable")
        withheld = self.get_fact_ids(result, "withheld")

        self.assertEqual(ROWAN_ORDINARY_KNOWLEDGE, disclosable)
        self.assertTrue(SECRET_FACTS.isdisjoint(disclosable))
        self.assertFalse(withheld)

    def test_rowan_after_trust(self):
        result = inspect_knowledge(self.world,
                                   "rowan",
                                   "after_trust")
        disclosable = self.get_fact_ids(result, "disclosable")
        withheld = self.get_fact_ids(result, "withheld")

        self.assertEqual(ROWAN_ORDINARY_KNOWLEDGE, disclosable)
        self.assertTrue(SECRET_FACTS.isdisjoint(disclosable))
        self.assertFalse(withheld)

if __name__ == "__main__":
    unittest.main()