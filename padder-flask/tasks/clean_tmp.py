#!/usr/bin/python3.6

"""Script to clean the /tmp/ directory from the littered PDF files.

Removes all files ending in .pdf from /tmp/ if it is more than 5 mins old.
"""

import os
import glob
import time

cur = time.time()
count = 0

for pdf in glob.glob('/tmp/*.pdf'):
    if cur - os.path.getmtime(pdf) > 5 * 60:
        os.remove(pdf)
        count += 1

print("Removed", count, "PDFs from /tmp/.")
