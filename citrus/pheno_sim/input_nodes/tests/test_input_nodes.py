import numpy as np
import os
import pytest

from ..hail_input import *

# Set up hail config
## TODO what file formats does hail accept?

@pytest.fixture
def hail_config(tmpdir):
    hail_config = {}
    hail_config["file"] = ""
    hail_config["input_nodes"] = []
    # Required Hail fields
    hail_config["file_format"] = "vcf"
    hail_config["reference_genome"] = "GRCh37"
    hail_config["force_bgz"] = True
    return hail_config

# Checks on hail input node
def test_hail_input(hail_config, vcfdir):
	#### Test loading existing file and single input node
	hail_config["file"] = os.path.join(vcfdir, "example_gts_chr19.vcf.gz")
	hail_config["input_nodes"].append({
		"alias": "testvar1",
		"type": "SNP",
		"chr": "19",
		"pos": 280540	
	})
	hail = HailInputSource(hail_config)
	assert(len(hail.input_sample_ids) == 2504)
	assert(len(hail.input_node_ids) == 1)
	hail_config["input_nodes"].append({
		"alias": "testvar2",
		"type": "SNP",
		"chr": "19",
		"pos": 523746	
	})
	hail = HailInputSource(hail_config)
	# For single variants, vals is a tuple of two 
	# arrays, each with 0/1 for each of the 2504 samples
	# First index = haplotype
	# Second index = sample
	vals = hail.load_input_node("testvar1")
	assert(isinstance(vals, tuple))
	assert(len(vals[0])==2504)
	assert(vals[0].ndim == 1)
	assert(vals[0][0]==0)
	assert(vals[0][2]==1)
	assert(vals[0][4]==0)
	assert(vals[1][0]==0)
	assert(vals[1][2]==1)
	assert(vals[1][4]==1)

	vals = hail.load_input_node("testvar2")
	assert(isinstance(vals, tuple))
	assert(len(vals[0])==2504)
	assert(vals[0].ndim == 1)
	assert(vals[0][0]==0)
	assert(vals[0][2]==0)
	assert(vals[0][3]==1)
	assert(vals[1][0]==0)
	assert(vals[1][2]==0)
	assert(vals[1][4]==0)

	#### Test loading two variants
	hail_config["input_nodes"] = []
	hail_config["input_nodes"].append({
		"alias": "test2SNP",
		"type": "SNP",
		"chr": "19",
		"pos": [280540, 523746]
	})
	hail = HailInputSource(hail_config)
	# For two variants in the same node, vals is
	# a tuple of m-d arrays, where m is the number of variants
	# First index = haplotype
	# Second index = variant ID
	# Third index = sample
	vals = hail.load_input_node("test2SNP")
	assert(isinstance(vals, tuple))
	assert(vals[0].ndim == 2)
	assert(vals[0][0][0]==0)
	assert(vals[0][0][2]==1)
	assert(vals[0][0][4]==0)
	assert(vals[1][0][0]==0)
	assert(vals[1][0][2]==1)
	assert(vals[1][0][4]==1)

	assert(vals[0][1][0]==0)
	assert(vals[0][1][2]==0)
	assert(vals[0][1][3]==1)
	assert(vals[0][1][4]==0)
	assert(vals[1][1][0]==0)
	assert(vals[1][1][2]==0)
	assert(vals[1][1][3]==0)
	assert(vals[1][1][4]==0)

# Checks on loading subsets of samples
def test_hail_input_samples(hail_config, vcfdir):
	hail_config["file"] = os.path.join(vcfdir, "example_gts_chr19.vcf.gz")
	hail_config["input_nodes"].append({
		"alias": "testvar1",
		"type": "SNP",
		"chr": "19",
		"pos": 280540	
	})
	hail = HailInputSource(hail_config)
	vals = hail.load_input_node("testvar1", ["HG00096", "HG00101"])
	assert(isinstance(vals, tuple))
	assert(len(vals[0])==2)
	assert(vals[0].ndim == 1)
	assert(vals[0][0]==0)
	assert(vals[0][1]==0)
	assert(vals[1][0]==0)
	assert(vals[1][1]==1)

	# TODO - test wrong samples
	assert(True)

# Checks on hail input node with wrong input
def test_hail_input_wronginput(hail_config, vcfdir):
	# test missing config fields
	new_hail_config = hail_config.copy()
	del new_hail_config["file_format"]
	with pytest.raises(KeyError):
		HailInputSource(new_hail_config)
	new_hail_config = hail_config.copy()
	del new_hail_config["reference_genome"]
	with pytest.raises(KeyError):
		HailInputSource(new_hail_config)
	new_hail_config = hail_config.copy()
	del new_hail_config["force_bgz"]
	with pytest.raises(KeyError):
		HailInputSource(new_hail_config)
		
	# test unsupported file format
	new_hail_config = hail_config.copy()
	new_hail_config["file_format"] = "txt"
	with pytest.raises(ValueError):
		HailInputSource(new_hail_config)

	# TODO - test wrong file
	# TODO - test unindexed file
	# TODO - test wrong file format
	# TODO - test wrong node id
	assert(True)