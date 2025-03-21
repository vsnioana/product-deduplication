import re

def printCount(label, df):
    print("Entries " + label + ":\t" + str(len(df)))

def buildHashForRow(x):
    if isinstance(x.brand, str):
        brand = re.sub(r'[^a-zA-Z0-9]', '', x.brand).lower()
        if brand in x.hash:
            x.hash = x.hash.replace(brand,'')
        x.hash += brand