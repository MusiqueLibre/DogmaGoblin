//Adds the slide up/down behavior to the <summary> and <detail> elements
$(function(){
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
  var $container = $('#masonery_container');
  // initialize
     $container.masonry({
       itemSelector: '.dashboard_band'
  });
  var msnry = $container.data('masonry');

});

//ajaxify the website
var first = true;
$.address.crawlable(true).init(function(event) {
    // Initializes plugin support for links
    $('a:not([href^=http])').address();
}).change(function(event) {

if(first){
  first = false;
  $.address.state('/');
}else{
    var handler = function(data) {
        console.debug($(data).find('main').html());
            $.address.title(/>([^<]*)<\/title/.exec(data)[1]);
            $('main').html($(data).filter('main').html());
    };

    //get the href from the link
    var link_href = event.value;
    // Loads the page content and inserts it into the content area
    $( "main" ).load( "main" );
    $.ajax({
        url: event.value,
        error: function(XMLHttpRequest, textStatus, errorThrown) {
            handler(XMLHttpRequest.responseText);
        },
        success: function(data, textStatus, XMLHttpRequest) {
            handler(data);
        }
    });
}

});
/*PLAYER */
$(function(){
  var template = ['<ul class="track_data">',
                    '<li class="bullet_less player_control"><span %{title}></span></li>',
                    '<li class="bullet_less player_control"><span %{timeleft}>%{hr_elp}:%{min_elp}:%{sec_elp} | %{hr_dur}:%{min_dur}:%{sec_dur}</span></li>',
                  '</ul>',
                  '<ul class="playhead">',
                    '<li class="bullet_less "><span %{scrubber}><span %{loaded}></span><span %{playhead}></span><span %{scrubberdrag}></span></span></li>',
                  '</ul>',
                  '<ul classe="control_bar">',
                    '<li class="bullet_less player_control"><span %{prev}>&#9027;</span></li>',
                    '<li class="bullet_less player_control"><span %{play}>&#9654;</span><span %{pause}>&#9646;&#9646;</span></li>',
                    '<li class="bullet_less player_control"><span %{next}>&#9028;</span></li>',
                    '<li class="bullet_less player_control"><span %{mute}>&#8709;</span><span %{unmute}>&#9673;</span><span %{vslider}><span %{vmarker}></span></span></span></li>',
                    '<li class="bullet_less player_control"><span %{loopon}>&#10560;</span><span %{loopoff}>&#10228;</span></li>',
                  '</ul>'].join('\n');
    projekktor("#main_player",
        {
            controls:true,
            height:100,
            plugin_controlbar:{
                controlsTemplate: template,
                //Always show controls
            }
        }
    );
    $('.play_track').click(function(){
        projekktor('#main_player').setActiveItem($(this).parent().index());
    });
    $('.remove_track').click(function(){
        player = projekktor('#main_player');
        parent = $(this).parent();
        parent_index = parent.index();

        console.debug(parent_index, player.getItemIdx());
        if(player.getItemCount() == 1){ //the player shows an error when removing the last object
          $("#main_player").addClass("empty");
        }else{
          player.setItem(null ,parent_index);
        }
        parent.remove();
    });

    $(".media_entry_wrapper").click(function(){
       player = projekktor('#main_player');
       button_index = $(this).parents('.thumb_gallery').find('.media_entry_wrapper').index($(this));
       console.debug(playlist_items[button_index]);
       //player.setFile()
       file = [{0:{src:"/mgoblin_media/media_entries/301/05_The_Lamia.webm", type:"audio/ogg"}, config: { title: "05 The Lamia"}}];
       player.setFile(file);
       console.debug("jkbkjb");
    });
});
