"""General math function nodes for the simulation.

Classes:

    * Identity: A node that returns the input. Mainly for testing.
    
    * Sum: A node that sums some inputs element-wise.

    * Product: A node that multiplies some inputs element-wise.
"""

import numpy as np

from ..data_types import HaplotypeValues, Values, ValuesDict
from ..base_nodes import AbstractBaseFunctionNode


class Identity(AbstractBaseFunctionNode):
    """A node that returns the input.
    
    Examples:
    ```python
        >>> Identity("identity", "arr")(np.array([1, 2, 3]))
        array([1, 2, 3])
        >>> Identity("identity", "hap")(
            (np.array([1, 2, 3]), np.array([4, 5, 6]))
        )
        (array([1, 2, 3]), array([4, 5, 6]))
    ```
    """
    
    def __init__(self, alias: str, input_alias: str):
        """Initialize Identity node.
        
        Args:
            alias: The alias of the node.
            input_alias: The alias of the input node.
        """
        super().__init__(alias)
        self.inputs = input_alias

    def run(self, input_vals):
        """Return the input."""
        return input_vals
    

class Sum(AbstractBaseFunctionNode):
    """A node that sums some inputs element-wise.

    If all inputs are vectors (num_samples length arrays), then the output
    is a vector that is the element-wise sum of the inputs.

    If all inputs are all matrices (num_feats x num_samples arrays), then
    the output is a matrix (with the same dimensions) that is the 
    element-wise sum.

    If the input is a mix of vectors and matrices:
        - All matrices must have the same dimensions.
        - Matrices are summed element-wise.
        - Vectors are summed element-wise over each of the num_feats of
            the matrices.

    Examples:
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
    """

    def __init__(self, alias: str, input_aliases: list):
        """Initialize Sum node.

        Args:
            alias: The alias of the node.
            input_aliases (list): The aliases of the inputs to be summed.
        """
        super().__init__(alias)
        self.inputs = input_aliases

    def run(self, *input_vals):
        """Return the sum of the inputs."""
        return np.sum(np.array(input_vals, dtype=object), axis=0).astype(float)
    

class Product(AbstractBaseFunctionNode):
    """A node that multiplies some inputs element-wise.

    If all inputs are vectors (num_samples length arrays), then the output
    is a vector that is the element-wise product of the inputs.

    If all inputs are all matrices (num_feats x num_samples arrays), then
    the output is a matrix (with the same dimensions) that is the
    element-wise product.

    If the input is a mix of vectors and matrices:
        - All matrices must have the same dimensions.
        - Matrices are multiplied element-wise.
        - Vectors are multiplied element-wise over each of the num_feats of
            the matrices.

    Examples:
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
    """

    def __init__(self, alias: str, input_aliases: list):
        """Initialize Product node.
        
        Args:
            alias: The alias of the node.
            input_aliases (list): The aliases of the inputs to be multiplied.
        """
        super().__init__(alias)
        self.inputs = input_aliases

    def run(self, *input_vals):
        """Return the product of the inputs."""
        return np.prod(np.array(input_vals, dtype=object), axis=0).astype(float)

    
if __name__ == "__main__":
    from pheno_sim.pheno_simulation import PhenoSimulation
    
    # Test Identity
    vals = np.array([1, 2, 3])
    hap_vals = (np.array([1, 2, 3]), np.array([4, 5, 6]))

    identity_node = Identity("identity", "arr")

    print(identity_node(vals))
    print(identity_node(hap_vals))


    # Test Sum
    sum_node = Sum("sum", ["arrs"])

    print(sum_node([np.array([1, 2, 3]), np.array([4, 5, 6])]))
    print(sum_node([
        np.array([[1, 2, 3], [4, 5, 6]]),
        np.array([[7, 8, 9], [10, 11, 12]])
    ]))
    print(sum_node([	
        np.array([1, 2, 3]),
        np.array([[1, 1, 1], [2, 2, 2]]),
        np.array([[1, 1, 1], [2, 2, 2]])
    ]))

    vals = [	
        np.array([1, 2, 3]),
        np.array([[1, 1, 1], [2, 2, 2]]),
        np.array([[1, 1, 1], [2, 2, 2]])
    ]
    hap_vals = (vals, vals)

    print(sum_node(vals))
    print(sum_node(hap_vals))


    # Test Product
    product_node = Product("product", ["arrs"])

    print(product_node([np.array([1, 2, 3]), np.array([4, 5, 6])]))
    print(product_node([
        np.array([[1, 2, 3], [4, 5, 6]]),
        np.array([[7, 8, 9], [10, 11, 12]])
    ]))
    print(product_node([
        np.array([1, 2, 3]),
        np.array([[1, 1, 1], [2, 2, 2]]),
        np.array([[1, 1, 1], [2, 2, 2]])
    ]))