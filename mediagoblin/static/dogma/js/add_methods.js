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
//  var info_several_choices = "{% trans %}There\'s several cities for this postal code, click to select : {%endtrans %}"
//  var info_loading = "{% trans %}loading ...{% endtrans %}"
//  var error_not_precise_enough = "{% trans %} The postal code is incorrect, or not precise enough (e.g : you can try 75007 instead of 75000) <a id='searchPlace'>Reload</a> {% endtrans %}"
//  var error_no_country = "{% trans %}You need to select a country first !{% endtrans %}"

$(function(){
  // Fire up some functions (it's not directly there, cause I got to
  // fire them up later after DOM modifications
  setDatePicker();
  copyBandDate();
  copyBandLocation();
  //"add member" setup as default
  addMember('_', true)
});


//#############################################################
// GENERIC FORM UI IMPROVEMENTS 
//#############################################################

$(function(){
  $('input[type=file]').change(function(){
    if($(this).attr('name').indexOf('picture') != -1){
      console.debug("nono2");
      var extension = $(this).val().split('.').pop();
      if (['jpg', 'jpeg', 'JPEG', 'JPG'].indexOf(extension) > -1) {
          console.log('validated');
      } else {
        $(this).val('');
        $(this).siblings('p').wrapInner('<mark class="form_hint" >')
      }
   }
 });
 $('#wmd-input').wrap('<div id="wmd-panel"></div>')
 $('#wmd-input').before('<div id="wmd-button-bar" class="wmd-button-bar"></div>')
 $('#wmd-input').after('<div id="wmd-preview"></div>')
  var converter = new Markdown.Converter();
  var editor = new Markdown.Editor(converter);
  editor.run();

});

// ______________________
//|                      |
//|   Location UI        |
//|______________________|
//
// A fake search button, here for the sole purpose to make people understand they have to blur the field to trigger
// the postalcode search
$(function(){
  $(".search_location").click(function(){$(this).siblings(".postalcode").blur()});

  // Also deactivating "enter" when this field is on focus to prevent instinctive behavior that'd submit the form
  //intercept the "Enter" button to prevent intuitive mistake after entering the zipcode
  $(".postalcode").focus().keypress(function(key){
      var keycode = key.keyCode || key.which;
      if(keycode == 13){
          key.preventDefault();
          $(this).blur();
          return false;
      }
  })
});
// SHORTCUT TO COPY ALL LOCATION DATA FROM THE BAND
function copyBandLocation(){

    $(".copy_band_location").click(function(){
        $(this).siblings('input').each(function(){
            $(this).attr('value', 
                         $("#band_"+$(this).attr("class")).html())
        });
        $(this).siblings('.placeDisplay').html($('#band_place').html())
    });
    $(".copy_band_country").click(function(){
        $(this).siblings('.countrySelect').val($("#band_country").html())
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
                  thisCalendar[index].children(".date_picker_input").attr('value',
                  cal.currentDate.getFullYear()+'-'+(cal.currentDate.getMonth()+1)
                  +'-'+cal.currentDate.getDate());
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
      console.debug(date);
      console.debug(date.getFullYear());
      $(this).siblings("div").remove();
      $(this).parent(".datePicker").calendarPicker({
              showDayArrows:true,
              date:date
          })
      });
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
      postalCodeInit();
      setDatePicker();
      copyBandDate();
      copyBandLocation();
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
      div_content =  $("#track_inputs").html();
      //add to list
      $('.file_attributes').append('<li class="submit_file_list">'+
                                   '<h3>'+files[x].name+'</h3>'+increment(x, '_')+
                                   '</li>'
                                  );

    }
    //fire the addMember function for the additionnal performers
    addMember('No',false)
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
