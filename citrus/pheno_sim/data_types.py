""" Data types used in simulation. 

Data types:

	Values: A numpy array of values. The first dimension is the number of
		individuals. If there is a second dimension, then it some number of
		values for each individual. For example, if there are 100 individuals
		and each individual has 3 values, then the shape of the array would be
		(100, 3).
        
	HaplotypeValues: A tuple of two numpy arrays of values. The should be
		indexed such that for each chromosome, the first item in the tuple is
        always the value from the same copy of the chromosome. And similarly,
        the second item in the tuple is always the value from the other copy
        of the chromosome.
        
	ValuesDict: A dictionary of Values or HaplotypeValues.
"""

import numpy as np
from typing import Tuple, Union, Dict

Values = np.ndarray
HaplotypeValues = Tuple[np.ndarray, np.ndarray]
ValuesDict = Dict[str, Union[HaplotypeValues, Values]]
