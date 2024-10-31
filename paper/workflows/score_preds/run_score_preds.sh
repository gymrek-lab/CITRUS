# Score PRS predictions

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

# MODEL_TYPE=prsice
# MODEL_TYPE=basil
# MODEL_TYPE=lgbm_thresh
# MODEL_TYPE=lgbm_prsice
MODEL_TYPE=lgbm_basil

echo ${MODEL_TYPE}

if [ "$MODEL_TYPE" = prsice ]; then
	MODEL_OUT_DIR=output/prsice/${PHENO}
elif [ "$MODEL_TYPE" = basil ]; then
	MODEL_OUT_DIR=output/basil/${PHENO}
elif [ "$MODEL_TYPE" = lgbm_basil ]; then
	MODEL_OUT_DIR=output/aml_basil_vars/${PHENO}
elif [ "$MODEL_TYPE" = lgbm_prsice ]; then
	MODEL_OUT_DIR=output/aml_prsice_vars/${PHENO}
elif [ "$MODEL_TYPE" = lgbm_thresh ]; then
	MODEL_OUT_DIR=output/aml_thresh_vars/${PHENO}
else
	echo "Invalid model type"
	exit 1 
fi

SPLITS_DIR=data/splits
TEMP_DIR=/tmp

DOCKER_URL=gcr.io/ucsd-medicine-cast/nonlin_prs_prs_score_preds:latest

# Start docker env
module load singularitypro

singularity exec --containall \
    --bind /expanse/projects/gymreklab/rdevito:/mnt \
    docker://${DOCKER_URL} \
    bash -c "cd /mnt/citrus/CITRUS/paper && \
	awk -v OFS='\t' '{ print \$2, \$3 }' ${PHENO_DIR}/${PHENO}.pheno > \
		${TEMP_DIR}/reformatted_${PHENO}.tsv \
	&& \
	python3 /mnt/citrus/CITRUS/paper/workflows/score_preds/score_preds.py \
		--val-preds ${MODEL_OUT_DIR}/val_preds.csv \
		--test-preds ${MODEL_OUT_DIR}/test_preds.csv \
		--pheno-file ${TEMP_DIR}/reformatted_${PHENO}.tsv \
		--wb ${SPLITS_DIR}/wb_samples.txt \
		--out-dir ${MODEL_OUT_DIR}"