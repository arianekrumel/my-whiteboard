Model representation
* m = number of training examples
* x = input variables/ features
* y = output variable/ target variable
* (x, y)

Cost function
training set -> learning algorithm -> h
x -> h (hypothesis) -> y
h is a function that maps x to y
h[theta](x) = theta[0] = theta[1]*x
idea: choose thetas so that h(x) is close to y for given training examples
minimize theta[0], theta[1]
the cost function/ square error function/ mean squared error function J
J(theta[0], theta[1]) = 1/(2m) sum from i=1 to m (h[theta](x[i]0 - y[i])^2

