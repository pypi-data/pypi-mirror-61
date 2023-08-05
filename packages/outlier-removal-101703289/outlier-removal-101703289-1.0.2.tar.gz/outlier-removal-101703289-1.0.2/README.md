# Outlier Removal using Interquartile Range - Python

**Project 2 : UCS633**


Submitted By: **Khushnuma Grover 101703289**

***
pypi: <https://pypi.org/project/outlier-removal-101703289>
<br>
git: <https://github.com/khushgrover/outlier-removal-python.git>
***

## What are Outliers ?

There are certain things which, if are not done in the Exploratory Data Analysis phase, can affect further statistical/Machine Learning modelling. One of them is finding **Outliers**.

In statistics, an **outlier** is an observation point that is distant from other observations.

## Interquartile Range Method

<p>A robust method for labelling outliers is the IQR (interquartile range) method of outlier detection developed by John Tukey, the pioneer of exploratory data analysis. This was in the days of calculation and plotting by hand, so the datasets involved were typically small, and the emphasis was on understanding the story the data told. A box-and-whisker plot (also a Tukey contribution), shows this method in action.</p>

<p>A box-and-whisker plot uses quartiles (points that divide the data into four groups of equal size) to plot the shape of the data. The box represents the 1st and 3rd quartiles, which are equal to the 25th and 75th percentiles. The line inside the box represents the 2nd quartile, which is the median.</p>

<p>The interquartile range, which gives this method of outlier detection its name, is the range between the first and the third quartiles (the edges of the box). Tukey considered any data point that fell outside of either 1.5 times the IQR below the first – or 1.5 times the IQR above the third – quartile to be outside or far out. In a classic box-and-whisker plot, the 'whiskers' extend up to the last data point that is not outside.</p>


<br>

## How to use this package:

In this package this method is implemented. It take in the dataset csv file and outputs out a csv file in the rows having outlier values are removed. This package handles univariate datasets as well as multivariate. Each feature having outlier rows are removed.

OUTLIER-REMOVAL-KHUSHNUMA-101703289  can be run as in the following example:

## Installing the package

On your Command Prompt run the following command:

pip install outlier-removal-101703289

## Sample dataset

The dataset should be constructed with each row representing a data, and each column representing a criterion feature, ending with a target.

<br>

Feature | Target
------- | ------
10 | 0.62
100 | 0.44
100 | 0.31
100 | 0.67
10 | 0.56

<br>

### In Command Prompt:
```
>> remove-outlier data.csv
```
<br>

### In Python IDLE:
```
>>> from outlier_removal.outlier import remove_outlier
>>> file1 = pd.read_csv('data.csv')
>>> remove_outlier(file1)
```

<br>

## Output


Feature | Target
------- | ------
100 | 0.44
100 | 0.31
100 | 0.67

<br>
