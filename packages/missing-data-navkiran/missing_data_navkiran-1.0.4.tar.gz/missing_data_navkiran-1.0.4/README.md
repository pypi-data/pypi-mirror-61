# Library for Handling Missing Data

```
PROJECT 3, UCS633 - Data Analysis and Visualization
Navkiran Singh  
COE17
Roll number: 101703365
```

Takes two inputs - filename of input csv, intended filename of output csv. 

Two optional arguments - which must be provided together or left out.


Resulting csv is saved with the name you provide. 


## Installation
`pip install missing_data_navkiran`

*Recommended - test in a virtual environment.* 

## Use via command line

Defaults are drop NaN with parameter along = 0 (drops rows containing NaN)
 
`missing_data_navkiran_cli in.csv out.csv`

Drop rows with NaN
`missing_data_navkiran_cli in.csv out.csv DROP 0` 

Drop columns with NaN
`missing_data_navkiran_cli in.csv out.csv DROP 1`

Forward filling
`missing_data_navkiran_cli in.csv out.csv FILL 0`

Backward filling
`missing_data_navkiran_cli in.csv out.csv FILL 1`

Imputing with mean
`missing_data_navkiran_cli in.csv out.csv IMPUTE 0`

Imputing with median
`missing_data_navkiran_cli in.csv out.csv IMPUTE 1`

Imputing with mode
`missing_data_navkiran_cli in.csv out.csv IMPUTE 2`

First argument after outcli is the input csv filename from which the dataset is extracted. The second argument is for storing the final dataset after processing.

## Use in .py script
```
from missing_data_navkiran import dropval,filler,impute
input_df = pd.read_csv('in.csv')
```
axis = 0
`output_df = dropval(input_df,along=0)`

axis = 1 
`output_df = dropval(input_df,along=1)`

backward-filling
`output_df = filler(input_df,0)`

forward-filling
`output_df = filler(input_df,1)`

Mean
`output_df = impute(input_df,0)`

Median
`output_df = impute(input_df,1)`

Mode
`output_df = impute(input_df,2)`


There are also stand alone functions to fill numerical data and fill categorical data.

```
from missing_data_navkiran import fill_numerical,fill_categorical
fill_numerical(input_df,list_of_numerical_columns)
fill_categorical(input_df,list_of_categorical_columns)
```

