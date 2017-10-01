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

class HaClustering():
    
    """
    Initialization function for class.
    """    
    def __init__(self, k, data, attr_order):
        self.data = data
        self.attr_order = attr_order
        self.k = k
        self.clusters = {}
        self.distanceMatrix = []
        self.mergedIndices = []
        self.labels = {}
        
        self.run()
       
    """
    This function processes the algorithm. It iterates to find pairs in a set of clusters,
    merges them into a new cluster and repeat until desired
    """
    def run(self):
        self.clusters = self.initClusters()
        self.createDistanceMatrix()
        
        newClusterIndex = len(self.data) + 1
        while not self.convergence():
            (cluster1, cluster2) = self.getClosestPair()
            if cluster1 == False and cluster2 == False:
                break
            if newClusterIndex in self.labels.keys():
                self.labels[newClusterIndex].append(cluster1)
                self.labels[newClusterIndex].append(cluster2)
            else:
                self.labels[newClusterIndex] = []
                self.labels[newClusterIndex].append(cluster1)
                self.labels[newClusterIndex].append(cluster2)
            cluster_new = self.merge(cluster1, cluster2)
            self.clusters[newClusterIndex] = cluster_new
            self.updateDistanceMatrix(newClusterIndex)
            newClusterIndex += 1
    
    """
    This function retrives a pair of clusters with the smallest distance
    
    @return (Tuple) A key and two data values for clusters
    """
    def getClosestPair(self):
        (distance, pair) = (heapq.heappop(self.distanceMatrix))
        while pair[0] in self.mergedIndices or pair[1] in self.mergedIndices:
            if len(self.distanceMatrix) == 0:
                return (False, False)
            (distance, pair) = (heapq.heappop(self.distanceMatrix))
            
        cluster1Index = pair[0]
        cluster2Index = pair[1]
        
        cluster1 = self.clusters[cluster1Index]
        cluster2 = self.clusters[cluster2Index]
        
        del self.clusters[cluster1Index]
        del self.clusters[cluster2Index]
        
        self.mergedIndices.append(cluster1Index)
        self.mergedIndices.append(cluster2Index)

        return (cluster1, cluster2)
    
    """
    This function merges two clusters by taking an average
    
    @param cluster1 (Array) Set of values for a cluster
    @param cluster2 (Array) Set of values for a cluster
    
    @return (Array) A set of values averaged from input
    """
    def merge(self, cluster1, cluster2):
        cluster_shifted = []
        
        for elementIndex in range(len(cluster1)):
            element = float(cluster1[elementIndex]) + float(cluster2[elementIndex]) / 2.0
            cluster_shifted.append(element)
        return cluster_shifted
    
    """
    This function returns state of converage
    
    @return (Boolean) True if k clusters are found, False otherwise
    """
    def convergence(self):
        return len(self.clusters) == self.k
    
    """
    This function creates a singleton cluster per data point
    
    @return (Dictionary) Set of clusters
    """
    def initClusters(self):
        firstClusters = {}
        for dataIndex in range(len(self.data)):
            clusterIndex = dataIndex
            firstClusters[clusterIndex] = self.data[dataIndex]
        return firstClusters
    
    """
    This function updates the distance matrix for all clusters
    """
    def createDistanceMatrix(self):
        for clusterIndex in self.clusters:
            for clusterOtherIndex in self.clusters:
                if clusterIndex != clusterOtherIndex:
                    distance = self.getDistance(self.clusters[clusterIndex], self.clusters[clusterOtherIndex])
                    element = (distance, [clusterIndex, clusterOtherIndex])
                    self.distanceMatrix.append(element)
        heapq.heapify(self.distanceMatrix)
        
    def updateDistanceMatrix(self, newClusterIndex):
        for clusterOtherIndex in self.clusters:
            if clusterOtherIndex != newClusterIndex:
                distance = self.getDistance(self.clusters[newClusterIndex], self.clusters[clusterOtherIndex])
                element = (distance, [newClusterIndex, clusterOtherIndex])
                heapq.heappush(self.distanceMatrix,element)
    """
    This function calculates the distance between two points
    
    @param point1 (Array) This is a set of values for a data element
    @param point2 (Array) This is a set of values for a data element
    
    @return (Array) Set of distance values calculated from inputs
    """
    def getDistance(self, point1, point2):
        array1 = np.array(point1)
        array2 = np.array(point2)
        difference = np.subtract(array1, array2)
        return sum(np.square(difference)) / len(difference)
        

dataSets = ["glass", "iris"]

for dataSet in dataSets:
    data_ingest_object = DataIngest("Data/" + dataSet)
    data_ingest_object.raw_from_data_file = data_ingest_object.read_data(".data")
    data_ingest_object.raw_from_attr_file = data_ingest_object.read_data(".attributes")
    data_ingest_object.parse_attributes()
    data_ingest_object.parse_data()

    hac = HaClustering(3, data_ingest_object.data, data_ingest_object.attr_order)
    print "**********************************************************"
    print "Hierarchal Agglomerative Clustering Results for static k = 3 on 1000 samples\n"

    print len(hac.clusters), "Dendrogram Cluster Vertices"
    for cluster in hac.clusters:
        print hac.clusters[cluster], "\n"