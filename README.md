# multi-processing-lab
This repo contains all the code for research lab 3 for CMPE-275.

There is a network intensive I/O task of downloading Master's project papers from the SJSU library website. The script for this can be found [here](./paper_fetcher.py).

There is a CPU intensive task of searching for a given keyword in the downloaded papers. The script for this can be found [here](./paper_miner.py).

## Getting Started
- Run `pip3 install -r requirements.txt` to download all the project requirements

- [paper_fetcher.py](./paper_fetcher.py) makes use of flags to control the parameters to the script
    - `--help` prints the help message
        - E.g: `python3 paper_fetcher.py --help`
    - `--noparallel` disables parallelization and runs the script sequentially
        - E.g: `python3 paper_fetcher.py --noparallel`
    - `--nomultiprocessing` disables multiprocessing - this is set to True by default, i.e., `--multiprocessing`
        - E.g: `python3 paper_fetcher.py --nomultiprocessing`
    - `--threads` sets the number of threads to use while `--nomultiprocessing` flag is used - this is set to `17` by default
        - E.g.: `python3 paper_fetcher.py --nomultiprocessing --threads=30`
    - `--processes` sets the number of processes to use while multiprocessing is being used - this is set to `8` by default
        - E.g.: `python3 paper_fetcher.py --multiprocessing --processes=10` or just `python3 paper_fetcher.py --processes=10`

- [paper_miner.py](./paper_miner.py) makes use of the same flags that were used for `paper_fetcher.py` and can be run the same way

## References
- https://docs.python.org/3/library/concurrent.futures.html
- https://rednafi.github.io/digressions/python/2020/04/21/python-concurrent-futures.html
- https://pdfminersix.readthedocs.io/en/latest/
- https://towardsdatascience.com/which-is-faster-python-threads-or-processes-some-insightful-examples-26074e90848f
- https://rvprasad.medium.com/performance-of-map-operation-in-mpi4py-and-multiprocessing-modules-55eb30a68d9d
