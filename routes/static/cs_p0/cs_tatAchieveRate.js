(function() {
    'use strict';

    const config = {
        apiUrl: '/api/v2/csP0Dashboard/tatAchieveRate'
    }; 


    $(document).ready(function() {
        // Not essential, just check cookie exist or not.
        const accessToken = Cookies.get("accessToken");
        const hasAuth = accessToken && accessToken.length > 0;
        updateUIWithAuthState(hasAuth);
        
        $("#submitButton").click(function() {
            console.log("It is working!");
            tableau.connectionName = "cs_tatAchieveRate"; // This will be the data source name in Tableau
            tableau.submit(); // This sends the connector object to Tableau
        });
    });

    // ------- UI controled by javascript side from the index.html, not Flask session side. ------ //
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

      const accessToken = Cookies.get("accessToken");
      const hasAuth = (accessToken && accessToken.length > 0) || tableau.password.length > 0;
    //   updateUIWithAuthState(hasAuth);

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
                tableau.submit() // tweak here
              }

              return;
          }
      }
  };


    // Define the schema
    
    myConnector.getSchema = function(schemaCallback) {
        const cols = [{
            id: "Master_Lab_ID",
            dataType: tableau.dataTypeEnum.string
        }, {
            id: "courier_dispatch_time",
            dataType: tableau.dataTypeEnum.datetime
        }, {
            id: "report_delivery_time",
            dataType: tableau.dataTypeEnum.datetime
        }, {
            id: "specimen_accessioning_time",
            dataType: tableau.dataTypeEnum.datetime
        }, {
            id: "trf_scanning_time",
            dataType: tableau.dataTypeEnum.datetime
        }, {
            id: "trf_verification_time",
            dataType: tableau.dataTypeEnum.datetime
        }, {
            id: "internal_TAT",
            dataType: tableau.dataTypeEnum.int
        }, {
            id: "porter_Service_TAT",
            dataType: tableau.dataTypeEnum.int
        }, {
            id: "partner_TAT",
            dataType: tableau.dataTypeEnum.int
        }, {
            id: "trf_Entry_TAT",
            dataType: tableau.dataTypeEnum.int
        }];

        const tableSchema = {
            id: "tatAchieveRate",
            alias: "Schema for TAT Achieve Rate and By TAT Dashboard",
            columns: cols
        };

        schemaCallback([tableSchema]);
    };

  
    // Download the data
    myConnector.getData = function(table, doneCallback) {
        let tableData = [];
        const accessToken = tableau.password;
        
        $.ajax({
            url: config.apiUrl,
            headers: {
                'authorization': 'Bearer ' + accessToken
            },
            dataType: 'json',
            success: function (resp) {
                if (resp) {  
                    const dataSource = resp.table
                    for (const element of dataSource) {
                        tableData.push({
                            "Master_Lab_ID": element["Master_Lab_ID"],
                            "courier_dispatch_time": element["courier_dispatch_time"],
                            "report_delivery_time": element["report_delivery_time"],
                            "specimen_accessioning_time": element["specimen_accessioning_time"],
                            "trf_scanning_time": element["trf_scanning_time"],
                            "trf_verification_time": element["trf_verification_time"],
                            "internal_TAT": element["internal_TAT"],
                            "porter_Service_TAT": element["porter_Service_TAT"],
                            "partner_TAT": element["partner_TAT"],
                            "trf_Entry_TAT": element["trf_Entry_TAT"]
                        });
                    }

                    table.appendRows(tableData);
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
    tableau.registerConnector(myConnector);
})();
