<!-- markdownlint-disable -->

<a href="../../pheno_sim/func_nodes/util_func.py#L0"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

# <kbd>module</kbd> `util_func`
Utility functions for simulations. 

Classes: 

 * Concatenate: A node that concatenates some inputs into a single array. 



---

<a href="../../pheno_sim/func_nodes/util_func.py#L13"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `Concatenate`
A node that concatenates some inputs into a single array. 

The inputs are concatenated in the order they are given in the input list. 



**Examples:**
 ```python
         >>> Concatenate("concat", ["arrs"])(
                 [np.array([1, 2, 3]), np.array([4, 5, 6])]
         )
         array([[1, 2, 3],
                    [4, 5, 6]])

         >>> Concatenate("concat", ["arrs"])(
                 [np.array([[1, 2, 3], [4, 5, 6]]), np.array([[7, 8, 9]])]
         )
         array([[1, 2, 3],
                    [4, 5, 6],
                    [7, 8, 9]])
``` 

<a href="../../pheno_sim/func_nodes/util_func.py#L35"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `__init__`

```python
__init__(alias: str, input_aliases: list)
```

Initialize Concatenate node. 



**Args:**
 
 - <b>`alias`</b>:  The alias of the node. 
 - <b>`input_aliases`</b> (list):  The aliases of the inputs to be concatenated. 




---

<a href="../../pheno_sim/func_nodes/util_func.py#L45"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `run`

```python
run(*input_vals)
```

Return concatenated array of input values. 




---

_This file was automatically generated via [lazydocs](https://github.com/ml-tooling/lazydocs)._
