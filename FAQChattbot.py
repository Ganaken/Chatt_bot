# -*- coding: UTF-8 -*-
import numpy
import json
import os.path
import sys
from sklearn.feature_extraction.text import CountVectorizer # countvectoriser creats tokens for each data set
import time
import numpy.linalg as LA #importing the linear algebra module
# from Deep_chat import the_best_chatbot


# corpus
data = {
    1:{'driving under the influence of Alcohol':'Vehicle confiscation period : 60 Days ; Fine : To be decided by court ; Black Points : 23',
       'driving under the influence of drugs or brain affecting substances or any other similar items':'Vehicle confiscation period : 60 Days ; Fine : To be decided by court ; Black Points : 23',
       'driving a vehicle without plates':'Vehicle confiscation period : 90 Days ; Fine : 3000 AED ; Black Points : 23',
       'driving the vehicle against the traffic direction':'Vehicle confiscation period : 7 Days ; Fine : 1000 AED ; Black Points : 8',
       'entering the vehicle into a prohibited area':'Vehicle confiscation period : 7 Days ; Fine : 1000 AED ; Black Points : 8',
       'exceeding the maximum speed limit by more than 80 km/hour':'Vehicle confiscation period : 60 Days ; Fine : 3000 AED ; Black Points : 23',
       'exceeding the maximum speed limit by more than 60 km/hour':'Vehicle confiscation period : 30 Days ; Fine : 2000 AED ; Black Points : 12',
       'what is the fine for over speeding':'The over speeding fine depends on how severely you have exceeded your speed limit',
       'what is the fine for drunk driving': 'Vehicle confiscation period : 60 Days ; Fine : To be decided by court ; Black Points : 23',
       'what is the fine for not carrying the driving license':'The is no specific fine associated with it.',
       'fine for driving with expired tyres':'Vehicle confiscation period : 7 Days ; Fine : 500 AED; Black Points : 4',
       'what is the fine for jumping a red light':'Vehicle confiscation period : 15 Days ; Fine : 800 AED; Black Points : 8',
       'what do you do when someone gets killed by accident':'Vehicle confiscation period : 30 Days ; Fine : To be decided by court ; Black Points : 12',
       'Not stopping after causing an accident that resulted in injuries':'Vehicle confiscation period : 60 Days ; Fine : To be decided by court ; Black Points : 24',
       'Driving a vehicle without number plates':'Vehicle confiscation period : 60 Days ; Fine : 1000 AED; Black Points : 24',
       'Running away from a traffic policeman':'Vehicle confiscation period : 30 Days ; Fine : 800 AED ; Black Points : 12',
       'Causing moderate injury':'Fine : To be decided by court ; Black Points : 6',
       'Driving a noisy vehicle':'Vehicle confiscation period : 30 Days ; Fine : 800 AED; Black Points : 12',
       'Driving a vehicle that causes pollution':'Fine : 500 AED',
       'failure to stop after causing an accident':'Fine 500 AED',
       'Throwing waste from vehicles onto roads':'Fine : 500 AED ; Black points : 4'
}
}



def model(train_dataset,new_data):
    new = [new_data]
    ques_list = list(train_dataset.keys())
    vectorizer, trainVectorizerArray = train_func(ques_list)
    new_test = vectorizer.transform(new).toarray()  # creating a token for the new input data

    cx = lambda a, b: round(numpy.inner(a, b) / (LA.norm(a) * LA.norm(b)), 3)

    for testV in new_test:  # selecting the new token that was created for the input question
        cos = 0.0
        ans = ''
        for n, vector in enumerate(trainVectorizerArray):  # selecting the first token
            cosine = cx(vector, testV)  # finding the cosine similarity between the selected token and the new token
            if cosine > cos:
                cos = cosine
                # print(type(train_dataset))
                a = ques_list[n]
                ans = train_dataset[a]
        if cos<0.3:
            return "I dont know"
        else:
            return ans


def train_func(train):
    # stopWords = stopwords.words('english')
    stopWords = ['the', 'is', 'are', 'were', 'a', 'an', 'was', 'has', 'had', 'have','to','do','of','on','my','any','be','by'] #the words that should be ignored by countvectoriser
    vectorizer = CountVectorizer(stop_words=stopWords)  # adding the words list to countvectoriser
    # training data
    train_set = train # creating the training set
    trainVectorizerArray = vectorizer.fit_transform(train_set).toarray()  # creating tokens froms the trainng set, This is a 2D array
    # print(trainVectorizerArray)  # just to help us debug
    return vectorizer,trainVectorizerArray


def main_bot(question_id, user_query):
    question_dict = data[question_id]
    answer = model(question_dict, user_query)
    return (answer)
