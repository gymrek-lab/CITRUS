""" Preliminary testing v2: Using real input data from VCF. 

Implements a simple model with LDLR gene related SNPs. SNPs contribute
either 0 for the reference allele or some beta for the alternate allele.

Model assumes additive effects of SNPs.
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from pheno_sim import PhenoSimulation


if __name__ == "__main__":

	# Create simulation
	sim_spec = {
		"input": [
			{
				"file": "1000_genomes_data/ALL.chr19.phase3_shapeit2_mvncall_integrated_v5b.20130502.genotypes.vcf.gz",
				"file_format": "vcf",
				"reference_genome": "GRCh37",
				"force_bgz": True,
				"input_nodes": [
					{
						"alias": "LDLR_upstream_variant",
						"type": "SNP",
						"chr": "19",
						"pos": 11197261
					},
					{
						"alias": "LDLR_intron_A_variants",
						"type": "SNP",
						"chr": "19",
						"pos": [11202306, 11206575]
					},
					{
						"alias": "LDLR_intron_B_variant",
						"type": "SNP",
						"chr": "19",
						"pos": 11216561
					},
					{
						"alias": "LDLR_missense_variants",
						"type": "SNP",
						"chr": "19",
						"pos": [11242133, 11222300]
					}
				]
			}
		],
		"simulation_steps": [
			# Draw/set beta values for each SNP
			{
				"type": "Constant",
				"alias": "LDLR_upstream_variant_beta",
				"input_match_size": "LDLR_upstream_variant",
				"constant": 0.1
			},
			# {
			# 	"type": "Constant",
			# 	"alias": "LDLR_intron_A_variants_betas",
			# 	"input_match_size": "LDLR_intron_A_variants",
			# 	"constant": 0.05,
			# },
			# {
			# 	"type": "Constant",
			# 	"alias": "LDLR_intron_B_variant_beta",
			# 	"input_match_size": "LDLR_intron_B_variant",
			# 	"constant": 0.05
			# },
			# {
			# 	"type": "Constant",
			# 	"alias": "LDLR_missense_variants_betas",
			# 	"input_match_size": "LDLR_missense_variants",
			# 	"constant": 0.1
			# },
			{
				"type": "RandomConstant",
				"alias": "LDLR_intron_A_variants_betas",
				"input_match_size": "LDLR_intron_A_variants",
				"dist_name": "normal",
				"dist_kwargs": {
					"loc": 0.0,
					"scale": 0.25
				},
				"by_feat": True
			},
			{
				"type": "RandomConstant",
				"alias": "LDLR_intron_B_variant_beta",
				"input_match_size": "LDLR_intron_B_variant",
				"dist_name": "normal",
				"dist_kwargs": {
					"loc": -0.05,
					"scale": 0.1
				}
			},
			{
				"type": "RandomConstant",
				"alias": "LDLR_missense_variants_betas",
				"input_match_size": "LDLR_missense_variants",
				"dist_name": "normal",
				"dist_kwargs": {
					"loc": 0.25,
					"scale": 0.2
				},
				"by_feat": True
			},

			# Multiply beta values by 0/1 alt allele by haplotype
			{
				"type": "Product",
				"alias": "LDLR_upstream_variant_effect",
				"input_aliases": [
					"LDLR_upstream_variant_beta", "LDLR_upstream_variant"
				],
			},
			{
				"type": "Product",
				"alias": "LDLR_intron_A_variants_effects",
				"input_aliases": [
					"LDLR_intron_A_variants_betas", "LDLR_intron_A_variants"
				],
			},
			{
				"type": "Product",
				"alias": "LDLR_intron_B_variant_effect",
				"input_aliases": [
					"LDLR_intron_B_variant_beta", "LDLR_intron_B_variant"
				],
			},
			{
				"type": "Product",
				"alias": "LDLR_missense_variants_effects",
				"input_aliases": [
					"LDLR_missense_variants_betas", "LDLR_missense_variants"
				],
			},

			# Additive dominance model
			{
				"type": "Concatenate",
				"alias": "LDLR_effects_by_haplotype",
				"input_aliases": [
					"LDLR_upstream_variant_effect",
					"LDLR_intron_A_variants_effects",
					"LDLR_intron_B_variant_effect",
					"LDLR_missense_variants_effects"
				]
			},
			{
				"type": "AdditiveCombine",
				"alias": "LDLR_effects",
				"input_alias": "LDLR_effects_by_haplotype"
			},

			# Final phenotype is sum of linear effects
			{
				"type": "SumReduce",
				"alias": "phenotype",
				"input_alias": "LDLR_effects",
			}
		]
	}

	simulator = PhenoSimulation(sim_spec)

	# Run in two steps
	import copy

	input_vals = simulator.run_input_step()
	print(input_vals)
	output_vals = simulator.run_simulation_steps(copy.deepcopy(input_vals))

	# Plot phenotype distribution with Seaborn
	sns.displot(output_vals["phenotype"], kde=True)
	plt.show()

	# Estimate heritability
	heritability = simulator.estimate_heritability(input_vals)


	# # Run sim with nodes from spec
	# output_vals = simulator.run_simulation_steps(input_vals)

	# # Sum haplotypes in output vals to make into a dataframe
	# df_dict = {}

	# for key in output_vals:
	# 	if isinstance(output_vals[key], tuple):
	# 		val = output_vals[key][0] + output_vals[key][1]
	# 	else:
	# 		val = output_vals[key]

	# 	if val.ndim == 1:
	# 		df_dict[key] = val

	# df = pd.DataFrame(df_dict)

	# # Rename "promoter_SNP" col to "promoter_SNP_count"
	# # and "gene_LOF" to "gene LOF SNP count"
	# df.rename(columns={"promoter_SNP": "promoter SNP count"}, inplace=True)
	# df.rename(columns={"gene_LOF": "gene LOF SNP count"}, inplace=True)

	# # Do both of the above plots in one figure
	# fig, axes = plt.subplots(1, 2, figsize=(10, 5))
	# sns.kdeplot(ax=axes[0], data=df, x="phenotype")
	# axes[0].set_title("Phenotype distribution")
	# sns.kdeplot(ax=axes[1], data=df, x="phenotype", hue="promoter SNP count")
	# axes[1].set_title("Phenotype distribution by promoter SNP count")
	# plt.tight_layout()
	# plt.show()

	# # Do both of the above plots in one figure
	# fig, axes = plt.subplots(1, 2, figsize=(10, 5))
	# sns.kdeplot(ax=axes[0], data=df, x="phenotype")
	# axes[0].set_title("Phenotype distribution")
	# sns.kdeplot(ax=axes[1], data=df, x="phenotype", hue="gene LOF SNP count")
	# axes[1].set_title("Phenotype distribution by gene LOF SNP count")
	# plt.tight_layout()
	# plt.show()

	# # Plot the underlying distributions for when
	# # promoter_SNP = 0 and promoter_SNP = 1
	# fig, ax = plt.subplots()
	# sns.kdeplot(ax=ax, data=df, x="normal_function")
	# sns.kdeplot(ax=ax, data=df, x="function_wo_promoter")
	# plt.show()
