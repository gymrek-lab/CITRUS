import argparse

parser = argparse.ArgumentParser(
        prog = 'citrusIO',
        description = "IO files for citrus"
        )

parser.add_argument(
        '-g',
        dest = 'genotypes', 
        type = str, 
        help = ".vcf file for genotype (input)"
        )
parser.add_argument(
        '-m',
        dest = 'model',
        type = str,
        help = ".json file for model (input)"
        )
parser.add_argument(
        '-p',
        dest = 'simPhen',
        type = str,
        help = ".phen file for simulated phenotypes (output)"
        )
parser.add_argument(
        '-s',
        dest = 'shapVals',
        type = str,
        help = ".tab file for SHAP values (output)"
        )

args = parser.parse_args()
