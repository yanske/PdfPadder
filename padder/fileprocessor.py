from pdf2image import convert_from_path

class FileProcessor:
  """padder/FileProcessor

  Performs FileI/O operations, and conversion between PDF <-> JPEG
  """

  def open_pdf_as_image(path):
    """Opens PDF files from path and return them as PIL image objects."""
    return convert_from_path(path)

  def image_to_pdf(image, path):
    """Converts PIL image objects to PDF file objects."""
    return

  def save_pdf(pages, path):
    """Saves multiple PDF pages at path."""
    return

  def save_images_as_temp(images):
    """Save images to temp locations, returning the file addresses."""
    return
