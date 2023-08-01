<!-- markdownlint-disable -->

<a href="../../pheno_sim/func_nodes/node_builder.py#L0"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

# <kbd>module</kbd> `node_builder`
Class that initializes and returns function nodes. Used by PhenoSimulation to initialize steps.  

By default registers all function nodes (subclasses of AbstractBaseFunctionNode) in the func_nodes package. User can also provide a list of custom function nodes to register. 



---

<a href="../../pheno_sim/func_nodes/node_builder.py#L14"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `FunctionNodeBuilder`




<a href="../../pheno_sim/func_nodes/node_builder.py#L16"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `__init__`

```python
__init__(custom_classes=[])
```

Initialize node builder. 

By default registers all function nodes (subclasses of AbstractBaseFunctionNode) in func_nodes dir.  

Any classes specified in custom_classes list will also be registered. 




---

<a href="../../pheno_sim/func_nodes/node_builder.py#L51"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `create_node`

```python
create_node(class_name, **kwargs)
```

Creates a function node of the specified class.  




---

_This file was automatically generated via [lazydocs](https://github.com/ml-tooling/lazydocs)._
