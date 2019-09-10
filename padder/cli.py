"""CLI for padding PDFs using padder.

See `python3 cli.py -h` for usage.
"""

import argparse
import padder

def _parse_arguments():
  parser = argparse.ArgumentParser()
  parser.add_argument("path", help = "path to the target PDF")
  parser.add_argument("-r", "--ratio",
    help = "ratio of the padding compared to the PDF width",
    type = float, default = 0.4)
  parser.add_argument("-o", "--output",
    help = "output path of the padded PDF",
    type = str, default = None)
  return parser.parse_args()

def main():
  args = _parse_arguments()
  output_path = padder.pad_pdf(args.path, args.ratio, args.output)

  print("PDF padded at:", output_path)

main()
