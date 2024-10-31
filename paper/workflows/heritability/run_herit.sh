# Estimate heritability

TEMP_DIR=/tmp

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
	export SPARK_DRIVER_MEMORY=10G && \
	export SPARK_EXECUTOR_MEMORY=10G && \
	export SPARK_DRIVER_MEMORY_OVERHEAD=3g && \
	export SPARK_EXECUTOR_MEMORY_OVERHEAD=3g && \
	python3 est_heritability.py "

	# export SPARK_DRIVER_MEMORY=10G && \
	# export SPARK_EXECUTOR_MEMORY=10G && \
	# export SPARK_DRIVER_MEMORY_OVERHEAD=50g && \
	# export SPARK_EXECUTOR_MEMORY_OVERHEAD=50g && \