# Run GEPSi simulation

OUT_DIR=output/gepsi_fmt_data
TEMP_DIR=/tmp

GENO_DIR=data/geno_data/pgen
PGEN_FNAME=imputed_chr19_1ID

SAMPLE_FILE=data/splits/all_samples.txt

PLINK_DOCKER_URL=gcr.io/ucsd-medicine-cast/nonlin_prs_prs_aml_filter_vars:latest
GEPSI_DOCKER_URL=gcr.io/ucsd-medicine-cast/gepsi:latest

# Start docker env
module load singularitypro

# singularity shell --containall \
#     --bind /expanse/projects/gymreklab/rdevito:/mnt \
#     docker://${DOCKER_URL}

singularity exec --containall \
    --bind /expanse/projects/gymreklab/rdevito:/mnt \
    docker://${PLINK_DOCKER_URL} \
    bash -c "cd /mnt/citrus/CITRUS/paper && \
	mkdir -p ${OUT_DIR} && \
	plink2 \
		--pfile ${GENO_DIR}/${PGEN_FNAME} \
		--geno 0 \
		--maf 0.01 \
		--make-just-bim \
		--out ${OUT_DIR}/chr19 \
	&& \
	plink2 \
		--pfile ${GENO_DIR}/${PGEN_FNAME} \
		--geno 0 \
		--maf 0.01 \
		--export A \
		--out ${OUT_DIR}/chr19 "

singularity exec --containall \
	--bind /expanse/projects/gymreklab/rdevito:/mnt \
	docker://${GEPSI_DOCKER_URL} \
	bash -c "cd /mnt/citrus/CITRUS/paper/${OUT_DIR} && \
	ls && \
	gepsi genotype \
		--config genotype.yaml "
