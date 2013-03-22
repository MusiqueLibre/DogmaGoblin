
    $(function(){
      setDefaultCountry();
        $("#searchPlace").click(function(){postalCodeLookup()});
      $("#postalcodeInput").blur(function(){
        if($("#postalcodeInput").attr('value') !=  ''){
           postalCodeLookup();
        }
      })
    });
    var postalcodes;
    
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
        document.getElementById('suggestBoxElement').style.visibility = 'visible';
        var suggestBoxHTML  = '';
        // iterate over places and build suggest box content
        for (i=0;i< jData.postalcodes.length;i++) {
          // for every postalcode record we create a html div 
          // each div gets an id using the array index for later retrieval 
          // define mouse event handlers to highlight places on mouseover
          // and to select a place on click
          // all events receive the postalcode array index as input parameter
          suggestBoxHTML += "<div class='suggestion'>" + postalcodes[i].countryCode + ' ' + postalcodes[i].postalcode + ' &nbsp;&nbsp; ' + postalcodes[i].placeName  +'</div>' ;
        }
        $('#placeDisplay').html('<small><i>{% trans %}There\'s several cities for this postal code : {%endtrans %}</i></small>');
        $('#suggestBoxElement').html(suggestBoxHTML);
        $('.suggestion').hover(function(){
          $(this).addClass('selected') 
        },
        function(){
          $(this).removeClass('selected') 
        });
        $('.suggestion').click(function(){
           currentChoice = $(this);
           index = $('.suggestion').index(currentChoice);
           fillFields(postalcodes[index].placeName,postalcodes[index].lat,postalcodes[index].lng);
            $('#suggestBoxElement').html('');


        });

      }
       else if(postalcodes.length == 0){
          $('#placeDisplay').html("{% trans %} The postal code is incorrect, or not precise enough (try 75007 instread of 75000) <a id='searchPlace'>Reload</a> {% endtrans %}");
        }
        else {
        if (postalcodes.length == 1) {
          // exactly one place for postalcode
          // directly fill the form, no suggest box required 
          fillFields(postalcodes[0].placeName,postalcodes[0].lat,postalcodes[0].lng);
        }
      }
      function fillFields(place,lat,lng){
          $('#placeInput').attr('value', place);
          $('#latitude').attr('value', lat);
          $('#longitude').attr('value', lng);
          $('#placeDisplay').html(place);
      }
    }


    // this function is called when the user leaves the postal code input field
    // it call the geonames.org JSON webservice to fetch an array of places 
    // for the given postal code 
    function postalCodeLookup() {

      var country = $('#countrySelect').attr('value');

      if (geonamesPostalCodeCountries.toString().search(country) == -1) {
         return; // selected country not supported by geonames
      }
      // display loading in suggest box
      $('#placeDisplay').html('<small><i>{% trans %}loading ...{% endtrans %}</i></small>');

      var postalcode = $('#postalcodeInput').attr('value');

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
      var countrySelect = $('#countrySelect');
      for (i=0;i< countrySelect.length;i++) {
        // the javascript geonamesData.js contains the countrycode
        // of the userIp in the variable 'geonamesUserIpCountryCode'
        if (countrySelect[i].value ==  geonamesUserIpCountryCode) {
          // set the country selectionfield
          countrySelect.selectedIndex = i;
        }
      }
    }
