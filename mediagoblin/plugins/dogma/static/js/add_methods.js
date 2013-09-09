//You need to set those variables inside a jinja template BEFORE this script
//so they can be translated :
//
//  var text_not_precise_enough = "{% trans %} The postal code is incorrect, or not precise enough (e.g : you can try 75007 instead of 75000) <a id='searchPlace'>Reload</a> {% endtrans %}"
//  var text_no_country = "{% trans %}You need to select a country first !{% endtrans %}"
//  var text_no_result = "{%trans%}Your query returned no results. Check spelling or try a bigger city{%endtrans%}"
//  var text_select_city = "{%trans%}Please select the correct city bellow{%endtrans%}"
//  var text_not_proper_file = "{%trans%}You can only upload audiofiles here. This file will be skipped :{%endtrans%}"
//  var text_you_selected = "{%trans%}You've selected{%endtrans%}"
//  var text_coordinates = "{%trans%}Coordinates{%endtrans%}"
var thisCalendar = new Array();
var postalcodes;
//starts with "1", cause the member 0 is already displayed
var member_no = 0;

//###################################################
//### A SET OF METHODS TO IMPROVE SUBMIT FORMS UI ###
//###################################################
//
//### POSTAL CODE ET LOCATION LOOKUP ###
//
//You need to set those variables inside a jinja template BEFORE this script
//so they can be translated :
//
//  var text_preview = "{% trans %}Preview{% endtrans %}"

$(function(){
  // Fire up some functions (it's not directly there, cause I got to
  // fire them up later after DOM modifications
  setDatePicker();
  citySearch()
  copyBandDate();
  copyBandLocation();
  jpegCheck();
  //"add member" setup as default
  addMember('_', true)
  //add the markdown wysiwyg if there's the proper textarea input
  if($('#wmd-input_0').length > 0){
   $('#wmd-input_0').wrap('<div id="wmd-panel_0"></div>')
   $('#wmd-input_0').before('<div id="wmd-button-bar_0" class="wmd-button-bar"></div>')
   $('#wmd-input_0').after('<h3>'+text_preview+'</h3></p><div id="wmd-preview_0"></div>')
   converter = new Markdown.Converter();
   editor = new Markdown.Editor(converter, '_0');
   editor.run();
  }
});


//#############################################################
// GENERIC FORM UI IMPROVEMENTS 
//#############################################################

function jpegCheck(){
  $('input[type=file]').change(function(){
    if($(this).attr('name').indexOf('picture') != -1){
      var extension = $(this).val().split('.').pop();
      if (['jpg', 'jpeg', 'JPEG', 'JPG'].indexOf(extension) == -1) {
        $(this).attr('value','');
        $(this).siblings('p').wrapInner('<mark class="form_hint" >')
      }
   }
 });
}



//#############################################################
// CITY SEARCH 
//#############################################################
// ______________________

// A simple way to check something is actually typed
//
var city_length = 0;
var stoppedTyping = null;

function citySearch(){
  $(".city_search").click(function(){
    $(this).attr('value','');
  });
  $(".city_search").keyup(function(){
     if (stoppedTyping){
       clearTimeout(stoppedTyping); 
     }
     //create an empty list for the suggestion list
     list = "";
     counter = $(this).attr('data-counter');
     country_code = $('#country'+counter).val();
     city = $(this).val();
     var thisField = $(this);
     //check the country is selected
     if(country_code == "_None"){
         $("#SuggestBoxElement"+counter).html('<mark class="form_hint">'+text_no_country+'</mark>');
         return;
     }
     stoppedTyping = setTimeout(function(){
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
                 var index = $('.suggestion').index(currentChoice);
                 fillFields(counter, geonames[index].name,geonames[index].lat,geonames[index].lng);
                 thisField.attr('value',geonames[index].name);

                 //Add a div with all the data of the city selected by the user
                 location_data = '<div id="selected_city'+counter+'">'+text_you_selected+' : '+geonames[index].name+', '+
                     geonames[index].adminName3+', '+geonames[index].adminName2+' - '+text_coordinates+
                     ' ('+geonames[index].lat+', '+geonames[index].lng+' )</div>';
                 if( $('#selected_city'+counter).html() == null){
                   thisField.after(location_data);
                 }else{
                  $('#selected_city'+counter).html(location_data);
                 }
                 $("#SuggestBoxElement"+counter).html('');
              });
           });
      },1000);
    });

    //Loop #internationnal_n inputs and fill the city + country inputs
    i = 0;
    while($("#internationnal_"+i).length > 0){
      $("#internationnal_"+i).click(function(){
        if($(this).attr("checked") == "checked"){
          $(".place_0").attr('value',"int_band");
          $(".city_search_0").attr('value',"Internationnal band");
          $(".city_search_0").attr("disabled", "disabled");
          //prevent messages for internationnal bands
          $("#SuggestBoxElement"+counter).html('');
        }else{
          $(".place_0").attr('value',"");
          $(".city_search_0").attr('value',"");
          $(".city_search_0").removeAttr("disabled");
        }
      });
      i++;
    }
};
function fillFields(counter,place,lat,lng){
    $('#location'+counter).children('input').attr('value', place);
    $('#Location-latitude'+counter).attr('value', lat);
    $('#Location-longitude'+counter).attr('value', lng);
}

// SHORTCUT TO COPY ALL LOCATION DATA FROM THE BAND
function copyBandLocation(){

    $(".copy_band_location").click(function(){
      counter = $(this).siblings('input').attr('data-counter');
      fillFields(counter, $('#band_place').html(),$('#band_latitude').html(), $('#band_longitude').html());
      $('#country'+counter).val($('#band_country').html());
    });
    $(".copy_band_country").click(function(){
    });
}
//#############################################################
// CALENDAR 
//#############################################################
// ______________________
//|                      |
//|     Date picker      |
//|______________________|
var cal_clicked = false;
function setDatePicker(){
    //For the dynamic member form, you need to target unprocessed calendars with a custom class
    //in order to prevent duplicates or fails
    $(".datePicker").each(function(index){
        calendar_count = $(".datePicker").length;
        //skip every calendar but the last two, else you have duplicates (gotta change this number if you
        //change the number of calendars)
        if(index - calendar_count < -2){
            return;
        }
        //prevent the calendar from seting a value at onload
        $(".datePicker").click(function(){cal_clicked = true});
        //use the millis as date if applicable
        existing_date_millis = $(this).attr('data-millis');
        if (existing_date_millis != ''){
            existing_date = new Date(parseInt(existing_date_millis));
        }else{
            existing_date = false;
        }

        //create an instance of calendar for each present in the page
        thisCalendar[index] = $(this);
        $(this).calendarPicker({
          monthNames:["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"],
          dayNames: ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"],
          useWheel:true,
          showDayArrows:true,
          date: existing_date,
          callback:function(cal){
              if(cal_clicked){
                calendarCallBack(thisCalendar[index], cal);
              }
              //if it is the album calendar, add the function to hide members who weren't in the band at the time of the 
              //release
              if(thisCalendar[index].is(".album_release")){
                album_millis = thisCalendar[index].find('.selected').attr('millis')
                $(".album_member").each(function(){
                  millis_until = $(this).attr("data-until");
                  if(!millis_until){
                    millis_until  = album_millis;
                  }

                  if($(this).attr("data-since") > album_millis || millis_until < album_millis){
                    $(this).children("input").attr("disabled", "disabled")
                  }else{
                    $(this).children("input").removeAttr("disabled");
                  }
                });
              }
          }
        });
  });
}
//_______________________
//|                      |
//|  Date picker UI      |
//|______________________|
function copyBandDate(){
  $(".copy_band_date").click(function(){
      date = new Date(parseInt($("#band_millis").html()));
      $(this).siblings("div").remove();
      thisCalendar = $(this).parent(".datePicker");
      thisCalendar.calendarPicker({
              showDayArrows:true,
              date:date,
              callback:function(cal){
                calendarCallBack(thisCalendar, cal)}
          })
      });
}
function calendarCallBack(thisCalendar, cal){
  thisCalendar.children(".date_picker_input").attr('value',
  cal.currentDate.getFullYear()+'-'+(cal.currentDate.getMonth()+1)
  +'-'+cal.currentDate.getDate());
}

//#############################################################
// ADD INPUTS
//#############################################################
//
// ___________________________
//|                           |
//|  Add a member/role input  |
//|___________________________|
//
function addMember(pattern, member_page){
  $(".button_add_member").click(function(){
    //clone the div
    new_member = $(this).prev().clone()
    //remove datepicker divs to avoid duplicate
    $(new_member).find(".datePicker").children("div").remove();
    //remove markdown toolbar to avoid duplicates (generated afterward)
    $(new_member).find(".wmd-button-row").remove();
    //insert the clone before teh [+] button
    $(new_member).insertBefore(this);

    //replace the new div's data
    member_div = $(this).prev();
    div_content = member_div.html();

    //replace all occurence of the inputs numbers
    member_div.html(increment(member_no, pattern, true));
    member_no++;

    if(member_page){
      //Relunch functions so they are aware of those new doms elements
      //set up a calendar
      setDatePicker();
      citySearch();
      copyBandDate();
      copyBandLocation();
      jpegCheck();
      editor[member_no] = new Markdown.Editor(converter, pattern+member_no);
      editor[member_no].run();
    }
  })
}

// ___________________________
//|                           |
//| Increment a given pattern |
//|___________________________|
//
  function increment(){
    do {
         member_div_content = member_div_content.replace(pattern+member_no, pattern+member_no_inc);
       } while(member_div_content.indexOf(pattern+member_no) !== -1);

    return member_div_content;

  }

//#############################################################
// Multiple File Input
//#############################################################
// This copies the standard track's form, one per file in the file[] input and increment their names accordingly
$(function(){
  //hide the file input and create a button to activate it
  $('#multi_browse').click(function(){$('#multi_file_input').click()});


  //return the js object to get the files attribute
  $('#multi_file_input').bind('change', function(){
    //for every file...
    files = $(this).prop('files')
    $('#file_list').html('<ul class="file_attributes"></ul>');
    for (var x = 0; x < files.length; x++) {
      var extension = files[x].name.split('.').pop();
      if (['mp3', 'ogg', 'flac', 'MP3', 'OGG', 'FLAC'].indexOf(extension) > -1) {
        div_content =  $("#track_inputs").html();
        //add to list
        $('.file_attributes').append('<li class="submit_file_list">'+
                                     '<h3>'+files[x].name+'</h3>'+increment(x, '_')+
                                     '</li>'
                                    );
     }else{
       $('.file_attributes').append('<li><mark class="form_hint">'+text_not_proper_file+files[x].name+'</mark></li>');
     }

    }
    //fire the addMember function for the additionnal performers
    addMember('No',false)
    //reinitialize details
    $('details').details();
  });

  // ___________________________
  //|                           |
  //| Multiup files progression |
  //|___________________________|
  //
  var progress_bar = $('#upload_progress');
   $('#multi_file_input').parents('form').ajaxForm({
      clearForm: true,
      beforeSend: function() {
         progress_bar.attr('value',0);
      },
      uploadProgress: function(event, position, total, percentComplete) {
          var percentVal = percentComplete;
          if(percentComplete > 99){
            percentVal= "NaN";
          }
          progress_bar.attr('value',percentVal);
      },
      success: function() {
          progress_bar.attr('value',0);
          $('#file_list').empty();
          $('#upload_status').html("files uploaded ! You can add some more");
      },
  }); 
});
//#############################################################
// GENERAL FUNCTIONS
//#############################################################
//
//Increment every number that fallows a certain pattern in a string
function increment(x, pattern, from_latest){
    if(from_latest){
      prev=x;
      x++;
    }
    else
      prev=0
    if(x>0){
      do {
            div_content = div_content.replace(pattern+prev, pattern+(x));
         } while(div_content.indexOf(pattern+prev) !== -1);
    }
  return div_content;
}
