<!-- markdownlint-disable -->

<a href="../../pheno_sim/func_nodes/distribution_func.py#L0"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

# <kbd>module</kbd> `distribution_func`
Function nodes that draw values from a distribution. 



---

<a href="../../pheno_sim/func_nodes/distribution_func.py#L8"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `Distribution`
Class that draws values from a distribution. 

Any distribution that can be sampled from using numpy.random.Generator can be used. The parameters for the distribution (see numpy docs https://numpy.org/doc/stable/reference/random/generator.html#distributions) are passed as the dist_kwargs argument. 'size' should not be passed as it is determined by the shape of the match_size input array. 

Note that the distribution is sampled every time the node is called. There is not one value that is drawn and then used in the future, as is the case with RandomConstant. 



**Examples:**
 ```python
     >>> match_size = np.array([[1, 2, 3], [4, 5, 6]])
     >>> Distribution(
         "dist", "match_size", "uniform", 
         {"low": 0, "high": 1}
     )(match_size)
     array([[0.5488135 , 0.71518937, 0.60276338],
            [0.54488318, 0.4236548 , 0.64589411]])
``` 



**Args:**
 
 - <b>`alias`</b>:  The alias of the node. 
 - <b>`input_match_size`</b>:  The alias of the input node for values used to  determine the size of the output array. 
 - <b>`dist_name`</b>:  The name of the distribution to sample from. 
 - <b>`dist_kwargs`</b>:  The keyword arguments for the distribution. 

<a href="../../pheno_sim/func_nodes/distribution_func.py#L40"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `__init__`

```python
__init__(alias: str, input_match_size: str, dist_name: str, dist_kwargs: dict)
```

Initialize Distribution node. 




---

<a href="../../pheno_sim/func_nodes/distribution_func.py#L53"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `run`

```python
run(input_match_size)
```

Draw values from the distribution. 




---

_This file was automatically generated via [lazydocs](https://github.com/ml-tooling/lazydocs)._
