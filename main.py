import pandas as pd
import numpy as np
import re
import utils

# Load the dataset.
df = pd.read_parquet('veridion_product_deduplication_challenge.snappy.parquet', engine='pyarrow')
df = df.map(str)
utils.printCount("before processing", df)

# Replace empty values with NaN.
df = df.replace('[]', np.nan)
df = df.replace('None', np.nan)

# We want to remove columns that contain the same values for all rows.
# They don't add any value to our dataset.
for column in df:
    if len(df[column].unique()) == 1:
        print("Dropping column " + column)
        df = df.drop(column, axis=1)

# Deduplication
df['hash'] = df['product_title'].map(lambda x: re.sub(r'[^a-zA-Z0-9]', '', x).lower(), na_action='ignore')
df.apply(lambda x: utils.buildHashForRow(x), axis=1)

df = df.groupby('hash').agg(utils.buildAggregator(df)).reset_index()
utils.printCount("after deduplication", df)

df.to_parquet('myfile.parquet')