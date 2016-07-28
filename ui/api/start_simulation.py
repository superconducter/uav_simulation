from time import sleep

import sys

from simulation_core.simcore import main
from ui_sim_interface.pass_data import complete_simulation
"""
This file can be executed from external places and provide arguments for simcore.
The first argument should be the primary key of the newly created simulation.
"""
if __name__ == "__main__":
    main(*sys.argv[1:3])
    complete_simulation(sys.argv[1])
