'''
Function:         step(FVr_x)
Author:           Rainer Storn, Mathew McAteer (Python Implementation)
Description:      Implements the step function which is 0 for
                  negative input arguments and 1 otherwise.
Parameters:       FVr_x        (I)    Input vector
Return value:     FVr_y        (O)    Output vector
'''
import numpy as np

def step(FVr_x):
	# np.sign is the signum function
	FVr_y = 0.5 * np.sign(FVr_x) + 0.5
	return FVr_y