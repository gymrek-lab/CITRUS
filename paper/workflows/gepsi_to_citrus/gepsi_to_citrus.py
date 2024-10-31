"""Create CITRUS simulation config from GEPSi sim info.

Args:
	-g, --gepsi-out-dir: Directory containing GEPSi output files.
	-d, --gepsi-out-desc: Description part of GEPSi output file names.
	-h, --herit: Heritability
	-o, --output-dir: Directory to write simulation config to.
"""

import argparse
import os
import json

import pandas as pd


# Template needs pos, betas, and heritability added
TEMPLAT_CONFIG = {
    "input": [
        {
            "file": "../data/geno_data/vcf/phased_chr19.vcf",
            "file_format": "vcf",
            "reference_genome": "GRCh37",
            "input_nodes": [
                {
                    "alias": "variants",
                    "type": "SNP",
                    "chr": "19",
                    "pos": None
                }
            ]
        }
    ],
    "simulation_steps": [
        {
            "type": "Constant",
            "alias": "variants_betas",
            "input_match_size": "variants",
            "constant": None
        },
        {
            "type": "Product",
            "alias": "variant_effects",
            "input_aliases": [
                "variants_betas",
                "variants"
            ]
        },
        {
            "type": "AdditiveCombine",
            "alias": "combined_variant_effects",
            "input_alias": "variant_effects"
        },
        {
            "type": "SumReduce",
            "alias": "no_noise_phenotype",
            "input_alias": "combined_variant_effects"
        },
        {
            "type": "Heritability",
            "alias": "phenotype",
            "input_alias": "no_noise_phenotype",
            "heritability": None
        }
    ]
}


def parse_args():
	parser = argparse.ArgumentParser()
	parser.add_argument("-g", "--gepsi-out-dir", required=True)
	parser.add_argument("-d", "--gepsi-out-desc", required=True)
	parser.add_argument("-h2", "--herit", required=True)
	parser.add_argument("-o", "--output-dir", required=True)
	return parser.parse_args()


if __name__ == '__main__':

	args = parse_args()

	# Load GEPSi SNP info
	causal_snps = pd.read_csv(
		os.path.join(
			args.gepsi_out_dir, f"{args.gepsi_out_desc}_causal_snps_info.csv"
		)
	)

	# Create simulation config
	sim_config = TEMPLAT_CONFIG

	# Pos
	sim_config['input'][0]['input_nodes'][0]['pos'] = causal_snps[
		'Position'
	].values.tolist()

	# Betas
	sim_config['simulation_steps'][0]['constant'] = causal_snps[
		'effect_size'
	].values.tolist()

	# Heritability
	sim_config['simulation_steps'][-1]['heritability'] = float(args.herit)

	# Save JSON config
	h = str(args.herit).split('.')[-1]
	with open(os.path.join(
		args.output_dir, f"{args.gepsi_out_desc}_h{h}.json"
	), 'w') as f:
		json.dump(
			sim_config,
			f,
			indent=4
		)


	# g='../../output/gepsi_phenos'
	# d='gepsi_lin_add_h2'
	# h2=0.2
