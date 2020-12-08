import pandas as pd
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
analyser = SentimentIntensityAnalyzer()

scores =[]
sentences = ["A really bad, horrible book.","A good, awesome, wonderful, cool book !!!  :)"]

for sentence in sentences:
    score = analyser.polarity_scores(sentence)
    scores.append(score)

dataFrame= pd.DataFrame(scores)

print(dataFrame)
dataFrame.mean()

