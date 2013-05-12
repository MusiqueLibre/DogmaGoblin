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
       perf_field = $(this).siblings(".edit_extra_perf_field");
       role_field = $(this).siblings(".edit_extra_role_field");
       descr_span = $(this).siblings(".extras_descr");
       perf_field.attr('value', descr_span.children(".extra_perf_descr").html());
       role_field.attr('value', descr_span.children(".extra_role_descr").html());
       descr_span.hide();
       perf_field.show();
       role_field.show();
   },
   function(){
       perf_field = $(this).siblings(".edit_extra_perf_field");
       role_field = $(this).siblings(".edit_extra_role_field");
       descr_span = $(this).siblings(".extras_descr");
       descr_span.show();
       perf_field.hide();
       role_field.hide();
       descr_span.children(".extra_perf_descr").html(perf_field.attr('value'));
       descr_span.children(".extra_role_descr").html(role_field.attr('value'));
   }
                               );
   $(".rm_extra_perf").toggle(function(){
    //strike the text
    $(this).siblings(".extras_descr").wrap("<del>");
    //change the button to "Undo" (external variable so jinja can translate it)
    $(this).html(undo);
    //get the id and copy it to the hidden field
    console.debug($(this).siblings(".extra_perf_descr"))
    keyword_id = $(this).attr('data_kw_id');
    $(this).siblings(".rm_extra_perf_field").attr('value', keyword_id);
   },
   function(){
     $(this).siblings("del").children(".extras_descr").unwrap();;
     $(this).html(redo);
     $(this).siblings(".rm_extra_perf_field").removeAttr('value')
   });

})
