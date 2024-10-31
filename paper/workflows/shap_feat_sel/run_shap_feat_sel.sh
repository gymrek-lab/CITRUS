# Get local SHAP values

# PHENO=mult_pheno_1
# PHENO=mult_pheno_2
# PHENO=xor_pheno_1
# PHENO=xor_pheno_2
# PHENO=compound_het
# PHENO=compound_het_2
# PHENO=gepsi_lin_add_h0625_h0625
# PHENO=gepsi_lin_add_h125_h125
PHENO=gepsi_lin_add_h25_h25
# PHENO=gepsi_lin_add_h5_h5
# PHENO=gepsi_lin_add_hFULL_hFULL

echo ${PHENO}

OUT_DIR=../output/shap_feat_sel/${PHENO}
TEMP_DIR=/tmp

VAR_INFO=../data/geno_data/chr19_var_info.csv

BASIL_OUT_DIR=../output/aml_filter_vars_basil/${PHENO}
PRSICE_OUT_DIR=../output/aml_filter_vars_prsice/${PHENO}
THRESH_OUT_DIR=../output/aml_filter_vars/${PHENO}
THRESH_BEST_DIR=../output/aml_thresh_vars/${PHENO}

SHAP_DIR=../output/shap_per_loci/${PHENO}

DOCKER_URL=gcr.io/ucsd-medicine-cast/citrus:latest

# Start docker env
module load singularitypro

# singularity shell --containall \
#     --bind /expanse/projects/gymreklab/rdevito:/mnt \
#     docker://${DOCKER_URL}

singularity exec --containall \
    --bind /expanse/projects/gymreklab/rdevito:/mnt \
    docker://${DOCKER_URL} \
    bash -c "cd /mnt/citrus/CITRUS/paper/workflows && \
	mkdir -p ${OUT_DIR} && \
	python3 shap_feat_sel/shap_by_feat_sel.py \
		-s ${SHAP_DIR}/comb_shap_vals.csv \
		-b ${BASIL_OUT_DIR}/filtered_vars.json \
		-p ${PRSICE_OUT_DIR}/filtered_vars.json \
		-t ${THRESH_OUT_DIR}/filtered_vars.json \
		-m ${THRESH_BEST_DIR}/best_model_config.json \
		-v ${VAR_INFO} \
		-o ${OUT_DIR} "
