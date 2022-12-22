const start_date = document.getElementById('start_date')
const end_date = document.getElementById('end_date')
const investment = document.getElementById('investment')
var date = new Date()
var max_date = String(date.getFullYear())+'-'+String(date.getMonth()+1)+'-'+String(date.getDate()-1)


$(document).ready(function(){

    function date_setter(){
        start_date.value = ''
        end_date.value = ''
        start_date.min = "2022-07-01"
        end_date.min = "2022-07-01"
        start_date.max = max_date
        end_date.max = max_date
    }
    date_setter()

    
    $('#end_date').click(function(){
        if(start_date.value == ''){
            end_date.min = '2022-07-02'
        }
        else{
            end_date.min = start_date.value
        }
        

    })
    $('#end_date').change(function(){
        start_date.max = end_date.value

    })

     //------------------------------ Analyise a single date range-------------------------
     $('#analyze_button').click(function(){
        
        if(start_date.value != '' && end_date.value != '' && investment.value != ''){
            $.ajax({
                url:'/forecasting',
                type: 'get',
                contentType: 'application/json',
                data: {
                    start_date: start_date.value,
                    end_date: end_date.value,
                    total_investment: investment.value
                },
                success: function(response){

                    res = response.table;
                    id = response.id;
                    metrics = response.range_metrics;
    
                    if (typeof(res)!='undefined'){
    
                        var htmlTableList = 
                        '<div class="accordion-item">'+
                        '<h2 class="accordion-header">'+
                          '<button class="accordion-button collapsed" type="button" data-bs-toggle="collapse" data-bs-target="#table'+id+'"'+ 'aria-expanded="false" aria-controls="table+id">'+
                        '<strong>'+response.invest_date + ' -- ' + res[res.length-1][0]+ '</strong>'+
                       '</button>'+
                        '</h2><div id="table'+id+'" class="accordion-collapse collapse" >'+
                        '<div class="accordion-body" style="background:#E6E5A3;border-color:#E6E5A3 ;">'+
                          '<table class="table table-sm table-bordered table-hover" style="border: 1px solid black;">'+
                            '<tbody>'+
                                '<tr><td><strong>Total Investment</strong></td><td>'+investment.value+' PKR</td></tr>'+
                                '<tr><td><strong>Buying Price</strong></td><td>'+metrics.investment_price+' PKR</td></tr>'+
                                '<tr><td><strong>Predicted Decision</strong></td><td>'+metrics.decision_pred+'</td></tr>'+
                                '<tr><td><strong>Real Decision</strong></td><td>'+metrics.decision_real+'</td></tr>'+
                                '<tr><td><strong>Predicted ROI</strong></td><td>'+metrics.roi_pred+'%</td></tr>'+
                                '<tr><td><strong>Actual ROI</strong></td><td>'+metrics.roi_real+'%</td></tr>'+
                                '<tr><td><strong>Accuracy</strong></td><td>'+metrics.accuracy+'%</td></tr>'+
                                '<tr><td><strong>RMSE</strong></td><td>'+metrics.rmse+'</td></tr>'+
                            '</tbody>'+'</table>'+
                            '<div style="text-align:center;margin-bottom:1vh"><strong> You will get an estimated '+response.profit_loss+' of '+metrics.roi_pkr+' PKR.</strong></div>'+
                          '<table class="table table-sm table-bordered table-hover" style="border: 1px solid black;">'+
                                '<thead><tr style="height: 10px;">'+
                                    '<th>Date</th>'+
                                    '<th>Actual USD Price</th>'+
                                    '<th>Predicted USD Price</th>'+
                                    '</tr></thead>'+
                                    '<tbody id= "tableBody'+id+'">'+
                                    '</tbody>'+
                                    '</table>'+
                                '</div>'+
                            '</div>'+
                        '</div>'
    
                        $('#rangeList').append(htmlTableList)
                        for (let i =0; i<res.length;i++){
                            var htmlTableData = '<tr>' 
                            htmlTableData += '<td>' + res[i][0] + '</td>' 
                            htmlTableData += '<td>' + res[i][1] + '</td>'  
                            htmlTableData += '<td>' + res[i][2] + '</td>' 
                            htmlTableData += '</tr>'
                            $('#tableBody'+id).append(htmlTableData)
                        }
                    }
                    date_setter()
                    investment.value = '' 
                },
                error: function(err){
                    console.log(err)
                }
            })
        }
        else {
            alert('Please enter correct inputs.')
        }
    })

    // ########################## RESET BUTTON ##################################
    $('#reset_button').click(function(){
        $('#rangeList').empty()
        $('#evaluation_div').empty()
        date_setter()
        $.ajax({
            url:'/reset_forecasting',
            type: 'get',
            contentType: 'application/json',
            })

    })

    // ########################## METRICS EVALUATE ##################################

    $('#evaluate_pred').click(function(){
        $.get('/evaluation_metric', function(response) {
            var metrics_table = `
            <table class="table table-sm table-bordered table-hover" style="border: 1px solid black;">`+
            '<thead><tr>'+
                    '<th colspan="2">Model Evaluation Metrics </th>'+
                '</tr></thead>'+
            '<tbody>'+
                            '<tr><td><strong>No. of Predictions</strong></td><td>'+response.total_pred+'</td></tr>'+
                            '<tr><td><strong>Precision</strong></td><td>'+response.prec+'</td></tr>'+
                            '<tr><td><strong>Recall</strong></td><td>'+response.rec+'</td></tr>'+
                            '<tr><td><strong>F1 Score</strong></td><td>'+response.f1_score+'</td></tr>'+
                            '<tr><td><strong>RMSE</strong></td><td>'+response.rmse+'</td></tr>'+
                            '<tr><td><strong>Accuracy</strong></td><td>'+response.accuracy+'%</td></tr>'+

                        '</tbody>'+'</table>'
            $('#evaluation_div').html(metrics_table)
          });
        
    })
})