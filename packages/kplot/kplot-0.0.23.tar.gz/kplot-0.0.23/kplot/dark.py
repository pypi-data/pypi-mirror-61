import matplotlib.pyplot as plt
from glob import glob
import sys

def find():
    for p in sys.path:
        search = glob(p+'*dark.mplstyle')
        print(search)
        if len(search) == 1:
            return search[0]
           
dark = find()
print(dark)
plt.style.use(dark)
plt.plot([1,2],[1,2])
plt.show()