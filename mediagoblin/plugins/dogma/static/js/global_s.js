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
//  var undo = {%trans%}Cancel{%endtrans%}
//  var redo = {%trans%}Delete{%endtrans%}
var thisCalendar = new Array();
var postalcodes;
//starts with "1", cause the member 0 is already displayed
var member_no = 0;

//#######################
//### UI IMPROVMENT  ###
//#######################
//
//Adds the slide up/down behavior to the <summary> and <detail> elements
$(function(){
  //Go to login menu
  $('.go_to_loggin').click(function(){
    $('html, body').animate({ scrollTop: 0 }, 'slow');
    $('#connection_button').click();
  });
  if($('#masonry_container').length > 0){
    var container = document.querySelector('#masonry_container');
    var msnry = new Masonry( container, {
        itemSelector: '.masonry_item'
    });
  }
    
  //chat window
  if($('#chat_container').length > 0){
    var chat_iframe='<iframe width="600" height="400" src="http://www.coomute.net:7778" id="footer_chat">You need a Frames Capable browser to view this content.</iframe><button type="button" id="chat_hide">&#8690;</button>';
    $('#chat_button.open').click(function(){
      $('#chat_container').html(chat_iframe);
      $(this).hide();
      var full_chat= true;
      $('#chat_hide').click(function(){
        if(full_chat){
          $('#chat_container').css('height', '38px');
          full_chat = false;
          $(this).html("&#8689;");
        }else{
          $('#chat_container').css('height', 'auto');
          $(this).html("&#8690;");
          full_chat = true;
        }

      });
    });
  }
  $('details').details();
  $('details').on({
   'open.details': function() {
      //fallback to be used with masonery. Else the unfolded details passes bellow other elements
      $(".dashboard_band .open").parents(".dashboard_band").css("z-index", "10");
    },
    'close.details': function() {
      $(".dashboard_band .open").parents(".dashboard_band").css("z-index", "0");
    }
  });

  
  //make the entire menu boxes clickable
  $('#secondary_logo_box_title, #logo_box_title, .header_sub_button').click(function(){
    $(this).siblings('.header_button').click();
  });
  //displaying drop down menu properly 
  $('.sub_menu_container').hide()
  $('.sub_menu_container').each(function(){
    parentheight = $(this).parents(".menu_container").outerHeight();
    window_width = $(window).width() - parseInt($(".sub_menu_container").css("padding-left").replace(/[^-\d\.]/g, '')) - parseInt($(".sub_menu_container").css("padding-right").replace(/[^-\d\.]/g, ''));
    $(this).css({ 'top' : parentheight, 'width' : window_width -10 });
  });
  //global menu toggle function

  $(".menu_more_button").click(function(){
    toggleMenu($(this));
  });

  //slide all up when it loses focus
  $('#general_menu').mouseleave(function(){
    closeMenu();
  })
  //adding a "close menu" on the bottom of each menu to avoid the anoyance of scrolling up
  $('.sub_menu_container').append('<button class="hollow_button menu_more_button button_thick menu_close" style="float:right">-</button>');
  $('.menu_close').click(function(){
    closeMenu();
  });
  //AJAX connection stuffs
  var url = window.location;
  $('#connection_button').click(function(){
    toggleMenu($(this));
    $('#login_container').html('<div style="text-align:center"><img alt="loading gif" src="/global_statics/images/ajax-loader.gif" /></div>').load('/user/index.php?r=user/login/remotelogin&url='+url);
  });
  $('#deconnection_button').click(function(){
    $.ajax({
            type: 'POST',
            url:'/user/index.php?r=user/logout&url=1',
            success: function(){document.location.reload()}
           });
  });
    
//Filters
  var filter_count = $(".side_filter_title").length;
  var filter_size = 30;
  $('.side_filter_content').css('width', 'calc(100% - '+filter_size*filter_count+'px)');
  var filter_content_width  = $(".side_filter_content").outerWidth();
  $(".side_filter_title").click(function(){
    filter_right = 0;
    clicked_filter = $(this)
    $(".side_filter_title").each(function(){
      //loop through all filters and give the first position to the clicked one
      if( $(this).html() != clicked_filter.html()){
        $(this).css('right', filter_right);
        filter_right += filter_size;
        $(this).siblings(".side_filter_content").css('left', -filter_content_width)
      }else{
        $(clicked_filter).css('right', (filter_count-1)*filter_size);
        $(this).siblings(".side_filter_content").css('left', 0)
      }

    });
  });
});
function closeMenu(){
      if($(".menu_more_button.lower_button").html()== '-'){
        $(".menu_more_button.lower_button").html("+");
      }
      $(".lower_button").removeClass('lower_button');
      $(".enlighted").removeClass('enlighted');
      $('.sub_menu_container').slideUp(200);

}
$(".full_track_item").click(function(){
  $(this).children('.media_entry_wrapper').click();
});

//Extending the "add to player" button in 2.5
//

//_______________________
//|                      |
//|  Generic UI Methods  |
//|______________________|

function toggleMenu(thisButton){
      $(".enlighted").removeClass('enlighted');
      if( $(".menu_more_button.lower_button").html() == '-'){
        $(".menu_more_button.lower_button").html("+");
      }
      if(!thisButton.hasClass('lower_button')){
        //remove this class from other buttons
        $(".lower_button").removeClass('lower_button');
        //add this class to the clicked button
        thisButton.addClass('lower_button');
        if(thisButton.html() == '+'){
          thisButton.prev().addClass('enlighted');
          thisButton.html('-');
        }
        $('.sub_menu_container').slideUp(500);
        thisButton.siblings('.sub_menu_container').slideDown(500);
      }else{
        $(".lower_button").removeClass('lower_button');
        thisButton.siblings('.sub_menu_container').slideUp(500);
        if( $(".menu_more_button.lower_button").html() == '-'){
          $(".menu_more_button.lower_button").html("+");
        }
      }
 };


//###############
//### PLAYER  ###
//###############
//
function changeTrack(){
  player = projekktor('#main_player');
  index = player.getItemIdx();
  $('#current_playlist').children().removeClass("played");
  $('#current_playlist').children().eq(index).addClass("played");
}
/* Main player method */
function startPlayer(){
  var template = [
                  '<ul class="playhead">',
                    '<li class="bullet_less player_time_control"><span %{timeleft}>%{hr_elp}:%{min_elp}:%{sec_elp} | %{hr_dur}:%{min_dur}:%{sec_dur}</span>',
                    '<span %{scrubber}><span %{title}></span><span %{loaded}></span><span %{playhead}></span><span %{scrubberdrag}></span></span></li>',
                  '</ul>',
                  '<ul class="control_bar">',
                    '<li class="bullet_less player_control"><button type="button" %{prev}>&#9027;</button></li>',
                    '<li class="bullet_less player_control"><button type="button" %{play}>&#9654;</button><button type="button" %{pause}>&#9646;&#9646;</button></li>',
                    '<li class="bullet_less player_control"><button type="button" %{next}>&#9028;</button></li>',
                    '<li class="bullet_less player_control" id="player_mute_buttons"><button type="button" %{mute}>&#9835;&#10007;</button><button type="button" %{unmute}>&#9835;</button></li>',
                    '<li class="bullet_less player_control"><span %{vslider}><span %{vmarker}></span></span></span></li>',
                  '</ul>'].join('\n');
    projekktor("#main_player",
        {
            controls:true,
            height:70,
            plugin_controlbar:{
                controlsTemplate: template,
                toggleMute: true,
                //Always show controls
            }
        }
    ).addListener('item', function(){changeTrack()});
    if(projekktor('#main_player').getItemCount() == 0){
      $('#main_player').addClass('empty');
    }
    playlistButtons();

};
//Adapts the player behavior to the user's actions on the playlist.
function playlistButtons(){ 

    $('#main_player').removeClass('empty');
    $('#main_player').removeClass('tooltip');
      parent = $(this).parent();
      parent_index = parent.index();
      $('#current_playlist').on('click', '.play_track', function(){
          projekktor('#main_player').setActiveItem($(this).parent().index());
          player.setPlay();
      });
      $('#current_playlist').on('click', '.remove_track', function(){
          player = projekktor('#main_player');
          parent = $(this).parent();
          parent_index = parent.index();

          if(player.getItemCount() == 1){ //the player shows an error when removing the last object
            $("#main_player").addClass("empty");
          }else{
            player.setItem(null ,parent_index);
          }
          parent.remove();
          playlistCountUpdate();
     });
}
//Allow the user to use the playlist to interact with the player. Adding and removing items from both the site's and the player's JSON
//playlist.
function playlistPageButtons(){
      json_playlists = {};
      id = [];
      this_album = []
      //store the data for each playlist's albums
      $(".band_album_list").each(function(index){
        //using an array cause the each is faster than the json request. If not, the variable changes too soon
        ////using an array cause the each is faster than the json request. If not, the variable changes too soon
        id[index] = $(this).attr('data-id');
        playlist = $(this).attr('data-playlist');
        //the "$this" changes after the doe/fail, I need to store the one I need here
        this_album[index] = $(this);
        $.getJSON(playlist, function(data){
          json_playlists[id[index]] = data;
        }).done(function(){
                this_album[index].children('.media_entry_wrapper')
                                                                  .removeClass('loading_playlist');
                this_album[index].siblings('.add_album_to_playlist').removeClass('loading_playlist');
                playlistPageButtonsLoaded(this_album[index], json_playlists[id[index]]);
              }).fail(function(){
                            this_album[index].children('.media_entry_wrapper').addClass('loading_problem');
                            this_album[index].siblings('.add_album_to_playlist').addClass('loading_problem');
                            this_album[index].children('.loading_problem .add_track').html(reload);
                          });
      });

}
//wait until the json succeed to launch this
function playlistPageButtonsLoaded(this_album, data){
      //prevent this function to work if it's a download button that is clicked
      //Is there a more elegant solution ? Probably.
      add_to_playlist = true;
      $('.no_click').hover(
        function(){add_to_playlist = false; },
        function(){add_to_playlist = true;}
      );
      this_album.children(".media_entry_wrapper").click(function(){
         if(add_to_playlist){
           if(typeof player === 'undefined'){
             player = projekktor('#main_player');
           }
           id= $(this).parents('.band_album_list').attr('data-id');
           button_index = $(this).index();
           track = data[button_index]
           $('#current_playlist').
           append('<li class="bullet_less"><button class="play_track">'+track.config['title']+'</button><button class="remove_track hollow_button">'+remove+'</button></li>');
           $("#player_helper").css('display',' block');
           $("#player_notif_t_added").addClass('show_slow');
           setTimeout(function(){$("#player_notif_t_added").removeClass('show_slow')}, 3000);
           //relaunch the buttons actions for the new DOM
           //if the player is empty add the first file
           if(player.getItemCount() == 0){
             player.setFile(data.slice(button_index, button_index+1),0);
           }else{
             //if there's already something, append the new track
             player.setItem(data[button_index],player.getItemCount());
           }
           playlistCountUpdate();
         }
      });
      //add album
      album_button = this_album.siblings(".add_album_to_playlist");
      album_button.click(function(){
            $("#player_helper").css('display',' block');
            $("#player_notif_a_added").addClass('show_slow');
            setTimeout(function(){$("#player_notif_a_added").removeClass('show_slow')}, 3000);
            if(typeof player === 'undefined'){
              player = projekktor('#main_player');
            }
            id= $(this).next('.band_album_list').attr('data-id');
            //I have to setFile if empty or happend to the existing tracks if there's already something with setItem 
            if(player.getItemCount() == 0){
               player.setFile(data);
            }else{
              $.each( data, function(index, track){
                 player.setItem(track, player.getItemCount());
              });
            }
            $.each( data, function(index, track){
               $('#current_playlist').
                 append('<li class="bullet_less"><button class="play_track">'+track.config['title']+'</button><button class="remove_track hollow_button">'+remove+'</button></li>');
            });
            playlistCountUpdate();
      });
      $("body").on('click', ".add_album_and_clear_playlist" ,function(){
            playlistCountUpdate();
            player.setFile(data);
            $('#current_playlist').html('');
            $.each( data, function(index, track){
               $('#current_playlist').
                 append('<li class="bullet_less"><button class="play_track">'+track.config['title']+'</button><button class="remove_track hollow_button">'+remove+'</button></li>');
            });
     });
     //REMOTE CONTROL
     // got to player/playlist
     $('#go_to_player').click(function(){
       $('html, body').animate({ scrollTop: 0 }, 'slow');
     });
     $('#go_to_playlist').click(function(){
       $('html, body').animate({ scrollTop: 0 }, 'slow', function(){
       });
       $('#main_player_container .menu_more_button').click();
     });
     $("#remote_prev").click(function(){
       projekktor('#main_player').setActiveItem('prev');
     });
     $("#remote_play").click(function(){
       projekktor('#main_player').setPlay();
     });
     $("#remote_pause").click(function(){
       projekktor('#main_player').setPause();
     });
     $("#remote_next").click(function(){
       projekktor('#main_player').setActiveItem('next');
     });
}
function playlistCountUpdate(){
  $('#playlist_count').html($('#current_playlist').children().length);
}

//###############################
//### AJAXIFY INTERNAL LINKS  ###
//###############################
//
//If we're dealing with an internal link, it'll load the content of the <main> tag into current <main>.
//It works perfectly with back and forward browser buttons
//Links still work even if the JS is not enabled.
//
function ajaxify(){
  var init = true, 
      state = window.history.pushState !== undefined;
  var handler = function(data) {
          $.address.title(/>([^<]*)<\/title/.exec(data)[1]);
          $('main').html($(data).filter('main').html());
  };
  $.address.state(address_state).init(function(event) {
      // Initializes plugin support for links
      $('a:not([href^=http]):not([href$=mp3]):not([href$=webm]):not([href$=flac]):not([href$=ogg]):not([href^=#])').address();
  }).change(function(event) {
  if(init && state){
    init = false;
  }else{
       

      //get the href from the link
      var link_href = event.value;
      // Loads the page content and inserts it into the content area
      //$( "main" ).load( "main" );
      $.ajax({
          url: $.address.state() + event.value,
          error: function(XMLHttpRequest, textStatus, errorThrown) {
              handler(XMLHttpRequest.responseText);
          },
          success: function(data, textStatus, XMLHttpRequest) {
              handler(data);
              initAtPageLoad();
          }
      });
  }

  });
}

//###################################################
//### A SET OF METHODS TO IMPROVE SUBMIT FORMS UI ###
//###################################################
//
//You need to set those variables inside a jinja template BEFORE this script
//so they can be translated :
//
//  var text_preview = "{% trans %}Preview{% endtrans %}"



//#############################################################
// GENERIC FORM UI IMPROVEMENTS 
//#############################################################
//Check that the image the user provided is of the proper format
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
        //TODO add class to the last date picker to hide the former member.
  });
}
//_______________________
//|                      |
//|  Date picker UI      |
//|______________________|
function copyBandDate(){
  $(".copy_band_date").click(function(){
      date = new Date(parseInt($("#band_millis").html()));
      $(this).siblings("div").html('');
      thisCalendar = $(this).siblings(".datePicker");
      thisCalendar.calendarPicker({
              showDayArrows:true,
              date:date,
              callback:function(cal){
                calendarCallBack(thisCalendar, cal)}
          })
      });
}
function calendarCallBack(thisCalendar, cal){
  thisCalendar.siblings(".date_picker_input").attr('value',
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
      init()

      editor[member_no] = new Markdown.Editor(converter, pattern+member_no);
      editor[member_no].run();
    }
  })
}

//#############################################################
// Multiple File Input
//#############################################################
// This copies the standard track's form, one per file in the file[] input and increment their names accordingly
function multiupUI(){
  $('#multi_file_input').bind('change', function(){
    //for every file...
    files = $(this).prop('files')
    $('#file_list').html('<ul class="file_attributes"></ul>');
    for (var x = 0; x < files.length; x++) {
      var extension = files[x].name.split('.').pop();
      if (['mp3', 'ogg', 'flac', 'MP3', 'OGG', 'FLAC'].indexOf(extension) > -1) {
        div_content =  $("#track_inputs_layout").html();
        //add to list
        $('.file_attributes').append('<li class="submit_file_list bullet_less">'+
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
};
//#############################################################
// EDIT METHODS
//#############################################################
//

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
  //FLATTR
  var s = document.createElement('script'), t = document.getElementsByTagName('script')[0];
  s.type = 'text/javascript';
  s.async = true;
  s.src = 'http://api.flattr.com/js/0.6/load.js?mode=auto';
  t.parentNode.insertBefore(s, t);
