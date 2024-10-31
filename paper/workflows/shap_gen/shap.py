"""Get SHAP values with CITRUS.

Args:

	-c, --config_path: Path to JSON simulation config.
	-o, --output_path: Path to output directory.
"""

import argparse
import json

from pheno_sim.shap import run_SHAP


def parse_args():
	parser = argparse.ArgumentParser()
	parser.add_argument(
		"-c", "--config_path", type=str, help="Path to JSON simulation config."
	)
	parser.add_argument(
		"-o", "--output_path", type=str, help="Path to output directory."
	)
	return parser.parse_args()


if __name__ == "__main__":
	args = parse_args()

	# Load config
	with open(args.config_path, "r") as f:
		config = json.load(f)

	# Run SHAP
	run_SHAP(
		config,
		save_path=args.output_path
	)
