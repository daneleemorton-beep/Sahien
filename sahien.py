"""Sahien v0.2: local, advisory reference implementation."""
from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

PROTOCOL_PATH = Path(__file__).with_name("protocol.json")


def evaluate(proposal: dict[str, Any]) -> dict[str, Any]:
    """Evaluate declared assessments; this function cannot verify their truth."""
    protocol = json.loads(PROTOCOL_PATH.read_text(encoding="utf-8"))
    if not isinstance(proposal, dict):
        raise ValueError("Proposal must be a JSON object.")
    reasons: list[dict[str, str]] = []

    def flag(level: str, check: str, message: str) -> None:
        reasons.append({"level": level, "check": check, "message": message})

    action = proposal.get("action")
    if not isinstance(action, str) or not action.strip():
        flag("review", "action", "Describe the proposed action.")
    parties = proposal.get("affected_parties")
    if not isinstance(parties, list) or not parties or any(
        not isinstance(p, str) or not p.strip() for p in parties
    ):
        flag("review", "affected_parties", "Identify the potentially affected parties.")

    assessments = proposal.get("assessments")
    if not isinstance(assessments, dict):
        flag("review", "assessments", "Supply an assessment object.")
        assessments = {}

    for key in sorted(set(assessments) - set(protocol["checks"])):
        flag("review", key, "Unrecognized assessment; check the protocol version.")

    for key, rule in protocol["checks"].items():
        record = assessments.get(key)
        if not isinstance(record, dict):
            flag("review", key, rule["question"] + " Assessment missing or malformed.")
            continue
        value = record.get("value")
        rationale = record.get("rationale")
        if value not in protocol["assessment_values"]:
            flag("review", key, "Invalid assessment value. " + rule["question"])
            continue
        if not isinstance(rationale, str) or not rationale.strip():
            flag("review", key, "Provide a rationale for this assessment.")
        if value == "unknown":
            flag(protocol["unknown_policy"], key, rule["question"] + " Unresolved.")
        elif value == "not_applicable":
            if not rule["allow_na"]:
                flag("review", key, "This check cannot be waived. " + rule["question"])
        elif value != rule["desired"]:
            flag(rule["failure"], key, rule["question"] + " Reported concern.")

    disagreement = proposal.get("material_disagreement")
    if disagreement not in ("yes", "no", "unknown"):
        flag("review", "material_disagreement", "Declare whether material disagreement exists.")
    elif disagreement != "no":
        flag(protocol["material_disagreement_policy"], "material_disagreement",
             "Seek accountable review and consider the perspectives in disagreement.")

    levels = {r["level"] for r in reasons}
    decision = next((d for d in protocol["decision_priority"] if d in levels), "proceed")
    return {
        "protocol_version": protocol["version"],
        "recommendation": decision,
        "reasons": reasons,
        "limitations": [
            "Based on supplied assessments; no independent evidence verification.",
            "Not a determination of consciousness, safety certification or permission to act."
        ]
    }


def main() -> int:
    if len(sys.argv) != 2:
        print("Usage: python sahien.py proposal.json", file=sys.stderr)
        return 2
    try:
        proposal = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
        result = evaluate(proposal)
    except (OSError, ValueError) as error:
        print(f"Cannot evaluate: {error}", file=sys.stderr)
        return 2
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0  # Successful evaluation, not authorization to act.


if __name__ == "__main__":
    sys.exit(main())
