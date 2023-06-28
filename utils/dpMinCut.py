import numpy as np
from sys import maxsize

def minCut(img_overlap, out_overlap, loc):
    """
    Function to perform min-cut image segmentation based on energy values.
    Min-Cut of a weighted graph is defined as the minimum sum of weights of (at least one)edges 
    that when removed from the graph divides the graph into two groups. Mechthild Stoer and Frank Wagner proposed an 
    algorithm in 1995 to find minimum cut in an undirected weighted graphs.
    Args:
    - img_overlap: Input image overlap matrix
    - out_overlap: Output overlap matrix
    - loc: Location parameter, "horizontal" or "vertical"

    Returns:
    - cut: Matrix indicating the cut path

    """

    # Calculate the difference between input and output overlap matrices
    diff = img_overlap - out_overlap

    # Calculate the energy matrix by squaring the differences and summing along the third axis
    E = np.sum(np.multiply(diff, diff), axis=2)

    # Transpose the energy matrix if loc is set to "horizontal"
    if loc == "horizontal":
        E = np.transpose(E)

    # Get the dimensions of the energy matrix
    R, C = E.shape[:2]

    # Initialize matrices for cut and dynamic programming (DP)
    cut = np.ones((R, C))
    DP = np.zeros((R, C))

    # Populate the first row of DP with corresponding values from the first row of E
    for i in range(C):
        DP[0, i] = E[0, i]

    # Calculate the minimum energy path using dynamic programming
    for i in range(1, R):
        for j in range(C):
            paths = []
            paths.append(DP[i-1, j])
            if j != 0:
                paths.append(DP[i-1, j-1])
            if j != C-1:
                paths.append(DP[i-1, j+1])
            DP[i, j] = E[i, j] + min(paths)

    # Find the index with the minimum value in the last row of E
    min_val = min_idx = maxsize
    for i in range(C):
        if min(min_idx, E[R-1, i]) < min_val:
            min_idx = i

    # Set the corresponding element in the last row of cut to 0 and adjust the values in cut based on the minimum index
    cut[R-1, min_idx] = 0
    cut[R-1, min_idx+1:C] = 1
    cut[R-1, 0:min_idx] = -1

    # Iterate over the remaining rows in reverse order and adjust the values in cut based on the minimum index
    for i in range(R-2, -1, -1):
        for j in range(C):
            if min_idx < C-1:
                if E[i, min_idx+1] == min(E[i, max(0, min_idx-1):min_idx+2]):
                    min_idx = min_idx + 1
            if min_idx > 0:
                if E[i, min_idx-1] == min(E[i, min_idx-1:min(C-1, min_idx+2)]):
                    min_idx = min_idx - 1
            cut[i, min_idx] = 0
            cut[i, min_idx+1:C] = 1
            cut[i, 0:min_idx] = -1

    # Transpose cut if loc is "horizontal" before returning
    if loc == "horizontal":
        cut = np.transpose(cut)

    return cut
