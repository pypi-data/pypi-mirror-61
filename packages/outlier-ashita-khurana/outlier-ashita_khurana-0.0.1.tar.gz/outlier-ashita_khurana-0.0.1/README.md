This Python package is created to remove outlier rows from a dataset. To use thi dataset you need to create a pandas dataframe(you can use pd.read_csv() to do it), and to to use this package your dataset should have only numerical values and if you have any strings then you can use one hot encoding or simple label encoder to do that, but make sure before using it that it is all done. Now this function takes one argument that is the dataframe. To use it you have to write:

from outliers-ashita_khurana import outlier df = outlier.rem_out(data)

and your df variable will now contain the new data which will not contain outlier rows and this function will also print the number of rows deleted!