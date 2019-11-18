from numpy import mat, dot, zeros, diag
from numpy.linalg import svd, inv

a = mat([[1, 2], [3, 4], [5, 6]])
print(a)
u, s, v = svd(a)
sigma = zeros(a.shape)
sigma[:a.shape[1], :a.shape[1]] = diag(s)
b = u*sigma*v
print(b)
