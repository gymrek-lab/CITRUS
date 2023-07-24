<!-- markdownlint-disable -->

<a href="../../pheno_sim/func_nodes/conditional_func.py#L0"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

# <kbd>module</kbd> `conditional_func`
Conditional functions. 

Includes:  IfElse 



---

<a href="../../pheno_sim/func_nodes/conditional_func.py#L12"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `IfElse`
Implements an If-Else conditional statement. 

A node that takes as input a numpy array of values, parameters for a conditional statement, one array of values to be returned if the condition is true, and one array of values to be returned if the condition is false. The condition is evaluated element-wise. All arrays must have the same shape. 

Comparison function may be greater that (gt), greater than or equal (ge), less than (lt), less than or equal (le), equal (eq), or not equal (ne). 



**Examples:**
 ```python
     >>> cond_vals = np.array([0, 1, 0])
     >>> if_vals = np.array([1, 1, 1])
     >>> else_vals = np.array([-1, -1, -1])
     >>> IfElse("if_else", "cond_vals", "if_vals", "else_vals")(cond_vals)
     array([-1, 1, -1])

     >>> cond_vals = np.array([[0, .9, 0], [.8, .1, .5]])
     >>> if_vals = np.array([[1, 1, 1], [1, 1, 1]])
     >>> else_vals = np.array([[-1, -1, -1], [-1, -1, -1]])
     >>> IfElse("if_else", "cond_vals", "if_vals", "else_vals",
     ...             threshold=.5, comparison="lt")(cond_vals)
     array([[1, -1,  1],
         [-1, 1, -1]])
```  



**Args:**
 
 - <b>`alias`</b>:  The alias of the node. 
 - <b>`input_cond_vals`</b>:  The alias of the input node for values used to  evaluate the condition. 
 - <b>`input_if_vals`</b>:  The alias of the input node for values to be  returned if the condition is true. 
 - <b>`input_else_vals`</b>:  The alias of the input node for values to be  returned if the condition is false. 
 - <b>`threshold`</b>:  The threshold to use for the condition. Default is 1. 
 - <b>`comparison`</b>:  The comparison operator to use. One of 'ge' (default),  'le', 'gt', 'lt', 'eq', or 'ne'. 

<a href="../../pheno_sim/func_nodes/conditional_func.py#L54"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `__init__`

```python
__init__(
    alias: str,
    input_cond_vals: str,
    input_if_vals: str,
    input_else_vals: str,
    threshold: float = 1,
    comparison: str = 'ge'
)
```

Initialize IfElse node. 




---

<a href="../../pheno_sim/func_nodes/conditional_func.py#L73"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `run`

```python
run(cond_vals, if_vals, else_vals)
```

Run the node. 



**Args:**
 
 - <b>`cond_vals`</b>:  The values to use to evaluate the condition. 
 - <b>`if_vals`</b>:  The values to return if the condition is true. 
 - <b>`else_vals`</b>:  The values to return if the condition is false. 




---

_This file was automatically generated via [lazydocs](https://github.com/ml-tooling/lazydocs)._
