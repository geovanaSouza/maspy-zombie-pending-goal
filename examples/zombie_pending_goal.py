import threading
import time

from maspy import agent
# Force a very short pending window so the zombie effect is easy to observe.
agent.PENDING_TIMER = 1

from maspy import *


class Z(Agent):
    @pl(gain, Goal("goal_a"), context=Belief("never_here"))
    def a(self, src):
        self.print("A EXECUTED")

    @pl(gain, Goal("goal_b"), context=Belief("never_here"))
    def b(self, src):
        self.print("B EXECUTED")


if __name__ == "__main__":
    ag = Z(goals=[Goal("goal_a"), Goal("goal_b")])

    def expire_and_stop():
        time.sleep(2)
        print("TIMEOUT / observation: B was never reprocessed because A expired at the front", flush=True)
        ag.stop_cycle()

    threading.Thread(target=expire_and_stop, daemon=True).start()
    Admin().start_system()
    print("SYSTEM ENDED", flush=True)