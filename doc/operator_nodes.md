# Operator Nodes

Operator nodes implement functionson some input values. The following provides an overview of the different types available and links to the full documentation in the operator_nodes subdirectory. Arguments to an operator node's `__init__` function may be used as keys in the dictionaries defining them in the simulation configuration file.

## [Conditional Operators](operator_nodes/conditional_func.md)

Implement conditional functions. Includes:

- IfElse


## [Constant Operators](operator_nodes/constant_func.md)

Generate values representing constants and broadcast to some shape. Includes:

- Constant
- RandomConstant


## [Distribution Operators](operator_nodes/distribution_func.md)

Function nodes that draw values from a distribution. Includes:

- Distribution


## [Haplotype Combine Operators](operator_nodes/hap_combine_func.md)

Combine haplotypes into a single array. Includes:

- AdditiveCombine
- MaxCombine
- MinCombine
- MeanCombine


## [Math Operators](operator_nodes/math_func.md)

General math operators. Includes:

- Identity
- Sum
- Product


## [Reduce Operators](operator_nodes/reduce_func.md)

Reduce a Values matrix to one value per sample using some operation. Includes:

- SumReduce
- MinReduce
- MaxReduce
- MeanReduce
- AnyReduce
- AllReduce


## [Utility Operators](operator_nodes/util_func.md)

Utility functions. Includes:

- Concatenate: A node that concatenates some inputs into a single array.