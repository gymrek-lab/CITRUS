# Run PRSice2 PRS on CITRUS simulated phenotype


# PHENO=mult_pheno_1
# PHENO=mult_pheno_2
# PHENO=xor_pheno_1
# PHENO=xor_pheno_2
# PHENO=compound_het
# PHENO=compound_het_2
# PHENO=gepsi_lin_add_h0625_h0625
# PHENO=gepsi_lin_add_h125_h125
# PHENO=gepsi_lin_add_h25_h25
# PHENO=gepsi_lin_add_h5_h5
# PHENO=gepsi_lin_add_hFULL_hFULL

# PHENO=gepsi_lin_add_h0625
# PHENO=gepsi_lin_add_h125
# PHENO=gepsi_lin_add_h25
# PHENO=gepsi_lin_add_h5
# PHENO=gepsi_lin_add_hFULL

# PHENO=gepsi_lin_add_h0625_gcta
# PHENO=gepsi_lin_add_h125_gcta
# PHENO=gepsi_lin_add_h25_gcta
# PHENO=gepsi_lin_add_h5_gcta
PHENO=gepsi_lin_add_hFULL_gcta

# PHENO_DIR=pheno_sim/citrus_phenos
# PHENO_DIR=output/gepsi_phenos
PHENO_DIR=output/gcta_phenos

echo ${PHENO}
echo ${PHENO_DIR}

TEMP_DIR=/tmp
OUT_DIR=output/prsice/${PHENO}
GWAS_OUT_DIR=output/GWAS

SPLITS_DIR=data/splits
VAL_SPLIT_FNAME=val_samples.txt
TEST_SPLIT_FNAME=test_samples.txt
GENO_DIR=data/geno_data/bed
BED_FNAME=imputed_chr19
PC_DIR=data/geno_data/PCs

DOCKER_URL=gcr.io/ucsd-medicine-cast/nonlin_prs_prs_prsice2:latest
N_THREADS=$(lscpu | grep "^CPU(s):" | awk '{print $2}')

# Start docker env
module load singularitypro

# singularity shell --containall \
#     --bind /expanse/projects/gymreklab/rdevito:/mnt \
#     docker://${DOCKER_URL}

singularity exec --containall \
    --bind /expanse/projects/gymreklab/rdevito:/mnt \
    docker://${DOCKER_URL} \
    bash -c "cd /mnt/citrus/CITRUS/paper && \
	mkdir -p ${OUT_DIR} && \
	echo 'made out dir' && \
    PRSice_linux \
        --base ${GWAS_OUT_DIR}/${PHENO}.phenotype.glm.linear \
        --extract ${GENO_DIR}/prsice_valid_SNPs.valid \
        --A1 A1 \
        --beta \
        --bp POS \
        --chr '#CHROM' \
        --snp ID \
        --pvalue P \
        --target ${GENO_DIR}/${BED_FNAME} \
        --nonfounders \
        --keep ${SPLITS_DIR}/${VAL_SPLIT_FNAME} \
        --ignore-fid \
        --pheno ${PHENO_DIR}/${PHENO}.pheno \
		--cov ${PC_DIR}/pcs.tsv \
        --thread ${N_THREADS} \
        --out ${OUT_DIR}/prs_prsice2_${PHENO} \
    && \
    BEST_P_THRESH=\$(tail -n 1 ${OUT_DIR}/prs_prsice2_${PHENO}.summary | awk '{print \$3}') \
    && \
    echo \${BEST_P_THRESH} \
	&& \
	printf 'best_p 0.0 %s\n' \"\$BEST_P_THRESH\" > \"${OUT_DIR}/prsice2_${PHENO}_best_p_thresh.txt\" \
	&& \
	head ${OUT_DIR}/prsice2_${PHENO}_best_p_thresh.txt \
	&& \
	plink2 \
		--bfile ${GENO_DIR}/${BED_FNAME} \
		--extract ${GENO_DIR}/prsice_valid_SNPs.valid \
		--clump-p1 1 \
		--clump-r2 0.1 \
		--clump-kb 250 \
		--clump ${GWAS_OUT_DIR}/${PHENO}.phenotype.glm.linear \
		--out ${OUT_DIR}/prs_prsice2_clump_${PHENO} \
	&& \
	echo MKDIR \
	&& \
	mkdir -p ${OUT_DIR} \
	&& \
	plink2 \
		--bfile ${GENO_DIR}/${BED_FNAME} \
		--score ${GWAS_OUT_DIR}/${PHENO}.phenotype.glm.linear 3 7 12 header \
		--extract ${OUT_DIR}/prs_prsice2_clump_${PHENO}.clumps \
		--q-score-range ${OUT_DIR}/prsice2_${PHENO}_best_p_thresh.txt \
			${GWAS_OUT_DIR}/${PHENO}.phenotype.glm.linear 3 15 header \
		--out ${OUT_DIR}/prs_prsice2_score_${PHENO} \
	&& \
	awk -v OFS='\t' '{ print \$2, \$3 }' ${PHENO_DIR}/${PHENO}.pheno > \
		${OUT_DIR}/reformatted_${PHENO}.tsv \
	&& \
	python3 /home/fit_wrapper.py \
		--pheno-file ${OUT_DIR}/reformatted_${PHENO}.tsv \
		--covar-file ${PC_DIR}/pcs_just_IID.tsv \
		--score-file ${OUT_DIR}/prs_prsice2_score_${PHENO}.best_p.sscore \
		--val-iids ${SPLITS_DIR}/${VAL_SPLIT_FNAME} \
		--test-iids ${SPLITS_DIR}/${TEST_SPLIT_FNAME} \
		--out-dir ${OUT_DIR} "