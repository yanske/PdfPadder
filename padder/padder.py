import argparse

from padder.imageprocessor import ImageProcessor
from padder.fileprocessor import FileProcessor

def _parse_arguments():
  parser = argparse.ArgumentParser()
  parser.add_argument("path", help = "path to the target PDF")
  parser.add_argument("-r", "--ratio", help = "ratio of the padding compared to the PDF width", type = float, default = 0.4)
  return parser.parse_args()

def main():
  args = _parse_arguments()

  images = FileProcessor.open_pdf_as_image(args.path)

  padding_options = { "ratio": args.ratio }
  padded_images = [ImageProcessor.pad(img, padding_options) for img in images]
  
  FileProcessor.save_images_as_pdf(padded_images)
