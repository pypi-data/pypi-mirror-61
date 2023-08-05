import matplotlib.pyplot as plt
import os 
dir_path = os.path.dirname(os.path.realpath(__file__))

def find(name, path):
    for root, dirs, files in os.walk(path):
        if name in files:
            return os.path.join(root, name)
            
            
dark = find('dark.mplstyle', dir_path)
plt.style.use(dark)