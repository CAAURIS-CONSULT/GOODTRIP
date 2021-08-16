
var data = {};

$('.marque').click(function(){
   var marque = $('#marque').val();
   getModels(marque);
})

// function getModels(marque){
//     $.ajax({
//         url:"http://localhost:8000/location/marque",
//         type:'POST',
//         datatype: 'json',
//         data:{
//             'marque':marque,
//         },
//         success: function(response){
//             alert('ok')
//         },
//     });
// }
//Function Ajout produits
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