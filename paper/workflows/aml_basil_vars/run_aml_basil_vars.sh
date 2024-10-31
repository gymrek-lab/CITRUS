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

# PHENO_DIR=pheno_sim/citrus_phenos
# PHENO_DIR=output/gepsi_phenos
PHENO_DIR=output/gcta_phenos

echo ${PHENO}
echo ${PHENO_DIR}

TEMP_DIR=/tmp
OUT_DIR=output/aml_basil_vars/${PHENO}
FILTER_OUT_DIR=output/aml_filter_vars_basil/${PHENO}

SPLITS_DIR=data/splits
TRAIN_SPLIT_FNAME=train_samples.txt
VAL_SPLIT_FNAME=val_samples.txt
TEST_SPLIT_FNAME=test_samples.txt
GENO_DIR=data/geno_data/pgen
PGEN_FNAME=imputed_chr19_1ID
PC_DIR=data/geno_data/PCs

BASIL_INCL_FILE=output/basil/${PHENO}/included_features.csv

DOCKER_URL=gcr.io/ucsd-medicine-cast/nonlin_prs_prs_aml:latest

# Start docker env
module load singularitypro

singularity exec --containall \
	--bind /expanse/projects/gymreklab/rdevito:/mnt \
	docker://${DOCKER_URL} \
	bash -c "cd /mnt/citrus/CITRUS/paper && \
	mkdir -p ${OUT_DIR} && \
	awk 'NR==1 {print \"IID\tphenotype\"; next} {print \$1\"_\"\$2\"\t\"\$3}' \
		${PHENO_DIR}/${PHENO}.pheno > ${OUT_DIR}/${PHENO}_1ID.pheno \
	&& \
	awk '{print \$1\"_\"\$2}' \
		${SPLITS_DIR}/${TRAIN_SPLIT_FNAME} > ${TEMP_DIR}/${TRAIN_SPLIT_FNAME} \
	&& \
	awk '{print \$1\"_\"\$2}' \
		${SPLITS_DIR}/${VAL_SPLIT_FNAME} > ${TEMP_DIR}/${VAL_SPLIT_FNAME} \
	&& \
	awk '{print \$1\"_\"\$2}' \
		${SPLITS_DIR}/${TEST_SPLIT_FNAME} > ${TEMP_DIR}/${TEST_SPLIT_FNAME} \
	&& \
	python3 workflows/aml_basil_vars/fit_automl_prs.py \
		--training-config /mnt/citrus/CITRUS/paper/workflows/aml_basil_vars/lgbm_v0h1_basil.json \
		--geno-parquet ${FILTER_OUT_DIR}/filtered_vars.parquet \
		--var-subsets ${FILTER_OUT_DIR}/filtered_vars.json \
		--pheno ${OUT_DIR}/${PHENO}_1ID.pheno \
		--covars ${PC_DIR}/pcs_1ID.tsv \
		--train-ids ${TEMP_DIR}/${TRAIN_SPLIT_FNAME} \
		--val-ids ${TEMP_DIR}/${VAL_SPLIT_FNAME} \
		--test-ids ${TEMP_DIR}/${TEST_SPLIT_FNAME} \
		-o ${OUT_DIR} "