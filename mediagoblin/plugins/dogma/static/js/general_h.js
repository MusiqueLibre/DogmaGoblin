  $(function(){
    //FLATTR
    var s = document.createElement('script'), t = document.getElementsByTagName('script')[0];
    s.type = 'text/javascript';
    s.async = true;
    s.src = 'http://api.flattr.com/js/0.6/load.js?mode=auto';
    t.parentNode.insertBefore(s, t);

    
    //displaying drop down menu properly 
    $('.sub_menu_container').each(function(){
      parentheight = $(this).parents(".menu_container").outerHeight();
      //get the window width and remove block's padding to have the proper size
      window_width = $(window).width() - parseInt($(".sub_menu_container").css("padding-left").replace(/[^-\d\.]/g, '')) - parseInt($(".sub_menu_container").css("padding-right").replace(/[^-\d\.]/g, ''));
      $(this).css({ 'top' : parentheight, 'width' : window_width -10 }).hide();
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
    
  });
  function closeMenu(){
        if($(".menu_more_button.lower_button").html()== '-'){
          $(".menu_more_button.lower_button").html("+");
        }
        $(".lower_button").removeClass('lower_button');
        $(".enlighted").removeClass('enlighted');
        $('.sub_menu_container').slideUp(200);

  }
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
          $('.sub_menu_container').slideUp(100);
          thisButton.siblings('.sub_menu_container').slideDown(200);
        }else{
          $(".lower_button").removeClass('lower_button');
          thisButton.siblings('.sub_menu_container').slideUp(200);
          if( $(".menu_more_button.lower_button").html() == '-'){
            $(".menu_more_button.lower_button").html("+");
          }
        }
  }
