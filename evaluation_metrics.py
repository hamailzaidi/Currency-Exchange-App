class MetricsEvaluator:
    def __init__(self,db) -> None:
        self.__db = db
    
    @property
    def db(self):
        return self.__db
    
