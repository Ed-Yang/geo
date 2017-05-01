
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from scipy import misc
import os


dirname, filename = os.path.split(os.path.abspath(__file__))

#image=misc.imread(dirname + "\\marker-icon.png")
image=mpimg.imread(dirname + "\\marker-icon.png")
#plt.imshow(image, cmap=plt.cm.gray)
#plt.imshow(image)
plt.imshow(image, aspect='auto', extent=(0.4, 0.6, .5, .7), zorder=-1)

#lum_img = image[:,:,0]
#imgplot = plt.imshow(lum_img)

plt.show()



