from flask import Flask, render_template, request, jsonify
from scrapper import Scrapper
from graphs import Graph
from database import Database
import threading, time
from datetime import datetime
from data_synthesis import DataSynthesizer
from learning_models import LinearRegression
from model_evaluation import ModelEvaluator
from range_evaluation import RangeEvaluator


#--------------------------------------------------------------------------------------------------------------
# ------------------------------------------ Classes Instantiation --------------------------------------------
#--------------------------------------------------------------------------------------------------------------
scrap = Scrapper()
graph = Graph(scrap.history_table)
db = Database('database.db')
data_syn  = DataSynthesizer(scrap.scrapped_data)
model1 = LinearRegression()
model1.load_model('Trained_model.csv')

# model = LinearRegression()
# x_train, y_train = data_syn.create_trainingSet('2022-06-30')
# model.fit(x_train,y_train)
# model.save_model('Trained3_model.csv')

#-----------------------------------------------------------------------------------------------------------------
# ---------------------------------------------  App config ------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------
app = Flask(__name__)

#-----------------------------------------------------------------------------------------------------------------
#------------------------------------------------Home route-------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------

@app.route('/',methods = ['GET','POST'])
def home():
    time_list = [row[1][12:17] for row in reversed(db.view("data"))]
    usd_val_list = [round(row[2],2) for row in reversed(db.view("data"))]
    wAvg = [round(avg,2) for avg in graph.weekly_avg[1][-2:]]
    mAvg = [round(avg,2) for avg in graph.monthly_avg[1][-2:]]
    
    if request.is_json:
        if request.args.get('btn_id') == '1':
            try:
                usd_val = request.args.get('usd_val')
                pkr_val = round(float(usd_val) * db.view("data")[0][2],2) 
            except: 
                pkr_val = ''
            return jsonify({'pkr_val': pkr_val})
        elif request.args.get('btn_id') == '2':
            try:
                pkr_val = request.args.get('pkr_val')
                usd_val = round(float(pkr_val) / db.view("data")[0][2],2)
            except: 
                usd_val = ''
            return jsonify({
                'usd_val': usd_val
            })

    return render_template('home.html',x=time_list,y=usd_val_list,weekAvg=wAvg, monthAvg=mAvg)

#-----------------------------------------------------------------------------------------------------------------
# ------------------------------------------ Hitory table route --------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------   
@app.route('/history-table')
def history_table(): 
    return render_template('history_table.html',history=scrap.history_table)

#-----------------------------------------------------------------------------------------------------------------
#-----------------------------------------------Chart routes------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------

@app.route('/daily-chart')
def daily_chart():
    chart_title = 'Daily USD to PKR exchange rate'
    return render_template('charts.html',x=graph.daily_data[0],y=graph.daily_data[1],text=chart_title)

@app.route('/weekly-chart')
def weekly_chart():
    chart_title = 'Weekly average of USD to PKR exchange rate'
    return render_template('charts.html',x=graph.weekly_avg[0],y=graph.weekly_avg[1],text=chart_title)

@app.route('/monthly-chart')
def monthly_chart():
    chart_title = 'Monthly average of USD to PKR exchange rate'
    return render_template('charts.html',x=graph.monthly_avg[0],y=graph.monthly_avg[1],text=chart_title)

#-----------------------------------------------------------------------------------------------------------------
# --------------------------------------- USD rate forecasting route ---------------------------------------------
#-----------------------------------------------------------------------------------------------------------------

@app.route('/forecasting',methods = ['GET','POST'])
def forecasting():

    if request.is_json:
        try:
            start_date = request.args.get('start_date')
            end_date = request.args.get('end_date')
            total_investment = float(request.args.get('total_investment'))
            
            x_test,y_test,dates = data_syn.create_testSet(start_date,end_date)
            yhat_test = model1.predict(x_test)
            #numpyarray of shape (-1,1) y[0] corresponsds to the first value (.value)
            pred_table = [[date,y[0],yhat] for date,y,yhat in zip(dates[1:],y_test,yhat_test)]   
            investment_price = x_test[0][0]
            
            range_evaluator = RangeEvaluator(db,y_test,yhat_test,investment_price,total_investment)
            range_metrics = range_evaluator.dict
            pred_class = db.view('classifier')[-1]
            print(db.view('classifier'))
            return jsonify({
                'id': pred_class[0],
                'profit_loss':pred_class[4],
                'table': pred_table,
                'invest_date':  dates[0],
                'invest_price': investment_price,
                'range_metrics':range_metrics
            })
        except:
            render_template('forecasting.html')

    db.clear_table('classifier')   
    return render_template('forecasting.html')

#-----------------------------------------------------------------------------------------------------------------
#-------------------------------------------------EvaluationMetric------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------

@app.route('/evaluation_metric')
def evaluate_model():

    classification_rows = db.view('classifier')
    classifications = [item[1] for item in classification_rows]
    rmse_list = [item[2] for item in classification_rows]
    accuracy_list = [item[3] for item in classification_rows]

    metrics = ModelEvaluator(db,classifications,rmse_list,accuracy_list)
    model_metrics = metrics.dict
    return model_metrics

#-----------------------------------------------------------------------------------------------------------------
#-------------------------------------------------Reset Forecasting-----------------------------------------------
#-----------------------------------------------------------------------------------------------------------------
@app.route('/reset_forecasting')
def reset_table():
    db.clear_table('classifier')
    return ''

#-----------------------------------------------------------------------------------------------------------------
#---------------------------------Second thread for live usd price scrapping and storing in db--------------------
#-----------------------------------------------------------------------------------------------------------------
def tick_data():
    while True:
        date = datetime.now().replace(microsecond=0).strftime('%d-%m-%Y (%H:%M)')
        # date = datetime.now().replace(microsecond=0).strftime('%H:%M')
        try:   
            db.insert_tick(date,scrap.usd_price_now())  
        except:
            pass
        print(db.view("data")[0])
        time.sleep(60)

#-----------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------App Run-----------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------

if __name__ == '__main__':
    thread2 = threading.Thread(target=tick_data)
    thread2.start()
    app.run(debug=False)