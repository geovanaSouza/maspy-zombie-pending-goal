# maspy-zombie-pending-goal

Reproducible example for [laca-is/MASPY#24](https://github.com/laca-is/MASPY/issues/24) — an expired pending Goal occupying the front of `Agent._pending_events` blocked later pending Goals, which were never retried even after their context became satisfied.

The issue was fixed in `maspy-ml==2026.11.12`. This repo now serves as a deterministic A/B test: the same script reproduces the bug on `2026.5.13` and shows the fix on `2026.11.12`.

## What the example does

`zombie_pending_goal.py` is fully cycle-based — no sleeps, no threads, no wall-clock timing:

- `goal_a` depends on `Belief("never_here")`, which never arrives, so it is parked in `_pending_events` (window: `PENDING_TIMER = 20` cycles from cycle ~1, expiring around cycle 21).
- `goal_b` depends on `Belief("permission_b")`, which is granted by the agent itself at `GRANT_AT_CYCLE = 18` — inside the window.
- A self-perpetuating noise chain keeps the agent's cycle counter advancing deterministically until `STOP_NOISE_AT_CYCLE = 20`, so the first idle check of the pending queue happens right when `goal_a`'s window has just expired.

Note: the pending window is measured in reasoning cycles, not wall-clock time, so its real-world duration depends on the agent's event load.

## Observed behavior per version

**`maspy-ml==2026.5.13` (bug):** the pending queue freezes on the first idle check after `goal_a` expires — the front is expired, so `_select_event` never pops it, and nothing behind it is ever retried. `goal_b` is never reprocessed even though `permission_b` has been satisfied since cycle ~20. The agent idles forever (the process has to be killed).

```text
Doesnt have Plan with proper context for Event gain:Goal goal_a()[self]
Doesnt have Plan with proper context for Event gain:Goal goal_b()[self]
LOG: permission_b added at cycle 20; goal_b context is now satisfied
(nothing else — agent idles forever)
```

**`maspy-ml==2026.11.12` (fixed):** the expired `goal_a` is retried, removed from the goal base and a `failure` event is emitted; the queue advances and `goal_b` is reprocessed and executes.

```text
LOG: permission_b added at cycle 19; goal_b context is now satisfied
Doesnt have Plan with proper context for Event gain:Goal goal_a()[self]
Doesnt have Plan with proper context for Event gain:Goal goal_b()[self]
Doesnt have Plan with proper context for Pending Event gain:Goal goal_a()[self]
B EXECUTED (cycle 24)
SYSTEM ENDED
```

## Run the A/B test

```bash
make setup          # create the venv and install maspy-ml==2026.5.13 (pyproject pin)
make run-zombie     # old behavior: hangs, goal_b never reprocessed (kill the process)

make install-maspy  # install the latest published maspy-ml (2026.11.12)
make run-zombie     # fixed: goal_a fails+removed, B EXECUTED, system ends
```

MASPY debug logging can be turned on to inspect the cycles; `run-zombie-log` sets `MASPY_LOG=1`, which the example reads to enable `Admin(console_log=True)`:

```bash
make run-zombie-log
```

Run `make help` for the full, up-to-date list of targets.

## Contrast: within the pending window, Goal A can fail and Goal B can proceed

`within_window_goal_b_runs.py` keeps the same kind of pending window, but the context arrives before the retry, so `goal_a` fails and `goal_b` runs:

```text
Agent:Z> Doesnt have Plan with proper context for Event gain:Goal goal_a()[self]
Agent:Z> B EXECUTED
```

```bash
make run-within-window
```

## Choosing the MASPY version

`make setup` installs the published `maspy-ml` from the pin in `pyproject.toml` (`2026.5.13`, the version with the bug). To test a different version, a fork, a git ref or a local checkout, override the `MASPY` requirement:

```bash
make install-maspy MASPY="maspy-ml==2026.11.12"       # pinned version
make install-maspy MASPY="git+https://github.com/<fork>/MASPY.git@<branch>"
make install-maspy MASPY="-e ../MASPY"
make install-maspy                                   # back to the latest published package
```
