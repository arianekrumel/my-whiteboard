
# coding: utf-8

# # k Nearest Neighbors and Model Evaluation

# In[1]:

import xlrd
import csv
import math
import matplotlib.pyplot as plt
import random
import copy
import numpy as np



# ***csv_from_excel***
# 
# This function take a filename of an existing xls file and desired csv filename. It converts the data from the xls format to the csv format. Use the data in concrete_compressive_strength.csv for this assignment obtainable at [UCI ML Repository - Concrete Compressive Strength](https://archive.ics.uci.edu/ml/datasets/Concrete+Compressive+Strength).
# 

# In[2]:

def csv_from_excel(xls_name, csv_name):
    wb = xlrd.open_workbook(xls_name)
    sh = wb.sheet_by_name('Sheet1')
    csv_file = open(csv_name, 'wb')
    wr = csv.writer(csv_file, quoting=csv.QUOTE_ALL)

    for rownum in xrange(sh.nrows):
        wr.writerow(sh.row_values(rownum))

    csv_file.close()

csv_from_excel('Concrete_Data.xls', 'Concrete_Data.csv')

print 'Concrete_Data.csv created from Concrete_Data.xls'


# ***get_data_and_attributes***
# 
# This function takes a csv file and returns dataset and attributes

# In[3]:

def get_data_and_attributes(csv_file):
    dataset = {}

    with open(csv_file, 'rb') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',')
        i = 0
        for row in spamreader:
            if i == 0:
                attributes = row
            else:
                dataset[i-1] = {}
                j = 0
                for attribute in attributes:
                    dataset[i-1][attribute] = float(row[j])
                    j += 1
            i += 1
    return (attributes, dataset)

(attributes, dataset) = get_data_and_attributes('Concrete_Data.csv')

print len(attributes), "attributes created"
print len(dataset), "data points created"
outputVariable = attributes[8]
print "Output variable attribute is:", outputVariable


# ***getDistance***
# 
# This function calculates the euclidean distance between two data points, example and query.

# In[4]:

def getDistance(example, query):
    distance = 0
    for attribute in attributes:
        if(attribute != outputVariable):
            x_i = example[attribute]
            y_i = query[attribute]
            difference = (x_i-y_i)
            distance += math.pow(difference, 2)
    
    distance = math.sqrt(distance)
    return distance


# ***getNearest***
# 
# This function returns the k first values from the distances list.

# In[5]:

def getNearest(distances, k, dataset):
    nearestK = {}
    for i in range(k):
        (distance, example) = distances[i]
        nearestK[example] = dataset[example]
    return nearestK


# ***processing***
# 
# This function takes a number of nearest neighbors and returns an average for regression.

# In[6]:

def processing(nearest):
    mySum = 0
    k = len(nearest)
    for n in nearest:
        mySum += nearest[n][outputVariable]
    return mySum/k


# ***knn***
# 
# This function takes a particular data query, k and list instances and returns a prediction

# In[7]:

def knn(k, dataset, query):
    distances = []
    for example in dataset:
        distance = getDistance(dataset[example], query)
        distances.append((distance, example))
    
    distances.sort(key=lambda tup: tup[0])

    nearest = getNearest(distances, k, dataset)
    
    return processing(nearest)

k = 1
query = dataset[100]
print "An example execution of KNN results in predicted value of:", knn(k, dataset, query)


# # 2. Use validation curves as described in Module 9 to determine the best value of k trying values of 1 to 10. 
# 
# (You don't need to use odd values for regression). For this you can simply split the data randomly into a training and a test set with a 67/33 split.

# ***prep_data***
# 
# This function randomizes the data set and splits into training and test at a selected percent.

# In[8]:

def prep_data(data, percentOfTraining):
    splitIndex = (int) (len(data) * percentOfTraining)
    trainingSet = {};
    testSet = {};
    
    keys=data.keys()
    random.shuffle(keys)
    for d in keys:
        if d < splitIndex:
            trainingSet[d] = data[d];
        else:
            testSet[d] = data[d];
    return (trainingSet, testSet);

(trainingSet, testSet) = prep_data(dataset, .67);
print "Number in training data set:", len(trainingSet);
print "Number in test data set:", len(testSet);


# ***getPredictions***
# 
# This function creates a prediction list for a given training set using KNN with a test set

# In[9]:

def getPredictions(trainingSet, testSet, k):
    predictions = {}
    for t in testSet:
        query = testSet[t]
        prediction = knn(k, trainingSet, query)
        predictions[t] = prediction
    return predictions

predictions = getPredictions(trainingSet, testSet, 1);


# ***evaluate***
# 
# This function evaluates the error between the prediction and actual value using Manhattan distance.

# In[10]:

def evaluate(data, predictions):
    error = 0
    for i in predictions:
        label = data[i][outputVariable]
        predictedLabel = predictions[i]
        error += abs(label - predictedLabel)
    return error/len(data)


# ***generate_validation_curves***
# 
# Additionally, because you can't be *wrong* with the k = 1 in the training data, your curves will look a little funky initially.

# In[11]:

validation_curve = []
validation_curve_compare = []
for n in [1,2,3,4,5,6,7,8,9,10]:
    predictions = getPredictions(trainingSet, testSet, n);
    error = evaluate(testSet, predictions)
    validation_curve.append(error)
    
    predictions = getPredictions(trainingSet, trainingSet, n);
    error = evaluate(trainingSet, predictions)
    validation_curve_compare.append(error)


# In[12]:

def generate_validation_curves(data, data2, xlabel, ylabel):
    plt.plot(data)
    plt.plot(data2)
    plt.ylabel(ylabel)
    plt.xlabel(xlabel)
    plt.axis([0, 9, 0, 12])
    plt.title('Validation Curves')
    plt.show()

generate_validation_curves(validation_curve, validation_curve_compare, 'K-value', 'Error rate');


# # 3. Use learning curves as described in Module 9 to determine if your model could use more data. 
# 
# For this you can simply split the data randomly into a training and a test set with a 67/33 split. Use the best k from part 2.

# ***prep_portion_of_data***
# 
# This function returns a random selection up to a given percentage of the training data.

# In[13]:

def prep_portion_of_data(data, percent):
    splitIndex = (int) (len(data) * percent)
    trainingSet = {};
    keys=data.keys()
    random.shuffle(keys)
    for d in keys:
        if d < splitIndex:
            trainingSet[d] = data[d];
    return trainingSet;

print "Number in training data set:", len(trainingSet);


# In[14]:

bestK = 5
learning_curve = []
learning_curve_compare = []

for n in [.05, .15, .25, .35, .45, .55, .65, .75, .85, .95]:
    portion_of_trainingSet = prep_portion_of_data(trainingSet, n);
    predictions = getPredictions(portion_of_trainingSet, testSet, bestK);
    error = evaluate(testSet, predictions)
    learning_curve.append(error)
    
    predictions = getPredictions(portion_of_trainingSet, portion_of_trainingSet, bestK);
    error = evaluate(portion_of_trainingSet, predictions)
    learning_curve_compare.append(error)
    
print learning_curve


# ***generate_learning_curves***
# 
# This function plots the learning curve.

# In[15]:

def generate_learning_curves(data, data2, xlabel, ylabel):
    plt.plot(data)
    plt.plot(data2)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.axis([0, 9, 0, 15])
    plt.title('Learning Curves')
    plt.show()

generate_learning_curves(learning_curve, learning_curve_compare, '', 'Error rate');


# # 4. Use 10-fold cross-validation to establish confidence bounds on your model's performance. 
# 
# Calculate the mean (average) MSE (which sounds funny, I know) and the standard deviation. 

# ***merge_dictionaries***
# 
# This function merges multiple dictionary into one. It is a helper function for cross validation.

# In[16]:

def merge_dictionaries(*dict_args):
    result = {}
    for d in dict_args:
        result.update(d)
    return result


# ***get_mse_and_dev***
# 
# This function return the mean squared error and standard deviation given a list of error values.

# In[17]:

def get_mse_and_dev(models):
    numOfModels = len(models)
    
    squaredErrors = 0 
    for model in range(numOfModels):
        thisErrors = models[model]
        squaredErrors += math.pow(error, 2)
        
    meanOfSquaredErrors = squaredErrors / numOfModels
    return (meanOfSquaredErrors, math.sqrt(meanOfSquaredErrors))


# ***crossvalidation***
# 
# This function performs the cross validation for a given number of folds.

# In[18]:

def crossvalidation(data, numFolds):
    dataFolds = {}
    numInFold = math.ceil(len(data) / numFolds)
    
    keys = data.keys()
    random.shuffle(keys)
    foldIndex = 0
    dataFolds[foldIndex] = {}
    for d in keys:
        dataFolds[foldIndex][d] = data[d]
        if(len(dataFolds[foldIndex]) == numInFold) and len(dataFolds) != numFolds:
            foldIndex += 1
            dataFolds[foldIndex] = {}
    
    foldModels = {}
    for i in range(numFolds):
        testSet = dataFolds[i%10]
        trainingSet = merge_dictionaries(dataFolds[(i+1)%10], dataFolds[(i+2)%10], dataFolds[(i+3)%10], dataFolds[(i+4)%10], dataFolds[(i+5)%10], dataFolds[(i+6)%10], dataFolds[(i+7)%10], dataFolds[(i+8)%10], dataFolds[(i+9)%10])
        predictions = getPredictions(trainingSet, testSet, bestK);
        foldModels[i] = evaluate(testSet, predictions) 
        
    return get_mse_and_dev(foldModels)


# In[19]:

(mse, std_dev) = crossvalidation(dataset, 10)

print "Mean square error:", mse
print "Standard deviation:", std_dev

# In[ ]:



