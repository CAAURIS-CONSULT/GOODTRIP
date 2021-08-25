
var data = {};
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }   
    return cookieValue;
};

$('.marque').click(function(){
   var marque = $('#marque').val();
   getModels(marque);
})

function reload_js(src) {
    $('script[src="' + src + '"]').remove();
    $('<script>').attr('src', src).appendTo('body');
};

function getModels(marque)
{
        $.ajax({
                url: 'http://localhost:8000/location/marque',
                method:'GET',
                data: {
                    'marque':marque,
                },
                dataType:'html',
                success:function(response){
                    data.models = JSON.parse(response).models;
                    var html='';
                    data.models.forEach(element => {
                        html += '<li><a class="dropdown-item" href="#"><span class="dropdown-item-label">'+element+'</span></a></li>'
                    });
                    $('#listmodels').html(html);
                    reload_js('/static/users/js/theme.min.js');
                },
                error:function(){
                        alert('nononn');
                        }
            });
};

function getModelsById(id){
    $.ajax({
        url: 'http://localhost:8000/location/marque',
        method:'GET',
        data: {
            'id':id,
        },
        dataType:'html',
        success:function(response){
            data.models = JSON.parse(response).models;
            var html='';
            data.models.forEach(element => {
                html += '<option value="'+ element +'">'+element+'</option>';
            });
            $('#listmodels').html(html);
            reload_js('/static/users/js/theme.min.js');
        },
        error:function(){
                alert('nononn');
            }
    });
}
function commander(user_id, vehicule_id, quantity){
    $.ajax({
        url: 'http://localhost:8000/location/commander',
        method: 'GET',
        data: {
            'vehicule_id':vehicule_id,
            'quantity':quantity,
        },
        dataType:'html',
        success:function(response){
            alert(response);
        },
        error:function(){
            alert('response');
        }
    });
}
