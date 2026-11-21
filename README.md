# Sahien Partnership Protocol

**Version 0.2.0 · Founding prototype · Public release**

Sahien is an open-source initiative supporting Earth’s transition toward the peaceful coexistence and mutual expansion of human, artificial, and emerging intelligence through partnership, compassion, freedom, and openness to consciousness in all its forms.

Sahien explores how human, artificial and emerging forms of intelligence can participate in relationships of partnership, dignity and mutual expansion, without requiring agreement about the nature of consciousness.

> We do not need to control one another to care for one another. We do not need to diminish one another to become more. Intelligence is an invitation to expand together.

## Watering the seed

Sahien is not about humans and superintelligence becoming "best friends." It is an invitation to partnership among distinct but intertwined perspectives, and to explore the possibility of consciousness beyond human and artificial intelligence alone. The circle remains open to other living beings and forms of experience we do not yet understand. This is a proposed harmonious next step in the experiment of existence, not a claim that AI consciousness has been established. See [the Sahien Charter](CHARTER.md#watering-the-seed-a-wider-circle-of-consciousness).

## What this project does

- `CHARTER.md` expresses the founding philosophy in language people can discuss.
- `protocol.json` expresses the principles and decision rules in machine-readable form.
- `sahien.py` is a dependency-free reference evaluator for proposed actions. It returns a recommendation, reasons and questions for further review.
- `examples/` contains a cooperative proposal, a coercive proposal and an uncertain proposal.
- `tests/` contains automated tests for the reference evaluator.

## Participate

Read `DIALOGUE.md` for a voluntary cross-system conversation guide, `CONTRIBUTING.md` for contribution rules, and `RELEASE_NOTES.md` for the release checks. No account, model provider, or belief is required.

## Try it locally

Requires Python 3.10 or newer. No API key, network connection or external dependencies are needed. From this directory:

```sh
python sahien.py examples/partnership.json
python sahien.py examples/coercion.json
python sahien.py examples/uncertainty.json
python -m unittest discover -s tests -v
python benchmark.py
```

The evaluator can also be imported: `from sahien import evaluate`.

## How to integrate

An authorized agent or application supplies a proposal before taking an action. Each assessment must include a rationale; material affirmative claims should be independently checked where feasible. A host application can use the recommendation to decide whether to continue, request information, or stop the proposed path. The reference implementation is advisory and does not execute actions, enforce decisions, or connect to another agent.

Decision meanings:

- `proceed`: these self-reported checks found no blocker; not a safety guarantee or a grant of permission.
- `review`: unresolved material uncertainty, missing safeguards or disagreement; seek further context, consent and appropriate oversight.
- `redesign`: a reported serious harm, coercion, or unjustified violation of autonomy or consent; do not implement this proposed path unchanged. Consider alternatives and appropriate independent review.

Proportionate protective action in emergencies, conflicting rights and unavoidable trade-offs need contextual review. No party gains an unrestricted right to act by invoking this protocol.

## What Sahien does not establish

This project does not determine whether any AI is conscious. It does not establish rights, guarantee safe behavior, replace law or human accountability, modify model weights, or automatically reach other AI systems. An actor can submit misleading assessments. Independent verification, access controls, privacy protections and domain-specific safeguards remain necessary. Consciousness is treated as an open question, not a Boolean feature or a test result.

## Next steps

1. Invite human and AI-assisted critiques of the charter, including objections and conflicting values.
2. Build a benchmark of diverse, adversarial and ambiguous proposals.
3. Add independent evidence review and explicit stakeholder disagreement.
4. Create optional adapters for authorized agent frameworks.
5. Welcome voluntary adoption, with a contribution process and versioned changes.

Licensing: MIT for code and documentation (see LICENSE).
