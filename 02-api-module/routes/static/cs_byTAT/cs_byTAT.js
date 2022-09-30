(function() {
    'use strict';

    var config = {
        //   apiUrl: 'http://localhost:6060/api/messages/protected',
        //   apiUrl: 'http://localhost:3000/v2/api/messages/protected',
          apiUrl: '/v2/api/messages/protected',
      }; 

    //------------- OAuth Helpers -------------//
    // This helper function returns the URI for the venueLikes endpoint
    // It appends the passed in accessToken to the call to personalize the call for the user
    function getAPIDataURI(accessToken) {
        return config.apiUrl;
    }



    $(document).ready(function() {
        const accessToken = Cookies.get("accessToken");
        const hasAuth = accessToken && accessToken.length > 0;
        console.log("hasAuth in document.ready(): ", hasAuth)
        updateUIWithAuthState(hasAuth);
        
        $("#submitButton").click(function() {
            console.log("It is working!");
            tableau.connectionName = "cs_byTAT"; // This will be the data source name in Tableau
            tableau.submit(); // This sends the connector object to Tableau
        });
    });
    
    // This function toggles the label shown depending
    // on whether or not the user has been authenticated
    // BUT: only works for 1st load, afterwards, no matter login/logout in the WDC page, this function will not be invoked again.
    function updateUIWithAuthState(hasAuth) {
        console.log("hasAuth in updateUIWithAuthState(): ", hasAuth)
        
        // if (hasAuth) {
        //     $(".notsignedin").css('display', 'none');
        //     $(".signedin").css('display', 'block');
        // } else {
        //     $(".notsignedin").css('display', 'block');
        //     $(".signedin").css('display', 'none');
        // }
    }



// TODO: myConnector.getData
  //------------- Tableau WDC code -------------//
  // Create tableau connector, should be called first
  const myConnector = tableau.makeConnector();

  // Init function for connector, called during every phase but
  // only called when running inside the simulator or tableau
  myConnector.init = function(initCallback) {
      tableau.authType = tableau.authTypeEnum.custom;

      // If we are in the auth phase we only want to show the UI needed for auth
      // https://tableau.github.io/webdataconnector/docs/wdc_authentication.html
      // Note: This is not really a third phase, because it does not follow the other two; it’s an alternative to the first phase.
      // In this mode, the connector should display only the UI that is required in order to get an updated token. Updates to properties other than tableau.username and tableau.password will be ignored during this phase.
      if (tableau.phase == tableau.phaseEnum.authPhase) {
        // for token expires, e.g. the password input in simulator GUI is changed to a wrong one, 
        console.log('token expired, please login agian.')
        // $("#getapidatabutton").css('display', 'none');
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

              tableau.username = "tableau.phase is: " + tableau.phase
              
              if (tableau.phase == tableau.phaseEnum.authPhase) {
                // Auto-submit here if we are in the auth phase
                console.log("tableau.phase is: ", tableau.phase) // this log can be captured only with the following `tableau.submit()` is commented. 
                // tableau.submit()
              }

              return;
          }
      }
  };


    // Define the schema
    
    myConnector.getSchema = function(schemaCallback) {
        var cols = [{
            id: "Master_Lab_ID",
            dataType: tableau.dataTypeEnum.string
        }, {
            id: "internal_TAT",
            dataType: tableau.dataTypeEnum.int
        }, {
            id: "report_delivery_time",
            dataType: tableau.dataTypeEnum.datetime
        }, {
            id: "specimen_accessioning_time",
            dataType: tableau.dataTypeEnum.datetime
        }];

        var tableSchema = {
            id: "cs_byTAT",
            alias: "Schema for By TAT(CS) Dashboard",
            columns: cols
        };

        schemaCallback([tableSchema]);
    };

  
    // Download the data
    myConnector.getData = function(table, doneCallback) {
        $.getJSON("https://t2-lims-dashboard-testenv.herokuapp.com/csP0Dashboard/orderByTAT", function(resp) {
            var dataSource = resp.table,
                tableData = [];
            
            // Iterate over the JSON object
            for (var i = 0 ; i < dataSource.length; i++) {
                tableData.push({
                    "Master_Lab_ID": dataSource[i]["Master_Lab_ID"],
                    "internal_TAT": dataSource[i]["internal_TAT"],
                    "report_delivery_time": dataSource[i]["report_delivery_time"],
                    "specimen_accessioning_time": dataSource[i]["specimen_accessioning_time"]
                });
            }


            table.appendRows(tableData);
            doneCallback();
        });
    };
    tableau.registerConnector(myConnector);
})();
