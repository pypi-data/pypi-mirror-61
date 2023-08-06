Python package use cuda to normalize input variables using cuda package in ATLAS analysis

Function use to do Guassian Normalization:
Mean:
$$\mu_{i}=\frac{\sum x_{i}\times w_{i}}{\sum w_{i}}$$
Variance:
$$\sigma_{i}=\frac{\sum (x_{i}-\mu_{i})^{2}\times w_{i}}{\frac{N-1}{N}\times\sum w_{i}}$$
Normalized input feature:
$$\bar{x_{i}}=\frac{x_{i}-\mu_{i}}{\sigma_{i}}$$

Main function: guass_normal((1),(2),(3))

Input:

(1):Numpy array contain all input features you want to normalize.
(2):Numpy array used to calculate each feature's mean and variance.
(3):1-d Numpy array contains each events weight in (2)

(1) and (2) must have the same number of columns.

cuda_cut((1),(2),(3)): Used to calculate event yield after applying DNN cut.

Input:
(1): 1-d numpy array include the variable  you want to cut.
(2): 1-d numpy array include event weight.
(3): cut threshold 
