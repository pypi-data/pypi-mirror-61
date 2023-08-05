# Package for implementing topsis functionality

```
Naveen Budhwal  
COE-16
Roll number: 101703362
```
## Description
Package for implementing the topsis functionality easily.

## Installation
`pip install topsis_naveen`

## Command Line Arguments
`topsis_naveen <dataset>.csv "<weigths> "<levels>"`

First argument is the input csv filename containing the dataset. 
The second argument is the weigths assigned to each column.
The third argument is a string of +,- denoting whether the particular column/feature needs to be increased(+) or decreased(-)

## Use via py script
```
from topsis_naveen import topsis
topsis('<input_filename>.csv', '<Weights>', '<Levels>')
```
