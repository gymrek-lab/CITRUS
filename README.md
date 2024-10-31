# CITRUS🍊: A phenotype simulation tool with the flexibility to model complex interactions

CITRUS, the CIs and Trans inteRaction nUmerical Simulator, is a collection of tools for simulating phenotypes with complex genetic architectures that go beyond simple models that assume linear, additive contributions of individual SNPs. The goal of CITRUS is to provide better simulations for benchmarking GWAS/PRS models.

The key component of CITRUS is the ability to specify custom models relating genotypes to phenotypes. See the [designing simulations](doc/designing_simulations.md) for details on specifying models. Example models are provided in `example-files/`.

CITRUS provides multiple command line utilities for performing and analyzing simulations:

* [citrus simulate](doc/cli.md#simulate): Perform a simulation using a given model
* [citrus plot](doc/cli.md#plot): Visualize a phenotype model
* [citrus shap](doc/cli.md#shap): Generate SHAP values for a model

## Installation

### With conda 

**TODO - conda install instructions**

### With pip 

**TODO - pip install instructions**

### From source

To install from source (only recommended for development), clone the CITRUS repository and checkout the branch you're interested in:

```bash
git clone https://github.com/gymrek-lab/CITRUS.git
cd CITRUS
```

Now, create 1) a conda environment with our development tools and 2) a virtual environment with our dependencies and an editable install of CITRUS:

```
conda env create -n citrus -f dev-env.yml
conda run -n citrus poetry install
conda activate citrus
```

Note, for plotting models, you will need to have [graphviz](https://graphviz.org/) installed.

## Quickstart

```
# Visualize a model
citrus plot -c example-files/linear_additive.json
```

## Full documentation

[Command Line Interface](doc/cli.md)

[User Guide](doc/user_guide.md)

[Designing Simulations](doc/designing_simulations.md)


