
function getModels(maque){
    $.ajax({
        url:'marque',
        type:'POST',
        datatype: 'json',
        data:{
            ''
        },
        success: function(response){
            if (JSON.parse(response).status) {
                connected = false;
                newData = null;
            }else{
                newData = JSON.parse(response);
            }
        },
    });
}