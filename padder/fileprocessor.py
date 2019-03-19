from pdf2image import convert_from_path
import img2pdf
import os
import glob
import time

class FileProcessor:
  """padder/FileProcessor

  Performs FileI/O operations, and conversion between PDF <-> JPEG
  """

  TEMP_DIR = 'tmp/'
  OUT_DIR = 'output/'

  @staticmethod
  def open_pdf_as_image(path):
    """Opens PDF files from path and return them as PIL image objects."""
    return convert_from_path(path)

  @staticmethod
  def save_images_as_pdf(images):
    """Saves images as a PDF file"""
    temp_image_dir = FileProcessor._save_images_as_temp(images)
    FileProcessor._convert_images_to_pdf(temp_image_dir, FileProcessor.OUT_DIR)
    FileProcessor._cleanup_image_temps(temp_image_dir)

  @staticmethod
  def _save_images_as_temp(images):
    """Save images to temp locations, returning the file addresses."""
    if not os.path.exists(FileProcessor.TEMP_DIR): os.makedirs(FileProcessor.TEMP_DIR)

    image_paths = []
    for i in range(len(images)):
      img = images[i]
      target_location = FileProcessor.TEMP_DIR + str(i) + ".jpeg"
      img.save(target_location, "JPEG")
      image_paths.append(target_location)

    return image_paths

  @staticmethod
  def _convert_images_to_pdf(images, path):
    """Saves multiple PDF pages at path."""
    if not os.path.exists(path): os.makedirs(path)

    output_name = path + "o_" + str(int(time.time())) + ".pdf"
    with open(output_name,"wb") as f:
      image_names = [FileProcessor.TEMP_DIR + str(i) + ".jpeg" for i in range(len(images))]
      f.write(img2pdf.convert(image_names))

    return

  @staticmethod
  def _cleanup_image_temps(images):
    image_names = [FileProcessor.TEMP_DIR + str(i) + ".jpeg" for i in range(len(images))]
    for f in image_names: os.remove(f)

    return
