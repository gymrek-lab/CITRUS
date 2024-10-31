# Run GEPSi simulation

HERIT='0625'
PHENO=gepsi_lin_add_h${HERIT}

GEPSI_DIR=output/gepsi_phenos
OUT_DIR=output/gcta_sim_configs
TEMP_DIR=/tmp

VAR_INFO=data/geno_data/chr19_var_info.csv

DOCKER_URL=gcr.io/ucsd-medicine-cast/gepsi:latest

# Start docker env
module load singularitypro

# singularity shell --containall \
#     --bind /expanse/projects/gymreklab/rdevito:/mnt \
#     docker://${DOCKER_URL}

# Run GEPSi simulation
singularity exec --containall \
	--bind /expanse/projects/gymreklab/rdevito:/mnt \
	docker://${DOCKER_URL} \
	bash -c "cd /mnt/citrus/CITRUS/paper/workflows/gepsi_to_gcta && \
	mkdir -p ../../${OUT_DIR} && \
	python3.9 gepsi_to_gcta.py \
		-g ../../${GEPSI_DIR} \
		-d ${PHENO} \
		-h2 0.${HERIT} \
		-v ../../${VAR_INFO} \
		-o ../../${OUT_DIR} "