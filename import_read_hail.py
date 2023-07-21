from hail import import_vcf
from hail import read_matrix_table
if __name__ == "__main__":
    # data = import_vcf(
    #     'pheno_sim_demos/1000_genomes_data/ALL.chr19.phase3_shapeit2_mvncall_integrated_v5b.20130502.genotypes.vcf.gz',
    #     force_bgz=True,
    #     reference_genome="GRCh37")
    
    # data.write('output.mt')
    data = read_matrix_table('output.mt')

    
    
    
        # 'pheno_sim/shap/test_configs/simple_sim.json', 