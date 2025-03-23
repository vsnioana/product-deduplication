# product-deduplication

This is my submission for the **Product Deduplication** engineering challenge proposed by **Veridion**. It's a solution for cleaning and deduplicating a dataset of products entries scraped from multiple web sources. In the following, I will explain my thought process regarding the implementation.

<br>

## Analyzing the dataset
Looking at the columns and the entries in the dataset, my first thought was identifying the fields that make a product unique. The ones that caught my attention were *product_title*, *product_name*, *brand* and *product_identifier*.<br><br>
Since *product_name* seemed to be more generic and usually included in *product_title*, I decided the latter would be more useful. The brand will also be useful in identifying a product, since multiple manufacturers could sell the same product.<br><br>
Also, I noticed there wasn't a clear convention for representing empty values - most were empty lists, some were represented as -1 and others were null.<br><br>

## Choosing the tools
Since I didn't have prior experience with similar tasks, I did a little research online on what tools would be more suitable for manipulating large datasets and doing the operations needed.<br><br>
After comparing multiple libraries, I decided to go with *Pandas*, as I already had some python knowledge. This tool allowed me to easily navigate and manipulate the parquet file provided. Before jumping into the actual implementation, I played around with it using the python CLI and learned what it's capable of.<br><br>

## Cleaning the data
I wanted to have a single value for all empty fields in the dataset. I used the *pyarrow* engine for reading the parquet file, since *fastparquet* didn't correctly import all the columns for some reason. With pyarrow, I got empty values in the form of *[]* and *None*, so I replaced all these values with *NaN*, as I noticed it exported them as null.<br><br>
Another thing I did in the cleaning step was to remove the columns that contained the same value for all rows, since they didn't add any value to the dataset. This was actually a single columns - *manufacturing_year*, which had the value -1 for all entries.<br><br>

## Deduplication
For deduplicating the entries in the dataset, I used pandas' *groupby* method. This allowed me to select one or more key fields for the merged entry, and also to specify how I want the rest of the fields to be handled, as opposed to the *drop_duplicates* method, which would have lost data from partial entries.<br><br>
After experimenting with different key fields combinations, I decided actually group the entries by a custom field (called it hash). This hash contains the product title (product name in case the title is empty) and the brand. It also removes non-alphanumeric characters from these fields, in order to account for different formatting from different sources. Using this approach, I got the following result:

	Entries before processing:      21946
	Entries after deduplication:    18878

In order to not lose data from incomplete entries, I used a custom aggregator function to merge the fields of the deduplicated rows, by simply joining them with commas. The basic fields (*product_title*, *brand* etc.) were not joined, as they were most likely the same, so I configured it to keep the first occurence.<br><br>

## Results
After running the script on the given file, we obtain a clean and deduplicated dataset, where each product contains all its available information in an unique entry.