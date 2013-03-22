$(function(){
  var member_no = 0;
  $("#button_add_member").click(function(){
    //clone the div
    $(this).prev().clone().insertBefore(this);

    //replace the new div's data
    member_div = $(this).prev();   
    member_div_content = member_div.html();
    member_div_id= member_div.attr('id');
    member_no_inc = member_no+1;
    //inc the ID
    member_div.attr('id', member_div_id.replace('_'+member_no, '_'+member_no_inc));

    //replace all occurence of the inputs numbers
    member_div.html(increment());
    member_no = member_no_inc;
  
  })
  function increment(){
    do {
          member_div_content = member_div_content.replace('_'+member_no, '_'+member_no_inc);
       } while(member_div_content.indexOf('_'+member_no) !== -1);

    return member_div_content;

  }
});
