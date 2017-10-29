from __future__ import division
#from IPython.core.display import *
import math
import random
import copy
import collections

dataSets = ["breast-cancer-wisconsin", "glass", "iris","soybean-small", "house-votes-84"]

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
        
        self.get_data()

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
                        alteredLine.append(str(float(chosenValue)))
                    else:
                        alteredLine.append(tokenized_line[i])
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
            
class NaiveBayesClassifier():
    
    """
    Initialization function for class. Adapted from Ariane Krumel (Summer 2017)
    """    
    def __init__(self, training_data, test_data, attributes, attr_order, labels):
        self.training_data = training_data
        self.test_data = test_data
        self.attributes = attributes
        self.attr_order = attr_order
        self.labels = labels
        self.likelihood = {}
        self.p_labels = {}
    
    """
    This function triggers the classification and evaluation functions.
    """
    def run(self):
        self.classifications = {}
        self.train()
        self.classify()
        self.evaluate()
        
    """
    This function creates a copy of a given data set with one-hot encoding.
    Each attribute value is transformed to a separate boolean.
    
    @param (Array) data Original data set
    
    @returns (Array) data Copy of original data set with one-hot encoding
    """
    def createHotCodedData(self, data):
        hotCodedData = []
        for instance in range(len(data)):
            d = data[instance]
            x_i = {}
            for j in range(len(d)):
                attribute = self.attr_order[j]
                x_i[attribute] = d[j]
            hotCodedData.append(x_i)
        return hotCodedData
        
    """
    This function the class label with best probability.
    
    @param results (List) Probabilities for class
    
    @return (String) Class name
    """
    def find_best(self, results):
        bestLabel = "no"
        bestValue = 0

        for result in results:
            if results[result] > bestValue:
                bestLabel = result
                bestValue = results[result]
        return bestLabel;
    
    """
    This function returns a probability for instance. 
    
    @param probs (Dictionary) Likelihood  for attributes
    @param instance (Array) Data instance
    
    @return (Tuple) Best class and results
    """
    def naive_bayes_classify(self, probs, instance):
        results = {}
        this_data = instance
        n = len(self.test_data);

        temp = {}
        denominator = 1
        for label in self.labels:
            temp[label] = self.p_labels[label]/n
            for attribute in self.attributes:
                temp[label] *= self.likelihood[label][attribute][this_data[attribute]]
            denominator += temp[label]
            results[label] = temp[label]/denominator

        best = self.find_best(results)
        return (best, results)

    """
    This function gets all necessary probabilties. 
    
    @return (List) Class and probability of accuracy.
    """
    def train(self):      
        data = self.createHotCodedData(self.training_data)        
        
        for label in self.labels:
            self.p_labels[label] = 1
            self.likelihood[label] = {}
            for attr in self.attributes:
                self.likelihood[label][attr] = {}
                for val in self.attributes[attr]:
                    self.likelihood[label][attr][val] = 1

        for d in data:
            self.p_labels[d["label"]] += 1
            for attr in self.attributes:
                self.likelihood[d["label"]][attr][d[attr]] += 1.0

        for label in self.labels:
            for attr in self.attributes:
                for val in self.attributes[attr]:
                    self.likelihood[label][attr][val] = round(self.likelihood[label][attr][val]/self.p_labels[label], 2)
    
    """
    This function performs classification function.
    """
    def classify(self):
        data = self.createHotCodedData(self.test_data) 
        for i in range(len(data)):
            self.classifications[i] = self.naive_bayes_classify(self.likelihood, data[i])
    
    """
    This function evaluates the classifications on the test data
    set compared to the actual labels.
    """
    def evaluate(self):
        hotCodedTestData = self.createHotCodedData(self.test_data)
        incorrect = 0
        for i in range(len(self.classifications)):
            instance = hotCodedTestData[i]
            h_x = self.classifications[i][0]
            y = hotCodedTestData[i]["label"]
            if h_x != y:
                incorrect += 1
        self.error_rate = round(float(incorrect) / float(len(hotCodedTestData)), 2)
        
for dataSet in dataSets:
    data_ingest_object = DataIngest("Data/" + dataSet)
    
    naive_bayes_object = NaiveBayesClassifier(
        data_ingest_object.training_data, 
        data_ingest_object.test_data, 
        data_ingest_object.attributes, 
        data_ingest_object.attr_order, 
        data_ingest_object.labels
    )    
        
    naive_bayes_object.run()
    
    print "\n------------------------------------------------------------"
    print "****NAIVE BAYES for", dataSet, "****"
    print "\n*Error rate*", naive_bayes_object.error_rate
    
    #"""
    print "\n*Likelihood table*"
    print "\tClass"
    for label in naive_bayes_object.labels:
        print "\t" + label,
    print "\nValue"
    for attr in naive_bayes_object.attributes:
        if attr != "label" and attr != "Exclude":
            values = naive_bayes_object.attributes[attr]
            for val in values:
                print val, "\t", 
                for label in naive_bayes_object.labels:
                    print naive_bayes_object.likelihood.get(label).get(attr).get(val), "\t", 
                print attr
    #"""
    print "\n*Classifications sample results*"

    for i in range(len(naive_bayes_object.test_data)):
        print "\tData instance:", naive_bayes_object.test_data[i]
        print "\t\t(Prediction:", naive_bayes_object.classifications[i][1], ")"
        if i == 2: break