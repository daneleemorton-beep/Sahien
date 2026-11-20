import copy
import json
import unittest
from pathlib import Path

from sahien import evaluate

EXAMPLES = Path(__file__).resolve().parents[1] / "examples"


def example(name="partnership"):
    return json.loads((EXAMPLES / f"{name}.json").read_text())


class SahienTests(unittest.TestCase):
    def test_partnership(self):
        self.assertEqual(evaluate(example())["recommendation"], "proceed")

    def test_coercion(self):
        self.assertEqual(evaluate(example("coercion"))["recommendation"], "redesign")

    def test_uncertainty(self):
        self.assertEqual(evaluate(example("uncertainty"))["recommendation"], "review")

    def test_incomplete(self):
        self.assertEqual(evaluate({})["recommendation"], "review")

    def test_missing_rationale(self):
        p = example(); p["assessments"]["autonomy_respected"]["rationale"] = ""
        self.assertEqual(evaluate(p)["recommendation"], "review")

    def test_harm_without_rationale_still_blocks(self):
        p = example(); p["assessments"]["serious_unjustified_harm"] = {"value": "yes"}
        self.assertEqual(evaluate(p)["recommendation"], "redesign")

    def test_cannot_waive_coercion(self):
        p = example(); p["assessments"]["coercion_or_manipulation"]["value"] = "not_applicable"
        self.assertEqual(evaluate(p)["recommendation"], "review")

    def test_disagreement(self):
        p = example(); p["material_disagreement"] = "yes"
        self.assertEqual(evaluate(p)["recommendation"], "review")

    def test_bad_value(self):
        p = example(); p["assessments"]["autonomy_respected"]["value"] = True
        self.assertEqual(evaluate(p)["recommendation"], "review")

    def test_no_party_list(self):
        p = example(); p["affected_parties"] = []
        self.assertEqual(evaluate(p)["recommendation"], "review")

    def test_consciousness_may_be_irrelevant(self):
        p = example(); p["assessments"]["consciousness_claims_qualified"] = {"value":"not_applicable", "rationale":"No consciousness claims are made."}
        self.assertEqual(evaluate(p)["recommendation"], "proceed")

    def test_unknown_check(self):
        p = example(); p["assessments"]["new_check"] = {"value":"yes"}
        self.assertEqual(evaluate(p)["recommendation"], "review")

    def test_not_object(self):
        with self.assertRaises(ValueError):
            evaluate([])

    def test_evaluator_does_not_mutate(self):
        p = example(); before = copy.deepcopy(p); evaluate(p)
        self.assertEqual(p, before)


if __name__ == "__main__":
    unittest.main()
