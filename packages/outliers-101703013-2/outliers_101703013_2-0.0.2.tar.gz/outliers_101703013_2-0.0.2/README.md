With the help of this package, we can remove the outliers present in the dataset. 
To do so, the Interquartile range is calculated which is the difference between the third quartile and first quartile.
The target is to remove the rows having values greater than maximum and less than minimum, 
where minimum = Q1 - 1.5 * IQR
      maximum = Q3 + 1.5 * IQR
 
