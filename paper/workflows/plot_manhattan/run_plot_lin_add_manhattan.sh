# Plot Manhattan and QQ plots for GWAS

# HERIT=0625
# HERIT=125
HERIT=25
# HERIT=5
# HERIT=FULL

GWAS_OUT_DIR=../../output/GWAS

DOCKER_URL=gcr.io/ucsd-medicine-cast/nonlin_prs_prs_score_preds:latest

# Start docker env
module load singularitypro

# singularity shell --containall \
#     --bind /expanse/projects/gymreklab/rdevito:/mnt \
#     docker://${DOCKER_URL}

singularity exec --containall \
	--bind /expanse/projects/gymreklab/rdevito:/mnt \
	docker://${DOCKER_URL} \
	bash -c "cd /mnt/citrus/CITRUS/paper/workflows/plot_manhattan && \
	pip install geneview && \
	python3 plot_manhattan_lin_add.py \
		--herit ${HERIT} --gwas-out-dir ${GWAS_OUT_DIR} "