from evaluation_metrics import MetricsEvaluator
from math import sqrt 
from configparser import ConfigParser
config = ConfigParser()
config.read('config.ini')

class RangeEvaluator(MetricsEvaluator):
    def __init__(self, db,y_real,y_pred,investment_price,total_investment) -> None:
        super().__init__(db)
        
        y_pred = y_pred.reshape(-1,1)
        accuracy_bound = float(config.get('Metrics','accuracy_bound'))
        self.__accuracy = self.compute_accuracy(accuracy_bound,y_real,y_pred)
        self.__rmse = self.compute_rmse(y_real,y_pred)
        
        rois = self.compute_roi(investment_price,y_real[-1][0],y_pred[-1][0])
        self.__roi_real = rois['roi_real']
        self.__roi_pred = rois['roi_pred']
        
        decisions = self.compute_decision(investment_price,y_real[-1][0],y_pred[-1][0])
        self.__decision_real = decisions['decision_real']
        self.__decision_pred = decisions['decision_pred']
        
        self.__class_type = self.classify(investment_price,y_real[-1][0],y_pred[-1][0])
        self.__roi_pkr = self.compute_roi_pkr(self.__roi_pred,total_investment)
        self.__dict = {
            'investment_price':investment_price,
            'accuracy':self.__accuracy,
            'rmse': self.__rmse,
            'roi_real': self.__roi_real,
            'roi_pred': self.__roi_pred,
            'decision_real': self.__decision_real,
            'decision_pred': self.__decision_pred,
            'class_type': self.__class_type,
            'roi_pkr': self.__roi_pkr
        }

    @property
    def roi_pkr(self):
        return self.__roi_pkr
    @property
    def dict(self):
        return self.__dict
    
    @property 
    def accuracy(self):
        return self.__accuracy

    @property 
    def rmse(self):
        return self.__rmse

    @property 
    def roi_real(self):
        return self.__roi_real

    @property 
    def roi_pred(self):
        return self.__roi_pred

    @property 
    def decision_real(self):
        return self.__decision_real

    @property 
    def decision_pred(self):
        return self.__decision_pred

    @property 
    def class_type(self):
        return self.__class_type
    
    def compute_roi_pkr(self,roi,investment):
        return round(abs(roi/100)*investment,2)

    def compute_rmse(self,y,yhat):
        rmse = sqrt( ((y-yhat) ** 2).sum() / y.size)
        return round(rmse,2)
    
    def compute_accuracy(self,bound,y,yhat):
        classy = (abs(y-yhat) < y * bound/100).astype(int)
        accuracy = classy.sum()/classy.size * 100
        return round(accuracy)

    def classify(self,investment_price,y_actual,y_pred):
        if y_actual >= investment_price and y_pred >= investment_price:
            self.db.insert_classification('tp',self.__rmse,self.__accuracy,self.__decision_pred)
        elif y_actual > investment_price and y_pred < investment_price:
            self.db.insert_classification('fn',self.__rmse,self.__accuracy,self.__decision_pred)
        elif y_actual < investment_price and y_pred < investment_price:
            self.db.insert_classification('tn',self.__rmse,self.__accuracy,self.__decision_pred)
        elif y_actual < investment_price and y_pred > investment_price:
            self.db.insert_classification('fp',self.__rmse,self.__accuracy,self.__decision_pred)

        return self.db.view('classifier')[-1][1]

    def compute_roi(self,investment_price,y_actual,y_pred):
        roi_real = (y_actual-investment_price) / investment_price * 100
        roi_pred = (y_pred-investment_price) / investment_price * 100      
        roi = {
            'roi_real' : round(roi_real,2),
            'roi_pred' : round(roi_pred,2)
        }
        return roi
    
    def compute_decision(self,investment_price,y_actual,y_pred):
        decision_real = 'Profit' if y_actual > investment_price else 'Loss' if y_actual < investment_price else 'No change in Price'
        decision_pred = 'Profit' if y_pred > investment_price else 'Loss' if y_pred < investment_price else 'No change in Price'
        decision = {
            'decision_real': decision_real,
            'decision_pred' : decision_pred
        }
        return decision
