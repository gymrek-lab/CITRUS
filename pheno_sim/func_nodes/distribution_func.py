"""Function nodes that draw values from a distribution.

Classes:

    * Distribution: Draw values from a distribution.
"""

import numpy as np

from pheno_sim.base_nodes import AbstractBaseFunctionNode


class Distribution(AbstractBaseFunctionNode):
    """Class that draws values from a distribution.
    
    Any distribution that can be sampled from using numpy.random.Generator
    can be used. The parameters for the distribution (see numpy docs
    https://numpy.org/doc/stable/reference/random/generator.html#distributions)
    are passed as the dist_kwargs argument. 'size' should not be passed as
    it is determined by the shape of the match_size input array.

    Note that the distribution is sampled every time the node is called. There
    is not one value that is drawn and then used in the future, as is the case
    with RandomConstant.

    Examples:
    ```python
        >>> match_size = np.array([[1, 2, 3], [4, 5, 6]])
        >>> Distribution(
            "dist", "match_size", "uniform", 
            {"low": 0, "high": 1}
        )(match_size)
        array([[0.5488135 , 0.71518937, 0.60276338],
               [0.54488318, 0.4236548 , 0.64589411]])
    ```
    
    Args:
        alias: The alias of the node.
        input_match_size: The alias of the input node for values used to
            determine the size of the output array.
        dist_name: The name of the distribution to sample from.
        dist_kwargs: The keyword arguments for the distribution.
    """
    
    def __init__(
        self,
        alias: str,
        input_match_size: str,
        dist_name: str, 
        dist_kwargs: dict
    ):
        """Initialize Distribution node."""
        super().__init__(alias)
        self.inputs = input_match_size
        self.dist_name = dist_name
        self.dist_kwargs = dist_kwargs

    def run(self, input_match_size):
        """Draw values from the distribution."""
        dist = getattr(np.random.default_rng(), self.dist_name)
        return dist(size=input_match_size.shape, **self.dist_kwargs)
    

if __name__ == "__main__":
    
    # Test Distribution
    match_size = np.array([[1, 2, 3], [4, 5, 6]])

    dist = Distribution(
        "dist", "match_size", "uniform",
        {"low": 0, "high": 1}
    )
    
    print(dist(match_size))