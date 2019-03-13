from PIL import Image

class ImageProcessor:
  """padder/ImageProcessor
  
  Pads images with specified whitespace
  """

  DEFAULT_OPTIONS = {"ratio": 0.4, "color": "white"}

  @staticmethod
  def pad(image, options = {}):
    """Pad image with specified parameters
    
    Optional parameters:
      ratio: ratio of whitespace to orginal image width, default = 40%
      color: color of padding, default = white
    """

    params = ImageProcessor.DEFAULT_OPTIONS.copy()
    params.update(options)

    w, h = image.size

    # Expand width by ratio
    target_width = int(w * (1.0 + params["ratio"]))

    # Create a new white layer and compose the PDF mask over it
    background = Image.new("RGB", (target_width, h), params["color"])
    background.paste(image, (0, 0))

    return background
