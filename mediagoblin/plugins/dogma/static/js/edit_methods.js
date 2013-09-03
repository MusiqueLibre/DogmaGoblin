/*
 *Here you go with a set of functions to improve the UX when it comes to deletion of data 
 *
 * extarnal variables to put on the jinja template before the script : 
 * var undo = {%trans%}Cancel{%endtrans%}
 * var redo = {%trans%}Delete{%endtrans%}
 * */

// Remove extra perfomers : copy its ID in the hidden field and hide the row


$(function(){
   //EDIT roles
   $(".edit_extra_perf").toggle(function(){
       $(this).html(_confirm)
       role_desc = $(this).siblings(".extra_role_descr");
       role_field = $(this).siblings(".edit_extra_role_field");
       $(this).siblings(".rm_extra_role").hide()
       role_field.show();
       role_desc.hide()
   },
   function(){
       $(this).html(edit)
       role_desc = $(this).siblings(".extra_role_descr");
       role_field = $(this).siblings(".edit_extra_role_field");
       role_desc.html(role_field.attr('value'));
       role_field.attr('value', role_desc.html());
       $(this).siblings(".rm_extra_role").show()
       role_desc.show()
       role_field.hide()
   });
   // REMOVE roles
   $(".rm_extra_role").toggle(function(){
     keyword_id = $(this).attr('data_kw_id');
     $(this).html(restore);
     $(this).siblings('.extra_role_descr').wrap('<del>');
     $(this).siblings('.rm_role_field').attr('value', keyword_id );
     $(this).siblings('.edit_extra_perf').hide()
   },
   function(){
     $(this).html(remove);
     $(this).siblings('del').children('.extra_role_descr').unwrap();
     $(this).siblings('.rm_role_field').attr('value', '' );
     $(this).siblings('.edit_extra_perf').show()
   });
   $(".change_role").click(function(){
    //get the id and copy it to the hidden field
    keyword_id = $(this).attr('data_kw_id');
    if($(this).parent('li').hasClass("selected_role")){
      $(this).parent('li').removeClass("selected_role");
      $(this).html(redo);
      $(this).siblings(".rm_role_field").attr('value', keyword_id);
      $(this).siblings(".add_role_field").removeAttr('value')
    }else{
      $(this).parent('li').addClass("selected_role");
      //change the button to "Undo" (external variable so jinja can translate it)
      $(this).siblings(".rm_role_field").removeAttr('value')
      $(this).siblings(".add_role_field").attr('value', keyword_id);
      redo = $(this).html();
      $(this).html(undo);
    }
   });
   $(".countrySelect").val($(".countrySelect").parent(".form_field_input").attr("data-country"));

   //ADD extra perf
   $(".add_extra_perf").click(function(){
       $(this).siblings('.add_extra_role_field').show();
       $(this).siblings('.cancel_extra_perf').show();
       $(this).siblings('.form_field_description').show();
       $(this).hide();

    });
    $(".cancel_extra_perf").click(function(){
      $(this).siblings('.add_extra_role_field').hide();
      $(this).siblings('.form_field_description').hide();
      $(this).siblings('.add_extra_role_field').attr('value', '');
      $(this).siblings('.extra_role_descr').html('');
      $(this).hide();
      $(this).siblings('.add_extra_perf').show();
       $(this).siblings('.form_field_description').hide();
    });
})
