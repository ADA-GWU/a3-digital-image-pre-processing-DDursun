[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-22041afd0340ce965d47ae6ef1cefeee28c7c493a6346c4f15d667ab976d596c.svg)](https://classroom.github.com/a/0tZ_gm55)


# Some observations
Task 1:
- Smaller kernel size is better when the pixels are close but they should not be connected (letters).
- Connected Component presents great advantage to remove noise which is far from the structure.
- When used together with Closing, the details are even sharper. 

Task 2:
Crimming performs usually better than standard filtering because it adaptively adjusts each pixel based on its local neighborhood, effectively reducing noise while preserving details and edges that uniform smoothing seem to erase.

# References
1) T. Crimmins The Geometric Filter for Speckle Reduction, Applied Optics, Vol. 24, No. 10, 15 May 1985.
2) https://homepages.inf.ed.ac.uk/rbf/HIPR2/crimmins.htm
3) https://opencv24-python-tutorials.readthedocs.io/en/latest/py_tutorials/py_imgproc/py_morphological_ops/py_morphological_ops.html
