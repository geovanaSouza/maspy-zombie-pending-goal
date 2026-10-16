import os
import threading
import time

from maspy import *


class Z(Agent):
    @pl(gain, Goal("goal_a"), context=Belief("never_here"))
    def a(self, src):
        self.print("A EXECUTED")

    @pl(gain, Goal("goal_b"), context=Belief("permission_b"))
    def b(self, src):
        self.print("B EXECUTED")
        self.stop_cycle()

    @pl(gain, Belief("permission_b"))
    def on_permission(self, src):
        print("LOG: permission_b arrived; goal_b context is now satisfied", flush=True)

    # Non-blocking noise plan: keeps __events busy without blocking the agent cycle
    @pl(gain, Belief("noise"))
    def noise(self, src):
        self.print("Processing noise")
        pass


if __name__ == "__main__":
    # Set MASPY_LOG to enable MASPY logging (and show the debug log of the expiry)
    if os.environ.get("MASPY_LOG"):
        Admin(console_log=True)
    ag = Z(goals=[Goal("goal_a"), Goal("goal_b")])

    def noise_feeder():
        # Add one noise belief at a time so the agent always has a normal event
        # to process and never reaches the pending queue before the window expires
        for _ in range(21):
            time.sleep(0.1)
            ag.add(Belief("noise"))

    def grant_permission_after_window():
        time.sleep(3.0)
        print("GRANTING permission_b", flush=True)
        ag.add(Belief("permission_b"))

    def expire_and_stop():
        time.sleep(10.0)
        print("TIMEOUT / observation: B was never reprocessed because A expired at the front", flush=True)
        ag.stop_cycle()

    threading.Thread(target=noise_feeder, daemon=True).start()
    threading.Thread(target=grant_permission_after_window, daemon=True).start()
    threading.Thread(target=expire_and_stop, daemon=True).start()

    Admin().start_system()
    print("SYSTEM ENDED", flush=True)