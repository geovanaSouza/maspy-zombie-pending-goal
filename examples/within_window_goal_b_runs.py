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


if __name__ == "__main__":
    ag = Z(goals=[Goal("goal_a"), Goal("goal_b")])

    def grant_permission():
        time.sleep(1.0)
        ag.add(Belief("permission_b"))

    threading.Thread(target=grant_permission, daemon=True).start()

    print("Start with 20-cycle default window", flush=True)
    Admin().start_system()
    print("System ended", flush=True)