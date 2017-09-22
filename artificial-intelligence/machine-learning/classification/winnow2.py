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

class Winnow2Classifier():
    
    """
    Initialization function for class.
    
    @param (Array) training_data Set of data split for training
    @param (Array) test_data Set of data split for test
    @param (Dictionary) attributes Attribute names with related value options
    @param (Array) attr_order List of all attribute name in data order
    @param (Array) labels List of classifications
    @param (Int) alpha Learning rate used to modify weight
    @param (Double) theta Threshold value to test classification
    """    
    def __init__(self, training_data, test_data, attributes, attr_order, labels):
        self.training_data = training_data
        self.test_data = test_data
        self.attr_order = attr_order
        self.attributes = attributes
        self.labels = labels
        self.labelsValue = {}
        self.alpha = 2
        self.theta = len(attributes) #0.5
        self.classifications = []
        self.classificationsMultiClass = {}
        self.error_rate = 0
                
        if(len(self.labels) > 2):
            for i in range(len(self.labels)):
                for j in range(len(self.labels)):
                    if(j == i):
                        self.labelsValue[self.labels[j]] = 0
                    else: 
                        self.labelsValue[self.labels[j]] = 1
                self.train()
                self.classifyMultiClass()
                self.evaluateMultiClass()
        else:
            for i in range(len(self.labels)):
                self.labelsValue[self.labels[i]] = i
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
    This function initializes a weight vector for each boolean feature.
    """
    def createWeights(self):
        weight_vector = {}
        defaultWeight = 1
        for attribute in self.attr_order:
            if attribute != "label" and attribute != "Exclude":
                for value in self.attributes[attribute]:
                    weight_vector[(attribute,value)] = defaultWeight
        return weight_vector
                    
    """
    This function retrieves the calculated sum of weights and 
    attributes for a data instance.
    
    @param (Array) instance A single data instance
    
    @returns (Int) Calculated sum
    """
    def getFx(self, instance):
        f_x = 0
        for attribute in self.attr_order:
            if attribute != "label" and attribute != "Exclude":
                for value in self.attributes[attribute]:
                    key = (attribute,value)
                    w_i = self.weight_vector.get(key)
                    x_i = 1 if (instance[attribute] == value) else 0
                    
                    f_x += x_i * w_i
        return f_x
    
    """
    This function performed demoting on weights for a data instance.
    It goes through event non-label attribute. For every value = 1,
    change corresponding weight by dividing by alpha.
    
    @param (Array) instance A single data instance
    """
    def demoting(self, instance):
        for attribute in self.attr_order:
            if attribute != "label" and attribute != "Exclude":
                value = instance[attribute]
                key = (attribute,value)
                w_i = self.weight_vector.get(key)
                self.weight_vector[key] = w_i/self.alpha
                
    """
    This function performed promoting on weights for a data instance.
    It goes through event non-label attribute. For every value = 1,
    change corresponding weight by multiplying by alpha.
    
    @param (Array) instance A single data instance
    """
    def promoting(self, instance):
        for attribute in self.attr_order:
            if attribute != "label" and attribute != "Exclude":
                value = instance[attribute]
                key = (attribute,value)
                w_i = self.weight_vector.get(key)
                self.weight_vector[key] = w_i * self.alpha
    
    """
    This function trains a model using the Winnow 2 algorithm.
    It initializes weights and creates the encoded data set.
    It loops over the data to compare predicted class value to 
    actual and transforms weights according to accuracy.
    """
    def train(self):
        self.weight_vector = self.createWeights()
        hotCodedTrainingData = self.createHotCodedData(self.training_data)
        
        for instance in hotCodedTrainingData:
            f_x = self.getFx(instance)
            h_x = 1 if f_x > self.theta else 0
            
            y = self.labelsValue.get(instance["label"])

            if h_x < y:
                self.promoting(instance)
            elif h_x > y:
                self.demoting(instance)
    
    """
    This function performs classifications on test data
    using a model created the training function.
    """
    def classify(self):
        hotCodedData = self.createHotCodedData(self.test_data)        
        for instance in hotCodedData:
            f_x = self.getFx(instance)
            h_x = 1 if f_x > self.theta else 0
            self.classifications.append(h_x)
    def classifyMultiClass(self):
        hotCodedData = self.createHotCodedData(self.test_data)        
        for instance in hotCodedData:
            f_x = self.getFx(instance)
            h_x = 1 if f_x > self.theta else 0
            #self.classifications.append(h_x)
            ans = (self.labels[h_x], f_x)
            self.classificationsMultiClass[h_x] = f_x
    """
    This function evaluates the classifications on the test data
    set compared to the actual labels.
    """
    def evaluate(self):
        hotCodedTestData = self.createHotCodedData(self.test_data)
        incorrect = 0
        for i in range(len(self.classifications)):
            instance = hotCodedTestData[i]
            h_x = self.classifications[i]
            y = self.labelsValue.get(instance["label"])
            if h_x != y:
                incorrect += 1
        self.error_rate = round(float(incorrect) / float(len(hotCodedTestData)), 2)
    def evaluateMultiClass(self):
        hotCodedTestData = self.createHotCodedData(self.test_data)
        incorrect = 0
        for i in range(len(self.classificationsMultiClass)):
            instance = hotCodedTestData[i]
            h_x = max(self.classificationsMultiClass, key=self.classificationsMultiClass.get)
            y = self.labelsValue.get(instance["label"])
            if h_x != y:
                incorrect += 1
        self.error_rate = round(float(incorrect) / float(len(hotCodedTestData)), 2)

for dataSet in dataSets:
    data_ingest_object = DataIngest("Data/" + dataSet)
    
    if len(data_ingest_object.labels) == 2:
        winnow_object = Winnow2Classifier(
            data_ingest_object.training_data, 
            data_ingest_object.test_data, 
            data_ingest_object.attributes, 
            data_ingest_object.attr_order, 
            data_ingest_object.labels
        )
        print "\n----------------------------------------"
        print "****Winnow2 for", dataSet, "****"
        print "*Error rate*", winnow_object.error_rate
        print "*Classifications sample results on test data*"

        for i in range(len(winnow_object.test_data)):
            print "\tData instance:", winnow_object.test_data[i],
            h_x = winnow_object.classifications[i]
            prediction = winnow_object.labels[h_x]
            print "\n\t\t(Prediction:", prediction, ")"
            if i == 2: break
    else:
        winnow_object = Winnow2Classifier(
            data_ingest_object.training_data, 
            data_ingest_object.test_data, 
            data_ingest_object.attributes, 
            data_ingest_object.attr_order, 
            data_ingest_object.labels
        )
        print "\n----------------------------------------"
        print "****Winnow2 for", dataSet, "****"
        print "*Error rate*", winnow_object.error_rate
        print "*Classifications sample results on test data*"

        for i in range(len(winnow_object.test_data)):
            print "\tData instance:", winnow_object.test_data[i],
            h_x = max(winnow_object.classificationsMultiClass, key=winnow_object.classificationsMultiClass.get)
            prediction = winnow_object.labels[h_x]
            print "\n\t\t(Prediction:", prediction, ")"
            if i == 2: break