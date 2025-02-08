# The code in this file calculates the 'score' the algorithm attributes to each company
# based on a normal distribution curve. This data is then used by the 'main.py' file
# to make the decision on whether to buy the company or not

from math import exp, sqrt, pi

def standardized_normal_dist(x, std, mean):
    """Returns the normal place of x in a normal distribution curve whose standard
       variation and expected value are passed as parameters."""
    peak_val = (1/sqrt(2 * pi * (std**2))) * exp(-((1 - mean)**2/(2 * std**2)))
    return ((1/sqrt(2 * pi * (std**2))) * exp(-((x - mean)**2/(2 * std**2))))/peak_val

