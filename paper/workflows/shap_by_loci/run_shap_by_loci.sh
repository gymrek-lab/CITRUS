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

OUT_DIR=../output/shap_per_loci/${PHENO}
TEMP_DIR=/tmp

SHAP_OUT_DIR=../output/shap/${PHENO}
SIM_OUT_DIR=../pheno_sim/citrus_output
SIM_CONFIG=${SIM_OUT_DIR}/${PHENO}_config.json

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
	python3 shap_by_loci/shap_by_loci.py \
		-s ${SHAP_OUT_DIR}/shap_vals.csv \
		-c ${SIM_CONFIG} \
		-o ${OUT_DIR} "
