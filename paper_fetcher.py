"""
This script downloads Master's project papers from SJSU ScholarWorks
for the Computer Engineering and Computer Science department
"""

import os
import requests
import time
from absl import app
from absl import flags
from absl import logging
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor

BASE_URL = "https://scholarworks.sjsu.edu/cgi/viewcontent.cgi?article=%s&context=etd_projects"

START_INDEX = 1000
END_INDEX = 2060
THREADS = 17
PROCESSES = 8
CHUNKSIZE = (END_INDEX - START_INDEX) // PROCESSES

FLAGS = flags.FLAGS

flags.DEFINE_boolean("debug", False, "Print debug messages")
flags.DEFINE_boolean("parallel", True, "Download papers in parallel")
flags.DEFINE_boolean("multiprocessing", True, "Download papers in multiprocessing vs. threading")
flags.DEFINE_integer("threads", THREADS, "Number of threads to use while using multithreading")
flags.DEFINE_integer("processes", PROCESSES, "Number of processes to use while using multiprocessing")


def func_timer(func):
    """
    Decorator for timing functions
    """
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        logging.info("Time taken: %.2f seconds" % (end_time - start_time))
        return result
    return wrapper


def download_pdf(index):
    """
    Downloads the PDF using the index provided
    index: (int) Index of the paper
    """
    r = requests.get(BASE_URL % index)
    if r.status_code == 200:
        # FLAGS.debug can't be used if using multiprocessing as the FLAGS haven't been defined yet
        # in the new processes spawned
        # if FLAGS.debug:
        #     logging.info(f"Downloading paper at index {index}")
        logging.info(f"Downloading paper at index {index}")
        with open("papers/%s.pdf" % index, "wb") as f:
            f.write(r.content)


@func_timer
def download_papers_sequentially():
    """
    Downloads papers sequentially
    """
    logging.info("Downloading papers sequentially")
    for i in range(START_INDEX, END_INDEX + 1):
        download_pdf(i)


@func_timer
def download_papers_in_parallel():
    """
    Downloads papers in parallel
    """
    multi_executor = None
    if FLAGS.multiprocessing:
        multi_executor = ProcessPoolExecutor(FLAGS.processes)
        logging.info("Downloading papers using multiprocessing")
    else:
        multi_executor = ThreadPoolExecutor(FLAGS.threads)
        logging.info("Downloading papers using multithreading")

    with multi_executor as executor:
        for arg, res in zip(range(START_INDEX, END_INDEX + 1), executor.map(download_pdf, range(START_INDEX, END_INDEX + 1), chunksize=CHUNKSIZE)):
            pass
        return "done"


def main(argv):
    global CHUNKSIZE    # Use global CHUNKSIZE varible
    CHUNKSIZE = (END_INDEX - START_INDEX) // FLAGS.processes

    logging.info("Paper fetcher is starting...\n")

    # Create papers directory if it doesn't exist
    if not os.path.exists(os.getcwd() + "/papers"):
        logging.info("Creating papers directory")
        os.mkdir("papers")

    if FLAGS.parallel:
        download_papers_in_parallel()
    else:
        download_papers_sequentially()

    logging.info("Paper fetcher is done!")


if __name__ == "__main__":
    app.run(main)
