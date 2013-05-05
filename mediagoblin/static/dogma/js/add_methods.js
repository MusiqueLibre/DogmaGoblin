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
  postalCodeInit();
  setDatePicker();
  copyBandDate();
  copyBandLocation();
  //"add member" setup as default
  addMember('_', true)
});

//#############################################################
// GEONAMES
//#############################################################
// ______________________
//|                      |
//| Postal code selector |
//|______________________|
function postalCodeInit(){
  parent_div=''
  setDefaultCountry();
  $(".postalcode").blur(function(){
    parent_div = '#'+$(this).parents(".form_container").attr('id');
    if($(parent_div+" .postalcode").attr('value') !=  ''){
       postalCodeLookup();
    }
  })
}

// this function is called when the user leaves the postal code input field
// it call the geonames.org JSON webservice to fetch an array of places 
// for the given postal code 
function postalCodeLookup() {

  var country = $(parent_div+' .countrySelect').attr('value');

  if(country == "__None"){
     $(parent_div+' .placeDisplay').html('<small><i>'+error_no_country+'</i></small>');
  }

  if (geonamesPostalCodeCountries.toString().search(country) == -1) {
     return; // selected country not supported by geonames
  }
  // display loading in suggest box
  $(parent_div+' .placeDisplay').html('<small><i>'+info_loading+'</i></small>');

  var postalcode = $(parent_div+' .postalcode').attr('value');

  request = 'http://api.geonames.org/postalCodeLookupJSON?postalcode=' + postalcode  + '&country=' + country  + '&username=dogmazic&callback=getLocation';

  // Create a new script object
  aObj = new JSONscriptRequest(request);
  // Build the script tag
  aObj.buildScriptTag();
  // Execute (add) the script tag
  aObj.addScriptTag();
}

// set the country of the user's ip (included in geonamesData.js) as selected country 
// in the country select box of the address form
function setDefaultCountry() {
  var countrySelect = $(parent_div+' .countrySelect');
  for (i=0;i< countrySelect.length;i++) {
    // the javascript geonamesData.js contains the countrycode
    // of the userIp in the variable 'geonamesUserIpCountryCode'
    if (countrySelect[i].value ==  geonamesUserIpCountryCode) {
      // set the country selectionfield
      countrySelect.selectedIndex = i;
    }
  }
}
// ______________________
//|                      |
//|  location callback   |
//|______________________|
// postalcodes is filled by the JSON callback and used by the mouse event handlers of the suggest box

// this function will be called by our JSON callback
// the parameter jData will contain an array with postalcode objects
function getLocation(jData) {
    if (jData == null) {
      // There was a problem parsing search results
      return;
    }

    // save place array in 'postalcodes' to make it accessible from mouse event handlers

    postalcodes = jData.postalcodes;
        
    if (postalcodes.length > 1 ) {
      $(parent_div+' .suggestBoxElement').css('visibility', 'visible');
      var suggestBoxHTML  = '';
      // iterate over places and build suggest box content
      for (i=0;i< jData.postalcodes.length;i++) {
        // for every postalcode record we create a html div 
        // each div gets an id using the array index for later retrieval 
        // define mouse event handlers to highlight places on mouseover
        // and to select a place on click
        // all events receive the postalcode array index as input parameter
        suggestBoxHTML += "<div class='suggestion'>" + postalcodes[i].countryCode + ' '  + postalcodes[i].postalcode + ' &nbsp;&nbsp; ' + postalcodes[i].placeName  +'</div>' ;
      }
      $(parent_div+' .placeDisplay').html('<small><i>'+info_several_choices+'</i></small>');
      $(parent_div+' .suggestBoxElement').html(suggestBoxHTML);
      $(parent_div+' .suggestion').hover(function(){
        $(this).addClass('selected') 
      },
      function(){
        $(this).removeClass('selected') 
      });
      $('.suggestion').click(function(){
         currentChoice = $(this);
         index = $('.suggestion').index(currentChoice);
         fillFields(postalcodes[index].placeName,postalcodes[index].lat,postalcodes[index].lng);
          $(parent_div+' .suggestBoxElement').html('');


      });

    }
     else if(postalcodes.length == 0){
        $(parent_div+' .placeDisplay').html(error_not_precise_enough);
      }
      else {
      if (postalcodes.length == 1) {
        // exactly one place for postalcode
        // directly fill the form, no suggest box required 
        fillFields(postalcodes[0].placeName,postalcodes[0].lat,postalcodes[0].lng);
      }
    }
    function fillFields(place,lat,lng){
        $(parent_div+' .place').attr('value', place);
        $(parent_div+' .latitude').attr('value', lat);
        $(parent_div+' .longitude').attr('value', lng);
        $(parent_div+' .placeDisplay').html(place);
    }
  }

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
function setDatePicker(){
  $(".dateUnprocessed").each(function(index){
    $(this).removeClass("dateUnprocessed");
    if(index < thisCalendar.length){
      index = thisCalendar.length;
    }
    thisCalendar[index] = $(this);
    $(this).calendarPicker({
      monthNames:["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"],
      dayNames: ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"],
      useWheel:true,
      showDayArrows:true,
      callback:function(cal){
          thisCalendar[index].children(".date_picker_input").attr('value',
          cal.currentDate.getFullYear()+'-'+(cal.currentDate.getMonth()+1)
          +'-'+cal.currentDate.getDate());
          //if it is the album calendar, add the field disabling function
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
    $(this).prev().clone().insertBefore(this);

    //replace the new div's data
    member_div = $(this).prev();
    div_content = member_div.html();
    //member_div_id= member_div.attr('id');
    //inc the ID
    //member_div.attr('id', member_div_id.replace(pattern+member_no, pattern+member_no_inc));

    //replace all occurence of the inputs numbers
    member_div.html(increment(member_no, pattern, true));
    member_no++;

    if(member_page){
      //Relunch functions so they are aware of those new doms elements
      //set up a calendar
      //add the class so it can be processed
      member_div.find(".datePicker").addClass("dateUnprocessed");
      //remove previous divs
      $(".dateUnprocessed").children("div").remove();
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
