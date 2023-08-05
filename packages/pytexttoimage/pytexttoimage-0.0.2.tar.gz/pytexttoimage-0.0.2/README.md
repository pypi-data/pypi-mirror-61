# Text_To_Image
Method to convert text to image in python using opencv2

# INSTALL
pip install pytexttoimage

# EXAMPLE
```python
from pytexttoimage.texttoimage import text_2_image

fontscale = 2
filename = 'sample.png'
thickness = 2
textcolor = (0,0,0)
mark = 'EXAMPLE TEXT'
text_2_image(mark,filename,fontscale,thickness,textcolor)
```
