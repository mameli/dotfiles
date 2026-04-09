---
name: python-antirez-testing
description: >
  Design and generate robust tests for Python repos using antirez-style
  testing: inspect the repo first, prioritize risky public behavior, define
  invariants and simple oracles, target edge cases and structured randomness,
  then write pytest tests. Use Hypothesis when it adds value, but do not
  depend on it.
---

# Python Antirez Testing

Use this skill when the user asks to create, improve, replace, or review tests in a Python repo and the goal is to find real bugs, protect refactors, and exercise behavioral boundaries instead of chasing coverage.

## Quick start

1. Inspect the repo before proposing tests.
2. Find the real public surfaces: module APIs, CLI commands, HTTP handlers, parsers, serializers, transforms, storage boundaries, and state transitions.
3. Detect whether existing tests are trustworthy, weak, or scaffolding. If tests are broken placeholders, note that and do not extend them blindly.
4. For each high-risk surface, define:
   - the stable public behavior
   - one or more invariants or a simple oracle
   - targeted edge cases near real boundaries
   - whether structured randomness or property tests will expose more states
5. Prefer black-box tests in the repo's existing framework. Default to `pytest`.
6. Use `Hypothesis` only when it materially improves generation or shrinking and the repo can accept the dependency.
7. Present work in this order:
   - prioritized risk map
   - invariants and simple oracles
   - edge-case matrix
   - concrete tests to add or rewrite
   - note on what not to test directly

## Discovery workflow

Start with a short repo diagnosis. Check:

- packaging and runtime metadata: `pyproject.toml`, `requirements*.txt`, `setup.cfg`, `tox.ini`, `noxfile.py`
- test framework and layout: `tests/`, `conftest.py`, CI commands, coverage settings
- whether `Hypothesis` is already installed or easy to add
- entrypoints that expose real behavior: public functions, CLI commands, API routes, file format boundaries
- fixtures, sample data, snapshots, golden files, and fake services already present
- signs of dead or misleading tests: imports to missing modules, trivial hello-world checks, tests tied to removed code

Follow the repo's conventions if they are coherent. If the repo has no clear convention, default to `pytest` and behavior-oriented files such as `tests/test_<behavior>.py`.

## Strategy rules

- Black-box first. Test public behavior and stable outputs before private helpers.
- Use implementation knowledge only to aim the tests at risky boundaries, not to lock tests to internals.
- Prefer invariants over example enumeration when the behavior is transformation-heavy or stateful.
- Use a simpler oracle when possible. If the production logic is complex, compare it with a stupid but obviously correct implementation.
- Use roundtrip properties for parsers and serializers.
- Use targeted edge cases around empties, `None`, duplicate keys, separators, encoding, malformed input, off-by-one lengths, threshold values, ordering, and corruption of valid examples.
- Use structured randomness, not pure noise. Generate semantically plausible data that stresses the right branches.
- Keep randomness reproducible. If not using `Hypothesis`, use deterministic seeds.

Read `references/strategy-matrix.md` when you need a quick mapping from surface type to likely invariants, edge cases, and test style.

## Hypothesis guidance

Use `Hypothesis` when one of these is true:

- the input space is large and structured
- shrinking will materially improve debugging
- the behavior is naturally expressed as a property or invariant
- parser, serializer, normalization, coercion, or state transition logic has many combinations

Do not use unconstrained generators that produce mostly junk. Shape strategies around the domain:

- prefer bounded text, collections, and numbers over unconstrained generators
- bias toward real separators, boundary lengths, nullability, duplicate elements, and mixed valid/invalid values
- add concrete examples for known thresholds even when using properties

If `Hypothesis` is not available or not appropriate, use `pytest.mark.parametrize`, fixtures, and seeded random generation.

## Writing tests

- Name tests by behavior or invariant, not by internal function mechanics.
- Group tests by user-visible capability or boundary.
- Keep setup minimal and explicit.
- Prefer direct assertions on observable outputs, persisted artifacts, emitted events, or errors.
- If a test depends on a known bug-prone threshold, encode that threshold in the test data.
- When testing parsers or validators, mutate valid examples before generating fully arbitrary invalid data.

## Guardrails

- Do not optimize for line coverage as the main goal.
- Do not default to unit tests for trivial helpers, wrappers, or simple getters.
- Do not start from "write tests for file X" without first identifying risky behavior.
- Do not make tests brittle by asserting private call sequences, local variable structure, or incidental formatting unless that behavior is part of the contract.
- Do not suggest ASAN or Valgrind by default for pure Python repos. Suggest memory-safety tooling only when native extensions, C bindings, or subprocess-heavy native components are in play.

## Output contract

When using this skill, structure the response so the user can act on it immediately:

1. `Risk map`: highest-value test surfaces in priority order.
2. `Invariants and oracles`: what must always hold, and what simple reference behavior can be used.
3. `Edge-case matrix`: the specific boundaries to hit.
4. `Concrete tests`: files or behaviors to add, rewrite, or remove.
5. `Do not test directly`: low-value or brittle targets to avoid.

If the user asked for implementation, move from diagnosis to actual test creation after this analysis.
