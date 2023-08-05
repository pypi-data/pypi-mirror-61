# Outlier Removal Project 2 UCS633 


Submitted By:kunal bajaj 
roll no : 101703297
***
pypi: <https://pypi.org/project/outlier-removal-101703297>
<br>

***

In statistics, an **outlier** is an observation point that is distant from other observations.

## Interquartile Range Method is used which mean if a data point lies below lower_quartile-1.5*iqr or above upper_quartile+1.5*iqr then it is a outlier 

## Installing the package

Run the following command to install from command line:

pip install outlier-removal-101703297


<br>


# In Command Prompt:
```
>> remove-outliers data.csv
```
<br>

### In Python IDLE:
```
>>> from outlier_removal.outlier import remove_outliers
>>> new_file = pd.read_csv('input_data.csv')
>>> remove_outliers(new_file)

<br>

## Output
Will shows the removed outliers

<br>
