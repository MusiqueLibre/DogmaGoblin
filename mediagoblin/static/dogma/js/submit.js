$(function(){
  //hide the file input and create a button to activate it
  $('#multi_browse').click(function(){$('#multi_file_input').click()});


  //return the js object to get the files attribute
  $('#multi_file_input').bind('change', function(){
    //for every file...

    files = $(this).prop('files')
    $('#file_list').html('<ul class="file_attributes"></ul>');
    for (var x = 0; x < files.length; x++) {
      div_content =  $("#track_inputs").html();
      //add to list
      $('.file_attributes').append('<li class="submit_file_list">'+
                                   '<h3>'+files[x].name+'</h3>'+increment(x)+
                                   '</li>'
                                  );

    }
  });

});
function increment(x){
if(x>0){
    do {
          div_content = div_content.replace('_0', '_'+x);
       } while(div_content.indexOf('_0') !== -1);
}
return div_content;
}
