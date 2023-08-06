# Replace Missing Values

A python package for implementation of replacing NaN values in the dataset using Simple Imputer method.

Missing values can lead to inconsistent results. We can either ignore the rows with missing data columns or substitute the values with some calculated output.
When the dataset is too small, we can’t afford to lose the row data even if it contains missing columns. In those cases, we will look at substituting the column data with some values.
Imputation is another approach to resolve the problem of missing data.
The missing column values are substituted by another computed value. There might be scenarios where the dataset is small or where each row of the dataset represents a critical value.
In those cases, we cannot remove the row from the dataset. The missing values can be imputed.
There are different strategies to define the substitute for the missing value.
The value can be substituted by these values:
The mean value of the other column values available in the training dataset.
The median value of the other values available in the training dataset.
Substitute with the most frequent value in the training dataset.
