### UCS633 Project Submission
* **Name** - *Kartikey Tiwari* 
* **Roll no.** - *101703282* 

# remove-outliers

remove-outliers is a Python package for removing outliers from a dataset using IQR Interquartile range

## IQR Interquartile range Description

Any set of data can be described by its five-number summary. These five numbers, which give you the information you need to find patterns and outliers, consist of (in ascending order):

The minimum or lowest value of the dataset
The first quartile Q1, which represents a quarter of the way through the list of all data
The median of the data set, which represents the midpoint of the whole list of data
The third quartile Q3, which represents three-quarters of the way through the list of all data
The maximum or highest value of the data set.

These five numbers tell a person more about their data than looking at the numbers all at once could, or at least make this much easier. For example, the range, which is the minimum subtracted from the maximum, is one indicator of how spread out the data is in a set (note: the range is highly sensitive to outliers—if an outlier is also a minimum or maximum, the range will not be an accurate representation of the breadth of a data set).

Range would be difficult to extrapolate otherwise. Similar to the range but less sensitive to outliers is the interquartile range. The interquartile range is calculated in much the same way as the range. All you do to find it is subtract the first quartile from the third quartile:

IQR = Q3 – Q1.
The interquartile range shows how the data is spread about the median. It is less susceptible than the range to outliers and can, therefore, be more helpful.

## Using the Interquartile Rule to Find Outliers

Though it's not often affected much by them, the interquartile range can be used to detect outliers. This is done using these steps:


Calculate the interquartile range for the data.
Multiply the interquartile range (IQR) by 1.5 (a constant used to discern outliers).
Add 1.5 x (IQR) to the third quartile. Any number greater than this is a suspected outlier.
Subtract 1.5 x (IQR) from the first quartile. Any number less than this is a suspected outlier.
Remember that the interquartile rule is only a rule of thumb that generally holds but does not apply to every case. In general, you should always follow up your outlier analysis by studying the resulting outliers to see if they make sense. Any potential outlier obtained by the interquartile method should be examined in the context of the entire set of data.

## Interquartile Rule Example Problem

See the interquartile range rule at work with an example. Suppose you have the following set of data: 1, 3, 4, 6, 7, 7, 8, 8, 10, 12, 17. The five-number summary for this data set is minimum = 1, first quartile = 4, median = 7, third quartile = 10 and maximum = 17. You may look at the data and automatically say that 17 is an outlier, but what does the interquartile range rule say?

If you were to calculate the interquartile range for this data, you would find it to be:

Q3 – Q1 = 10 – 4 = 6
Now multiply your answer by 1.5 to get 1.5 x 6 = 9. Nine less than the first quartile is 4 – 9 = -5. No data is less than this. Nine more than the third quartile is 10 + 9 =19. No data is greater than this. Despite the maximum value being five more than the nearest data point, the interquartile range rule shows that it should probably not be considered an outlier for this data set.

## Getting Started

These instructions will help you to install and use this package for general use. 

## Prerequisites

Your csv file should have only one target variabl(last column of the dataset)


## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install remove-outliers.

```bash
pip install remove-outliers
```

## Usage
You can import it either in Python IDLE or run directly through command prompt

### For Command Prompt

If you want to use this package on "data.csv" file. You need to change the directory where "data.csv" is stored then pass the name of csv file ("data.csv") as an input, you can also provide name of your new file with removed outliers eg: "newdata.csv". After execution the directory where "data.csv" is stored will also have another csv named "newdata.csv" without all outliers removed. In case you dont provide name for your destination file then your new csv file without outliers will be stored as "OutlierRemoveddata.csv"

```bash
remove-outliers data.csv newdata.csv
```
or

```bash
remove-outliers data.csv 
```

### For Python IDLE

```python
from remove-outliers.remove import remove_outlier
remove_outlier(file1,file2)

#file1 is name of your csv file on which you will perform operation
#file2 is the name of your updated csvfile, if you dont pass any file2 name it will take the default name of "OutlierRemoved.csv"
```
### Sample dataset


|Scores 	   |Players   |
| ------------ |:------:  |      
|500	       | Player1  | 
|350	       | Player2  | 
|10	    	   | Player3  |
|300	       | Player4  |
|450	       | Player5  |

```bash
remove-outliers players.csv OutlierRemoved.csv
```

### Result

|Scores 	   |Players   |
| ------------ |:------:  |      
|500	       | Player1  | 
|350	       | Player2  | 
|300	       | Player4  |
|450	       | Player5  |

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
[MIT](https://choosealicense.com/licenses/mit/)