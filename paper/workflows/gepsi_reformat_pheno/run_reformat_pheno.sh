# Run GEPSi simulation

HERIT='001'
N_CAUSAL=2

# Check if N_CAUSAL is 100
if [ "$N_CAUSAL" -eq 100 ]; then
	FNAME=lin_add_h${HERIT}
    SIM_DIR="output/gepsi_sim_out/${FNAME}"
else
	FNAME=lin_add_n${N_CAUSAL}_h${HERIT}
    SIM_DIR="output/gepsi_sim_out/${FNAME}"
fi

OUT_DIR=output/gepsi_phenos
DATA_DIR=output/gepsi_fmt_data

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
    bash -c "cd /mnt/citrus/CITRUS/paper/workflows/gepsi_reformat_pheno && \
	mkdir -p ../../${OUT_DIR} && \
	python3.9 reformat_pheno.py \
		-g ../../${SIM_DIR} \
		-d chr19_None \
		-s ../../${DATA_DIR}/snplist_chr19_None.csv \
		-samp ../../${DATA_DIR}/sample_ids.txt \
		-o ../../${OUT_DIR} \
		-p gepsi_${FNAME} "