##
## Conseil Junior Taker - 2024
## mp [Ubuntu]
## File description:
## multipass library
## @julesreyn
##

from taker_lib import *
import logging
import datetime

log = logging.getLogger(__name__)

if __name__ == "__main__":
    logging.basicConfig(filename=f"logs/instances/init-vm-{datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.log",
                        level=logging.INFO,
                        format='%(asctime)s - %(levelname)s - %(message)s')
    init_instance()