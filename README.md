# maspy-zombie-pending-goal

Small reproducible example showing how an expired pending Goal can occupy the front of `_pending_events` and prevent a newer Goal from being retried.

## What to observe

`zombie_pending_goal.py` creates two goals:

- `goal_a` depends on `Belief("never_here")`, which never arrives.
- `goal_b` depends on `Belief("permission_b")`, which is granted later.

A noise feeder keeps the normal event queue busy past the default 20-cycle window, so the pending item for `goal_a` is never retried in time and expires at the front of the queue. When `permission_b` arrives, `goal_b`'s context is satisfied, but `goal_b` sits behind the expired `goal_a` and is never retried.

Expected output:

```text
Doesnt have Plan with proper context for Event gain:Goal goal_a()[self]
Doesnt have Plan with proper context for Event gain:Goal goal_b()[self]
GRANTING permission_b
LOG: permission_b arrived; goal_b context is now satisfied
TIMEOUT / observation: B was never reprocessed because A expired at the front
SYSTEM ENDED
```

## Run

Using the Makefile:

```bash
make setup        # create the venv and install the published MASPY
make run-zombie   # run the example
make run-all      # run all examples
```

Or directly with Python:

```bash
python examples/zombie_pending_goal.py
```

The expiry is reported through a MASPY debug log, so it only shows with logging enabled. `run-zombie-log` sets `MASPY_LOG=1`, which the example reads to turn on `Admin(console_log=True)`:

```bash
make run-zombie-log
```

Run `make help` for the full, up-to-date list of targets.

## Contrast: within the pending window, Goal A can fail and Goal B can proceed

`within_window_goal_b_runs.py` keeps the same kind of pending window, but the retry happens inside the default 20-cycle window. Here `goal_a` fails and `goal_b` runs:

```text
Agent:Z> Doesnt have Plan with proper context for Event gain:Goal goal_a()[self]
Agent:Z> B EXECUTED
```

```bash
make run-within-window
```

## Choosing the MASPY version

`make setup` installs the published `maspy-ml` from PyPI, which is the default. To test a fork, a git ref or a local checkout, override the `MASPY` requirement:

```bash
make install-maspy MASPY="git+https://github.com/<fork>/MASPY.git@<branch>"
make install-maspy MASPY="-e ../MASPY"
make install-maspy                                   # back to the published package
```
