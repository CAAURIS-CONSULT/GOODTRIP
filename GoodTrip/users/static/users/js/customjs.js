
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

function commander(vehicule_id, quantity){
    Swal.fire({
        title: 'Voulez-vous commander ce véhicule?',
        text: "Vous pourrez voir vos commandes dans votre historique!",
        icon: 'warning',
        showCancelButton: 'true',
        confirmButtonColor: '#26708b',
        cancelButtonColor: '#d33',
        confirmButtonText: 'Oui, commander!',
        cancelButtonText: 'Annuler',
        cancelButtonColor: '#f2ac2a',
      }).then((result) => {
        if (result.isConfirmed) {
            $.ajax({
                url: 'http://localhost:8000/location/commander',
                method: 'GET',
                data: {
                    'vehicule_id':vehicule_id,
                    'quantity':quantity,
                },
                dataType:'html',
                success:function(response){
                    Swal.fire({
                        title:'Effectuée!',
                        text:'Votre commande a été validée',
                        icon: 'success',
                        footer:'<a class="link text-success" href="#">Aller à mon historique <i class="fi fi-chevrons-right"><i/> </a>'
                    })
                },
                error:function(response){
                    Swal.fire({
                        title: 'Error!',
                        text: response,
                        icon: 'error',
                        confirmButtonText: 'Cool'
                    });
                }
            });
        }
    })
}