
//FUNCIONES PARA ACTIVAR LOS SPINNERS (LOADERS)
$('#spinner').addClass('d-none');
// Funciones para cargar Spinner
function cargando_mostrar(){
    $('#spinner').removeClass('d-none');
}

function cargando_ocultar(){
    $('#spinner').addClass('d-none');
}
//FUNCIONES PARA ACTIVAR LOS SPINNERS (LOADERS)

// DOCUMENT READY !!
$(document).ready( function () {
    // Proceso para generar botones de busqueda por columna y su funcionamiento
    $('#table_id thead tr').clone(true).appendTo( '#table_id thead' );
    $('#table_id thead tr:eq(1) th').each( function (i) {
          var title = $(this).text();
          if(title != ""){
            $(this).html( '<input type="text" placeholder="Buscar '+title+'" />' );
          }

          $( 'input', this ).on( 'keyup change', function () {
              if ( table.column(i).search() !== this.value ) {
                  table
                      .column(i)
                      .search( this.value )
                      .draw();
              }
          } );
      } );

      /* Se configura la tabla para mostrar botones de reportes
      adicional se agrega el arreglo de lenguaje para cambiar los textos
      */
      var table = $('#table_id').DataTable( {
        orderCellsTop: true,
        fixedHeader: true,
        dom: 'Bfrtip',
        buttons: [
            'copy', 'csv', 'excel', 'pdf', 'print'
        ],
        "language": {
          "decimal":        "",
          "emptyTable":     "No hay datos en la tabla",
          "info":           "Mostrando START a END de TOTAL registros",
          "infoEmpty":      "Mostrando 0 a 0 d 0 Registros",
          "infoFiltered":   "(Filtrando de MAX registros totales)",
          "infoPostFix":    "",
          "thousands":      ",",
          "lengthMenu":     "Mostrar MENU registros",
          "loadingRecords": "Cargando...",
          "processing":     "Procesando...",
          "search":         "Buscar:",
          "zeroRecords":    "No se encontraron registros",
          "paginate": {
              "first":      "Primero",
              "last":       "Ultimo",
              "next":       "Siguiente",
              "previous":   "Anterior"
          },
          "aria": {
              "sortAscending":  ": activate to sort column ascending",
              "sortDescending": ": activate to sort column descending"
          }
        }
      });

      //funciones_adicionales();

} );

function editar_registro(id,origen,appname){
    console.log(id+" : "+appname);
    modalEditar(id,origen,appname);
}

function eliminar_registro(id){
    $('#idEliminar').val(id);
    $('#eliminarOrigen').val("Vacio");
    $('#modal_eliminar').modal('show');
}

// Obtener informacion par ael modal Editar
function modalEditar(id,origen,appname){
    cargando_mostrar();
    $.ajax({
        url : "/modaleditar/", // the endpoint
        type : "POST", // http method
        data : { id : id, origen: origen, appname: appname, csrfmiddlewaretoken: window.CSRF_TOKEN }, // data sent with the post request

        // handle a successful response
        success : function(json) {          
            if(json.valido){
            
                $('#idEditar').val(id);
                if(origen != ""){
                    modal_edicion(json);
                }
                $('#modal_editar').modal('show');
            }
            else{
                alert(json.mensaje);
            }
            cargando_ocultar();
        },

        // handle a non-successful response
        error : function(xhr,errmsg,err) {
            alert("Error: " + err);
            cargando_ocultar();
        }
    });
}

function modal_edicion(json){
    for (var prop in json) {
        if(prop != 'valido'){
            //console.log(json[prop])
            $('#'+prop).val(json[prop]);
        }
    }
    // $("#tipoinmueble_editar option[value='"+json.idtipoinmueble+"']").attr("selected", true);
}


function funciones_adicionales(){
    // // Proceso para activar boton de eliminar registro y modal
    // $('.boton-eliminar').each((i, elm) => {
    //     $(elm).click(function(){
    //         $('#idEliminar').val($(this).data('id'));
    //         $('#eliminarOrigen').val($(this).data('origen'));
    //         $('#modal_eliminar').modal('show');
    //     });
    // })
    
    // // Funcion para activar boton de editar registro y modal
    // $('.boton-editar').each((i, elm) => {
    //     $(elm).click(function(){
    //         modalEditar($(this).data('id'),$(this).data('origen'),$(this).data('appname'));
    //     });
    // })

    
}