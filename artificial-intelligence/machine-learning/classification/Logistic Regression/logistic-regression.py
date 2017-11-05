
# coding: utf-8

# # Logistic Regression Classification

# In[1]:

get_ipython().magic(u'matplotlib inline')
from random import choice;
from IPython.core.display import display, HTML
from __future__ import division
import math;
import numpy as np
import matplotlib.pyplot as plt
import random
import copy

plain =  [0.0, 0.0, 0.0, 0.0,0.0, 0.0, 0.0, 0.0,0.0, 0.0, 0.0, 0.0,1.0, 1.0, 1.0, 1.0]
forest = [0.0, 1.0, 0.0, 0.0,1.0, 1.0, 1.0, 0.0,1.0, 1.0, 1.0, 1.0,0.0, 1.0, 0.0, 0.0]
hills =  [0.0, 0.0, 0.0, 0.0,0.0, 0.0, 1.0, 0.0,0.0, 1.0, 1.0, 1.0,1.0, 1.0, 1.0, 1.0]
swamp =  [0.0, 0.0, 0.0, 0.0,0.0, 0.0, 0.0, 0.0,1.0, 0.0, 1.0, 0.0,1.0, 1.0, 1.0, 1.0]

figure = plt.figure(figsize=(20,6))

axes = figure.add_subplot(1, 3, 1)
pixels = np.array([255 - p * 255 for p in plain], dtype='uint8')
pixels = pixels.reshape((4, 4))
axes.set_title( "Left Camera")
axes.imshow(pixels, cmap='gray')

axes = figure.add_subplot(1, 3, 2)
pixels = np.array([255 - p * 255 for p in forest], dtype='uint8')
pixels = pixels.reshape((4, 4))
axes.set_title( "Front Camera")
axes.imshow(pixels, cmap='gray')

axes = figure.add_subplot(1, 3, 3)
pixels = np.array([255 - p * 255 for p in hills], dtype='uint8')
pixels = pixels.reshape((4, 4))
axes.set_title( "Right Camera")
axes.imshow(pixels, cmap='gray')

plt.show()
plt.close()


# ## Data
# 
# We have clean examples of the different types of terrain but based on the location, the registration can be a bit off for some of the types and the visual sensor is often blurry.
# 
# Here are the clean examples with different registrations: 

# In[2]:

clean_data = {
    "plains": [
        [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 1.0, 1.0, 1.0, "plains"]
    ],
    "forest": [
        [0.0, 1.0, 0.0, 0.0, 1.0, 1.0, 1.0, 0.0, 1.0, 1.0, 1.0, 1.0, 0.0, 1.0, 0.0, 0.0, "forest"],
        [0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 0.0, 0.0, 1.0, 0.0, "forest"],
        [1.0, 0.0, 0.0, 0.0, 1.0, 1.0, 0.0, 0.0, 1.0, 1.0, 1.0, 0.0, 1.0, 0.0, 0.0, 0.0, "forest"],
        [0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 1.0, 0.0, 1.0, 1.0, 1.0, 0.0, 0.0, 0.0, 1.0, "forest"]
    ],
    "hills": [
        [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, "hills"],
        [0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 1.0, 1.0, 0.0, 1.0, 1.0, 1.0, 1.0, "hills"],
        [0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 1.0, 1.0, 0.0, 0.0, 1.0, 1.0, 1.0, 0.0, "hills"],
        [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 1.0, 0.0, 1.0, 1.0, 1.0, "hills"]
    ],
    "swamp": [
        [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 1.0, 0.0, 1.0, 1.0, 1.0, 1.0, "swamp"],
        [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 1.0, 1.0, 1.0, 1.0, 1.0, "swamp"]        
    ]
}


# Let's create a function that allows us to view any of these:

# In[3]:

def view_sensor_image( data):
    figure = plt.figure(figsize=(4,4))
    axes = figure.add_subplot(1, 1, 1)
    pixels = np.array([255 - p * 255 for p in data[:-1]], dtype='uint8')
    pixels = pixels.reshape((4, 4))
    axes.set_title( "Left Camera:" + data[-1])
    axes.imshow(pixels, cmap='gray')
    plt.show()
    plt.close()


# "I think that I shall never see a thing so lovely as a tree."

# In[4]:

view_sensor_image( clean_data[ "forest"][3])


# In[5]:

view_sensor_image( clean_data["swamp"][1])


# The data that comes in, however, is noisy. The values are never exactly 0 and 1. In order to mimic this we need a `blur` function.
# 
# We will assume that noise is normally distributed. For values that should be 0, the noisy values are distributed $N(0.10, 0.05)$. For values should be 1, the noisy values are distributed $N(0.9, 0.10)$.

# In[6]:

def blur( data):
    def apply_noise( value):
        if value < 0.5:
            v = random.gauss( 0.10, 0.05)
            if v < 0.0:
                return 0.0
            if v > 0.75:
                return 0.75
            return v
        else:
            v = random.gauss( 0.90, 0.10)
            if v < 0.25:
                return 0.25
            if v > 1.00:
                return 1.00
            return v
    noisy_readings = [apply_noise( v) for v in data[0:-1]]
    return noisy_readings + [data[-1]]


# We can see how this affects what the agent *actually* sees.

# In[7]:

view_sensor_image( blur( clean_data["swamp"][0]))


# ---
# ## Helper Functions

# ***get_y_hat***
# 
# This function calculates the y_hat value where y_hat = 1/[1+e^(-theta·x)].

# In[8]:

def get_y_hat(thetas, element):
    term = 0;
    for i in range(len(thetas)):
        theta = thetas[i];
        x = element[i];
        term += x*theta;
    term = math.exp(-1*term);
    denominator = 1 + term;
    
    y_hat = 1/denominator;
    return y_hat;


# ***calculate_error***
# 
# This function calculates error where log loss = -1/n · ε [y · log(y_hat) + (1-y)·log(1-y_hat)]

# In[9]:

def calculate_error(thetas, data):
    n = len(data);
    J = 0;
    
    for i in range(len(thetas)):
        y = data[i][17];
        y_hat = get_y_hat(thetas, data[i]);    
        J += y*math.log(y_hat) + (1-y)*math.log(1-y_hat);
        
    J *= -1/n;
    return J;


# ***derivative***
# 
# This function calculates the derivative where derivative = 1/n · ε [(y_hat – y) · x]

# In[10]:

def derivative(j, thetas, data):
    derivative = 0;
    n = len(data);
    
    for i in range(len(thetas)):
        y = data[i][17];
        y_hat = get_y_hat(thetas, data[i]);    
        x = data[i][j];
        derivative += (y_hat - y)*x;
        
    derivative *= 1.0/n;
    return derivative;


# ---
# 
# ## Main Functions

# ### `generate_data`
# 
# This function generates blurred hills and not hills examples. It transforms string labels into binary 0 or 1.

# In[11]:

def generate_data(data, n, label):
    new_data = [];
    
    for i in range(n):
        count1 = len(data[label]) - 1;
        thisIndex1 = random.randint(0, count1);
        thisElement1 = blur(data[label][thisIndex1]);
        thisElement1[16] = 1;
        thisElement1.insert(0,1.0);
        new_data.append(thisElement1);
    
        random_list = choice(list(data.values()));
        while(random_list[0][16] == label):
            random_list = choice(list(data.values()));
        count0 = len(random_list) - 1;
        thisIndex0 = random.randint(0, count0);
        thisElement0 = blur(random_list[thisIndex0]);
        thisElement0[16] = 0;
        thisElement0.insert(0,1.0);
        new_data.append(thisElement0);
    return new_data;

results = generate_data(clean_data, 10, "hills")
for result in results:
    print result


# ### `learn_model`
# 
# `learn_model` is the function that takes in training data and learns the logistic regression model with the gradient descent approach. When verbose is True, the error is printed out every 1,000 iterations. Returns the List of Thetas.

# In[12]:

def learn_model(data, verbose):
    epsilon = 0.0000001;
    alpha = 0.1;
    
    thetas = [];
    for i in range(17):
        thetas.append(random.uniform(-1, 1));
    previous_error = 0.0;
    current_error = calculate_error(thetas, data);
        
    iteration = 0;
    while abs(current_error - previous_error) >= epsilon:
        new_thetas = [];
        for j in range(len(thetas)):
            new_theta = thetas[j] - (alpha * derivative(j, thetas, data));
            new_thetas.append(new_theta);
        thetas = new_thetas;        
        previous_error = current_error;
        current_error = calculate_error(thetas, data);
        iteration += 1;
        if verbose and (iteration % 1000 == 0):
            print "Iteration #", iteration, "with error", current_error;
    return thetas;

train_data = generate_data(clean_data, 100, "hills")
model = learn_model(train_data, True)
print model


# Use `generate_data` to generate 100 blurred "hills" examples with balanced "non hills" examples and use this as your test data. Set labeled=True and generate results to use in `calculate_confusion_matrix`. Print out the first 10 results, one per line.

# In[13]:

print "\nFirst 10 Results:\n"
    
for i in range(10):
    print i+1, ') ', train_data[i], '\n';
    this_result = copy.copy(train_data[i]);
    del this_result[0];
    this_result[-1] = "Result Sample" + str(this_result[-1]);
    view_sensor_image(this_result);


# ### `apply_model`
# 
# This function takes a List of Thetas (the model) and either labeled or unlabeled data. If the data is unlabeled, it returns predictions for each observation as a Tuple of the inferred value (0 or 1) and the actual probability (so something like (1, 0.73) or (0, 0.19). If the data is labeled, it returns a Tuple of the actual value (0 or 1) and the predicted value (0 or 1).

# In[14]:

test_data = generate_data( clean_data, 100, "hills")

def apply_model( model, test_data, labeled=False):
    answer = [];
    
    if labeled:
        for element in test_data:
            actual_value = element[17];
            actual_probability = get_y_hat(model, element);
            if actual_probability > 0.5:
                inferred_value = 1;
            else:
                inferred_value = 0;
            answer.append((actual_value, inferred_value));
    else:
        for element in test_data:
            actual_probability = get_y_hat(model, element);
            if actual_probability > 0.5:
                inferred_value = 1;
            else:
                inferred_value = 0;
            answer.append((inferred_value, actual_probability));
    return answer;

results = apply_model( model, test_data)
print results


# Using the results above, show your confusion matrix for your model.
# 
# ### `calculate_confusion_matrix`
# 
# The `calculate_confusion_matrix` takes the results of `apply_model` when labeled=True and prints a nice HTML version of a confusion matrix and include statistics for error rate, true positive rate and true negative rate.

# In[15]:

results = apply_model( model, test_data, True)

def calculate_confusion_matrix(results):
    (tp, fn, fp, tn) = (0, 0, 0, 0);
    n = len(results);
    
    for result in results:
        (a, b) = result;
        if a:
            if b: tp += 1;
            else: fp += 1;
        else:
            if b: fn += 1;
            else: tn += 1;
    
    htmlString = '<h1>Confusion Matrix</h1><table>';
    htmlString += '<tr><th></th><th>Predicted Condition Positive</th><th>Predicted Condition Negative</th></tr>';
    htmlString += '<tr><th>Actual Condition Positive</th>';
    htmlString += '<td style="background-color:aquamarine; text-align: center">True Positive (TP): <br />';
    htmlString += str(tp) +'/'+ str(n) + ' = ' + str(tp/n*100) + '%</td>';
    htmlString += '<td style="background-color:pink; text-align: center">False Negative (FN): <br />';
    htmlString += str(fn) +'/'+ str(n) + ' = ' + str(fn/n*100) + '%</td></tr>';
    htmlString += '<tr><th>Actual Condition Negative</th>';
    htmlString += '<td style="background-color:pink; text-align: center">False Positive (FP): <br />';
    htmlString += str(fp) +'/'+ str(n) + ' = ' + str(fp/n*100) + '%</td>';
    htmlString += '<td style="background-color:aquamarine; text-align: center">True Negative (TN): <br />';
    htmlString += str(tn) +'/'+ str(n) + ' = ' + str(tn/n*100) + '%</td></tr>';
    htmlString += '</table>';
    htmlString += '<h2>Error rate</h2>' + str((fn+fp)/n*100) + '%';
    htmlString += '<h2>True positive rate</h2>' + str(tp/(tp+fn)*100) + '%';
    htmlString += '<h2>True negative rate</h2>' + str(tn/(tn+fp)*100) + '%';
    display(HTML(htmlString));
    
calculate_confusion_matrix(results);


# In[ ]:



