import matplotlib.pyplot as plt
import numpy as np

grid = np.random.random((10,10))

fig, (ax1, ax2, ax3, ax4, ax5) = plt.subplots(nrows=5, figsize=(6,10))

ax1.imshow(grid, extent=[0,100,0,1])
ax1.set_title('Default')

ax2.imshow(grid, extent=[0,100,0,1], aspect='auto')
ax2.set_title('Auto-scaled Aspect')

ax3.imshow(grid, extent=[0,100,0,1], aspect=100)
ax3.set_title('Manually Set Aspect')

ax4.imshow(grid, extent=[0,100,0,1], aspect=200)
ax4.set_title('Manually Set Aspect')

ax5.imshow(grid, extent=[0,100,0,1], aspect=50)
ax5.set_title('Manually Set Aspect')

plt.tight_layout()
plt.show()

