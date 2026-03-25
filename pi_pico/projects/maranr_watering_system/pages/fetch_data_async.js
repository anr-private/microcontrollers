// fetch_data_async.js


let isFetching = false;

async function fetchDataAsync(url, callbk) {
    console.log("fetchDataAsync@7  url=" + url);
    console.log("fetchDataAsync@8  isFetching=" + isFetching);

    if (isFetching) {
        console.log("fetchDataAsync@11 FETCHING IS ALREADY ACTIVE!");
        return;
    }
    isFetching = true;

    try {
        const response = await fetch(url);

        console.log("fetchDataAsync@19 got response:..."); console.log(response);

        if ( ! response.ok) {
            throw new Error(`HTTP error: ${response.status}`);
        }

        console.log("fetchDataAsync@25 AWAIT response:json");
        
        const data = await response.json();

        console.log("fetchDataAsync@29  data:..."); 
        console.log(data);

        callbk(data);

        console.log("fetchDataAsync@34 ALL DONE @@@@@@@@@@_______________@@@@@@@@@@@@@@@@@______________@@@@@@@@@@@");

        // Cannot return the data like this - because this function 
        // is async, the data gets wrapped in a Promise and the
        // caller must be async to unwrap it.
        ////return data

      } catch (error) {
          // Handle any errors that occurred during the fetch or processing
          console.error('fetchDataAsync@43 Error fetching data:', error);
          throw error; // Re-throw if necessary
      } finally {
          console.log("fetchDataAsync@46 FETCH COMPLETED.  RESETTING THE FLAG");
          isFetching = false;
      }
}

// ####

