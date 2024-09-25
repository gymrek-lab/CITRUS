# CITRUS🍊: A phenotype simulation tool with the flexibility to model complex interactions

CITRUS, the CIs and Trans inteRaction nUmerical Simulator, is a tool for simulating phenotypes with complex genetic archetectures that go beyond simple models that assume linear, additive contributions of individual SNPs. The goal of this tool is to provide better simulations for benchmarking GWAS/PRS models.

## Installation

For plotting models, you will need to have [graphviz](https://graphviz.org/) installed.

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

## Full documentation

[User Guide](doc/user_guide.md)

[Designing Simulations](doc/designing_simulations.md)

[Command Line Interface](doc/cli.md)

