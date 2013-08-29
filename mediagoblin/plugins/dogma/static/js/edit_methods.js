/*
 *Here you go with a set of functions to improve the UX when it comes to deletion of data 
 *
 * extarnal variables to put on the jinja template before the script : 
 * var undo = {%trans%}Cancel{%endtrans%}
 * var redo = {%trans%}Delete{%endtrans%}
 * */

// Remove extra perfomers : copy its ID in the hidden field and hide the row


$(function(){
   $(".edit_extra_perf").toggle(function(){
       $(this).html(_confirm)
       role_desc = $(this).siblings(".extra_role_descr");
       role_field = $(this).siblings(".edit_extra_role_field");
       role_field.attr('value', role_desc.html());
       role_field.show();
       role_desc.hide()
   },
   function(){
       $(this).html(edit)
       role_desc = $(this).siblings(".extra_role_descr");
       role_field = $(this).siblings(".edit_extra_role_field");
       role_desc.html(role_field.attr('value'));
       role_desc.show()
       role_field.hide()
   }
                               );
   $(".change_role").click(function(){
    //strike the text
    if($(this).parent('li').hasClass("selected_role")){
      $(this).parent('li').removeClass("selected_role");
      $(this).html(redo);
      $(this).siblings(".change_role_field").removeAttr('value')
    }else{
      $(this).parent('li').addClass("selected_role");
      //get the id and copy it to the hidden field
      keyword_id = $(this).attr('data_kw_id');
      $(this).siblings(".change_role_field").attr('value', keyword_id);
      //change the button to "Undo" (external variable so jinja can translate it)
      redo = $(this).html();
      $(this).html(undo);
    }
   });
   $(".countrySelect").val($(".countrySelect").parent(".form_field_input").attr("data-country"));

})
