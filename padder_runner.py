from pdf2image import convert_from_path
from PIL import Image
import img2pdf

import os
import glob
import time

TEMP_DIR = "tmp/"
OUTPUT_DIR = "output/"

def parse_arguments():
  parser = argparse.ArgumentParser()
  parser.add_argument("path", help = "path to the target PDF")
  parser.add_argument("-r", "--ratio", help = "ratio of the padding compared to the PDF width", type = float, default = 0.4)
  return parser.parse_args()

# Convert PDF to PIL image objects
def parse_pdf(path):
  images = convert_from_path(path)
  return images

# Modifies by adding padding to the desired ratio
def padded_image(image, ratio):
  w, h = image.size
  
  # Expand width by ratio
  target_width = int(w * (1.0 + ratio))

  # Create a new white layer and compose the PDF mask over it
  background = Image.new("RGB", (target_width, h), "white")
  background.paste(image, (0, 0))

  return background

def save_as_pdf(images):
  # First save the images as files to be processed
  if not os.path.exists(TEMP_DIR): os.makedirs(TEMP_DIR)

  for i in range(len(images)):
    img = images[i]
    img.save(TEMP_DIR + str(i) + ".jpeg", "JPEG")

  # Output to output folder
  if not os.path.exists(OUTPUT_DIR): os.makedirs(OUTPUT_DIR)

  output_name = OUTPUT_DIR + "o_" + str(int(time.time())) + ".pdf"
  with open(output_name,"wb") as f:
    image_names = [TEMP_DIR + str(i) + ".jpeg" for i in range(len(images))]
    f.write(img2pdf.convert(image_names))

  # Clean up
  files = glob.glob(TEMP_DIR + "*")
  for f in files: os.remove(f)
  return

if __name__ == '__main__':
  args = parse_arguments()
  images = parse_pdf(args.path)
  images = [padded_image(img, args.ratio) for img in images]
  save_as_pdf(images)
