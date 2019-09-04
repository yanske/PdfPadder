"""Main padding logic for PDF and temp file processing.
"""

import os
import pdf2image
import img2pdf
from PIL import Image

import random
import string

def _generate_tmp_path(tmp_dir='/tmp', ext=''):
  letters = string.ascii_lowercase
  path = ''.join(random.choice(letters) for _ in range(10)) + ext
  return os.path.join(tmp_dir, path)

def pad_pdf(path, ratio):
  """Pad PDF with a <ratio>% white margin increase on the right.

  Takes a path to the original PDF file, converts them to PIL images,
  and pads them with the appropriate whitespace. Returns a path to the
  padded PDF.
  """

  images = pdf2image.convert_from_path(path)

  # Pad the individual images by overlaying it on a white background.
  padded_images = []
  for img in images:
    w, h = img.size
    padded_img = Image.new("RGB", (int(w * (1.0 + ratio)), h), "white")
    padded_img.paste(img, (0, 0))

    padded_images.append(padded_img) 
  
  # Save the images as files.
  image_paths = []
  for img in padded_images:
    tmp_path = _generate_tmp_path(ext='.jpeg')
    img.save(tmp_path, "JPEG")
    image_paths.append(tmp_path)

  # Output as PDF.
  output = _generate_tmp_path(ext='.pdf')
  with open(output, 'wb') as f:
    f.write(img2pdf.convert(image_paths))
  
  # Clean up temp image files used.
  for tmp_img in image_paths:
    os.remove(tmp_img)

  return output
