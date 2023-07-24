<!-- markdownlint-disable -->

<a href="../../pheno_sim/func_nodes/noise.py#L0"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

# <kbd>module</kbd> `noise`
Operators that add noise in the phenotype simulation. 

Includes: 

 * GaussianNoise: A node that adds Gaussian noise to the input. 

 * Heritability: Contols what fraction of the information output by  the node is a function of the input vs. Gaussian noise. The output is  a weighted average of the input and Gaussian noise. The Gaussian noise  is scaled so that the output has the same variance as the input. 



**TODO:**
  * Correlated noise.      



---

<a href="../../pheno_sim/func_nodes/noise.py#L21"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `GaussianNoise`
Operator node that adds Gaussian noise to the input. 

Noise is added element-wise to the input. 



**Example:**
 ```python
         >>> vals = np.vstack([
                 np.random.randint(0, 10, size=10000),
                 np.ones(10000),
                 np.zeros(10000),
         ])
         >>> gn = GaussianNoise("gn", "vals", 1)

         >>> out_vals = gn(vals)
         >>> out_vals
         array([[ 7.260, -0.843, ...,  8.977, -0.345],
                 [ 0.260,  1.012, ...,  1.766,  3.573],
                 [-0.107,  0.222, ..., -0.526,  1.615]])
         >>> out_vals.mean(1)
         array([ 4.532,  1.013, -0.013])
         >>> out_vals.std(1)
         array([3.056, 1.008, 0.998])
``` 

<a href="../../pheno_sim/func_nodes/noise.py#L47"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `__init__`

```python
__init__(alias: str, input_alias: str, noise_std: float)
```

Initialize GaussianNoise node. 



**Args:**
 
 - <b>`alias`</b>:  The alias of the node. 
 - <b>`input_alias`</b>:  The alias of the input node. 
 - <b>`noise_std`</b>:  The standard deviation of the Gaussian noise. 




---

<a href="../../pheno_sim/func_nodes/noise.py#L59"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `run`

```python
run(input_vals)
```

Return the input with Gaussian noise added. 


---

<a href="../../pheno_sim/func_nodes/noise.py#L66"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `Heritability`
Operator node that caps heritability of it's output values. 

Contols what fraction of the information output by the node is a function of the input vs. Gaussian noise. The output is a weighted average of the input and Gaussian noise. The Gaussian noise is scaled so that the output has the same variance as the input. 

The output distribution of values is roughly scaled to have a mean of 0 and a standard deviation of 1. 

Heritability (h^2) ranges from 0 (all noise) to 1 (all input signal). 

Implements the following equation: 

```
for heritability (h^2) in [0, 1] and input values vector x:

output(x_i) = sqrt(h^2) * (x_i - mean(x)) / std(x)      # signal
                 + sqrt(1 - h^2) * N(0,1)                # noise
``` 



**Example:**
 ```python
         >>> vals = np.vstack([
                 np.random.randint(0, 10, size=10000),
                 np.ones(10000),
                 np.zeros(10000),
         ])
         >>> highly_heritable = Heritability("herit_cap", "vals", 0.99)
         >>> medium_heritable = Heritability("herit_cap", "vals", 0.5)
         >>> low_heritable = Heritability("herit_cap", "vals", 0.05)

         >>> high_herit_out = highly_heritable(vals)
         >>> med_herit_out = medium_heritable(vals)
         >>> low_herit_out = low_heritable(vals)

         >>> vals
         array([[8., 0., ..., 8., 0.],
                 [1., 1., ..., 1., 1.],
                 [0., 0., ..., 0., 0.]])
         >>> high_herit_out
         array([[ 1.382, -1.623, ...,  1.243, -1.495],
                 [ 0.138,  0.156, ...,  0.122,  0.141],
                 [ 0.2  , -0.108, ..., -0.053,  0.094]])
         >>> med_herit_out
         array([[ 0.917, -0.257, ...,  0.732, -2.233],
                 [ 0.271, -0.228, ...,  0.712, -0.722],
                 [-0.333,  0.565, ...,  1.331, -0.708]])
         >>> low_herit_out
         array([[ 0.319, -0.15 , ...,  1.397, -1.249],
                 [-0.572, -0.124, ...,  2.178,  1.469],
                 [-0.631, -1.017, ..., -1.227, -1.187]])

         >>> high_herit_out.mean(1)
         array([ 0.001,  0.001, -0.001])
         >>> high_herit_out.std(1)
         array([1.001, 0.099, 0.099])

         >>> low_herit_out.mean(1)
         array([ 0.001, -0.002,  0.002])
         >>> low_herit_out.std(1)
         array([1.005, 0.978, 0.975])
``` 

<a href="../../pheno_sim/func_nodes/noise.py#L132"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `__init__`

```python
__init__(alias: str, input_alias: str, heritability: float)
```

Initialize GaussianNoiseRatio node. 



**Args:**
 
 - <b>`alias`</b>:  The alias of the node. 
 - <b>`input_alias`</b>:  The alias of the input node. 
 - <b>`heritability`</b>:  Used to calculate the ratio of signal to noise. 




---

<a href="../../pheno_sim/func_nodes/noise.py#L144"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `run`

```python
run(input_vals)
```

Return the input with noise added to achieve some heritability. 




---

_This file was automatically generated via [lazydocs](https://github.com/ml-tooling/lazydocs)._
