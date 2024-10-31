# Simulate phenotypes using CITRUS

# PHENO=complex_pheno_1
# PHENO=complex_pheno_1_noise
# PHENO=complex_pheno_2
# PHENO=complex_pheno_3
# PHENO=complex_pheno_4
# PHENO=mult_pheno_1_more_noise
# PHENO=mult_pheno_1
# PHENO=mult_pheno_2
PHENO=xor_pheno_1
# PHENO=xor_pheno_2
# PHENO=lin_add_nvar1000_h2_v1
# PHENO=lin_add_nvar1000_h4_v1
# PHENO=compound_het
# PHENO=compound_het_2
# PHENO=gepsi_lin_add_h0625_h0625
# PHENO=gepsi_lin_add_h125_h125
# PHENO=gepsi_lin_add_h25_h25
# PHENO=gepsi_lin_add_h5_h5
# PHENO=gepsi_lin_add_hFULL_hFULL

echo ${PHENO}

OUTPUT_DIR=citrus_output
SIM_CONFIG_FILE=sim_configs/${PHENO}.json

TEMP_DIR=/tmp
DOCKER_URL=gcr.io/ucsd-medicine-cast/citrus:latest

# Run citrus simulate in docker
module load singularitypro

# singularity shell --containall \
#     --bind /expanse/projects/gymreklab/rdevito:/mnt \
#     docker://gcr.io/ucsd-medicine-cast/citrus:latest

singularity exec --containall --cleanenv --writable-tmpfs \
	--bind /expanse/projects/gymreklab/rdevito:/mnt \
	docker://${DOCKER_URL} \
	bash -c "cd /mnt/citrus/CITRUS/paper/pheno_sim/ && \
	JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64 && \
	export SPARK_DRIVER_MEMORY=50G && \
	export SPARK_EXECUTOR_MEMORY=50G && \
	citrus simulate \
		-c ${SIM_CONFIG_FILE} \
		-o ${OUTPUT_DIR} \
		-f ${PHENO}.csv \
		--output_config_filename ${PHENO}_config.json \
	&& \
	python3 citrus_out_to_plink_fmt.py ${PHENO} "
