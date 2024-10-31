#!/bin/bash

# Run PRSice2 PRS on CITRUS simulated phenotype

# PHENO=mult_pheno_1
# PHENO=mult_pheno_2
# PHENO=xor_pheno_1
# PHENO=xor_pheno_2
# PHENO=compound_het
# PHENO=compound_het_2
# PHENO=gepsi_lin_add_h0625_h0625
# PHENO=gepsi_lin_add_h125_h125
# PHENO=gepsi_lin_add_h25_h25
# PHENO=gepsi_lin_add_h5_h5
# PHENO=gepsi_lin_add_hFULL_hFULL

# PHENO=gepsi_lin_add_h0625
# PHENO=gepsi_lin_add_h125
# PHENO=gepsi_lin_add_h25
# PHENO=gepsi_lin_add_h5
# PHENO=gepsi_lin_add_hFULL

# PHENO=gepsi_lin_add_h0625_gcta
# PHENO=gepsi_lin_add_h125_gcta
# PHENO=gepsi_lin_add_h25_gcta
# PHENO=gepsi_lin_add_h5_gcta
PHENO=gepsi_lin_add_hFULL_gcta

echo ${PHENO}

MAX_N_VARS=10000

TEMP_DIR=/tmp
OUT_DIR=output/aml_filter_vars/${PHENO}
GWAS_OUT_DIR=output/GWAS

GWAS_SS=output/GWAS/${PHENO}.phenotype.glm.linear
SPLITS_DIR=data/splits
VAL_SPLIT_FNAME=val_samples.txt
TEST_SPLIT_FNAME=test_samples.txt
GENO_DIR=data/geno_data/pgen
PGEN_FNAME=imputed_chr19_1ID

DOCKER_URL=gcr.io/ucsd-medicine-cast/nonlin_prs_prs_aml_filter_vars:latest

# Start docker env
module load singularitypro

singularity exec --containall \
	--bind /expanse/projects/gymreklab/rdevito:/mnt \
	docker://${DOCKER_URL} \
	bash -c "cd /mnt/citrus/CITRUS/paper && \
	echo 'Filtering variants by p-value and window size' && \
	python3 /home/AutoML_PRS/data_preprocessing/filter_vars_by_pval.py \
		--sum-stats-file ${GWAS_SS} \
		-p 1e-5 1e-8 1e-16 1e-24 1e-32 1e-40 1e-64 1e-128 1e-256 \
		--window-bp 0 5000 20000 50000 100000 \
		-m ${MAX_N_VARS} \
		-o ${TEMP_DIR} \
	&& \
	echo 'Filter and convert to Python readable format' && \
	mkdir -p ${OUT_DIR} && \
	plink2 \
		--pfile ${GENO_DIR}/${PGEN_FNAME} \
		--extract ${TEMP_DIR}/filtered_vars_all.txt \
		--export A \
		--out ${OUT_DIR}/filtered_doseage_table \
	&& \
	python3 workflows/aml_filter_vars/raw_to_input_parquet.py \
		-f ${TEMP_DIR}/filtered_vars_raw.json \
		-r ${OUT_DIR}/filtered_doseage_table.raw \
		-o ${OUT_DIR} "

# -p 1e-5 1e-8 1e-14 1e-20 1e-26 \
# --window-bp 0 5000 10000 25000 100000 \