# Outlier Removal Using InterQuartile Range

**Project 2 : UCS633**


Submitted By: **Kunal Jindal 101703299**

***
pypi: <https://pypi.org/project/outlierRemoval-kjindal-101703299/>
***

## InterQuartile Range (IQR) Description

Any set of data can be described by its five-number summary. These five numbers, which give you the information you need to find patterns and outliers, consist of:

The minimum or lowest value of the dataset
The first quartile Q1, which represents a quarter of the way through the list of all data
The median of the data set, which represents the midpoint of the whole list of data
The third quartile Q3, which represents three-quarters of the way through the list of all data
The maximum or highest value of the data set.

These five numbers tell a person more about their data than looking at the numbers all at once could, or at least make this much easier.

## Calculation of IQR

IQR = Q3 – Q1.
MIN = Q1 - (1.5*IQR)
MAX = Q3 + (1.5*IQR)

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install outlierRemoval-kjindal-101703299.

```bash
pip install outlierRemoval-kjindal-101703299
```
<br>

## How to use this package:

outlierRemoval-kjindal-101703299 can be run as shown below:


### In Command Prompt
```
>> outlierRemoval dataset.csv
```
<br>


## Sample dataset

Marks | Students 
:------------: | :-------------:
3 | Student1
57 | Student2
65 | Student3
98 | Student4
43 | Student5
44 | Student6
54 | Student7
99 | Student8
1 | Student9

<br>


## Output Dataset after Removal

Marks | Students 
:------------: | :-------------:
57 | Student2
65 | Student3
98 | Student4
43 | Student5
44 | Student6
54 | Student7

<br>

It is clearly visible that the rows containing Student1, Student8 and Student9 have been removed due to them being Outliers.

<br>
## License
[MIT](https://choosealicense.com/licenses/mit/)



