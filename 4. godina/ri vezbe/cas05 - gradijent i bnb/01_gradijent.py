# -*- coding: utf-8 -*-
"""01_gradijent.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1fhFkgcjJLhbUJ2IxR6vlnew30ahtmCl1

***1. Gradijentni spust***
"""

import numpy as np

def f(x):
    return 0.5*(x[0]**2 + 10*x[1]**2)

def gradient(x):
    return np.array([x[0], 10*x[1]])

def gradient_descent(f, gradient, x0, alpha, eps, max_iter):
    x = x0
    
    for i in range(max_iter):
        x_new = x - alpha*gradient(x)
        
        if np.abs(f(x_new) - f(x)) < eps:
            break

        x = x_new

    converged = i != max_iter
    
    result = {}
    result['converged'] = converged
    result['num_iter'] = i
    result['x'] = x_new

    return result

x0 = np.array([3, 5])
alpha = 0.1
eps = 0.001
max_iter = 1000

gradient_descent(f, gradient, x0, alpha, eps, max_iter)

"""***2. Inercija***"""

def momentum(f, gradient, x0, alpha, eps, max_iter, beta):
    x = x0
    d = 0 # prosek

    for i in range(max_iter):
        d = beta*d + alpha*gradient(x)
        x_new = x-d

        if np.abs(f(x_new) - f(x)) < eps:
            break

        x = x_new

    converged = i != max_iter
    
    result = {}
    result['converged'] = converged
    result['num_iter'] = i
    result['x'] = x_new

    return result

momentum(f, gradient, x0, alpha, eps, max_iter, beta=0.9)

"""***3. Nesterov ubrzani gradijentni spust***"""

def nesterov(f, gradient, x0, alpha, eps, max_iter, beta):
    x = x0
    d = 0

    for i in range(max_iter):
        d = beta*d + alpha*gradient(x-beta*d)
        x_new = x-d

        if np.abs(f(x_new) - f(x)) < eps:
            break

        x = x_new

    converged = i != max_iter
    
    result = {}
    result['converged'] = converged
    result['num_iter'] = i
    result['x'] = x_new

    return result

nesterov(f, gradient, x0, alpha, eps, max_iter, beta=0.9)

"""***4. Adam***"""

def adam(f, gradient, x0, alpha, eps, max_iter, beta1, beta2, delta):
    # prvi moment EX
    m = 0
    # drugi moment EX^2
    v = 0

    x = x0
    for i in range(1, max_iter):
        m = beta1*m + (1-beta1)*gradient(x)
        v = beta2*v + (1-beta2)*gradient(x)**2

        m_hat = m / (1-beta1**i)
        v_hat = v / (1-beta2**i)

        x_new = x - alpha*(m_hat / (np.sqrt(v_hat) + delta))

        if np.abs(f(x_new) - f(x)) < eps:
            break

        x = x_new

    converged = i != max_iter
    
    result = {}
    result['converged'] = converged
    result['num_iter'] = i
    result['x'] = x_new

    return result

adam(f, gradient, x0, alpha, eps, max_iter, beta1=0.9, beta2=0.999, delta=1e-7)