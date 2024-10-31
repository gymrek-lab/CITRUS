# Get local SHAP values

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
PHENO=gepsi_lin_add_hFULL_hFULL

echo ${PHENO}

TEMP_DIR=/tmp
OUT_DIR=../output/shap/${PHENO}

SIM_OUT_DIR=../pheno_sim/citrus_output
SIM_CONFIG=${SIM_OUT_DIR}/${PHENO}_config.json

SPLITS_DIR=../data/splits
TEST_SPLIT_FNAME=test_samples.txt

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
	export SPARK_DRIVER_MEMORY=100G && \
	export SPARK_EXECUTOR_MEMORY=100G && \
	export SPARK_LOCAL_DIRS=/mnt/tmp && \
	export SPARK_WORKER_DIR=/mnt/tmp && \
	awk -v OFS='\t' '{ print \$1\"_\"\$1 }' ${SPLITS_DIR}/${TEST_SPLIT_FNAME} > \
		${TEMP_DIR}/${TEST_SPLIT_FNAME} \
	&& \
	mkdir -p ${OUT_DIR} && \
	citrus shap \
		-c ${SIM_CONFIG} \
		-i ${TEMP_DIR}/${TEST_SPLIT_FNAME} \
		-s ${OUT_DIR}/shap_vals.csv "
