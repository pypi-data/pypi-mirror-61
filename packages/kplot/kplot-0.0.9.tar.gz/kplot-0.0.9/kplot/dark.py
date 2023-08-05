import matplotlib.pyplot as plt
import os 
dir_path = os.path.dirname(os.path.realpath(__file__))

def find(name, path):
    for root, dirs, files in os.walk(path):
        if name in files:
            return str(os.path.join(root, name))
            
            
dark = find('dark.mplstyle', dir_path)
print(dark)
plt.style.use([dark])
plt.plot([1,2],[1,2])
plt.show()