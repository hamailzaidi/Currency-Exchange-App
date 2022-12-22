$(document).ready(function(){
    pInput = document.getElementById('pInput')
    uInput = document.getElementById('uInput')
    // sends the button id (clicked/active input field) to the backend, usd2pkr or pkr2usd calculation will be done on its basis.

    $('#pInput').on('input',function(){
        $.ajax({
            url:'',
            type: 'get',
            contentType: 'application/json',
            data: {
                btn_id: 2,
                pkr_val: pInput.value
            },
            success: function(response){
                uInput.value = response.usd_val
            } 
        })
    });

    $('#uInput').on('input',function(){
        $.ajax({
            url:'',
            type: 'get',
            contentType: 'application/json',
            data: {
                btn_id: 1,
                usd_val: uInput.value
            },
            success: function(response){
                pInput.value = response.pkr_val
            } 
        })
    });


})