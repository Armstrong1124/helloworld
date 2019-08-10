import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


# numpy类似列表append功能
a = np.array(range(10)).reshape((5, 2))
small = a[:2]
print(small)
for i in a[2:]:
    small = np.row_stack((small[1:], i))
    print(small)
