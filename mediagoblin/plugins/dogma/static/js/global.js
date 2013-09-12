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
