$(function(){
    projekktor("#main_player",
        {
            playlist:playlist,
            controls:true,
            width:600,
            height:45,
            plugin_controlbar:{
                controlsTemplate:'<ul class="left"><li><div %{play}></div><div %{pause}></div></li><li><div %{title}></div></li></ul><ul class="right"><li><div %{loopon}></div><div %{loopoff}></div></li><li><div %{mute}></div><div %{unmute}></div></li><li><div %{vslider}><div %{vmarker}></div><div %{vknob}></div></div></div></li><li><div %{timeleft}>%{hr_elp}:%{min_elp}:%{sec_elp} | %{hr_dur}:%{min_dur}:%{sec_dur}</div></li><li><div %{next}></div></li><li><div %{prev}></div></li></ul><ul class="bottom"><li><div %{scrubber}><div %{loaded}></div><div %{playhead}></div><div %{scrubberdrag}></div></div></li></ul>',
                //Always show controls
                showOnStart:true,
                showOnIdle:true,
            }
        }
    );
    $(".ppmute, ppunmute").addClass("toggle");
    for(i=0; i < playlist.length; i++){
        $("#current_playlist").append('<li class="playlist_file">'+playlist[i]['config'].title+"</li>")
    }

    $('.playlist_file').click(function(){
        projekktor('#main_player').setActiveItem($(this).index());
    });

});
