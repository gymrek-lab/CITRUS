# Run GEPSi simulation

HERIT='5'
PHENO=gepsi_lin_add_h${HERIT}_gcta

CONFIG_DIR=output/gcta_sim_configs
OUT_DIR=output/gcta_phenos
TEMP_DIR=/tmp

BED_DIR=data/geno_data/bed

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
	bash -c "cd /mnt/citrus/CITRUS/paper/workflows/gcta_pheno_sim && \
	mkdir -p ../../${OUT_DIR} && \
	./gcta-1.94.1-linux-kernel-3-x86_64/gcta64 \
		--bfile ../../${BED_DIR}/imputed_chr19 \
		--simu-qt \
		--simu-causal-loci ../../${CONFIG_DIR}/${PHENO}.csv \
		--simu-hsq 0.${HERIT} \
		--out ../../${OUT_DIR}/${PHENO} && \
	awk 'BEGIN {FS=\" \"; OFS=\"\\t\"; print \"FID\", \"IID\", \"phenotype\"} {print \$1, \$2, \$3}' \
		../../${OUT_DIR}/${PHENO}.phen > ../../${OUT_DIR}/${PHENO}.pheno "


#  --simu-hsq 0.${HERIT} \