# Operator Nodes

Operator nodes implement functionson some input values. The following provides an overview of the different types available and links to the full documentation in the operator_nodes subdirectory. Arguments to an operator node's `__init__` function may be used as keys in the dictionaries defining them in the simulation configuration file.

## [Conditional Operators](operator_nodes/conditional_func.md)

Implement conditional functions.

Classes:

* IfElse


## [Constant Operators](operator_nodes/constant_func.md)

Generate values representing constants and broadcast to some shape.

Classes:

* Constant: A node that generates constant values.

* RandomConstant: A node that generates constant values, where values are initially drawn from a distribution.


## [Distribution Operators](operator_nodes/distribution_func.md)

Function nodes that draw values from a distribution.

Classes:

* Distribution: Draw values from a distribution.


## [Haplotype Combine Operators](operator_nodes/hap_combine_func.md)

Combine haplotypes into a single array.

Classes:

* AdditiveCombine: A node that sums the two haplotypes element-wise to simulate an additive inheritance effect.

* MaxCombine: A node that takes the element-wise maximum of the two haplotypes to simulate a dominant inheritance effect.

* MinCombine: A node that takes the element-wise minimum of the two haplotypes to simulate a recessive inheritance effect.

* MeanCombine: A node that takes the element-wise mean of the two haplotypes. Mean is either arithmetic, geometric, or harmonic.


## [Math Operators](operator_nodes/math_func.md)

General math function nodes for the simulation.

Classes:

* Identity: A node that returns the input. Mainly for testing.

* Sum: A node that sums some inputs element-wise.

* Product: A node that multiplies some inputs element-wise.


## [Noise Operators](operator_nodes/noise.md)

Operators that add noise in the phenotype simulation.

Classes:

* GaussianNoise: A node that adds Gaussian noise to the input.

* Heritability: Contols what fraction of the information output by the node is a function of the input vs. Gaussian noise. The output is a weighted average of the input and Gaussian noise. The Gaussian noise is scaled so that the output has the same variance as the input.


## [Reduce Operators](operator_nodes/reduce_func.md)

Reduce a Values matrix to one value per sample using some operation.

Classes:

* SumReduce: Sum each sample's feature values into a single value per sample.

* MinReduce: Return the minimum of each sample's feature values as the sample's value.

* MaxReduce: Return the maximum of each sample's feature values as the sample's value.

* MeanReduce: Return the mean of each sample's feature values as the sample's value. Mean is either arithmetic (default), geometric, or harmonic.

* AnyReduce: Return 1 if any feature value is past a threshold, 0 otherwise.

* AllReduce: Return 1 if all feature values are past a threshold, 0 otherwise.


## [Scaling Operators](operator_nodes/scaling.md)

Operators that scaling input distributions in the phenotype simulation.

Classes:

* Clip: A node that clips the input to be greater than or equal to some minimum value and/or less than or equal to some maximum value.

* MinMaxScaler: A node that scales the input to be between 0 and 1 using the minimum and maximum values of the input.
	
* StandardScaler: A node that scales the input to have mean 0 and standard deviation 1 using the mean and standard deviation of the input.

* RobustScaler: A node that scales the input to have median 0 and interquartile range 1 using the median and interquartile range of the input.


## [Transformation Function Operators](operator_nodes/transform_func.md)

Non-linear transformation function operator nodes.

Take some input values and apply some transformation function, like a
sigmoid, tanh, ReLU, 

Classes:

* ReLU

* Sigmoid

* Softmax

* Tanh


## [Utility Operators](operator_nodes/util_func.md)

Utility functions.

Classes:

* Concatenate: A node that concatenates some inputs into a single array.