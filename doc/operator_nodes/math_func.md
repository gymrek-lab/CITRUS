<!-- markdownlint-disable -->

<a href="../../pheno_sim/func_nodes/math_func.py#L0"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

# <kbd>module</kbd> `math_func`
General math function nodes for the simulation. 

Includes: 

 * Identity: A node that returns the input. Mainly for testing.  

 * Sum: A node that sums some inputs element-wise. 

 * Product: A node that multiplies some inputs element-wise. 



---

<a href="../../pheno_sim/func_nodes/math_func.py#L18"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `Identity`
A node that returns the input. 



**Examples:**
 ```python
     >>> Identity("identity", "arr")(np.array([1, 2, 3]))
     array([1, 2, 3])
     >>> Identity("identity", "hap")(
         (np.array([1, 2, 3]), np.array([4, 5, 6]))
     )
     (array([1, 2, 3]), array([4, 5, 6]))
``` 

<a href="../../pheno_sim/func_nodes/math_func.py#L32"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `__init__`

```python
__init__(alias: str, input_alias: str)
```

Initialize Identity node. 



**Args:**
 
 - <b>`alias`</b>:  The alias of the node. 
 - <b>`input_alias`</b>:  The alias of the input node. 




---

<a href="../../pheno_sim/func_nodes/math_func.py#L42"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `run`

```python
run(input_vals)
```

Return the input. 


---

<a href="../../pheno_sim/func_nodes/math_func.py#L47"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `Sum`
A node that sums some inputs element-wise. 

If all inputs are vectors (num_samples length arrays), then the output is a vector that is the element-wise sum of the inputs. 

If all inputs are all matrices (num_feats x num_samples arrays), then the output is a matrix (with the same dimensions) that is the  element-wise sum. 

If the input is a mix of vectors and matrices: 
    - All matrices must have the same dimensions. 
    - Matrices are summed element-wise. 
    - Vectors are summed element-wise over each of the num_feats of  the matrices. 



**Examples:**
 ```python
     >>> Sum("sum", ["arrs"])([np.array([1, 2, 3]), np.array([4, 5, 6])])
     array([5, 7, 9])

     >>> Sum("sum", ["arrs"])([
         np.array([[1, 2, 3], [4, 5, 6]]),
         np.array([[7, 8, 9], [10, 11, 12]])
     ])
     array([[ 8, 10, 12],
            [14, 16, 18]])
     
     >>> Sum("sum", ["arrs"])([
         np.array([1, 2, 3]),
         np.array([[1, 1, 1], [2, 2, 2]]),
         np.array([[1, 1, 1], [2, 2, 2]])
     ])
     array([[3, 4, 5],
            [5, 6, 7]])
```          

<a href="../../pheno_sim/func_nodes/math_func.py#L85"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `__init__`

```python
__init__(alias: str, input_aliases: list)
```

Initialize Sum node. 



**Args:**
 
 - <b>`alias`</b>:  The alias of the node. 
 - <b>`input_aliases`</b> (list):  The aliases of the inputs to be summed. 




---

<a href="../../pheno_sim/func_nodes/math_func.py#L95"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `run`

```python
run(input_vals)
```

Return the sum of the inputs. 


---

<a href="../../pheno_sim/func_nodes/math_func.py#L100"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `Product`
A node that multiplies some inputs element-wise. 

If all inputs are vectors (num_samples length arrays), then the output is a vector that is the element-wise product of the inputs. 

If all inputs are all matrices (num_feats x num_samples arrays), then the output is a matrix (with the same dimensions) that is the element-wise product. 

If the input is a mix of vectors and matrices: 
    - All matrices must have the same dimensions. 
    - Matrices are multiplied element-wise. 
    - Vectors are multiplied element-wise over each of the num_feats of  the matrices. 



**Examples:**
 ```python
     >>> Product("product", ["arrs"])(
         [np.array([1, 2, 3]), np.array([4, 5, 6])]
     )
     array([ 4, 10, 18])

     >>> Product("product", ["arrs"])([
         np.array([[1, 2, 3], [4, 5, 6]]),
         np.array([[7, 8, 9], [10, 11, 12]])
     ])
     array([[ 7, 16, 27],
            [40, 55, 72]])
     
     >>> Product("product", ["arrs"])([
         np.array([1, 2, 3]),
         np.array([[1, 1, 1], [2, 2, 2]]),
         np.array([[1, 1, 1], [2, 2, 2]])
     ])
     array([[1, 2, 3],
            [4, 8, 12]])
``` 

<a href="../../pheno_sim/func_nodes/math_func.py#L140"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `__init__`

```python
__init__(alias: str, input_aliases: list)
```

Initialize Product node. 



**Args:**
 
 - <b>`alias`</b>:  The alias of the node. 
 - <b>`input_aliases`</b> (list):  The aliases of the inputs to be multiplied. 




---

<a href="../../pheno_sim/func_nodes/math_func.py#L150"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `run`

```python
run(*input_vals)
```

Return the product of the inputs. 




---

_This file was automatically generated via [lazydocs](https://github.com/ml-tooling/lazydocs)._
