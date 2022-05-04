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
KEYWORD = "machine"

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
def search_pdf(file_path):
    """
    Searches the PDF {index}.pdf for the specified word
    Args:
        word: (str) Word to search for
        index: (int) Index of the paper
    Returns:
        (int) Number of times the word was found in the paper
    """
    counter = 0
    try:
        text = extract_text(file_path)
        for word in text.split(" "):
            if word.lower() == KEYWORD:
                counter += 1
        print(f"Counter is {counter} for file {file_path}")
        return counter
    except Exception as e:
        logging.error(f"Exception {e} while extracting text from {file_path}")
        return None


@func_timer
def mine_papers_sequentially(files):
    """
    Mine the papers sequentially
    Args:
        files: (list) List of files to mine
    Returns:
        (map) Map of file path to number of times the keyword was found in the paper
    """
    logging.info("Searching papers sequentially")
    result = {}
    for f in files:
        counter = search_pdf(f)
        if counter is not None:
            result[f] = counter

    return result


def main(argv):
    global KEYWORD
    KEYWORD = FLAGS.keyword

    # Get list of all PDF files in papers directory
    files = os.listdir("papers")
    files = list(map("papers/{}".format, files))

    result = {}

    if FLAGS.parallel:
        # mine_papers_in_parallel()
        pass
    else:
        result = mine_papers_sequentially(files)

    print(result)



if __name__ == "__main__":
    app.run(main)
