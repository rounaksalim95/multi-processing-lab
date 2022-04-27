"""
This script downloads Master's project papers from SJSU ScholarWorks
for the Computer Engineering and Computer Science department
"""

import os
import requests
import time

BASE_URL = "https://scholarworks.sjsu.edu/cgi/viewcontent.cgi?article=%s&context=etd_projects"

START_INDEX = 1000
END_INDEX = 2060


def download_pdf(response, index):
    """
    Downloads the PDF obtained from the requests response object
    response: Requests response object
    index: (int) Index of the paper
    """
    with open("papers/%s.pdf" % index, "wb") as f:
        f.write(response.content)


def main():
    print("Paper fetcher is starting...\n")

    # Create papers directory if it doesn't exist
    if not os.path.exists(os.getcwd() + "/papers"):
        print("Creating papers directory")
        os.mkdir("papers")

    start_time = time.time()
    for i in range(START_INDEX, END_INDEX + 1):
        r = requests.get(BASE_URL % i)
        if r.status_code == 200:
            print("Downloading paper at index %d" % i)
            download_pdf(r, i)

    end_time = time.time()

    print("\nPaper fetcher is done!")

    print("Time taken: %.2f seconds" % (end_time - start_time))


if __name__ == "__main__":
    main()
