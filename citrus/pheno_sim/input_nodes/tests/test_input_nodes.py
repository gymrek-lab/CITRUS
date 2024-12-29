import numpy as np
import os
import pytest

from ..hail_input import *
import hail as hl

##### Note: sometimes these tests give a weird
##### spark error? Solved when disconnected from
##### the internet?

# Set up hail config
@pytest.fixture
def hail_config(tmpdir):
    hail_config = {}
    hail_config["engine"] = "hail"
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

	# Make chr a list
	hail_config["input_nodes"] = []
	hail_config["input_nodes"].append({
		"alias": "multisnp",
		"type": "SNP",
		"chr": ["19", "19"],
		"pos": [280540, 523746]
	})
	hail = HailInputSource(hail_config)
	vals = hail.load_input_node("multisnp")

def test_hail_input_samples(hail_config, vcfdir):
	#### Test inputting samples
	hail_config["file"] = os.path.join(vcfdir, "example_gts_chr19.vcf.gz")
	hail_config["input_nodes"] = []
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

	# now with multi-SNP input
	hail_config["input_nodes"] = []
	hail_config["input_nodes"].append({
		"alias": "test2SNP",
		"type": "SNP",
		"chr": "19",
		"pos": [280540, 523746]
	})
	hail = HailInputSource(hail_config)
	vals = hail.load_input_node("test2SNP", ["HG00096", "HG00101"])
	assert(isinstance(vals, tuple))
	assert(len(vals[0])==2)
	assert(vals[0].ndim == 2)

def test_hail_badinput(hail_config, vcfdir):
	#### test missing config fields
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
		
	#### test unsupported file format
	new_hail_config = hail_config.copy()
	new_hail_config["file_format"] = "txt"
	with pytest.raises(ValueError):
		HailInputSource(new_hail_config)

	#### test duplicate rows
	new_hail_config = hail_config.copy()
	new_hail_config["file"] = os.path.join(vcfdir, "duplicate_row.vcf.gz")
	new_hail_config["input_nodes"] = []
	new_hail_config["input_nodes"].append({
		"alias": "testdupSNP",
		"type": "SNP",
		"chr": "19",
		"pos": 523746
	})
	hail = HailInputSource(new_hail_config)
	with pytest.raises(ValueError):
		hail.load_input_node("testdupSNP")

	#### test non-existing SNP
	new_hail_config["input_nodes"] = []
	new_hail_config["input_nodes"].append({
		"alias": "doesnotexist",
		"type": "SNP",
		"chr": "19",
		"pos": 12345
	})
	hail = HailInputSource(new_hail_config)
	with pytest.raises(ValueError):
		hail.load_input_node("doesnotexist")

	#### Test malformatted multi-variant
	new_hail_config["input_nodes"] = []
	new_hail_config["input_nodes"].append({
		"alias": "badvar1",
		"type": "SNP",
		"chr": ["19","2"],
		"pos": 12345
	})
	hail = HailInputSource(new_hail_config)
	with pytest.raises(ValueError):
		hail.load_input_node("badvar1")

	new_hail_config["input_nodes"] = []
	new_hail_config["input_nodes"].append({
		"alias": "badvar2",
		"type": "SNP",
		"chr": ["19","2"],
		"pos": [12345, 2345, 3456]
	})
	hail = HailInputSource(new_hail_config)
	with pytest.raises(ValueError):
		hail.load_input_node("badvar2")

	# test nonexisting file
	new_hail_config = hail_config.copy()
	new_hail_config["file"] = "/xxx/does/not/exist"
	with pytest.raises(hl.utils.java.FatalError):
		HailInputSource(new_hail_config)

	# test unindexed file - works in Hail
	new_hail_config = hail_config.copy()
	new_hail_config["file"] = os.path.join(vcfdir, "unindexed.vcf.gz")
	HailInputSource(new_hail_config)

	# test unzipped file - works in Hail
	new_hail_config = hail_config.copy()
	new_hail_config["file"] = os.path.join(vcfdir, "nozip.vcf")
	HailInputSource(new_hail_config)

	# test bad file format
	new_hail_config = hail_config.copy()
	new_hail_config["file"] = os.path.join(vcfdir, "not_a_vcf.txt")
	with pytest.raises(hl.utils.java.FatalError):
		HailInputSource(new_hail_config)

	# test wrong node id
	hail_config["file"] = os.path.join(vcfdir, "example_gts_chr19.vcf.gz")
	hail_config["input_nodes"] = []
	hail_config["input_nodes"].append({
		"alias": "testvar1",
		"type": "SNP",
		"chr": "19",
		"pos": 280540	
	})
	hail = HailInputSource(hail_config)
	with pytest.raises(ValueError):
		vals = hail.load_input_node("badnodeid")

	# test wrong samples
	with pytest.raises(ValueError):
		vals = hail.load_input_node("testvar1", ["not_a_sample"])
