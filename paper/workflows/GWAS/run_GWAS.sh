# Run Plink2 GWAS on CITRUS simulated phenotype

# PHENO=complex_pheno_1
# PHENO=complex_pheno_1_noise
# PHENO=complex_pheno_2
# PHENO=complex_pheno_3
# PHENO=complex_pheno_4
# PHENO=mult_pheno_1_more_noise
# PHENO=mult_pheno_1
# PHENO=mult_pheno_2
# PHENO=xor_pheno_1
# PHENO=xor_pheno_2
# PHENO=lin_add_nvar100_h05_v1
# PHENO=lin_add_nvar100_h1_v1
# PHENO=lin_add_nvar100_h2_v1
# PHENO=lin_add_nvar100_h4_v1
# PHENO=lin_add_nvar100_h8_v1
# PHENO=lin_add_nvar1000_h2_v1
# PHENO=lin_add_nvar1000_h4_v1
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
# PHENO=gepsi_lin_add_n10_hFULL
PHENO=gepsi_lin_add_n2_h001

# PHENO=gepsi_lin_add_h0625_gcta
# PHENO=gepsi_lin_add_h125_gcta
# PHENO=gepsi_lin_add_h25_gcta
# PHENO=gepsi_lin_add_h5_gcta
# PHENO=gepsi_lin_add_hFULL_gcta

# PHENO_DIR=pheno_sim/citrus_phenos
PHENO_DIR=output/gepsi_phenos
# PHENO_DIR=output/gcta_phenos

echo ${PHENO}
echo ${PHENO_DIR}

SPLITS_DIR=data/splits
TRAIN_SPLIT_FNAME=train_samples.txt
GENO_DIR=data/geno_data/pgen
PGEN_FNAME=imputed_chr19
PC_FNAME=data/geno_data/PCs/pcs.tsv

DOCKER_URL=gcr.io/ucsd-medicine-cast/nonlin_prs_gwas_plink2:latest

# Start docker env
module load singularitypro

singularity exec --containall \
    --bind /expanse/projects/gymreklab/rdevito:/mnt \
    docker://${DOCKER_URL} \
    bash -c "cd /mnt/citrus/CITRUS/paper && \
	plink2 --glm 'hide-covar' \
    	--pfile ${GENO_DIR}/${PGEN_FNAME} \
    	--keep ${SPLITS_DIR}/${TRAIN_SPLIT_FNAME} \
    	--pheno ${PHENO_DIR}/${PHENO}.pheno \
		--covar ${PC_FNAME} \
    	--out output/GWAS/${PHENO}"