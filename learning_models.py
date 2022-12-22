import numpy as np 
import copy
import pandas as pd
from configparser import ConfigParser
config = ConfigParser()
config.read('config.ini')

class LearningModels():
    def __init__(self) -> None:
        pass

class LinearRegression(LearningModels):
    def __init__(self):
        self.__coef = None
        self.__intercept = None
        self.__score = None

    def fit(self, x:np.ndarray, y:np.ndarray, iterations = 30, alpha = 5.0e-6):
        w_init = np.fromstring(config.get('TrainingModel','w_initial'),sep=',')
        b_init = np.fromstring(config.get('TrainingModel','w_initial'),sep=',')

        self.__coef , self.__intercept = self.__apply_gradient_descent(x,y,w_init,b_init,alpha,iterations)
        yhat = np.dot(x,self.__coef)+self.__intercept
        self.__compute_score(y,yhat.reshape(-1,1))

    def save_model(self,filename):
        df = pd.DataFrame(np.concatenate([self.coef,self.intercept]))
        df.to_csv(filename,header=False,index=False)

    def load_model(self,model):
        params = pd.read_csv(model,header=None)
        self.__coef = params.iloc[0:-1,0].to_numpy()
        self.__intercept = params.iloc[-1,0]

    def predict(self,x):
        yhat = (np.dot(x,self.__coef) + self.__intercept).round(2)
        return yhat

    def __compute_score(self,y,yhat):
        self.__score = 1- ((y-yhat)**2).sum() / ((y-y.mean())**2).sum()

    @property
    def coef(self):
        return self.__coef
    
    @property
    def intercept(self):
        return self.__intercept

    @property
    def score(self):
        return self.__score

    def __compute_cost(self,x,y,w,b):
        """
        compute cost
        Args:
        X (ndarray (m,n)): Data, m examples with n features
        y (ndarray (m,)) : target values
        w (ndarray (n,)) : model parameters  
        b (scalar)       : model parameter 
                
        Returns:
        cost (scalar): cost
        """
        m = x.shape[0]
        cost = 0.0
        for i in range(m):                                
            f_wb_i = np.dot(x[i], w) + b           #(n,)(n,) = scalar (see np.dot)
            cost = cost + (f_wb_i - y[i])**2       #scalar
        cost = cost / (2 * m)                      #scalar    
        return cost
        
    
    def __compute_gradient(self,x,y,w,b):
        """
        Computes the gradient for linear regression 
        Args:
        X (ndarray (m,n)): Data, m examples with n features
        y (ndarray (m,)) : target values
        w (ndarray (n,)) : model parameters  
        b (scalar)       : model parameter
        
        Returns:
        dj_dw (ndarray (n,)): The gradient of the cost w.r.t. the parameters w. 
        dj_db (scalar):       The gradient of the cost w.r.t. the parameter b. 
        """
        m,n = x.shape           #(number of examples, number of features)
        dj_dw = np.zeros(n)
        dj_db = 0.

        for i in range(m):                             
            err = (np.dot(x[i], w) + b) - y[i]   
            for j in range(n):                         
                dj_dw[j] = dj_dw[j] + err * x[i, j]    
            dj_db = dj_db + err                        
        dj_dw = dj_dw / m                                
        dj_db = dj_db / m                                
            
        return dj_db, dj_dw

    def __apply_gradient_descent(self,x,y,w_in,b_in,alpha,iterations):
        """
        Performs batch gradient descent to learn w and b. Updates w and b by taking 
        num_iters gradient steps with learning rate alpha
        
        Args:
        X (ndarray (m,n))   : Data, m examples with n features
        y (ndarray (m,))    : target values
        w_in (ndarray (n,)) : initial model parameters  
        b_in (scalar)       : initial model parameter
        cost_function       : function to compute cost
        gradient_function   : function to compute the gradient
        alpha (float)       : Learning rate
        iterations (int)     : number of iterations to run gradient descent
        
        Returns:
        w (ndarray (n,)) : Updated values of parameters 
        b (scalar)       : Updated value of parameter 
        """
        # An array to store cost J and w's at each iteration primarily for graphing later
        w = copy.deepcopy(w_in)  #avoid modifying global w within function
        b = b_in
        
        for i in range(iterations):

            # Calculate the gradient and update the parameters
            dj_db,dj_dw = self.__compute_gradient(x, y, w, b)   ##None

            # Update Parameters using w, b, alpha and gradient
            w = w - alpha * dj_dw               ##None
            b = b - alpha * dj_db               ##None
            
        return w, b #return final w,b and J history for graphing