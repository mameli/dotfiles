# Strategy Matrix

Use this reference after discovery to pick the smallest high-value test set.

## Surface -> default strategy

| Surface | Primary strategy | Useful invariants | High-value edge cases |
| --- | --- | --- | --- |
| Parser or loader | Roundtrip or parse-failure tests, structured fuzzing | parse(valid(x)) preserves key fields; invalid inputs fail clearly | empty input, missing field, extra field, malformed separators, encoding, boundary lengths |
| Serializer or formatter | Roundtrip and normalization tests | serialize(parse(x)) is stable; repeated normalization is idempotent | quotes, separators, escapes, unicode, nulls, precision, ordering |
| Data transform | Oracle and invariant tests | shape preserved, aggregation laws, idempotence, monotonicity, sortedness, checksum consistency | empty dataset, duplicates, mixed types, nulls, threshold values, order perturbation |
| CLI | Black-box command tests | exit code and stable user-visible output | missing args, conflicting flags, invalid file path, malformed config |
| HTTP or API handler | Black-box request/response tests | status, schema, side effects, idempotence where relevant | invalid payload, auth edge, missing field, duplicate submission, ordering |
| Storage or persistence | Black-box save/load tests | saved then loaded data preserves contract | empty records, nulls, escaping, duplicate keys, transaction failure, partial write |
| Stateful workflow | Transition or model-based tests | illegal transitions rejected; reachable states preserve invariants | repeated action, interrupted action, reset, rollback, out-of-order events |

## Oracle patterns

- Compare a complex implementation against a slow but obvious reference.
- Compare normalized output against a second pass of the same normalizer when idempotence should hold.
- Compare aggregate results against recomputation from simpler primitives.
- Compare save/load or encode/decode paths against a roundtrip contract.

## Structured randomness patterns

- Start from valid examples and mutate one boundary at a time.
- Generate values near thresholds, not only across the full range.
- Mix valid and invalid fields in the same payload.
- Bias toward duplicates, empties, and mixed ordering.
- Seed custom random generators when not using `Hypothesis`.

## Low-value defaults to avoid

- Tests that only mirror implementation branches without asserting behavior.
- Snapshotting volatile text or framework-rendered output when the contract is elsewhere.
- Repeating coverage-driven examples with no new state explored.
- Testing private helpers when a stable public behavior already covers the risk.
