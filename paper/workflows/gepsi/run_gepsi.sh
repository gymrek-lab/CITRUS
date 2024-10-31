# Run GEPSi simulation

HERIT='001'

# Check if HERIT is equal to FULL
if [ "$HERIT" = "FULL" ]; then
    HERIT_FLOAT=1.0
else
    HERIT_FLOAT="0.${HERIT}"
fi

N_CAUSAL=2

# Check if N_CAUSAL is 100
if [ "$N_CAUSAL" -eq 100 ]; then
    OUT_DIR="output/gepsi_sim_out/lin_add_h${HERIT}"
else
    OUT_DIR="output/gepsi_sim_out/lin_add_n${N_CAUSAL}_h${HERIT}"
fi

DATA_DIR=output/gepsi_fmt_data
TEMP_DIR=/tmp

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
    bash -c "cd /mnt/citrus/CITRUS/paper && \
	pip install PyYAML && \
	mkdir -p ${OUT_DIR} && \
	cd ${OUT_DIR} && \
	gepsi phenotype \
		-dp ../../../${DATA_DIR}/ \
		-data chr19_None \
		--heritability ${HERIT_FLOAT} \
		-pname phenotype \
		-cut 0.0 \
		-mask 0.0 \
		-df 0.0 \
		-rf 0.0 \
		-cf 0.0 \
		-num_snps ${N_CAUSAL} \
		--causal_snp_mode random "

# Remember to manually move output to the output dir this creates 
# --heritability 0.${HERIT} \