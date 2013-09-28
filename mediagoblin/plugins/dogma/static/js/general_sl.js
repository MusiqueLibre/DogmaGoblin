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
      toggleMenu($(this), true);
      $('#login_container').html('<div style="text-align:center"><img alt="loading gif" src="/global_statics/images/ajax-loader.gif" /></div>').load('http://mlo.loc/user/index.php?r=user/login/remotelogin&url='+url);
    });
    $('#deconnection_button').click(function(){
      $.ajax({
              type: 'POST',
              url:'http://mlo.loc/user/index.php?r=user/logout&url=1',
              success: function(){document.location.reload()}
             });
    });
    
  });
  function closeMenu(){
        $(".menu_more_button.lower_button").html("+");
        $(".lower_button").removeClass('lower_button');
        $(".enlighted").removeClass('enlighted');
        $('.sub_menu_container').slideUp(200);

  }
function toggleMenu(thisButton,connection){
        //yeah, cause you can't set default value for functions parameters in JS
        if (connection === undefined){
          connection = false
        }
        $('.lower_button + .sub_menu_container').slideUp(100);
        $(".enlighted").removeClass('enlighted');
        $(".menu_more_button.lower_button").html("+");
        if(!thisButton.hasClass('lower_button')){
          $(".lower_button").removeClass('lower_button');
          thisButton.addClass('lower_button');
          if(!connection){
            thisButton.prev().addClass('enlighted');
            thisButton.html('-');
          }
          thisButton.siblings('.sub_menu_container').
                                                slideToggle(200);
        }else{
          $(".lower_button").removeClass('lower_button');
          if(!connection){
            $(".menu_more_button.lower_button").html("+");
          }
        }
  }
