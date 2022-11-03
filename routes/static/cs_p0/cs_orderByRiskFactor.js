(function() {
    'use strict';

    const config = {
        apiUrl: '/api/v2/csP0Dashboard/orderByRiskFactor'
    }; 


    $(document).ready(function() {
        // Not essential, just check cookie exist or not.
        const accessToken = Cookies.get("accessToken");
        const hasAuth = accessToken && accessToken.length > 0;
        updateUIWithAuthState(hasAuth);
        
        $("#submitButton").click(function() {
            console.log("It is working!");
            tableau.connectionName = "cs_orderByRiskFactor"; // This will be the data source name in Tableau
            tableau.submit(); // This sends the connector object to Tableau
        });
    });

    // ------- UI controled by javascript side from the index.html, not Flask session side. ------ //
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
        tableau.abortForAuth()
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
            id: "specimen_accessioning_time",
            dataType: tableau.dataTypeEnum.datetime
        }, {
            id: "trf_verification_time",
            dataType: tableau.dataTypeEnum.datetime
        }, {
            id: "current_smoker",
                dataType: tableau.dataTypeEnum.string
        }, {
            id: "current_symptoms_opt_0",
                dataType: tableau.dataTypeEnum.string
        }, {
            id: "current_symptoms_opt_1",
                dataType: tableau.dataTypeEnum.string
        }, {
            id: "current_symptoms_opt_2",
                dataType: tableau.dataTypeEnum.string
        }, {
            id: "current_symptoms_opt_3",
                dataType: tableau.dataTypeEnum.string
        }, {
            id: "current_symptoms_opt_4",
                dataType: tableau.dataTypeEnum.string
        }, {
            id: "current_symptoms_opt_5",
                dataType: tableau.dataTypeEnum.string
        }, {
            id: "current_symptoms_opt_6",
                dataType: tableau.dataTypeEnum.string
        }, {
            id: "current_symptoms_opt_7",
                dataType: tableau.dataTypeEnum.string
        }, {
            id: "current_symptoms_opt_8",
                dataType: tableau.dataTypeEnum.string
        }, {
            id: "current_symptoms_opt_9",
                dataType: tableau.dataTypeEnum.string
        }, {
            id: "current_symptoms_opt_10",
                dataType: tableau.dataTypeEnum.string
        }, {
            id: "current_symptoms_opt_11",
                dataType: tableau.dataTypeEnum.string
        }, {
            id: "current_symptoms_opt_12",
                dataType: tableau.dataTypeEnum.string
        }, {
            id: "current_symptoms_opt_13",
                dataType: tableau.dataTypeEnum.string
        }, {
            id: "current_symptoms_opt_14",
                dataType: tableau.dataTypeEnum.string
        }, {
            id: "current_symptoms_opt_15",
                dataType: tableau.dataTypeEnum.string
        }, {
            id: "current_symptoms_opt_16",
                dataType: tableau.dataTypeEnum.string
        }, {
            id: "current_symptoms_opt_17",
                dataType: tableau.dataTypeEnum.string
        }, {
            id: "current_symptoms_opt_18",
                dataType: tableau.dataTypeEnum.string
        }, {
            id: "current_symptoms_opt_19",
                dataType: tableau.dataTypeEnum.string
        }, {
            id: "current_symptoms_opt_20",
                dataType: tableau.dataTypeEnum.string
        }, {
            id: "current_symptoms_opt_21",
                dataType: tableau.dataTypeEnum.string
        }, {
            id: "family_history_of_npc_opt_0",
                dataType: tableau.dataTypeEnum.string
        }, {
            id: "family_history_of_npc_opt_1",
                dataType: tableau.dataTypeEnum.string
        }, {
            id: "family_history_of_npc_opt_2",
                dataType: tableau.dataTypeEnum.string
        }, {
            id: "family_history_of_npc_opt_3",
                dataType: tableau.dataTypeEnum.string
        }, {
            id: "family_history_of_npc_opt_4",
                dataType: tableau.dataTypeEnum.string
        }, {
            id: "family_history_of_npc_opt_5",
                dataType: tableau.dataTypeEnum.string
        }, {
            id: "family_history_of_npc_opt_6",
                dataType: tableau.dataTypeEnum.string
        }, {
            id: "family_history_of_npc_opt_7",
                dataType: tableau.dataTypeEnum.string
        }, {
            id: "family_history_of_npc_opt_8",
                dataType: tableau.dataTypeEnum.string
        }, {
            id: "family_history_of_npc_opt_9",
                dataType: tableau.dataTypeEnum.string
        }, {
            id: "previous_npc_screen_opt_0",
                dataType: tableau.dataTypeEnum.string
        }, {
            id: "previous_npc_screen_opt_1",
                dataType: tableau.dataTypeEnum.string
        }, {
            id: "previous_npc_screen_opt_2",
                dataType: tableau.dataTypeEnum.string
        }, {
            id: "previous_npc_screen_opt_3",
                dataType: tableau.dataTypeEnum.string
        }, {
            id: "previous_npc_screen_opt_4",
                dataType: tableau.dataTypeEnum.string
        }, {
            id: "previous_npc_screen_opt_5",
                dataType: tableau.dataTypeEnum.string
        }, {
            id: "previous_npc_screen_opt_6",
                dataType: tableau.dataTypeEnum.string
        }, {
            id: "previous_npc_screen_opt_7",
                dataType: tableau.dataTypeEnum.string
        }, {
            id: "previous_npc_screen_opt_8",
                dataType: tableau.dataTypeEnum.string
        }, {
            id: "previous_npc_screen_opt_9",
                dataType: tableau.dataTypeEnum.string
        }, {
            id: "previous_npc_screen_opt_10",
                dataType: tableau.dataTypeEnum.string
        }, {
            id: "previous_npc_screen_opt_11",
                dataType: tableau.dataTypeEnum.string
        }];

        
        const tableSchema = {
            id: "byRiskFactor",
            alias: "Schema for By Risk Factor",
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
                            "specimen_accessioning_time": element["specimen_accessioning_time"],
                            "trf_verification_time": element["trf_verification_time"],
                            "current_smoker": element["current_smoker"],
                            "current_symptoms_opt_0": element["current_symptoms_opt_0"],
                            "current_symptoms_opt_1": element["current_symptoms_opt_1"],
                            "current_symptoms_opt_2": element["current_symptoms_opt_2"],
                            "current_symptoms_opt_3": element["current_symptoms_opt_3"],
                            "current_symptoms_opt_4": element["current_symptoms_opt_4"],
                            "current_symptoms_opt_5": element["current_symptoms_opt_5"],
                            "current_symptoms_opt_6": element["current_symptoms_opt_6"],
                            "current_symptoms_opt_7": element["current_symptoms_opt_7"],
                            "current_symptoms_opt_8": element["current_symptoms_opt_8"],
                            "current_symptoms_opt_9": element["current_symptoms_opt_9"],
                            "current_symptoms_opt_10": element["current_symptoms_opt_10"],
                            "current_symptoms_opt_11": element["current_symptoms_opt_11"],
                            "current_symptoms_opt_12": element["current_symptoms_opt_12"],
                            "current_symptoms_opt_13": element["current_symptoms_opt_13"],
                            "current_symptoms_opt_14": element["current_symptoms_opt_14"],
                            "current_symptoms_opt_15": element["current_symptoms_opt_15"],
                            "current_symptoms_opt_16": element["current_symptoms_opt_16"],
                            "current_symptoms_opt_17": element["current_symptoms_opt_17"],
                            "current_symptoms_opt_18": element["current_symptoms_opt_18"],
                            "current_symptoms_opt_19": element["current_symptoms_opt_19"],
                            "current_symptoms_opt_20": element["current_symptoms_opt_20"],
                            "current_symptoms_opt_21": element["current_symptoms_opt_21"],
                            "family_history_of_npc_opt_0": element["family_history_of_npc_opt_0"],
                            "family_history_of_npc_opt_1": element["family_history_of_npc_opt_1"],
                            "family_history_of_npc_opt_2": element["family_history_of_npc_opt_2"],
                            "family_history_of_npc_opt_3": element["family_history_of_npc_opt_3"],
                            "family_history_of_npc_opt_4": element["family_history_of_npc_opt_4"],
                            "family_history_of_npc_opt_5": element["family_history_of_npc_opt_5"],
                            "family_history_of_npc_opt_6": element["family_history_of_npc_opt_6"],
                            "family_history_of_npc_opt_7": element["family_history_of_npc_opt_7"],
                            "family_history_of_npc_opt_8": element["family_history_of_npc_opt_8"],
                            "family_history_of_npc_opt_9": element["family_history_of_npc_opt_9"],
                            "previous_npc_screen_opt_0": element["previous_npc_screen_opt_0"],
                            "previous_npc_screen_opt_1": element["previous_npc_screen_opt_1"],
                            "previous_npc_screen_opt_2": element["previous_npc_screen_opt_2"],
                            "previous_npc_screen_opt_3": element["previous_npc_screen_opt_3"],
                            "previous_npc_screen_opt_4": element["previous_npc_screen_opt_4"],
                            "previous_npc_screen_opt_5": element["previous_npc_screen_opt_5"],
                            "previous_npc_screen_opt_6": element["previous_npc_screen_opt_6"],
                            "previous_npc_screen_opt_7": element["previous_npc_screen_opt_7"],
                            "previous_npc_screen_opt_8": element["previous_npc_screen_opt_8"],
                            "previous_npc_screen_opt_9": element["previous_npc_screen_opt_9"],
                            "previous_npc_screen_opt_10": element["previous_npc_screen_opt_10"],
                            "previous_npc_screen_opt_11": element["previous_npc_screen_opt_11"]
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
