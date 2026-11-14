import os

from maspy import *

GRANT_AT_CYCLE = 18
STOP_NOISE_AT_CYCLE = 20


class Z(Agent):
    @pl(gain, Goal("goal_a"), context=Belief("never_here"))
    def a(self, src):
        self.print("A EXECUTED")

    @pl(gain, Goal("goal_b"), context=Belief("permission_b"))
    def b(self, src):
        self.print(f"B EXECUTED (cycle {self.cycle_counter})")
        self.stop_cycle()

    @pl(gain, Belief("permission_b"))
    def on_permission(self, src):
        print(
            f"LOG: permission_b added at cycle {self.cycle_counter}; "
            "goal_b context is now satisfied",
            flush=True,
        )

    # Self-perpetuating noise: each processed noise adds the next one, so the
    # agent always has a normal event to process and the cycle counter ticks
    # deterministically until STOP_NOISE_AT_CYCLE.
    @pl(gain, Belief("noise"))
    def noise(self, src):
        if self.cycle_counter >= STOP_NOISE_AT_CYCLE:
            return  # noise chain ends; agent goes idle until the pending retry
        self.add(Belief("noise"), instant=False)
        if self.cycle_counter >= GRANT_AT_CYCLE and not self.has(Belief("permission_b")):
            self.add(Belief("permission_b"), instant=False)


if __name__ == "__main__":
    # Set MASPY_LOG to enable MASPY logging (and show the debug log of the cycles)
    if os.environ.get("MASPY_LOG"):
        Admin(console_log=True)
    ag = Z(goals=[Goal("goal_a"), Goal("goal_b")])
    ag.add(Belief("noise"), instant=False)  # seeds the noise chain

    Admin().start_system()
    print("SYSTEM ENDED", flush=True)
