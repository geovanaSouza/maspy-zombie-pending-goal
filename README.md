# maspy-zombie-pending-goal

Small reproducible example showing how an expired pending Goal can occupy the
front of `_pending_events` and prevent a newer Goal from being retried.

## What to observe

The agent creates two goals:

- `goal_a`
- `goal_b`

Both depend on a belief that never arrives: `Belief("never_here")`.

The expected effect is:

1. `goal_a` is processed first and becomes a pending Goal.
2. `goal_b` is processed afterward and becomes a second pending Goal.
3. The first pending Goal expires before the second can be retried.
4. The second Goal remains behind the expired pending item and is never retried.

Example output:

```text
Agent:Z> Doesnt have Plan with proper context for Event gain:Goal goal_a()[self]
Agent:Z> Doesnt have Plan with proper context for Event gain:Goal goal_b()[self]
TIMEOUT / observation: B was never reprocessed because A expired at the front
SYSTEM ENDED
```

## Run

```bash
python examples/zombie_pending_goal.py
```