# Run BASIL PRS on CITRUS simulated phenotype

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

PHENO=gepsi_lin_add_h0625_gcta
# PHENO=gepsi_lin_add_h125_gcta
# PHENO=gepsi_lin_add_h25_gcta
# PHENO=gepsi_lin_add_h5_gcta
# PHENO=gepsi_lin_add_hFULL_gcta

# PHENO_DIR=pheno_sim/citrus_phenos
# PHENO_DIR=output/gepsi_phenos
PHENO_DIR=output/gcta_phenos

echo ${PHENO}
echo ${PHENO_DIR}

R_SCRIPT=workflows/basil/run_basil_expanse.R
R_SCRIPT_COVAR=workflows/basil/run_basil_expanse_covars.R
TEMP_DIR=/tmp
OUT_DIR=output/basil/${PHENO}
GWAS_OUT_DIR=output/GWAS

SPLITS_DIR=data/splits
TRAIN_SPLIT_FNAME=train_samples.txt
VAL_SPLIT_FNAME=val_samples.txt
TEST_SPLIT_FNAME=test_samples.txt
GENO_DIR=data/geno_data/pgen
PGEN_FNAME=imputed_chr19_1ID
PC_DIR=data/geno_data/PCs

DOCKER_URL=gcr.io/ucsd-medicine-cast/nonlin_prs_prs_basil:latest
N_THREADS=$(lscpu | grep "^CPU(s):" | awk '{print $2}')

# Start docker env
module load singularitypro

# With PC covars
singularity exec --containall \
    --bind /expanse/projects/gymreklab/rdevito:/mnt \
    docker://${DOCKER_URL} \
    bash -c "cd /mnt/citrus/CITRUS/paper && \
    Rscript ${R_SCRIPT_COVAR} \
		--pheno_file ${PHENO_DIR}/${PHENO}.pheno \
		--pheno_name phenotype \
		--covar_file ${PC_DIR}/pcs.tsv \
		--pheno_desc ${PHENO} \
		--geno_file ${GENO_DIR}/${PGEN_FNAME} \
		--train_samples ${SPLITS_DIR}/${TRAIN_SPLIT_FNAME} \
		--val_samples ${SPLITS_DIR}/${VAL_SPLIT_FNAME} \
		--test_samples ${SPLITS_DIR}/${TEST_SPLIT_FNAME} \
		--alpha 1.0 \
		--n_iter 20 "

# w/o covars
# singularity exec --containall \
#     --bind /expanse/projects/gymreklab/rdevito:/mnt \
#     docker://${DOCKER_URL} \
#     bash -c "cd /mnt/citrus/CITRUS/paper && \
#     Rscript ${R_SCRIPT} \
# 		--pheno_file ${PHENO_DIR}/${PHENO}.pheno \
# 		--pheno_name phenotype \
# 		--pheno_desc ${PHENO} \
# 		--geno_file ${GENO_DIR}/${PGEN_FNAME} \
# 		--train_samples ${SPLITS_DIR}/${TRAIN_SPLIT_FNAME} \
# 		--val_samples ${SPLITS_DIR}/${VAL_SPLIT_FNAME} \
# 		--test_samples ${SPLITS_DIR}/${TEST_SPLIT_FNAME} \
# 		--alpha 1.0 \
# 		--n_iter 20 "
