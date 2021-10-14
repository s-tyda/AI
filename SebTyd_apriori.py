import pandas as pd
from mlxtend.frequent_patterns import apriori
from mlxtend.frequent_patterns import association_rules

df = pd.read_csv('resources/supermarket.csv')
df = df.drop('total', axis=1)


df = df.replace('t', True)
df = df.replace('?', False)

print('Most frequent combinations: ')
frequent = apriori(df, min_support=0.35, use_colnames=True).sort_values(by='support', ascending=False)
print(frequent)

print('\nRules:')
rules = association_rules(frequent, metric="confidence", min_threshold=0.8)
print(rules.to_string())
