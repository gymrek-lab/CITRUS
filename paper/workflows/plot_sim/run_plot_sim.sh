# Plot simulation graph

# PHENO=complex_pheno_1
# PHENO=complex_pheno_1_noise
# PHENO=complex_pheno_2
# PHENO=complex_pheno_3
# PHENO=complex_pheno_4
# PHENO=mult_pheno_1_more_noise
# PHENO=mult_pheno_1
# PHENO=mult_pheno_2
# PHENO=xor_pheno_1
# PHENO=lin_add_nvar1000_h2_v1
# PHENO=lin_add_nvar1000_h4_v1
# PHENO=compound_het
PHENO=gepsi_lin_add_h25_h25

echo ${PHENO}

TEMP_DIR=/tmp
SIM_CONFIG=sim_configs

DOCKER_URL=gcr.io/ucsd-medicine-cast/citrus:latest
N_THREADS=$(lscpu | grep "^CPU(s):" | awk '{print $2}')

# Start docker env
module load singularitypro

# singularity shell --containall \
#     --bind /expanse/projects/gymreklab/rdevito:/mnt \
#     docker://gcr.io/ucsd-medicine-cast/citrus:latest

singularity exec --containall --cleanenv --writable-tmpfs \
    --bind /expanse/projects/gymreklab/rdevito:/mnt \
    docker://${DOCKER_URL} \
    bash -c "cd /mnt/citrus/CITRUS/paper/pheno_sim/ && \
	citrus plot \
		--config_file ${SIM_CONFIG}/${PHENO}.json \
		--out ${SIM_CONFIG}/${PHENO} \
		--format png "