# Handling Missing Values using SimpleImputer Class

**Project 3 : UCS633**


Submitted By: **Kshitiz Varshney 101703295**

***
pypi: <https://pypi.org/project/missingValues-kvarshney-101703295/>
***

## SimpleImputer Class

SimpleImputer is a scikit-learn class which is helpful in handling the missing data in the predictive model dataset.
It replaces the NaN values with a specified placeholder.
It is implemented by the use of the SimpleImputer() method which takes the following arguments:
<br>
missing_data : The missing_data placeholder which has to be imputed. By default is NaN.
<br>
stategy : The data which will replace the NaN values from the dataset. The strategy argument can take the values � �mean'(default), �median�, �most_frequent� and �constant�.
<br>
fill_value : The constant value to be given to the NaN data using the constant strategy.


## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install missingValues-kvarshney-101703295.

```bash
pip install missingValues-kvarshney-101703295
```
<br>

## How to use this package:

missingValues-kvarshney-101703295 can be run as shown below:


### In Command Prompt
```
>> missingValues dataset.csv
```
<br>


## Input dataset



| a   | b   | c |
|-----|-----|---|
| 0   | NaN | 4 |
| 2   | NaN | 4 |
| 1   | 7   | 0 |
| 1   | 3   | 9 |
| 7   | 4   | 9 |
| 2   | 6   | 9 |
| 9   | 6   | 4 |
| 3   | 0   | 9 |
| 9   | 0   | 1 |


<br>


## Output Dataset after Handling the Missing Values

a | b | c 
:------------: | :-------------: | :-------------:
0	|4|	4
2	|4|4
1	|7|	0
1	|3|	9
7	|4	|9
2	|6|9
9	|6|	4
3	|0|	9
9	|0|	1


<br>

It is clearly visible that the rows,columns containing Null Values have been Handled Successfully using median values.


## License
[MIT](https://choosealicense.com/licenses/mit/)



