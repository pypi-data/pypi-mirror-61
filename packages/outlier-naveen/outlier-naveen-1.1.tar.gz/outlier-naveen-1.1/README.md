# Package for removing outliers from a dataset

```
Naveen Budhwal  
COE-16
Roll number: 101703362
```
## Description
Package for removing outliers from a given dataset using the IQR method.

## Installation
`pip install outlier_naveen`

## Command Line Arguments
`outlier_naveen <input_filename>.csv <output_filename>.csv`

First argument is the input csv filename containing the dataset. 
The second argument is the name of the output csv file that will store the modified dataset.

## Use via py script
```
from outlier_naveen import remove_outliers
remove_outliers('<input_filename>.csv', '<output_filename>.csv')
```
