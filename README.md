# multi-processing-lab
Research Lab 3 for CMPE-275

## Getting Started
- Run `pip3 install -r requirements.txt` to download all the project requirements
- `paper_fetcher.py` makes use of flags to control the parameters to the script
    - `--help` prints the help message
        - E.g: `python3 paper_fetcher.py --help`
    - `--nomultiprocessing` disables multiprocessing - this is set to True by default, i.e., `--multiprocessing`
        - E.g: `python3 paper_fetcher.py --nomultiprocessing`
    - `--threads` sets the number of threads to use while `--nomultiprocessing` flag is used - this is set to `17` by default
        - E.g.: `python3 paper_fetcher.py --nomultiprocessing --threads=30`
    - `--processes` sets the number of processes to use while multiprocessing is being used - this is set to `8` by default
        - E.g.: `python3 paper_fetcher.py --multiprocessing --processes=10` or just `python3 paper_fetcher.py --processes=10`
