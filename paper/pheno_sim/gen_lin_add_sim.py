"""Generate linear additive phenotype CITRUS simulation configs."""

import copy
import json

import numpy as np
import pandas as pd


CONFIG_TEMPLATE = {
	"input": [
		{
			"file": "../data/ukb/vcf/phased_chr19.vcf",
			"file_format": "vcf",
			"reference_genome": "GRCh37",
			"input_nodes": [
				{
					"alias": "variants",
					"type": "SNP",
					"chr": "19",
					"pos": []
				}
			]
		}
	],
	"simulation_steps": [
		{
			"type": "RandomConstant",
			"alias": "variants_betas",
			"input_match_size": "variants",
			"dist_name": "normal",
			"dist_kwargs": {
				"loc": 0.0,
				"scale": 1.0
			},
			"by_feat": True
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
		}
	]
}


class NpEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        if isinstance(obj, np.floating):
            return float(obj)
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return super(NpEncoder, self).default(obj)


def create_config(pos, heritability):
	sim_config = copy.deepcopy(CONFIG_TEMPLATE)

	sim_config['input'][0]['input_nodes'][0]['pos'] = list(pos)
	sim_config['simulation_steps'][-1]['heritability'] = float(heritability)

	return sim_config
	

if __name__ == '__main__':

	# Options
	n_vars = [10, 100, 1000]
	herit_vals = [0.05, 0.1, 0.2, 0.4, 0.8]
	version_num = 1

	config_save_dir = 'sim_configs'

	# Load variant info
	var_info_path = '../data/ukb/chr19_var_info.csv'
	var_df = pd.read_csv(
		var_info_path
	)

	# Add position column
	var_df['pos'] = var_df.locus.apply(lambda x: int(x.split(':')[1]))

	for n_var in n_vars:
		for herit in herit_vals:
			rng = np.random.default_rng(seed=147*version_num)
			
			# Select loci
			pos = rng.choice(
				var_df.pos,
				size=n_var,
				replace=False
			)

			sim_config = create_config(list(pos), herit)
			
			# Save config
			h_str = str(herit).split('.')[1]
			config_fname = f'lin_add_nvar{n_var}_h{h_str}_v{version_num}'

			with open(f'{config_save_dir}/{config_fname}.json', 'w') as f:
				json.dump(sim_config, f, indent=4, cls=NpEncoder)