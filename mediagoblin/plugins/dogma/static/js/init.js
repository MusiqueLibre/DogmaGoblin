//Things to be started only once
//
$(function(){
  address_state = '';
  ajaxify();
  startPlayer();
  initAtPageLoad();
});
//Things to be started at page load AND at DOM refresh
function initAtPageLoad(){
  addMember('_', true)
  setDatePicker();
  citySearch()
  copyBandDate();
  copyBandLocation();
  jpegCheck();
  filterPositionning();
  var $container = $('#masonery_container');
  // initialize
     $container.masonry({
       itemSelector: '.dashboard_band'
  });
  var msnry = $container.data('masonry');
  //TODO add some conditions before lunching stuffs
  //add the markdown wysiwyg if there's the proper textarea input
  if($('#wmd-input_0').length > 0){
   $('#wmd-input_0').wrap('<div id="wmd-panel_0" class="visual_block"></div>')
   $('#wmd-input_0').before('<div id="wmd-button-bar_0" class="wmd-button-bar"></div>')
   $('#wmd-input_0').after('<h3>'+text_preview+'</h3></p><div id="wmd-preview_0"></div>')
   converter = new Markdown.Converter();
   editor = new Markdown.Editor(converter, '_0');
   editor.run();
  }
  if($('#multi_file_input').length > 0){
    multiupUI();
  }

  if($('.band_album_list').length > 0){
    playlistPageButtons();
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
  Modernizr.load({
      test: Modernizr.inputtypes.date,
      nope: ['/plugin_static/coreplugin_dogma/js/jquery-ui.min.js'],
      complete: function () {
        $('input[type=date]').datepicker({
           dateFormat: 'yy-mm-dd',
           maxDate:'0 0',
           minDate: new Date(1900, 1 - 1, 1),
           changeYear: true,
           yearRange: "-60:+0",
           changeMonth: true,

        }); 
      }
  });
}

