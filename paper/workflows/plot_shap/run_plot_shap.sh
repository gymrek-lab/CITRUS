# Plot feature selection performance

PHENO_DIR=pheno_sim/citrus_phenos
SPLITS_DIR=data/splits
TEMP_DIR=/tmp

DOCKER_URL=gcr.io/ucsd-medicine-cast/nonlin_prs_prs_score_preds:latest

# Start docker env
module load singularitypro

# singularity shell --containall \
#     --bind /expanse/projects/gymreklab/rdevito:/mnt \
#     docker://${DOCKER_URL}

singularity exec --containall \
	--bind /expanse/projects/gymreklab/rdevito:/mnt \
	docker://${DOCKER_URL} \
	bash -c "cd /mnt/citrus/CITRUS/paper/workflows/plot_shap && \
	python3 plot_shap.py "