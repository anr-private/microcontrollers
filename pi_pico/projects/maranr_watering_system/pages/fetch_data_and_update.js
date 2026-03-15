// fetch_data_and_update.js

// Function to fetch data from the server and update the page
function fetchDataAndUpdate() {
    // In a real application, you would replace this URL with your server endpoint
    // For this example, we simulate fetching the current time
    const dataUrl = 'data?a=123'; 

    //console.log("@@@@ START FETCH function");

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
        
        var elt = document.getElementById('data-container');
        elt.innerText = `Age:${data.age} Name: ${data.name}  Date: ${data.datetime} `;
      })
      .catch(error => {
        // Handle any errors that occur during the fetch or JSON parsing
        console.error('Error:', error); 
      });
}

