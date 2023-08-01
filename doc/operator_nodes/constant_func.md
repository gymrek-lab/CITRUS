<!-- markdownlint-disable -->

<a href="../../pheno_sim/func_nodes/constant_func.py#L0"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

# <kbd>module</kbd> `constant_func`
Generate values representing constants and broadcast to some shape. 

Classes: 

 * Constant: A node that generates constant values. 

 * RandomConstant: A node that generates constant values, where values  are initially drawn from a distribution. 



---

<a href="../../pheno_sim/func_nodes/constant_func.py#L18"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `Constant`
Class that generates constant values. 

The constant for this function is either: 
    - A single value, which is broadcast to the shape of the input. 
    - A list of values (one per feature dim), which are broadcast to the  shape of the input. 



**Example:**
 ```python
     >>> match_size = np.array([[1, 2, 3], [4, 5, 6]])
     >>> Constant("const", "match_size", 1)(match_size)
     array([[1, 1, 1],
             [1, 1, 1]])
     >>> Constant("const", "match_size", [1, 2])(match_size)
     array([[1, 1, 1],
             [2, 2, 2]])
``` 



**Args:**
 
 - <b>`alias`</b>:  The alias of the node. 
 - <b>`input_match_size`</b>:  The alias of the input node for values used to  determine the size of the output array. Output will be the same  size as this input. 
 - <b>`constant`</b>:  The constant value(s) to generate. 

<a href="../../pheno_sim/func_nodes/constant_func.py#L45"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `__init__`

```python
__init__(alias: str, input_match_size: str, constant: Union[int, float, list])
```

Initialize Constant node. 




---

<a href="../../pheno_sim/func_nodes/constant_func.py#L56"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `run`

```python
run(input_match_size)
```

Generate the constant value(s). 



**Args:**
 
 - <b>`input_match_size`</b>:  The input values used to determine the size of  the output array. Output will be the same size as this input. 


---

<a href="../../pheno_sim/func_nodes/constant_func.py#L75"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `RandomConstant`
Generates constant values, where values are drawn from a distribution. 

Any distribution that can be sampled from using numpy.random.Generator can be used. The parameters for the distribution (see numpy docs https://numpy.org/doc/stable/reference/random/generator.html#distributions) are passed as the dist_kwargs argument. 'size' should not be passed in dist_kwargs. 

If by_feat is False, a single value is drawn from the distribution and broadcast to the shape of the input. If by_feat is True, a value is drawn from the distribution for each feature dim and broadcast to the shape of the input. 

get_config_updates() is implemented for this node to save the drawn constant value(s) to the config file. This will save a list value for the drawn_vals key in the config file. This list will have 1 value per feature dim (number of rows) and will be expanded to the shape of the input when the node is run. 



**Examples:**
 ```python
     >>> match_size = np.array([[1, 2, 3], [4, 5, 6]])

     >>> RandomConstant(
         "const", "match_size", "uniform", {"low": 0, "high": 1}
     )(match_size)
     array([[0.37454012, 0.37454012, 0.37454012],
            [0.37454012, 0.37454012, 0.37454012]])

     >>> RandomConstant(
         "const", "match_size", "uniform",
         {"low": 0, "high": 1}, by_feat=True
     )(match_size)
     array([[0.37454012, 0.37454012, 0.37454012],
            [0.95071431, 0.95071431, 0.95071431]])
``` 



**Args:**
 
 - <b>`alias`</b>:  The alias of the node. 
 - <b>`input_match_size`</b>:  The alias of the input node for values used to  determine the size of the output array. Output will be the same  size as this input. If by_feat is True, this input will also be  used to determine the number of feature dimensions. 
 - <b>`dist_name`</b>:  The name of the distribution to draw from. 
 - <b>`dist_kwargs`</b>:  The keyword arguments for the distribution. 
 - <b>`by_feat`</b>:  Whether to draw a value for each feature dim. Default  is False. 
 - <b>`drawn_vals`</b>:  The drawn constant value(s). Default is None, otherwise  must be a list. If by_feat is False, this list must have 1 value.  If by_feat is True, this list must have the same number of values  as feature dims (number of rows in input_match_size). This is  typically loaded from a config file for reproducability. If this  node is constructed from a config file where drawn_vals is not  None, the drawn_vals will be used instead of drawing new values. 

<a href="../../pheno_sim/func_nodes/constant_func.py#L132"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `__init__`

```python
__init__(
    alias: str,
    input_match_size: str,
    dist_name: str,
    dist_kwargs: dict,
    by_feat: bool = False,
    drawn_vals: list = None
)
```

Initialize RandomConstant node. 




---

<a href="../../pheno_sim/func_nodes/constant_func.py#L188"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `get_config_updates`

```python
get_config_updates()
```

Return drawn_vals for saving to config file. 

---

<a href="../../pheno_sim/func_nodes/constant_func.py#L162"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `run`

```python
run(input_match_size)
```

Generate the constant value(s). 



**Args:**
 
 - <b>`input_match_size`</b>:  The input values used to determine the size of  the output array. Output will be the same size as this input. 




---

_This file was automatically generated via [lazydocs](https://github.com/ml-tooling/lazydocs)._
