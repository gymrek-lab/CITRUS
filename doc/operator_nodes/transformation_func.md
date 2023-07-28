<!-- markdownlint-disable -->

<a href="../../pheno_sim/func_nodes/transformation_func.py#L0"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

# <kbd>module</kbd> `transformation_func`
Non-linear transformation function operator nodes. 

Take some input values and apply some transformation function, like a sigmoid, tanh, ReLU,  

Classes: 

 * ReLU  

 * Sigmoid  

 * Softmax  

 * Tanh 



---

<a href="../../pheno_sim/func_nodes/transformation_func.py#L22"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `ReLU`
Operator node that applies the ReLU function to the input. 

User can specify: 
        - The slope of the negative values. 
        - The threshold at which the slope changes. 



**Example:**
 

```python
         >>> vals = np.array([-2, -1, 0, 1, 2])

         >>> relu = ReLU("relu", "vals")
         >>> relu(vals)
         array([-0., -0.,  0.,  1.,  2.])

         >>> relu = ReLU("relu", "vals", neg_slope=0.5)
         >>> relu(vals)
         array([-1. , -0.5,  0. ,  1. ,  2. ])

         >>> relu = ReLU("relu", "vals", threshold=1.5)
         >>> relu(vals)
         array([-0., -0.,  0.,  0.,  2.])

         >>> relu = ReLU("relu", "vals", neg_slope=0.5, threshold=1.5)
         >>> relu(vals)
         array([-1. , -0.5,  0. ,  0.5,  2. ])

         >>> relu = ReLU("relu", "vals", neg_slope=-0.5)
         >>> relu(vals)
         array([ 1. ,  0.5, -0. ,  1. ,  2. ])
``` 

<a href="../../pheno_sim/func_nodes/transformation_func.py#L56"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `__init__`

```python
__init__(
    alias: str,
    input_alias: str,
    neg_slope: float = 0.0,
    threshold: float = 0.0
)
```

Initialize ReLU node. 



**Args:**
 
 - <b>`alias`</b>:  The alias of the node. 
 - <b>`input_alias`</b>:  The alias of the input node. 
 - <b>`neg_slope`</b> (float, default 0.0):  The slope of the negative values. 
 - <b>`threshold`</b> (float, default 0.0):  The threshold at which the slope  changes. 




---

<a href="../../pheno_sim/func_nodes/transformation_func.py#L77"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `run`

```python
run(input_vals)
```

Return the input with ReLU applied. 


---

<a href="../../pheno_sim/func_nodes/transformation_func.py#L86"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `Sigmoid`
Operator node that applies the sigmoid function to the input. 

Output is between 0 and 1. 



**Example:**
 ```python
         >>> vals = np.array([-3, -2, -1, 0, 1, 2, 3])
         >>> sigmoid = Sigmoid("sigmoid", "vals")
         >>> sigmoid(vals)
         array([0.018, 0.047, 0.119, 0.269, 0.5  , 0.731, 0.881, 0.953, 0.982])
``` 

<a href="../../pheno_sim/func_nodes/transformation_func.py#L100"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `__init__`

```python
__init__(alias: str, input_alias: str)
```

Initialize Sigmoid node. 



**Args:**
 
 - <b>`alias`</b>:  The alias of the node. 
 - <b>`input_alias`</b>:  The alias of the input node. 




---

<a href="../../pheno_sim/func_nodes/transformation_func.py#L110"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `run`

```python
run(input_vals)
```

Return the input with sigmoid applied. 


---

<a href="../../pheno_sim/func_nodes/transformation_func.py#L115"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `Softmax`
Applies softmax to each sample's multiple values. 

Only use this function when the input is a matrix (there are multiple values in the input for each sample). Default behavior is to throw an error if the input is not a matrix. 

The output will be a matrix with the same dimension as the input. The softmax function is applied to each sample's values independently, so the columns of the output matrix will sum to 1. 



**Example:**
 

```python
         >>> vals = np.array([
                 [-1, 0, 3, 2],
                 [0, 1, 3, -1],
                 [1, 2, 3, -4]
         ])
         >>> softmax = Softmax("softmax", "vals")
         >>> softmax(vals)
         array([
                 [0.09 , 0.09 , 0.333, 0.95 ],
                 [0.245, 0.245, 0.333, 0.047],
                 [0.665, 0.665, 0.333, 0.002]
         ])
``` 

<a href="../../pheno_sim/func_nodes/transformation_func.py#L144"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `__init__`

```python
__init__(alias: str, input_alias: str)
```

Initialize Softmax node. 



**Args:**
 
 - <b>`alias`</b>:  The alias of the node. 
 - <b>`input_alias`</b>:  The alias of the input node. 




---

<a href="../../pheno_sim/func_nodes/transformation_func.py#L154"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `run`

```python
run(input_vals)
```

Return the input with softmax applied. 


---

<a href="../../pheno_sim/func_nodes/transformation_func.py#L166"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `Tanh`
Operator node that applies the tanh function to the input. 

Output is between -1 and 1. 



**Example:**
 ```python
         >>> vals = np.array([-3, -2, -1, 0, 1, 2, 3])
         >>> tanh = Tanh("tanh", "vals")
         >>> tanh(vals)
         array([-0.995, -0.964, -0.762,  0.   ,  0.762,  0.964,  0.995])
``` 

<a href="../../pheno_sim/func_nodes/transformation_func.py#L180"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `__init__`

```python
__init__(alias: str, input_alias: str)
```

Initialize Tanh node. 



**Args:**
 
 - <b>`alias`</b>:  The alias of the node. 
 - <b>`input_alias`</b>:  The alias of the input node. 




---

<a href="../../pheno_sim/func_nodes/transformation_func.py#L190"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `run`

```python
run(input_vals)
```

Return the input with tanh applied. 




---

_This file was automatically generated via [lazydocs](https://github.com/ml-tooling/lazydocs)._
