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
  return parser.parse_args()

def main():
  args = _parse_arguments()
  output_path = padder.pad_pdf(args.path, args.ratio)

  print("PDF padded at:", output_path)

main()
