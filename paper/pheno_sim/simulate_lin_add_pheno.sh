# Simulate phenotypes using CITRUS

OUTPUT_DIR=citrus_output

N_VARS=(10 100 1000)
H_VALS=(05 1 2 4 8)
VERSION_NUM=1

# Loop over number of variables and heritability
for N_VAR in "${N_VARS[@]}"; do
	for H_VAL in "${H_VALS[@]}"; do
		SIM_NAME=lin_add_nvar${N_VAR}_h${H_VAL}_v${VERSION_NUM}
		SIM_CONFIG_FILE=sim_configs/${SIM_NAME}

		# Run citrus simulate

		JAVA_HOME=/home/rdevito/anaconda3/envs/citrus_env/

		citrus simulate \
			-c ${SIM_CONFIG_FILE} \
			-o ${OUTPUT_DIR} \
			-f ${SIM_NAME}.csv \
			--output_config_filename ${SIM_NAME}_config.json

		# Rewrite phenotype in plink format
		python citrus_out_to_plink_fmt.py ${SIM_NAME}
	done
done