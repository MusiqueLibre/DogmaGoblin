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
  setDatePicker();
  citySearch()
  copyBandDate();
  copyBandLocation();
  jpegCheck();
  filterPositionning();
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
}

