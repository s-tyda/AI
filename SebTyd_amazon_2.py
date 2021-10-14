import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation
from sklearn.cluster import KMeans


df = pd.read_csv('resources/train-amazon.tsv', sep='\t')

cv = CountVectorizer(max_df=0.9, min_df=2, stop_words='english')

matrix = cv.fit_transform(df['review'])
LDA = LatentDirichletAllocation(n_components=7, random_state=42)
LDA.fit(matrix)

topic_results_lda = LDA.transform(matrix)
lda_wynik = topic_results_lda.argmax(axis=1)
print(lda_wynik)


for index, topic in enumerate(LDA.components_):
    print(f'najwazniejsz 15 slow w temacie: #{index}')
    print([cv.get_feature_names()[i] for i in topic.argsort()[-15:]])
    print('\n')

text = ['WOW...Pampers, I thought you did enough trying to cut manufacturing costs when you changed the Baby-Dry diapers and made them into cheaply made, 50% less absorbing and easily breakable diapers - but wow, you e really done it now with the wipes packaging. I immediately came on Amazon to read up on the recent subscribe & save box I received because the wipes no longer had hr easy trae opening atop the packages - hoping I didn’t purchase a counterfeit product. I was very disappointed to learn I have now been let down twice by the most reputable diaper and wipes brand out there. Pampers - you’re losing your customer base and word travels, especially by moms who spend a ton of money on diaper supplies and expect thei brand they pay premium prices for',
'To live up to the quality of standard. Will br raising awareness to local hospitals, women’s groups, and spreading the word to peers of',
'This horrible unsatisfactory quality change in your products.',
'Amazon - look into this and refund your loyal customers for the price we have paid for a product we did not expect. Not good representation of the products/brands you recommend as “Amazon’s Choice”.',
'Incredibly disappointed']
transformation = cv.transform(text)
result = LDA.transform(transformation)
print(result)

kmeans = KMeans(init="random", n_clusters=7, n_init=10, max_iter=300, random_state=42)
results = kmeans.fit_transform(matrix)
result = kmeans.transform(transformation)

for index, topic in enumerate(kmeans.cluster_centers_):
    print(f'najwazniejsz 15 slow w temacie: #{index}')
    print([cv.get_feature_names()[i] for i in topic.argsort()[-15:]])
    print('\n')

print(result)
