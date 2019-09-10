"""Main padding logic for PDF and temp file processing.
"""

import os
import pdf2image
import img2pdf
from PIL import Image

import random
import string
from pathos.multiprocessing import ProcessingPool as Pool

def _generate_tmp_path(tmp_dir='/tmp', ext=''):
  letters = string.ascii_lowercase
  path = ''.join(random.choice(letters) for _ in range(10)) + ext
  return os.path.join(tmp_dir, path)

def pad_pdf(path, ratio, output_path = None):
  """Pad PDF with a <ratio>% white margin increase on the right.

  Takes a path to the original PDF file, converts them to PIL images,
  and pads them with the appropriate whitespace. Returns a path to the
  padded PDF.

  If a valid output_path is given, it will move the PDF to the given path
  and return the path.
  """

  images = pdf2image.convert_from_path(path)

  p = Pool(4)

  def overlay_and_store(img):
    """Pad the individual images by overlaying it on a white background.

    Passed to a multiprocessing pool as each individual PDF page is
    independent of each other. Saves the image in a temp path as a JPEG,
    and returns the absolute file path.
    """

    w, h = img.size
    padded_img = Image.new("RGB", (int(w * (1.0 + ratio)), h), "white")
    padded_img.paste(img, (0, 0))

    tmp_path = _generate_tmp_path(ext='.jpeg')
    padded_img.save(tmp_path, "JPEG")
    return tmp_path

  padded_images = p.map(overlay_and_store, images)

  # Output as PDF.
  output = _generate_tmp_path(ext='.pdf')
  with open(output, 'wb') as f:
    f.write(img2pdf.convert(padded_images))

  # Clean up temp image files used.
  for tmp_img in padded_images:
    os.remove(tmp_img)

  if output_path:
    os.rename(output, output_path)
    return output_path

  return output
