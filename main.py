import pandas as pd
import numpy as np

def printCount(label, df):
    print("Entries " + label + ":\t" + str(len(df)))

# Load the dataset.
df = pd.read_parquet('veridion_product_deduplication_challenge.snappy.parquet', engine='pyarrow')
df = df.map(str)
printCount("before processing", df)

# Same product title on the same domain should be duplicate.
df = df.drop_duplicates(['root_domain', 'product_title'])
printCount("after deduplication", df)

# Replace empty values with None.
df = df.replace('[]', np.nan)

# We want to remove columns that contain the same values for all rows.
# They don't add any value to our dataset.
for column in df:
    if len(df[column].unique()) == 1:
        print("scot " + column)
        df = df.drop(column, axis=1)

