(function() {
  'use strict';

  // This config stores the important strings needed to
  // connect to the foursquare API and OAuth service
  //
  // Storing these here is insecure for a public app
  // See part II. of this tutorial for an example of how
  // to do a server-side OAuth flow and avoid this problem
  const config = {
      // apiUrl: 'http://localhost:6060/api/messages/protected', // for api/routes separately run
      apiUrl: '/api/v2/api/messages/protected', // for 2 flask apps run together by `run_simple`
  }; 

  // Called when web page first loads and when
  // the OAuth flow returns to the page
  //
  // This function parses the access token in the URI if available
  // It also adds a link to the foursquare connect button
  $(document).ready(function() {
      // var dataToReturn = [];
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
      console.log("hasAuth in updateUIWithAuthState(): ", hasAuth)
      console.log("tableau.phase is: " + tableau.phase)
      // if (hasAuth) {
      //     $(".notsignedin").css('display', 'none');
      //     $(".signedin").css('display', 'block');
      // } else {
      //     $(".notsignedin").css('display', 'block');
      //     $(".signedin").css('display', 'none');
      // }
  }

  //------------- Tableau WDC code -------------//
  // Create tableau connector, should be called first
  var myConnector = tableau.makeConnector();

  // Init function for connector, called during every phase but
  // only called when running inside the simulator or tableau
  myConnector.init = function(initCallback) {
    // tableau.connectionName = "tableau.phase in init() is: " + tableau.phase
      tableau.authType = tableau.authTypeEnum.custom;
      console.log('----==== in the init() ====----')
      // If we are in the auth phase we only want to show the UI needed for auth
      // https://tableau.github.io/webdataconnector/docs/wdc_authentication.html
      // Note: This is not really a third phase, because it does not follow the other two; it’s an alternative to the first phase.
      // In this mode, the connector should display only the UI that is required in order to get an updated token. Updates to properties other than tableau.username and tableau.password will be ignored during this phase.
      if (tableau.phase == tableau.phaseEnum.authPhase) {
        // for token expires, e.g. the password input in simulator GUI is changed to a wrong one, 
        console.log('token expired, please login agian.')
        tableau.abortForAuth()
        // $("#getapidatabutton").css('display', 'none');
        // document.cookie = 'accessToken'+'=; Max-Age=-99999999;'; 
        // $.ajax({
        //   url: '/logout',
        //   success: function (data) {
        //         tableau.abortForAuth()
        //         // tableau.password = ''
        //         tableau.connectionData = 'aaaa'
        //         console.log('logged out.')
        //         console.log(data)
        //    }
        // })
      }
      
      if (tableau.phase == tableau.phaseEnum.gatherDataPhase) {
        // If the API that WDC is using has an endpoint that checks
        // the validity of an access token, that could be used here.
        // Then the WDC can call tableau.abortForAuth if that access token
        // is invalid.
        // tableau.abortForAuth()
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
              tableau.username = "tableau.phase in init() - YES hasAuth test is: " + tableau.phase
              // tableau.connectionName = "tableau.phase in init() hasAuth test is: " + tableau.phase


              console.log('----==== end of init() auth check ====----')


              if (tableau.phase == tableau.phaseEnum.authPhase) {
                $.ajax({
                  url: '/logout',
                  success: function (data) {
                        tableau.abortForAuth()
                        tableau.password = ''
                        tableau.connectionData = 'test writing to connectionData input'
                        tableau.connectionName = 'test writing to connectionName input'
                        console.log('logged out.')
                        console.log(data)
                   }
                })
                // Auto-submit here if we are in the auth phase
                console.log("tableau.phase is: ", tableau.phase) // this log can be captured only with the following `tableau.submit()` is commented. 
                tableau.submit()
              }

              return;
          }
          tableau.username = "tableau.phase in init() - NO hasAuth test is: " + tableau.phase
      }
      console.log('----==== end of init() ====----')
  };

  // Declare the data to Tableau that we are returning from Foursquare
  myConnector.getSchema = function(schemaCallback) {
    // tableau.connectionName = "tableau.phase in getSchema() is: " + tableau.phase // gatherData
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
    // tableau.connectionName = "tableau.phase in getData() is: " + tableau.phase // gatherData
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
