import pandas as pd
import numpy as np

# Load the dataset
df = pd.read_parquet('veridion_product_deduplication_challenge.snappy.parquet')
print(df.head())