import pandas as pd
import numpy as np

def printCount(label, df):
    print("Entries " + label + ":\t" + str(len(df)))

# Load the dataset.
df = pd.read_parquet('veridion_product_deduplication_challenge.snappy.parquet', engine='pyarrow')
printCount("before processing", df)

# Same product title on the same domain should be duplicate.
df = df.drop_duplicates(['root_domain', 'product_title'])
printCount("after deduplication", df)
