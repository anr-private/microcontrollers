// fetch_data_and_update.js

// Function to fetch data from the server and update the page
// See ex_get_data_from_server.html for an example.
// Typical use: 
/*
    <script src="fetch_data_and_update.js"></script>
    <script>
        const dataUrl = "data?a=123"
        // Use setInterval to call fetchDataAndUpdate every 3000 milliseconds (3 seconds)
        // This function will run repeatedly until the window is closed or clearInterval() is called.
        // In order to pass an arg to the function, we use an anonymous go-between function.
        const intervalId = setInterval(
            () =>   {  fetchDataAndUpdate(dataUrl); },  // anon funct calls fetch w URL arg
            3000);
        // Optional: call immed when page loads
        console.log("FIRST CALL TO THE FETCH");
        fetchDataAndUpdate(dataUrl);

        function handle_fetched_data(data) { // handle the received data
            var elt = document.getElementById('data-container');
            elt.innerText = `Age:${data.age} Name: ${data.name}  Date: ${data.datetime} `;
        }
*/

function fetchDataAndUpdate(dataUrl) {
    // In a real application, you would replace this URL with your server endpoint
    // For this example, we simulate fetching the current time
    ////const dataUrl = 'data?a=123'; 

    console.log("fetchDataAndUpdate START FETCH url=" + dataUrl);

    fetch(dataUrl)
      .then(response => {
        // response.json() is called here and returns a new Promise
        /*
            console.log("FETCH-THEN");
            console.log(response);
        */
        //var jsjs = response.json();
        //console.log(jsjs);
        //return jsjs;
        return response.json(); 
      })
      .then(data => {
        // This .then() receives the *resolved value* of the Promise
        // returned by response.json(). 'data' is now your JavaScript object.
        /*
            console.log("THEN-DATA");
            console.log(typeof data);
            console.log(data);
        */
            console.log("AGE and NAME and DATETIME");
            console.log(data.age);
            console.log(data.name);
            console.log(data.datetime);
        
            handle_fetched_data(data);

        ////var elt = document.getElementById('data-container');
        ////elt.innerText = `Age:${data.age} Name: ${data.name}  Date: ${data.datetime} `;
      })
      .catch(error => {
        // Handle any errors that occur during the fetch or JSON parsing
        console.error('fetch_data_and_update.js Error:', error); 
      });
}

