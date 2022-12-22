from evaluation_metrics import MetricsEvaluator
from collections import Counter

class ModelEvaluator(MetricsEvaluator):
    
    def __init__(self,db, classes, rmse_list,accuracy_list) -> None:
        super().__init__(db)
        self.__counter = Counter(elem for elem in classes)        
        self.__total_pred = len(classes)
        self.__prec = self.compute_precision(self.counter['tp'],self.counter['fp'])
        self.__rec = self.compute_recall(self.counter['tp'],self.counter['fn'])
        self.__accuracy = self.compute_average(accuracy_list)
        self.__rmse = self.compute_average(rmse_list)
        self.__f1_score = self.compute_f1_score(self.prec,self.rec)

        self.__dict = {
            'total_pred':self.__total_pred,
            'prec': self.__prec,
            'rec': self.__rec,
            'f1_score': self.__f1_score,
            'accuracy': self.__accuracy,
            'rmse': self.__rmse
        }

    @property
    def counter(self):
        return self.__counter
    @property
    def dict(self):
        return self.__dict

    @property
    def total_pred(self):
        return self.__total_pred


    @property
    def prec(self):
        return self.__prec
    @property
    def rec(self):
        return self.__rec
    @property
    def f1_score(self):
        return self.__f1_score
    @property
    def accuracy(self):
        return self.__accuracy
    
    def compute_precision(self,tp,fp):
        try:
            prec = round(tp/(tp+fp),3)
        except ZeroDivisionError:
            prec = 0
        return prec

    def compute_recall(self,tp,fn):
        try:
            rec = round(tp/(tp+fn),3)
        except ZeroDivisionError:
            rec = 0
        return rec
    
    def compute_f1_score(self,prec,rec):
        try:
            f1_score = round(2*prec*rec / (prec+rec),3)
        except ZeroDivisionError:
            f1_score = 0
        return f1_score
    
    def compute_average(self,list):
        avg = sum(list)/len(list)
        return round(avg,2)

