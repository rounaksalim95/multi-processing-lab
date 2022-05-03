"""
This script downloads Master's project papers from SJSU ScholarWorks
for the Computer Engineering and Computer Science department
"""

import os
import requests
import time
from absl import app
from absl import flags
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor, as_completed

BASE_URL = "https://scholarworks.sjsu.edu/cgi/viewcontent.cgi?article=%s&context=etd_projects"

START_INDEX = 1000
END_INDEX = 2060
WORKERS = 17

FLAGS = flags.FLAGS

flags.DEFINE_boolean("parallel", True, "Download papers in parallel")
flags.DEFINE_boolean("multiprocessing", True, "Download papers in multiprocessing vs. threading")
flags.DEFINE_integer("workers", WORKERS, "Number of workers to use")


def func_timer(func):
    """
    Decorator for timing functions
    """
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        print("\nTime taken: %.2f seconds" % (end_time - start_time))
        return result
    return wrapper


def download_pdf(index):
    """
    Downloads the PDF using the index provided
    index: (int) Index of the paper
    """
    r = requests.get(BASE_URL % index)
    if r.status_code == 200:
        print("Downloading paper at index %d" % index)
        with open("papers/%s.pdf" % index, "wb") as f:
            f.write(r.content)


@func_timer
def download_papers_sequentially():
    """
    Downloads papers sequentially
    """
    for i in range(START_INDEX, END_INDEX + 1):
        download_pdf(i)


@func_timer
def download_papers_in_parallel():
    """
    Downloads papers in parallel
    """
    if FLAGS.multiprocessing:
        parallel_executor = ProcessPoolExecutor(max_workers=FLAGS.workers)
    else:
        parallel_executor = ThreadPoolExecutor(max_workers=FLAGS.workers)

    with parallel_executor as executor:
        return executor.map(download_pdf, range(START_INDEX, END_INDEX + 1))


def main():
    print("Paper fetcher is starting...\n")

    # Create papers directory if it doesn't exist
    if not os.path.exists(os.getcwd() + "/papers"):
        print("Creating papers directory")
        os.mkdir("papers")

    if FLAGS.parallel:
        download_papers_in_parallel()
    else:
        download_papers_sequentially()

    print("\nPaper fetcher is done!")


if __name__ == "__main__":
    app.run(main)
