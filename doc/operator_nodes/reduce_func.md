<!-- markdownlint-disable -->

<a href="../../pheno_sim/func_nodes/reduce_func.py#L0"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

# <kbd>module</kbd> `reduce_func`
Reduce a Values matrix to one value per sample using some operation. 

Classes: 

 * SumReduce: Sum each sample's feature values into a single value  per sample. 

 * MinReduce: Return the minimum of each sample's feature values as  the sample's value. 

 * MaxReduce: Return the maximum of each sample's feature values as  the sample's value. 

 * MeanReduce: Return the mean of each sample's feature values as  the sample's value. Mean is either arithmetic (default),  geometric, or harmonic. 

 * AnyReduce: Return 1 if any feature value is past a threshold, 0  otherwise. 

 * AllReduce: Return 1 if all feature values are past a threshold, 0  otherwise. 



---

<a href="../../pheno_sim/func_nodes/reduce_func.py#L30"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `SumReduce`
Sum each sample's feature values into a single value per sample. 

For a Values matrix (num_feats, num_samples), returns a vector of the sum of the feature values for each sample (a num_samples length array). 



**Example:**
 ```python
         >>> SumReduce("sum_reduce", "vals")(np.array([[1, 2, 3], [4, 5, 6]]))
         array([ 5,  7,  9])
``` 

<a href="../../pheno_sim/func_nodes/reduce_func.py#L43"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `__init__`

```python
__init__(alias: str, input_alias: str)
```

Initialize SumReduce node. 



**Args:**
 
 - <b>`alias`</b>:  The alias of the node. 
 - <b>`input_alias`</b>:  The alias of the input node. 




---

<a href="../../pheno_sim/func_nodes/reduce_func.py#L53"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `run`

```python
run(input_vals)
```

Return sum of each sample's feature values as the sample's value. 


---

<a href="../../pheno_sim/func_nodes/reduce_func.py#L58"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `MinReduce`
Return the minimum of each sample's feature values as the sample's value. 

For a Values matrix (num_feats, num_samples), returns a vector of the minimum of the feature values for each sample (a num_samples length array). 



**Examples:**
 ```python
         >>> MinReduce("min_reduce", "vals")(np.array([[1, 2, 3], [4, 5, 6]]))
         array([1, 2, 3])
``` 

<a href="../../pheno_sim/func_nodes/reduce_func.py#L72"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `__init__`

```python
__init__(alias: str, input_alias: str)
```

Initialize MinReduce node. 



**Args:**
 
 - <b>`alias`</b>:  The alias of the node. 
 - <b>`input_alias`</b>:  The alias of the input node. 




---

<a href="../../pheno_sim/func_nodes/reduce_func.py#L82"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `run`

```python
run(input_vals)
```

Return min of each sample's feature values as the sample's value. 


---

<a href="../../pheno_sim/func_nodes/reduce_func.py#L87"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `MaxReduce`
Return the maximum of each sample's feature values as the sample's value. 

For a Values matrix (num_feats, num_samples), returns a vector of the maximum of the feature values for each sample (a num_samples length array). 



**Examples:**
 ```python
         >>> MaxReduce("max_reduce", "vals")(np.array([[1, 2, 3], [4, 5, 6]]))
         array([4, 5, 6])
``` 

<a href="../../pheno_sim/func_nodes/reduce_func.py#L101"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `__init__`

```python
__init__(alias: str, input_alias: str)
```

Initialize MaxReduce node. 



**Args:**
 
 - <b>`alias`</b>:  The alias of the node. 
 - <b>`input_alias`</b>:  The alias of the input node. 




---

<a href="../../pheno_sim/func_nodes/reduce_func.py#L111"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `run`

```python
run(input_vals)
```

Return max of each sample's feature values as the sample's value. 


---

<a href="../../pheno_sim/func_nodes/reduce_func.py#L116"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `MeanReduce`
Return the mean of each sample's feature values as the sample's value. 

For a Values matrix (num_feats, num_samples), returns a vector of the mean of the feature values for each sample (a num_samples length array). 

Mean is either arithmetic (default), geometric, or harmonic. 



**Examples:**
 ```python
         >>> MeanReduce("mean_reduce", "vals")(np.array([[1, 2, 3], [4, 5, 6]]))
         array([2.5, 3.5, 4.5])
         >>> MeanReduce("mean_reduce", "vals", mean_type="geometric")(
                 np.array([[1, 2, 3], [4, 5, 6]])
         )
         array([2., 3.16227766, 4.24264069])
         >>> MeanReduce("mean_reduce", "vals", mean_type="harmonic")(
                 np.array([[1, 2, 3], [4, 5, 6]])
         )
         array([1.6, 2.85714286, 4])
``` 

<a href="../../pheno_sim/func_nodes/reduce_func.py#L140"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `__init__`

```python
__init__(alias: str, input_alias: str, mean_type: str = 'arithmetic')
```

Initialize MeanReduce node. 



**Args:**
 
 - <b>`alias`</b>:  The alias of the node. 
 - <b>`input_alias`</b>:  The alias of the input. 
 - <b>`mean_type`</b>:  The type of mean to use. One of 'arithmetic' (default),  'geometric', or 'harmonic'. 




---

<a href="../../pheno_sim/func_nodes/reduce_func.py#L158"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `run`

```python
run(input_vals)
```

Return mean of each sample's feature values as the sample's value. 


---

<a href="../../pheno_sim/func_nodes/reduce_func.py#L172"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `AnyReduce`
Return 1 if any feature value is past a threshold, 0 otherwise. 

For a Values matrix (num_feats, num_samples), returns a num_samples length vector that is 1 if the sample has any feature values meet some comparison with a threshold value, and 0 otherwise. 

Comparison function may be greater that (gt), greater than or equal (ge), less than (lt), less than or equal (le), equal (eq), or not equal (ne). 



**Examples:**
 ```python
         >>> vals = np.array([[0, -1, 3], [.5, 1, 1]])
         >>> AnyReduce("any_reduce", "vals")(vals)
         array([0, 1, 1])
         >>> AnyReduce("any_reduce", "vals", threshold=0, comparison="lt")(vals)
         array([0, 1, 0])
``` 

<a href="../../pheno_sim/func_nodes/reduce_func.py#L192"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `__init__`

```python
__init__(
    alias: str,
    input_alias: str,
    threshold: float = 1,
    comparison: str = 'ge'
)
```

Initialize AnyReduce node. 



**Args:**
 
 - <b>`alias`</b>:  The alias of the node. 
 - <b>`input_alias`</b>:  The alias of the input. 
 - <b>`threshold`</b>:  The threshold to use for determining if a sample has any  feature values past the threshold. Default is 1. 
 - <b>`comparison`</b>:  The comparison operator to use. One of 'ge' (default),  'le', 'gt', 'lt', 'eq', or 'ne'. 




---

<a href="../../pheno_sim/func_nodes/reduce_func.py#L214"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `run`

```python
run(input_vals)
```

Return 1 if any feature value is past a threshold, 0 otherwise. 


---

<a href="../../pheno_sim/func_nodes/reduce_func.py#L234"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `AllReduce`
Return 1 if all feature values are past a threshold, 0 otherwise. 

For a Values matrix (num_feats, num_samples), return a num_samples length vector that is 1 if the sample has all feature values meet some comparison with a threshold value, and 0 otherwise. 

Comparison function may be greater that (gt), greater than or equal (ge), less than (lt), less than or equal (le), equal (eq), or not equal (ne). 



**Examples:**
 ```python
         >>> vals = np.array([[0, -1, 3], [.5, 1, 1]])
         >>> AllReduce("all_reduce", "vals")(vals)
         array([0, 0, 1])
         >>> AllReduce("all_reduce", "vals", threshold=0, comparison="lt")(vals)
         array([0, 0, 0])
``` 

<a href="../../pheno_sim/func_nodes/reduce_func.py#L254"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `__init__`

```python
__init__(
    alias: str,
    input_alias: str,
    threshold: float = 1,
    comparison: str = 'ge'
)
```

Initialize AllReduce node. 



**Args:**
 
 - <b>`alias`</b>:  The alias of the node. 
 - <b>`input_alias`</b>:  The alias of the input. 
 - <b>`threshold`</b>:  The threshold to use for determining if a sample has all  feature values past the threshold. Default is 1. 
 - <b>`comparison`</b>:  The comparison operator to use. One of 'ge' (default),  'le', 'gt', 'lt', 'eq', or 'ne'. 




---

<a href="../../pheno_sim/func_nodes/reduce_func.py#L276"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `run`

```python
run(input_vals)
```

Return 1 if all feature values are past a threshold, 0 otherwise. 




---

_This file was automatically generated via [lazydocs](https://github.com/ml-tooling/lazydocs)._
