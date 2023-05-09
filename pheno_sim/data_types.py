""" Data types used in simulation. """

import numpy as np
from typing import Tuple, Union, Dict

HaplotypeValues = Tuple[np.ndarray, np.ndarray]
Values = np.ndarray
ValuesDict = Dict[str, Union[HaplotypeValues, Values]]
