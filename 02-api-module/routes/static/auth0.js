(function() {
  'use strict';

  // This config stores the important strings needed to
  // connect to the foursquare API and OAuth service
  //
  // Storing these here is insecure for a public app
  // See part II. of this tutorial for an example of how
  // to do a server-side OAuth flow and avoid this problem
  var config = {
    //   apiUrl: 'http://localhost:6060/api/messages/protected',
    //   apiUrl: 'http://localhost:3000/v2/api/messages/protected',
      apiUrl: '/v2/api/messages/protected',
  }; 

  // Called when web page first loads and when
  // the OAuth flow returns to the page
  //
  // This function parses the access token in the URI if available
  // It also adds a link to the foursquare connect button
  $(document).ready(function() {
      var dataToReturn = [];
      var accessToken = Cookies.get("accessToken");
      var hasAuth = accessToken && accessToken.length > 0;
      updateUIWithAuthState(hasAuth);

      $("#getapidatabutton").click(function() {
          tableau.connectionName = "Autho0 Protected API Data";
          tableau.submit();
      });
  });

  //------------- OAuth Helpers -------------//
  // This helper function returns the URI for the venueLikes endpoint
  // It appends the passed in accessToken to the call to personalize the call for the user
  function getAPIDataURI(accessToken) {
      return config.apiUrl;
  }

  // This function toggles the label shown depending
  // on whether or not the user has been authenticated
  function updateUIWithAuthState(hasAuth) {
      if (hasAuth) {
          $(".notsignedin").css('display', 'none');
          $(".signedin").css('display', 'block');
      } else {
          $(".notsignedin").css('display', 'block');
          $(".signedin").css('display', 'none');
      }
  }

  //------------- Tableau WDC code -------------//
  // Create tableau connector, should be called first
  var myConnector = tableau.makeConnector();

  // Init function for connector, called during every phase but
  // only called when running inside the simulator or tableau
  myConnector.init = function(initCallback) {
      tableau.authType = tableau.authTypeEnum.custom;

      // If we are in the auth phase we only want to show the UI needed for auth
      if (tableau.phase == tableau.phaseEnum.authPhase) {
        $("#getapidatabutton").css('display', 'none');
      }

      if (tableau.phase == tableau.phaseEnum.gatherDataPhase) {
        // If the API that WDC is using has an endpoint that checks
        // the validity of an access token, that could be used here.
        // Then the WDC can call tableau.abortForAuth if that access token
        // is invalid.
      }

      var accessToken = Cookies.get("accessToken");
      var hasAuth = (accessToken && accessToken.length > 0) || tableau.password.length > 0;
      updateUIWithAuthState(hasAuth);

      initCallback();

      // If we are not in the data gathering phase, we want to store the token
      // This allows us to access the token in the data gathering phase
      if (tableau.phase == tableau.phaseEnum.interactivePhase || tableau.phase == tableau.phaseEnum.authPhase) {
          if (hasAuth) {
              tableau.password = accessToken;

              if (tableau.phase == tableau.phaseEnum.authPhase) {
                // Auto-submit here if we are in the auth phase
                tableau.submit()
              }

              return;
          }
      }
  };

  // Declare the data to Tableau that we are returning from Foursquare
  myConnector.getSchema = function(schemaCallback) {
      var schema = [];

      var col1 = { id: "Name", dataType: "string"};
      var col2 = { id: "Message", dataType: "string"};
      var cols = [col1, col2];

      var tableInfo = {
        id: "Authh0MessageTable",
        columns: cols
      }

      schema.push(tableInfo);

      schemaCallback(schema);
  };

  // This function actually make the foursquare API call and
  // parses the results and passes them back to Tableau
  myConnector.getData = function(table, doneCallback) {
      var dataToReturn = [];
      var hasMoreData = false;

      var accessToken = tableau.password;
      var connectionUri = getAPIDataURI(accessToken);

      var xhr = $.ajax({
          url: connectionUri,
          headers: {
            'authorization': 'Bearer ' + accessToken
          },
          dataType: 'json',
          success: function (data) {
              if (data) {
                //   var venues = data.response.venues.items;
                  var api_text_message = data;

                  var message = {
                    'Name': Object.keys(api_text_message),
                    'Message': Object.values(api_text_message)
                  };
                  dataToReturn.push(message);
                  
                  table.appendRows(dataToReturn);
                  doneCallback();
              }
              else {
                  tableau.abortWithError("No results found");
              }
          },
          error: function (xhr, ajaxOptions, thrownError) {
              // WDC should do more granular error checking here
              // or on the server side.  This is just a sample of new API.
              tableau.abortForAuth("Invalid Access Token");
          }
      });
  };

  // Register the tableau connector, call this last
  tableau.registerConnector(myConnector);
})();
