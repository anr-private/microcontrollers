// fetch_data_async.js


let isFetching = false;

async function fetchDataAsync(url, callbk) {
    console.log("fetchDataAsync@7  url=" + url);
    console.log("fetchDataAsync@8  isFetching=" + isFetching);

    if (isFetching) {
        console.log("fetchDataAsync@8 FETCHING IS ALREADY ACTIVE!");
        return;
    }
    isFetching = true;

    try {
        const response = await fetch(url);

        console.log("fetchDataAsync@9 got response:..."); console.log(response);

        if ( ! response.ok) {
            throw new Error(`HTTP error: ${response.status}`);
        }

        console.log("fetchDataAsync@16 AWAIT response:json");
        
        const data1 = await response.json();

        console.log("fetchDataAsync@20  data1:..."); 
        console.log(data1);

        //const data2 = await data1;
        const data2 = data1;

        // Use the 'data' here
        console.log("fetchDataAsync@27  data2:..."); 
        console.log(data2);
        callbk(data2);

        console.log("fetchDataAsync@31 ALL DONE @@@@@@@@@@_______________@@@@@@@@@@@@@@@@@______________@@@@@@@@@@@");

        //@@@@return data2;

      } catch (error) {
          // Handle any errors that occurred during the fetch or processing
          console.error('fetchDataAsync@26 Error fetching data:', error);
          throw error; // Re-throw if necessary
      } finally {
          console.log("fetchDataAsync@49 FETCH COMPLETED.  RESETTING THE FLAG");
          isFetching = false;
      }
}

// How to use the async function
// data = fetchData('https://api.example.com/data');

