
function getModels(marque){
    $.ajax({
        url:"{% url 'marque' %}",
        type:'POST',
        datatype: 'json',
        data:{
            'marque':marque,
        },
        success: function(response){
            alert('ok')
        },
    });
}