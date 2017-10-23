from __future__ import division
from IPython.core.display import *
import math;
import random;
import copy;

#######################################
## DataIngest
## This class performs data ingest including
## reading from files, parsing data and
## attributes
#######################################
class DataIngest():
  
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

    def read_data(self, postfix):
        raw_from_data_file = []
        with open( self.filename + postfix, 'r') as f:
            file_data = [x for x in f.readlines()]
        f.closed
        for line in file_data:
            line = line.strip()
            raw_from_data_file.append(line)
        return raw_from_data_file

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
                        minimum = float(tokenized_lineAttr[2])
                        maximum = float(tokenized_lineAttr[3])
                        step = float(tokenized_lineAttr[4])
                        chosenValue = minimum

                        j = 0
                        value = float(minimum)
                        while value < maximum:
                            value = minimum + step*j
                            if value > float(thisValue):
                                break
                            else:
                                chosenValue = value
                            j += 1
                        alteredLine.append(float(chosenValue))
                    else:
                        chosenValue = tokenized_line[i]
                        alteredLine.append(chosenValue)
            self.data.append(alteredLine)
                
    def parse_attributes(self):
        for line in self.raw_from_attr_file:
            tokenized_line = line.strip().split(',')
            values = []
            if tokenized_line[1] == "buckets":
                minimum = float(tokenized_line[2])
                maximum = float(tokenized_line[3])
                step = float(tokenized_line[4])

                i = 0
                value = float(minimum)
                while value < maximum:
                    value = minimum + step*i
                    values.append(value)
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


#######################################
## DecisionTree
## This class performs creation of 
## decision trees with ID3 classification main
## method with helper functions
#######################################
class DecisionTree():  
    def __init__(self, data, test_data, validation_data, attrs, labels, attr_order):
        self.data = data
        self.test_data = test_data
        self.validation_data = validation_data
        self.attrs = attrs
        self.labels = labels
        self.attr_order = attr_order
        self.labelIndex = self.get_attr_index("label")
        self.nodeId = 1
    
    ## Main tree generation methods
    def id3(self, data, attrs):
        if len(data) == 0 or len(attrs) == 0: 
            return self.majority(data)
        if self.is_homogeneous(data): 
            return self.is_homogeneous(data)

        best_attr = self.pick_best_attr(attrs,data)
        node = self.create_node(best_attr,len(data),None)
        domain_of_best_attr = attrs[best_attr]
        child_attrs = copy.deepcopy(attrs)
        child_attrs.pop(best_attr)
        
        for value in domain_of_best_attr:
            subset = self.get_categorical_subset(best_attr, value, data)
            child = self.id3(subset, child_attrs)
            node["children"].append(child)
        return node

    ## Evaluation Methods
    def evaluate(self, classifications, data):
        data = self.validation_data
        n = len(data)
        errors = 0
        for i in range(len(data)):
            d = data[i]
            label = d[self.labelIndex]
            classified_label = classifications[i]
            if label != classified_label:
                errors += 1
        return 1-errors/n

    def classify(self, tree, data):
        model = []
        for d in data:
            while tree not in data_ingest_object.labels:
                attr = tree.get("attr")
                attr_index = self.get_attr_index(attr)
                this_value = d[attr_index]
                domain = self.attrs.get(attr)
                children = tree.get("children")
                for i in range(len(domain)):
                    if this_value == domain[i]:
                        tree = children[i]
            model.append(tree)
        return model
        
    #Helper Methods
    def analyze_labels(self, data):
        p_i = {}
        for label in self.labels:
            p_i[label] = 0
        for dataPoint in data:
            label = dataPoint[self.labelIndex]
            p_i[label] += 1
        return p_i

    def is_homogeneous(self, data):
        p_i = self.analyze_labels(data)
        majorityLabel = self.majority(data)
        if p_i[majorityLabel] == len(data):
            return majorityLabel
        else:
            return False
    
    def majority(self, data):
        p_i = self.analyze_labels(data)
        return max(p_i, key=p_i.get)

    def get_entropy(self, n, p_i):
        entropy = 0
        for label in self.labels:
            p = p_i[label]
            if p <= 1:
                entropy = 0
            else:
                entropy += -1*(p/n)*math.log((p/n),2)
        return entropy
    
    def get_starting_entropy(self, data):
        p_i = self.analyze_labels(data)
        return self.get_entropy(len(data),p_i)

    def get_frequency(self, attr, data, attrs, value):
        attrIndex = self.get_attr_index(attr)
        frequency = 0
        p_i = {}
        for label in self.labels:
            p_i[label] = 0
        for d in data:
            valueOfDataPoint = d
            if value == valueOfDataPoint:
                frequency += 1
                label = data[d][self.labelIndex]
                p_i[label] += 1
        return (frequency, p_i)

    def get_info_gain(self, attr, data, attrs):
        resulting_entropy = 0
        for value in attrs.get(attr):
            (frequency, p_i) = self.get_frequency(attr, data, attrs, value)
            entropy = self.get_entropy(len(data),p_i)
            resulting_entropy += (frequency/len(data))*entropy
        return self.get_starting_entropy(data)-resulting_entropy
    
    def pick_best_attr(self, attrs, data):
        best_attr = None
        best_info_gain = -1
        for attr in attrs:
            if self.get_info_gain(attr, data, attrs) > best_info_gain:
                best_attr = attr
        return best_attr

    def create_node(self, attr, numElements, midPoint):
        node = {};
        node["children"] = []
        node["attr"] = attr
        node["numElements"] = numElements
        node["nodeId"] = self.nodeId
        self.nodeId += 1
        node["midPoint"] = midPoint
        return node
    
    def get_attr_index(self, thisAttr):
        ans = 0
        for i in range(len(self.attr_order)):
            attr = self.attr_order[i]
            if thisAttr == attr:
                ans = i
        return ans

    def get_categorical_subset(self, attr, value, data):
        attr_index = self.get_attr_index(attr)
        subset = []
        data_copy = copy.deepcopy(data)
        for d in data_copy:
            if d[attr_index] == value:
                subset.append(d)
        return subset


#######################################
## CrossValidation
## This class performs creation of 
## test, training and validation data sets
## for n-fold validation
#######################################
class CrossValidation():
      
    def __init__(self, k, data):
        self.k = k
        self.data = data
        self.test_subsets = {}
        self.training_subsets = {}
        self.validation_subset = {}
        
        random.shuffle(self.data)
        numData = len(self.data)
        tenPercentIndex = int(numData/10)
        self.validation_subset = self.data[0:tenPercentIndex]
        self.data = self.data[tenPercentIndex]
        
        numData = len(self.data)
        numInSubset = math.floor(numData/self.k)
        for i in range(self.k):
            startIndex = int(i*numInSubset)
            endIndex = int((i+1)*numInSubset)
            test_subset = self.data[startIndex:endIndex]
            self.test_subsets[i] = test_subset
            training_subset = self.data[0:startIndex] + self.data[endIndex:numData]
            self.training_subsets[i] = training_subset


#######################################
## PruneTree
## This class performs reduced error pruning
## for classification decision trees
#######################################
class PruneTree():
     
    def __init__(self, labels, tree, tree_obj, originalScore):
        self.labels = labels
        self.tree = tree
        self.tree_obj = tree_obj
        self.originalScore = originalScore
        self.visited = []
        self.complete = False
        self.currentBestScore = self.originalScore
        self.currentBestTree = self.tree
        self.prunedTree = self.get_replacement_value(self.tree)
    
    ## Main pruning method
    def prune(self):
        (nodeId, node) = self.get_unvisited_node(self.currentBestTree)
        pruned = False
        if nodeId != False:
            replacementValue = self.get_replacement_value(node)
            testTree = self.replace_value(nodeId, replacementValue, self.currentBestTree)
            testModel = tree_obj.classify(testTree, data_ingest_object.data)
            testScore = tree_obj.evaluate(testModel, self.tree_obj.data)
            if testScore >= self.currentBestScore:
                self.currentBestScore = testScore
                self.currentBestTree = testTree
                pruned = True
            self.visited.append(nodeId)
        else:
            self.complete = True
        return pruned

	## Helper methods
    def get_replacement_value(self, tree):
        p_i = {}
        for label in self.labels:
            p_i[label] = 0
        children = tree.get('children')
        for child in children:
            if type(child) is dict:
                value = self.get_replacement_value(child)
            else:
                value = child
            if value in p_i.keys():
                p_i[value] += 1
        majorityLabel = max(p_i, key=p_i.get)
        return majorityLabel
    
    def get_unvisited_node(self, tree):
        if type(tree) is not dict:
            return (False, False)
        tree = tree.copy()
        nodeId = tree.get('nodeId')
        if nodeId not in self.visited:
            return (nodeId, tree)
        children = tree.get('children')
        childNodeId = False
        childNode = False
        for child in children:
            if type(child) is dict:
                (childNodeId, childNode) = self.get_unvisited_node(child)
        return (childNodeId, childNode)
    
    def replace_value(self, nodeId, replacementValue, tree):
        if type(tree) is not dict:
            return replacementValue
        tree = tree.copy()
        thisNodeId = tree.get('nodeId')
        if thisNodeId == nodeId:
            return replacementValue
        children = tree.get('children')
        if len(children) != 0:
            newChildren = []
            for child in children:
                if type(child) is dict:
                    value = self.replace_value(nodeId, replacementValue, child)
                else:
                    value = child
                newChildren.append(value)
            tree['children'] = newChildren
        return tree


#######################################
## Function Evocations
#######################################
dataSets = [
    ("abalone", "classification"),
    ("car", "classification"), 
    ("segmentation", "classification")
]
foldNum = 5
f = open('output.txt', 'w')

for dataSet in dataSets:
    (name, thisType) = dataSet
    data_ingest_object = DataIngest("Data/" + name)
    data_ingest_object.raw_from_data_file = data_ingest_object.read_data(".data")
    data_ingest_object.raw_from_attr_file = data_ingest_object.read_data(".attributes")
    data_ingest_object.parse_attributes()
    data_ingest_object.parse_data()
    f.write("\n")
    print "\n"
    print "***Data Set: ", name, "***"
    print "\t Instance example:", data_ingest_object.data[0]
    print "\t Labels:", data_ingest_object.labels
    print "\t Problem type:", thisType
    f.write("\n")
    f.write("***Data Set: " + name + "***" + "\n")
    f.write("\t Problem type:" + thisType + "\n")
    
    cvo = CrossValidation(foldNum, data_ingest_object.data)
    sumErrors = 0
    for validationFold in range(foldNum):
        tree_obj = DecisionTree(
            cvo.training_subsets[validationFold], 
            cvo.test_subsets[validationFold], 
            cvo.validation_subset, 
            data_ingest_object.attributes, 
            data_ingest_object.labels, 
            data_ingest_object.attr_order)
        default = data_ingest_object.labels[0]
        tree = tree_obj.id3(data_ingest_object.data, data_ingest_object.attributes)
        model = tree_obj.classify(tree, data_ingest_object.data)
        score = tree_obj.evaluate(model, tree_obj.data)
        foldScore = score
        sumErrors += foldScore
    print "\t\t Tree size:", tree_obj.nodeId
    f.write("\t\t ***Tree size:" + str(tree_obj.nodeId)+ "\n")
    print "\t\t ***Averaged classification accuracy over validation folds:", sumErrors/foldNum, "***"
    f.write("\t\t ***Averaged classification accuracy over validation folds:" + str(sumErrors/foldNum) + "***" + "\n")
        
    pruned_tree_obj = PruneTree(data_ingest_object.labels, tree.copy(), tree_obj, sumErrors/foldNum)

    while pruned_tree_obj.complete == False:
        prunedBool = pruned_tree_obj.prune()
    print "\t\t ***Pruned averaged evaluation:", pruned_tree_obj.currentBestScore, "***"
    f.write("\t\t ***Pruned averaged evaluation:" + str(pruned_tree_obj.currentBestScore) + "***" + "\n")
f.close()