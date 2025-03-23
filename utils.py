import re

def printCount(label, df):
    print("Entries " + label + ":\t" + str(len(df)))

# The hash will contain the data that makes a product unique.
def buildHashForRow(x):
    if x.hash == "" and isinstance(x.product_name, str):
        x.hash += x.product_name.lower()
    if isinstance(x.brand, str):
        brand = re.sub(r'[^a-zA-Z0-9]', '', x.brand).lower()
        if brand in x.hash:
            x.hash = x.hash.replace(brand,'')
        x.hash += brand

# The default merge functionality will be joining the values.
def buildAggregator(df):
    aggregator = dict.fromkeys(df, '')
    aggregator.update(
        dict.fromkeys(df.columns[df.dtypes.eq(object)], lambda x: ', '.join(list(dict.fromkeys(filter(lambda x: isinstance(x, str), x))))))
    del aggregator['hash']

    aggregator['product_title'] = 'first'
    aggregator['brand'] = 'first'

    return aggregator
