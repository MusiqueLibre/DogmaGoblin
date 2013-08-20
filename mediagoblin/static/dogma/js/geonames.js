//You need to set those variables inside a jinja template BEFORE this script
//so they can be translated :
//
//  var text_not_precise_enough = "{% trans %} The postal code is incorrect, or not precise enough (e.g : you can try 75007 instead of 75000) <a id='searchPlace'>Reload</a> {% endtrans %}"
//  var text_no_country = "{% trans %}You need to select a country first !{% endtrans %}"
//  var text_no_result = "{%trans%}Your query returned no results. Check spelling or try a bigger city{%endtrans%}"
//  var text_select_city = "{%trans%}Please select the correct city bellow{%endtrans%}"

// A simple way to check something is actually typed
//
var city_length = 0;

$(".city_search").focus().keypress(function(key){
     keycode = key.keyCode || key.which;
     //intercept ENTER keypress to prevent form misfire and use it to search the city instead
     if(keycode == 13){
         key.preventDefault();
         $(this).blur();
         return false;
     }
});
$(function(){
  $(".city_search").blur(function(){
     //create an empty list for the suggestion list
     list = "";
     counter = $(this).attr('data-counter');
     country_code = $('#country'+counter).attr('value');
     city = $(this).val();
     thisField = $(this);

     //check the country is selected
     if(country_code == "_None"){
         $("#SuggestBoxElement"+counter).html('<mark class="form_hint">'+text_no_country+'</mark>');
         return
     }



     $.getJSON(
       'http://api.geonames.org/searchJSON?q='+city+'&country='+country_code+'&style=FULL&maxRows=10&fuzzy=0.8&username=dogmazic')
         .done(function(data){
           //iterate through the results
           geonames = data.geonames;
           if(geonames.length == 0){
             $("#SuggestBoxElement"+counter)
                     .html('<mark class="form_hint">'+text_no_result+'</mark>');
           }

           $.each( geonames, function(i,item){
             list += '<li class="suggestion">'+item.name+', '+item.adminName3+', '+item.adminName2+'</li>';
             $("#SuggestBoxElement"+counter).html('<mark class="form_hint">'+text_select_city+'</mark><ul>'+ list+'</ul>');
           });
            // Fill the data with the selected item
            $('.suggestion').click(function(){
               currentChoice = $(this);
               index = $('.suggestion').index(currentChoice);
               fillFields(counter, geonames[index].name,geonames[index].lat,geonames[index].lng);
               thisField.val(geonames[index].name+', '+geonames[index].adminName3+', '+geonames[index].adminName2);
               $("#SuggestBoxElement"+counter).html('');
            });
         });
    });
    i = 0;
    while($("#internationnal_"+i).length > 0){
      $("#internationnal_"+i).click(function(){
        if($(this).attr("checked") == "checked"){
          $(".place_0").val("int_band");
          $(".city_search_0").val("Internationnal band");
          $(".city_search_0").attr("disabled", "disabled");
          //prevent messages for internationnal bands
          $("#SuggestBoxElement"+counter).html('');
        }else{
          $(".place_0").val("");
          $(".city_search_0").val("");
          $(".city_search_0").removeAttr("disabled");
        }
      });
      i++;
    }
});
function fillFields(counter,place,lat,lng){
    $('.place'+counter).attr('value', place);
    $('.latitude'+counter).attr('value', lat);
    $('.longitude'+counter).attr('value', lng);
}
