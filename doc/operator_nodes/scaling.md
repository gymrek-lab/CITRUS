<!-- markdownlint-disable -->

<a href="../../pheno_sim/func_nodes/scaling.py#L0"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

# <kbd>module</kbd> `scaling`
Operators that scaling input distributions in the phenotype simulation. 

Includes: 

 * Clip: A node that clips the input to be greater than or equal to some  minimum value and/or less than or equal to some maximum value. 

 * MinMaxScaler: A node that scales the input to be between 0 and 1 using  the minimum and maximum values of the input.  

 * StandardScaler: A node that scales the input to have mean 0 and standard  deviation 1 using the mean and standard deviation of the input. 

 * RobustScaler: A node that scales the input to have median 0 and interquartile  range 1 using the median and interquartile range of the input. 



---

<a href="../../pheno_sim/func_nodes/scaling.py#L24"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `Clip`
Operator node that clips the input based on a min and/or max value(s). 

If a minimum value is provided, then all values less than the minimum value are set to the minimum value. If a maximum value is provided, then all values greater than the maximum value are set to the maximum value. 



**Example:**
 ```python
         >>> vals = np.array([
                 [1, 2, 3],
                 [4, 5, 6],
                 [7, 8, 9]
         ])

         >>> clip = Clip("clip", "vals", min_val=2, max_val=8)
         >>> clip(vals)
         array([[2, 2, 3],
                 [4, 5, 6],
                 [7, 8, 8]])

         >>> clip = Clip("clip", "vals", min_val=4)
         >>> clip(vals)
         array([[4, 4, 4],
                 [4, 5, 6],
                 [7, 8, 9]])

         >>> clip = Clip("clip", "vals", max_val=6)
         >>> clip(vals)
         array([[1, 2, 3],
                 [4, 5, 6],
                 [6, 6, 6]])
``` 

<a href="../../pheno_sim/func_nodes/scaling.py#L59"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `__init__`

```python
__init__(
    alias: str,
    input_alias: str,
    min_val: float = None,
    max_val: float = None
)
```

Initialize Clip node. 



**Args:**
 
 - <b>`alias`</b>:  The alias of the node. 
 - <b>`input_alias`</b>:  The alias of the input node. 
 - <b>`min_val`</b> (float, default None):  The minimum value to clip to. 
 - <b>`max_val`</b> (float, default None):  The maximum value to clip to. 




---

<a href="../../pheno_sim/func_nodes/scaling.py#L79"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `run`

```python
run(input_vals)
```

Return the input clipped to the min and/or max value(s). 


---

<a href="../../pheno_sim/func_nodes/scaling.py#L89"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `MinMaxScaler`
Operator node that scales the input to be between 0 and 1. 

The scaling is based on the minimum and maximum values of the input, such that the minimum value of the input is mapped to 0 and the maximum value of the input is mapped to 1. All other values are scaled linearly between 0 and 1. 

Scaling is done either by feature or among all features based on the 'by_feat' argument. 



**Example:**
 ```python
         >>> vals = np.array([
                 [1, 2, 3],
                 [4, 5, 6],
                 [7, 8, 9]
         ])

         >>> mms_by_feat = MinMaxScaler("mms", "vals", by_feat=True)
         >>> mms_all = MinMaxScaler("mms", "vals", by_feat=False)

         >>> print(mms_by_feat(vals))
         array([[0. , 0.5, 1. ],
                 [0. , 0.5, 1. ],
                 [0. , 0.5, 1. ]])
         >>> print(mms_all(vals))
         array([[0.   , 0.125, 0.25 ],
                 [0.375, 0.5  , 0.625],
                 [0.75 , 0.875, 1.   ]])
``` 

<a href="../../pheno_sim/func_nodes/scaling.py#L122"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `__init__`

```python
__init__(alias: str, input_alias: str, by_feat: bool = True)
```

Initialize MinMaxScaler node. 



**Args:**
 
 - <b>`alias`</b>:  The alias of the node. 
 - <b>`input_alias`</b>:  The alias of the input node. 
 - <b>`by_feat`</b> (bool, default True):  Whether to scale by feature or among all features. 




---

<a href="../../pheno_sim/func_nodes/scaling.py#L135"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `run`

```python
run(input_vals)
```

Return the input scaled to be between 0 and 1. 



**Args:**
 
 - <b>`input_vals`</b>:  The input values to scale. 



**Returns:**
 The input scaled to be between 0 and 1. 


---

<a href="../../pheno_sim/func_nodes/scaling.py#L161"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `StandardScaler`
Operator that scales input to have mean 0 and standard deviation 1. 

Scaling is either done by feature or among all features based on the 'by_feat' argument. 



**Example:**
 ```python
         >>> vals = np.array([
                 [1, 2, 3],
                 [4, 5, 6],
                 [7, 8, 9]
         ])
         >>> std_scaler_by_feat = StandardScaler(
                 "std_scaler", "vals", by_feat=True
         )
         >>> std_scaler_all = StandardScaler(
                 "std_scaler", "vals", by_feat=False
         )

         >>> by_feat_out = std_scaler_by_feat(vals)
         >>> all_out = std_scaler_all(vals)

         >>> by_feat_out
         array([[-1.225,  0.   ,  1.225],
                 [-1.225,  0.   ,  1.225],
                 [-1.225,  0.   ,  1.225]])
         >>> all_out
         array([[-1.549, -1.162, -0.775],
                 [-0.387,  0.   ,  0.387],
                 [ 0.775,  1.162,  1.549]])
         
         >>> by_feat_out.mean(1)
         array([0., 0., 0.])
         >>> by_feat_out.std(1)
         array([1., 1., 1.])

         >>> all_out.mean(1)
         array([-1.162,  0.   ,  1.162])
         >>> all_out.mean()
         0.0
         >>> all_out.std()
         1.0


<a href="../../pheno_sim/func_nodes/scaling.py#L206"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `__init__`

```python
__init__(alias: str, input_alias: str, by_feat: bool = True)
```

Initialize StandardScaler node. 



**Args:**
 
 - <b>`alias`</b>:  The alias of the node. 
 - <b>`input_alias`</b>:  The alias of the input node. 
 - <b>`by_feat`</b> (bool, default True):  Whether to scale by feature or among all features. 




---

<a href="../../pheno_sim/func_nodes/scaling.py#L219"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `run`

```python
run(input_vals)
```

Scale the input to have mean 0 and standard deviation 1. 


---

<a href="../../pheno_sim/func_nodes/scaling.py#L240"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `RobustScaler`
Operator that scales input to have median 0 and interquartile range 1. 

Scaling is either done by feature or among all features based on the 'by_feat' argument. 



**Example:**
 ```python
         >>> vals = np.array([
                 [1, 2, 3],
                 [4, 5, 6],
                 [7, 8, 9]
         ])
         >>> robust_by_feat = RobustScaler("robust", "vals", by_feat=True)
         >>> robust_all = RobustScaler("robust", "vals", by_feat=False)

         >>> robust_by_feat(vals)
         array([[-1.,  0.,  1.],
                 [-1.,  0.,  1.],
                 [-1.,  0.,  1.]])
         >>> robust_all(vals)
         array([[-1.  , -0.75, -0.5 ],
                 [-0.25,  0.  ,  0.25],
                 [ 0.5 ,  0.75,  1.  ]])

         >>> extreme_vals = np.array(
                 np.random.normal(0, 10, 1000).tolist() + [-1000000000000]
         )
         >>> robust_by_feat(extreme_vals)
         array([[-7.454e-01, -6.908e-01, ..., -1.848e+00, -7.676e+10]])
``` 

<a href="../../pheno_sim/func_nodes/scaling.py#L273"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `__init__`

```python
__init__(alias: str, input_alias: str, by_feat: bool = True)
```

Initialize RobustScaler node. 



**Args:**
 
 - <b>`alias`</b>:  The alias of the node. 
 - <b>`input_alias`</b>:  The alias of the input node. 
 - <b>`by_feat`</b> (bool, default True):  Whether to scale by feature or among all features. 




---

<a href="../../pheno_sim/func_nodes/scaling.py#L286"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `run`

```python
run(input_vals)
```

Scale the input to have median 0 and interquartile range 1. 




---

_This file was automatically generated via [lazydocs](https://github.com/ml-tooling/lazydocs)._
