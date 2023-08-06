# Library for Handling Missing Data

```
PROJECT 3, UCS633 - Data Analysis and Visualization
Nishchay Mahajan
COE18
Roll number: 101703377
```

Takes two inputs - filename of input csv, Method of handling data. 

Resulting csv is saved with the name OUTPUT.CSV. 


## Installation
`pip install missing-pypck`


## Use via command line

Drop rows with NaN
`python3 missing.py filename dropr` 

Drop columns with NaN
`python3 missing.py filename dropc`

Imputing with mean
`python3 missing.py filename mean`

Imputing with median
`python3 missing.py filename median`

Imputing with mode
`python3 missing.py filename mode`



