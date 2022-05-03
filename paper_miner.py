"""
This script extracts the text from all the downloaded Master's project papers
and searches for the specified keywords.
The list of papers with the frequency of the specified keywords is returned.
"""

import os
import time
from absl import app
from absl import flags
from absl import logging
from pdfminer.high_level import extract_text

START_INDEX = 1000
END_INDEX = 2060
THREADS = 17
PROCESSES = 8
CHUNKSIZE = (END_INDEX - START_INDEX) // PROCESSES

FLAGS = flags.FLAGS

flags.DEFINE_string("keyword", "machine", "Keyword to search for")
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


@func_timer
def search_pdf(keyword, index):
    """
    Searches the PDF {index}.pdf for the specified word
    word: (str) Word to search for
    index: (int) Index of the paper
    """
    text = extract_text(f"papers/{index}.pdf")
    counter = 0
    for word in text.split(" "):
        if word.lower() == keyword:
            counter += 1

    print(f"Counter is {counter}")


def main(argv):
    search_pdf("a", 2034)


if __name__ == "__main__":
    app.run(main)
