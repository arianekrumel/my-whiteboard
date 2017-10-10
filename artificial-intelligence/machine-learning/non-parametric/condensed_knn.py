from __future__ import division
from IPython.core.display import *
import math
import random
import copy
import collections
import heapq
import numpy as np
import xlrd
import csv
import matplotlib.pyplot as plt


class DataIngest():
    """
    Initialization function for class.
    """    
    def __init__(self, filename):
        self.filename = filename
        self.raw_from_data_file = []
        self.raw_from_attr_file = []
        self.data = []
        self.test_data = []
        self.training_data = []
        self.attributes = {}
        self.labels = []
        self.attr_order = []
        self.token = ','

    """
    This function reads from a specified file and returns raw data.
    
    @returns
    """
    def read_data(self, postfix):
        raw_from_data_file = []
        with open( self.filename + postfix, 'r') as f:
            file_data = [x for x in f.readlines()]
        f.closed
        for line in file_data:
            line = line.strip()
            raw_from_data_file.append(line)
        return raw_from_data_file

    """
    This function reads from source data file and attributes source file
    """
    def get_data(self):
        self.raw_from_data_file = self.read_data(".data")
        self.raw_from_attr_file = self.read_data(".attributes")
        self.parse_attributes()
        self.parse_data()
        self.split_data()
    
    def parse_data(self):
        for line in self.raw_from_data_file:
            alteredLine = []
            tokenized_line = line.strip().split(self.token)
            for i in range(len(self.raw_from_attr_file)):
                thisValue = tokenized_line[i]
                lineAttr = self.raw_from_attr_file[i]
                tokenized_lineAttr = lineAttr.strip().split(',')
                
                if lineAttr != "Exclude": 
                    if tokenized_lineAttr[1] == "buckets":
                        min = float(tokenized_lineAttr[2])
                        max = float(tokenized_lineAttr[3])
                        step = tokenized_lineAttr[4]
                        chosenValue = str(min)
                        j = 0
                        value = min
                        while value < max:
                            value = str(min + float(step)*i)
                            if thisValue > value:
                                break
                            else:
                                chosenValue = str(value)
                            j += 1
                        alteredLine.append(float(chosenValue))
                    else:
                        chosenValue = tokenized_line[i]
                        alteredLine.append(chosenValue)
            self.data.append(alteredLine)
    
    """
    This function sets up the attributes for data structure.
    """              
    def parse_attributes(self):
        for line in self.raw_from_attr_file:
            tokenized_line = line.strip().split(',')
            values = []
            
            if tokenized_line[1] == "buckets":
                min = float(tokenized_line[2])
                max = float(tokenized_line[3])
                step = tokenized_line[4]
                i = 0
                value = min
                while value < max:
                    value = min + float(step)*i
                    values.append(str(value))
                    i += 1
            else:
                for i in range(len(tokenized_line) - 1):
                    value = tokenized_line[i+1]
                    values.append(value)
            
            attribute = tokenized_line[0]
            if(attribute == "Exclude"):
                pass
            elif(attribute == "label"):
                self.labels = values
            else:
                self.attributes[attribute] = values
                
            self.attr_order.append(attribute)
            
    
    """
    This function randomizes the data and splits result into two (2) sets.
    """    
    def split_data(self):
        randomized_data = copy.deepcopy(self.data)      
        training_percentage = len(self.data) * 2 / 3
        for d in randomized_data:
            if(len(self.training_data) < training_percentage):
                self.training_data.append(d)
            else:
                self.test_data.append(d)


"""
This class contains the functionality for K-Nearest Neighbor algorithm
"""
class KNN():
    
    """
    Initialization function for class.
    """    
    def __init__(self, k, test_data, training_data, attr_order, type):
        self.test_data = test_data
        self.training_data = training_data
        self.attr_order = attr_order
        self.k = k
        self.attributesToSkip = ["label", "Exclude"]
        self.predicted_classes = {}
        self.actual_classes = {}
        self.errors = 0
        self.type = type
    
    """
    This function calculates the distance between two data points, point1 and point2.
    
    @param point1 (Array) This is data point for comparison
    @param point2 (Array) This is data point for comparison
    
    @returns (double) Distance between two given points
    """
    def getDistance(self, point1, point2):
        distance = 0.0
        for attrIndex in range(len(self.attr_order)):
            attribute = self.attr_order[attrIndex]
            if(attribute not in self.attributesToSkip):
                isNumeric1 = isinstance(point1[attrIndex], int) or isinstance(point1[attrIndex], float)
                isNumeric2 = isinstance(point2[attrIndex], int) or isinstance(point2[attrIndex], float)
                if isNumeric1 and isNumeric2:
                    diff = point1[attrIndex] - point2[attrIndex]
                else:
                    diff = self.categoricalDifference(point1[attrIndex], point2[attrIndex])
                distance += math.pow(diff, 2)
        distance = math.sqrt(distance)
        return distance
    
    def categoricalDifference(self, category1, category2):
        if category1 == category2:
            return 0
        else:
            return 50

    """
    This function returns the k first values from the distances list.
    
    @param distances (List) Tuples of data points and their distances
    @returns (Dictionary) K nearest neighbors
    """ 
    def getNearest(self, distances):
        dataset = self.training_data
        nearestK = {}
        for i in range(self.k):
            (distance, example) = distances[i]
            nearestK[example] = dataset[example]
        return nearestK
    
    """
    This function takes a number of nearest neighbors and returns an average for regression.
    
    @param nearest (Dictionary) K nearest neighbors
    """
    def regression(self, nearest):
        labelIndex = self.attr_order.index("label")
        mySum = 0.0
        for neighbor in nearest:
            mySum += float(nearest[neighbor][labelIndex])
        return mySum/self.k
    
    """
    This function takes a number of nearest neighbors and return majority class label.
    
    @param nearest (Dictionary) K nearest neighbors
    @returns (String) Predicted class
    """
    def classify(self, nearest):
        labelIndex = self.attr_order.index("label")
        labelsOfNearest = {}
        for neighbor in nearest:
            label = nearest[neighbor][labelIndex]
            if label in labelsOfNearest:
                numOfInstances = labelsOfNearest[label]
                numOfInstances += 1
                labelsOfNearest[label] = numOfInstances
            else: 
                labelsOfNearest[label] = 1
        label = max(labelsOfNearest, key=lambda k: labelsOfNearest[k])
        return label

    """
    This function takes a particular data query, k and list instances and returns a prediction.
    It calculates all distances from a particular query to all data points.
    Returns the majority vote classification of k neighbors.
    
    @param query (List) Data instance for classification
    @returns (String) Predicted class
    """
    def knn(self, query):
        distances = []
        for dataIndex in range(len(self.training_data)):
            distance = self.getDistance(self.training_data[dataIndex], query)
            distances.append((distance, dataIndex))
        distances.sort(key=lambda tup: tup[0])
        nearest = self.getNearest(distances)
        if self.type == "classification":
            return self.classify(nearest)
        elif self.type == "regression":
            return self.regression(nearest)
        
    """
    This function evaluates classification accuracy.
    
    @returns (Double) Percentage of error
    """
    def evaluate(self):
        labelIndex = self.attr_order.index("label")
        
        for dataIndex in range(len(self.test_data)):
            self.predicted_classes[dataIndex] = self.knn(self.test_data[dataIndex])
            self.actual_classes[dataIndex] = self.test_data[dataIndex][labelIndex]
            if self.predicted_classes[dataIndex] != self.actual_classes[dataIndex]:
                if self.type == "classification":
                    self.errors += 1
                elif self.type == "regression":
                    diff = float(self.predicted_classes[dataIndex]) - float(self.actual_classes[dataIndex])
                    distance = math.pow(diff, 2)
                    distance = math.sqrt(distance)
                    self.errors += distance
        return self.errors/len(self.test_data)

class CrossValidation():
    
    """
    Initialization function for class.
    """    
    def __init__(self, k, data):
        self.k = k
        self.data = data
        self.test_subsets = {}
        self.training_subsets = {}
        
        random.shuffle(self.data)
        numData = len(self.data)
        numInSubset = math.floor(len(self.data)/self.k)
        for i in range(self.k):
            startIndex = int(i*numInSubset)
            endIndex = int((i+1)*numInSubset)
            test_subset = self.data[startIndex:endIndex]
            self.test_subsets[i] = test_subset
            training_subset = self.data[0:startIndex] + self.data[endIndex:numData]
            self.training_subsets[i] = training_subset

print "****K NEAREST NEIGHBOR OUTPUTS****"

dataSets = [
    ("ecoli", "classification", 6), 
    ("segmentation", "classification", 2), 
    ("machine", "regression", 2), 
    ("forestfires", "regression", 3)
]

foldNum = 5
for dataSet in dataSets:
    (name, thisType, kNeighbors) = dataSet
    
    data_ingest_object = DataIngest("Data/" + name)
    data_ingest_object.raw_from_data_file = data_ingest_object.read_data(".data")
    data_ingest_object.raw_from_attr_file = data_ingest_object.read_data(".attributes")
    data_ingest_object.parse_attributes()
    data_ingest_object.parse_data()
    print "***Data Set:", name, "***"
    print "\t Tuned K Parameter:", kNeighbors
    print "\t Problem type:", thisType
    
    cvo = CrossValidation(foldNum, data_ingest_object.data)
    sumErrors = 0
    for validationFold in range(foldNum):
        knn_object = KNN(
            kNeighbors, 
            cvo.test_subsets[validationFold], 
            cvo.training_subsets[validationFold], 
            data_ingest_object.attr_order, 
            thisType)
        foldScore = knn_object.evaluate()
        sumErrors += foldScore
    if thisType == "classification":
        print "\t Averaged classification error rate:", sumErrors/foldNum
    elif thisType == "regression":
        print "\t Averaged evaluation score:", sumErrors/foldNum


class KNNCondensed():
    """
    Initialization function for class.
    """    
    def __init__(self, k, test_data, training_data, attr_order):
        self.grabbag = []
        self.store = []
        self.test_data = test_data
        self.training_data = training_data
        self.attr_order = attr_order
        self.k = k
        self.knn_object = None
    
    """
    This function runs the condensed KNN method. It first adds the minimum number of samples (k).
    Then it loops over the training data and grab bag until convergence.
    If classification is correct, sample added to grab bag and if not correct add to store.
    """
    def run(self):
        labelIndex = self.attr_order.index("label")
        for i in range(self.k):
            self.store.append(self.training_data.pop())
        self.knn_object = KNN(self.k, self.test_data, self.store, self.attr_order, "classification")
        
        for dataIndex in range(len(self.training_data)):
            query = self.training_data.pop()
            predicted_class = self.knn_object.knn(query)
            actual_class = query[labelIndex]
            if predicted_class == actual_class:
                self.grabbag.append(query)
            else:
                self.store.append(query)
            self.knn_object = KNN(self.k, self.test_data, self.store, self.attr_order, "classification")
            
        while len(self.grabbag) != 0:
            query = self.grabbag.pop()
            predicted_class = self.knn_object.knn(query)
            actual_class = query[labelIndex]
            if predicted_class == actual_class:
                self.grabbag.append(query)
                break
            else:
                self.store.append(query)
            self.knn_object = KNN(self.k, self.test_data, self.store, self.attr_order, "classification")
        
    def evaluate(self):
        self.knn_object = KNN(self.k, self.test_data, self.store, self.attr_order, "classification")
        return self.knn_object.evaluate()

print "****CONDENSED K NEAREST NEIGHBOR OUTPUTS****"

dataSets = [
    ("ecoli", 5), 
    ("segmentation", 3), 
]

foldNum = 5
for dataSet in dataSets:
    (name, kNeighbors) = dataSet
    
    data_ingest_object = DataIngest("Data/" + name)
    data_ingest_object.raw_from_data_file = data_ingest_object.read_data(".data")
    data_ingest_object.raw_from_attr_file = data_ingest_object.read_data(".attributes")
    data_ingest_object.parse_attributes()
    data_ingest_object.parse_data()
    print "***Data Set:", name, "***"
    
    cvo = CrossValidation(foldNum, data_ingest_object.data)
    sumErrors = 0
    for validationFold in range(foldNum):
        knn_object = KNNCondensed(
            kNeighbors, 
            cvo.test_subsets[validationFold], 
            cvo.training_subsets[validationFold], 
            data_ingest_object.attr_order)
        knn_object.run()
        foldScore = knn_object.evaluate()
        sumErrors += foldScore
        
    print "\t Tuned K Parameter:", kNeighbors
    print "\t Number of reduced samples in model:", len(knn_object.store)
    print "\t Averaged classification error:", sumErrors/foldNum


class KMeansClustering():
    """
    Initialization function for class.
    """    
    def __init__(self, k, data, attr_order):
        self.data = data
        self.attr_order = attr_order
        self.k = k
        self.centroids_archive = {}
        self.centroids = {}
        self.labels = {}
        
        self.initCentroids()
        self.run()

    """
    This function starts the process for this algorithm. It loops through the data 
    and attribute value in order to color to closest label. Then the centroid for 
    the category is moved to the center of its labeled points
    """
    def run(self):
        while not self.convergence():
            for centroidIndex in self.centroids:
                self.labels[centroidIndex] = []
            self.centroids_archive = self.centroids
            for dataIndex in range(len(self.data)):
                centroidIndex = self.color(dataIndex)
                self.labels[centroidIndex].append(dataIndex)
            self.moveCentroids()
    
    """
    This function moves the k centroids to the center of the labeled points
    """
    def moveCentroids(self):
        for centroidIndex in self.centroids:
            centroid_shifted = []
            for attrIndex in range(len(self.attr_order)):
                if self.attr_order[attrIndex] == "Exclude":
                    pass
                elif self.attr_order[attrIndex] == "Redacted":
                    averageValue = 0.0
                    centroid_shifted.append(averageValue)
                else:
                    averageValue = self.getAverageValue(attrIndex, centroidIndex)
                    centroid_shifted.append(averageValue)
            self.centroids[centroidIndex] = centroid_shifted
    
    """
    This function retrieves the average values for the points with a given label
    
    @param attrIndex (Int) The index of the attribute to examine
    @param centroidIndex (Int) The index of the centroid to examine
    
    @return Floating point number of average value
    """
    def getAverageValue(self, attrIndex, centroidIndex):
        sum = 0.0
        for dataIndex in self.labels[centroidIndex]:
            isNumeric = isinstance(self.data[dataIndex][attrIndex], int) or isinstance(self.data[dataIndex][attrIndex], float)
            if isNumeric:
                sum += float(self.data[dataIndex][attrIndex])
            else:
                sum += 1.0
        denom = len(self.labels[centroidIndex])
        if denom == 0:
            return 0
        else:
            return sum / denom

    """
    This function compares every data point to the centroids and colors to closest
    
    @param (Int) The index of the data element to examine
    
    @return (Array) Values for closest centroid
    """
    def color(self, dataIndex):
        point = self.data[dataIndex]
        bestDistance = 10000000
        bestCentroid = 0
        for centroid in self.centroids:
            distance = self.getDistance(self.centroids[centroid], point)
            if distance < bestDistance:
                bestDistance = distance
                bestCentroid = centroid
        return bestCentroid
            
    """
    This function retrieve the distance between two points
    
    @param point1 (Array) The values for data element
    @param point2 (Array) The values for data element
    
    @return The mean squared distance between two points
    """  
    def getDistance(self, point1, point2):
        distance = 0.0
        for attrIndex in range(len(self.attr_order)):
            attribute = self.attr_order[attrIndex]
            if self.attr_order[attrIndex] == "Exclude":
                pass
            elif self.attr_order[attrIndex] == "Redacted":
                pass
            else:
                isNumeric1 = isinstance(point1[attrIndex], int) or isinstance(point1[attrIndex], float)
                isNumeric2 = isinstance(point2[attrIndex], int) or isinstance(point2[attrIndex], float)
                if isNumeric1 and isNumeric2:
                    diff = point1[attrIndex] - point2[attrIndex]
                else:
                    diff = self.categoricalDifference(point1[attrIndex], point2[attrIndex])
                distance += math.pow(diff, 2)
        distance = math.sqrt(distance)
        return distance
    
    def categoricalDifference(self, category1, category2):
        if category1 == category2:
            return 0
        else:
            return 50
    
    """
    This function initializes the first values for k centroids
    """
    def initCentroids(self):
        for i in range(self.k):
            random_index = random.randint(0,len(self.data))
            self.centroids[i] = self.data[i]
            self.labels[i] = []
    
    """
    This function retrieves the boolean value for convergence if no change to centroids
    
    @return (Boolean) True if no change in centroids, False otherwise
    """
    def convergence(self):
        converged = self.centroids == self.centroids_archive
        return converged

dataSets = [
    ("ecoli", "classification", 3), 
    ("segmentation", "classification", 2), 
    ("machine", "regression", 2), 
    ("forestfires", "regression", 6)
]
print "****K-MEANS CLUSTERING OUTPUTS****"

for dataSet in dataSets:
    (dataSet, thisType, k) = dataSet
    data_ingest_object = DataIngest("Data/" + dataSet)
    data_ingest_object.raw_from_data_file = data_ingest_object.read_data(".data")
    data_ingest_object.raw_from_attr_file = data_ingest_object.read_data(".attributes")
    data_ingest_object.parse_attributes()
    data_ingest_object.parse_data()
    print "***Data Set:", dataSet, "***"
    
    kmc = KMeansClustering(k, data_ingest_object.data, data_ingest_object.attr_order)
    print "\tKMeans Clustering Results for static k =", k
    for label in kmc.labels:
        print "\tCentroid", label, "contains", len(kmc.labels[label]), "elements"

    print "\tCentroids: ", kmc.centroids, "\n"


# In[ ]:



