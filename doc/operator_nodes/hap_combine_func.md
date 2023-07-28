<!-- markdownlint-disable -->

<a href="../../pheno_sim/func_nodes/hap_combine_func.py#L0"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

# <kbd>module</kbd> `hap_combine_func`
Function nodes for combining HaplotypeValues into a single Value. 

Classes: 

 * AdditiveCombine: A node that sums the two haplotypes element-wise  to simulate an additive inheritance effect. 

 * MaxCombine: A node that takes the element-wise maximum of the two  haplotypes to simulate a dominant inheritance effect. 

 * MinCombine: A node that takes the element-wise minimum of the two  haplotypes to simulate a recessive inheritance effect. 

 * MeanCombine: A node that takes the element-wise mean of the two  haplotypes. Mean is either arithmetic, geometric, or harmonic. 



---

<a href="../../pheno_sim/func_nodes/hap_combine_func.py#L24"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `AdditiveCombine`
A node that sums the two haplotypes element-wise. 



**Example:**
 ```python
         >>> hap = (np.array([1, 2, 3]), np.array([4, 5, 6]))
         >>> AdditiveCombine("add", "hap")(hap)
         array([5, 7, 9])

         >>> hap = (
                         np.array([[1, 2, 3],
                                   [4, 5, 6]]),
                         np.array([[ 7,  8,  9],
                                           [10, 11, 12]])
                 )
         >>> AdditiveCombine("add", "hap")(hap)
         array([[ 8, 10, 12],
                    [14, 16, 18]])
``` 

<a href="../../pheno_sim/func_nodes/hap_combine_func.py#L45"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `__init__`

```python
__init__(alias: str, input_alias: str)
```

Initialize the node.  



**Args:**
 
 - <b>`alias`</b>:  The alias of the node. 
 - <b>`input_alias`</b>:  The alias of the input node. 




---

<a href="../../pheno_sim/func_nodes/hap_combine_func.py#L55"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `run`

```python
run(hap_vals: Tuple[ndarray, ndarray])
```






---

<a href="../../pheno_sim/func_nodes/hap_combine_func.py#L59"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `MaxCombine`
A node that takes the element-wise maximum of the two haplotypes.  



**Examples:**
 ```python
         >>> hap = (np.array([1, 2, 3]), np.array([4, 5, 6]))
         >>> MaxCombine("max", "hap")(hap)
         array([4, 5, 6])

         >>> hap = (
                         np.array([[1, 2, 3],
                                   [4, 5, 6]]),
                         np.array([[ 7,  8,  9],
                                           [10, 11, 12]])
                 )
         >>> MaxCombine("max", "hap")(hap)
         array([[ 7,  8,  9],
                    [10, 11, 12]])
``` 

<a href="../../pheno_sim/func_nodes/hap_combine_func.py#L80"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `__init__`

```python
__init__(alias: str, input_alias: str)
```

Initialize the node. 



**Args:**
 
 - <b>`alias`</b>:  The alias of the node. 
 - <b>`input_alias`</b>:  The alias of the input node. 




---

<a href="../../pheno_sim/func_nodes/hap_combine_func.py#L90"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `run`

```python
run(hap_vals: Tuple[ndarray, ndarray])
```






---

<a href="../../pheno_sim/func_nodes/hap_combine_func.py#L94"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `MinCombine`
A node that takes the element-wise minimum of the two haplotypes. 



**Examples:**
 ```python
         >>> hap = (np.array([1, 2, 3]), np.array([4, 5, 6]))
         >>> MinCombine("min", "hap")(hap)
         array([1, 2, 3])

         >>> hap = (
                         np.array([[1, 2, 3],
                                   [4, 5, 6]]),
                         np.array([[ 7,  8,  9],
                                           [10, 11, 12]])
                 )
         >>> MinCombine("min", "hap")(hap)
         array([[1, 2, 3],
                    [4, 5, 6]])
``` 

<a href="../../pheno_sim/func_nodes/hap_combine_func.py#L115"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `__init__`

```python
__init__(alias: str, input_alias: str)
```

Initialize the node. 



**Args:**
 
 - <b>`alias`</b>:  The alias of the node. 
 - <b>`input_alias`</b>:  The alias of the input node. 




---

<a href="../../pheno_sim/func_nodes/hap_combine_func.py#L125"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `run`

```python
run(hap_vals: Tuple[ndarray, ndarray])
```






---

<a href="../../pheno_sim/func_nodes/hap_combine_func.py#L129"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `MeanCombine`
A node that takes the element-wise mean of the two haplotypes. 

Mean is either arithmetic, geometric, or harmonic. 



**Examples:**
 ```python
         >>> hap = (np.array([1, 2, 3]), np.array([4, 5, 6]))
         >>> MeanCombine("mean", "hap")(hap)
         array([2.5, 3.5, 4.5])
         >>> MeanCombine("mean", "hap", mean_type="geometric")(hap)
         array([2.        , 3.16227766, 4.24264069])
         >>> MeanCombine("mean", "hap", mean_type="harmonic")(hap)
         array([1.6       , 2.85714286, 4.        ])

         >>> hap = (
                         np.array([[1, 2, 3],
                                   [4, 5, 6]]),
                         np.array([[ 7,  8,  9],
                                           [10, 11, 12]])
                 )
         >>> MeanCombine("mean", "hap")(hap)
         array([[4. , 5. , 6. ],
                    [7. , 8. , 9]])
         >>> MeanCombine("mean", "hap", mean_type="geometric")(hap)
         array([[2.64575131, 4.        , 5.19615242],
            [6.32455532, 7.41619849, 8.48528137]])
         >>> MeanCombine("mean", "hap", mean_type="harmonic")(hap)
         array([[1.75      , 3.2       , 4.5       ],
            [5.71428571, 6.875     , 8.        ]])
``` 

<a href="../../pheno_sim/func_nodes/hap_combine_func.py#L162"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `__init__`

```python
__init__(alias: str, input_alias: str, mean_type: str = 'arithmetic')
```

Initialize the node. 



**Args:**
 
 - <b>`alias`</b>:  The alias of the node. 
 - <b>`input_alias`</b>:  The alias of the input node. 
 - <b>`mean_type`</b>:  The type of mean to take. Can be "arithmetic" (default),  "geometric", or "harmonic". 




---

<a href="../../pheno_sim/func_nodes/hap_combine_func.py#L180"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `run`

```python
run(hap_vals: Tuple[ndarray, ndarray])
```

Run the node. 



**Args:**
 
 - <b>`hap_vals`</b>:  The haplotype values to combine. 




---

_This file was automatically generated via [lazydocs](https://github.com/ml-tooling/lazydocs)._
