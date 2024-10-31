# Score PRS predictions

PHENO_DIR=pheno_sim/citrus_phenos
SPLITS_DIR=data/splits
TEMP_DIR=/tmp

DOCKER_URL=gcr.io/ucsd-medicine-cast/nonlin_prs_prs_score_preds:latest

# Start docker env
module load singularitypro

singularity exec --containall \
    --bind /expanse/projects/gymreklab/rdevito:/mnt \
    docker://${DOCKER_URL} \
    bash -c "cd /mnt/citrus/CITRUS/paper/workflows/plot_all && \
	pip install tqdm && \
	python3 plot_all.py "