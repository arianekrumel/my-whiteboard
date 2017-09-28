from __future__ import division
from IPython.core.display import *
import math
import random
import copy
import collections
import heapq
import numpy as np

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
            tokenized_line = line.strip().split(',')
            for i in range(len(self.raw_from_attr_file)):
                thisValue = tokenized_line[i]
                lineAttr = self.raw_from_attr_file[i]
                tokenized_lineAttr = lineAttr.strip().split(',')
                
                if lineAttr != "Exclude": 
                    if tokenized_lineAttr[1] == "buckets":
                        min = float(tokenized_lineAttr[2])
                        max = float(tokenized_lineAttr[3])
                        step = float(tokenized_lineAttr[4])
                        chosenValue = str(min)

                        for j in range( 1 + int(math.floor((max-min)/ step))):
                            value = str(min + step*i)
                            if thisValue > value:
                                break
                            else:
                                chosenValue = str(value)
                        alteredLine.append(float(chosenValue))
                    else:
                        if tokenized_line[i] == "Iris-setosa":
                            chosenValue = 0
                        elif tokenized_line[i] == "Iris-versicolor":
                            chosenValue = 1
                        elif tokenized_line[i] == "Iris-virginica":
                            chosenValue = 2
                        else:
                            chosenValue = float(tokenized_line[i])
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
                step = float(tokenized_line[4])
                for i in range( 1+ int(math.floor((max-min)/ step))):
                    value = str(min + step*i)
                    values.append(value)
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
            sum += float(self.data[dataIndex][attrIndex])
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
        sum = 0.0
        for i in range(len(self.attr_order)):
            if self.attr_order[i] == "Exclude":
                pass
            elif self.attr_order[i] == "Redacted":
                pass
            else:
                point1Value = float(point1[i])
                point2Value = float(point2[i])
                diff = point1Value - point2Value
                absDiff = abs(diff)
                squaredDiff = absDiff * absDiff
                sum += squaredDiff
        return sum
    
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


dataSets = ["glass", "iris", "spambase"]

for dataSet in dataSets:
    data_ingest_object = DataIngest("Data/" + dataSet)
    data_ingest_object.raw_from_data_file = data_ingest_object.read_data(".data")
    data_ingest_object.raw_from_attr_file = data_ingest_object.read_data(".attributes")
    data_ingest_object.parse_attributes()
    data_ingest_object.parse_data()
    
    kmc = KMeansClustering(3, data_ingest_object.data, data_ingest_object.attr_order)
    print "**********************************************************"
    print "KMeans Clustering Results for static k = 3 on 1000 samples\n"
    for label in kmc.labels:
        print "Centroid", label, "contains", len(kmc.labels[label]), "elements\n"

    print "Centroids: ", kmc.centroids

    hac = HaClustering(3, data_ingest_object.data, data_ingest_object.attr_order)
    print "**********************************************************"
    print "Hierarchal Agglomerative Clustering Results for static k = 3 on 1000 samples\n"

    print len(hac.clusters), "Dendrogram Cluster Vertices"
    for cluster in hac.clusters:
        print hac.clusters[cluster], "\n"

    gaKm = GasFeatureSelection(data_ingest_object.data, data_ingest_object.attr_order, "km")
    print "**********************************************************"
    print "Genetic Algorithm Results over K-Means Clustering\n"

    print "Best Individual", ga.best_individual, "\n"

    print "Selected Features"
    for i in range(len(ga.best_individual)):
        bit = ga.best_individual[i]
        if bit == 1:
            print data_ingest_object.attr_order[i]

    print "\nRemoved Features"
    for i in range(len(ga.best_individual)):
        bit = ga.best_individual[i]
        if bit == 0:
            print data_ingest_object.attr_order[i]



