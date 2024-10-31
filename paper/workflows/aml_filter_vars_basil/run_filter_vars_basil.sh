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

TEMP_DIR=/tmp
OUT_DIR=output/aml_filter_vars_basil/${PHENO}
GWAS_OUT_DIR=output/GWAS

SPLITS_DIR=data/splits
VAL_SPLIT_FNAME=val_samples.txt
TEST_SPLIT_FNAME=test_samples.txt
GENO_DIR=data/geno_data/pgen
PGEN_FNAME=imputed_chr19_1ID

BASIL_INCL_FILE=output/basil/${PHENO}/included_features.csv

DOCKER_URL=gcr.io/ucsd-medicine-cast/nonlin_prs_prs_aml_filter_vars:latest

# Start docker env
module load singularitypro

# singularity shell --containall \
#     --bind /expanse/projects/gymreklab/rdevito:/mnt \
#     docker://${DOCKER_URL}

singularity exec --containall \
	--bind /expanse/projects/gymreklab/rdevito:/mnt \
	docker://${DOCKER_URL} \
	bash -c "cd /mnt/citrus/CITRUS/paper && \
	echo 'Filtering variants to BASIL included variants' && \
	mkdir -p ${OUT_DIR} && \
	python3 workflows/aml_filter_vars/filter_vars_by_basil.py \
		--basil-included-file ${BASIL_INCL_FILE} \
		-o ${OUT_DIR} \
	&& \
	echo 'Filter and convert to Python readable format' && \
	plink2 \
		--pfile ${GENO_DIR}/${PGEN_FNAME} \
		--extract ${OUT_DIR}/filtered_vars_all.txt \
		--export A \
		--out ${OUT_DIR}/filtered_doseage_table \
	&& \
	python3 workflows/aml_filter_vars/raw_to_input_parquet.py \
		-f ${OUT_DIR}/filtered_vars_raw.json \
		-r ${OUT_DIR}/filtered_doseage_table.raw \
		-o ${OUT_DIR} "
