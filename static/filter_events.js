document.addEventListener('DOMContentLoaded', () => { // code to execute when the DOM is fully loaded

  // 3-18 populates a dropdown menu with activity options
  const activityFilter = document.getElementById('activity_id');
  const applyFiltersButton = document.querySelector('#filter-form button');
  const eventsContainer = document.getElementById('event-container');

  console.log('Elements selected:', {
    activityFilter,
    applyFiltersButton,
    eventsContainer
  });

  // Load filter option on page load
  fetch('/get_activities')
      .then(response => response.json())
      /**
       * Populates the activity filter dropdown with options fetched from the server.
       * This code is executed when the DOM content is fully loaded.
       * 
       * The fetch request to '/get_activities' is made, and the response is parsed as JSON.
       * For each activity returned, a new <option> element is created and appended to the
       * 'activity_id' dropdown element.
       */
      .then(data => {
          data.forEach(activity => {
              let option = document.createElement('option');        
              option.value = activity.id;
              option.textContent = activity.name;
              activityFilter.appendChild(option);
          });
      });

  // 22-47 update the list of events displayed on the page based on the selected activity
  // Apply filters on button click
  applyFiltersButton.addEventListener('click', (event) => {
    event.preventDefault();
      const activityId = activityFilter.value;
      console.log('Selected Activity ID:', activityId);

      // Make AJAX request to fetch filtered events
      fetch('/filter_events', {
          method: 'POST',
          headers: {
              'Content-Type': 'application/json'
          },
          body: JSON.stringify({ activity_id: activityId })
      })

      // console.log dosen't work 
      .then(response => {
        console.log('Response status:', response.status); // Log status
        return response.json();
    })
      .then(events => {
        console.log('Filtered Events:', events);
          // Clear existing events
          eventsContainer.innerHTML = '';

          // Display filtered events
          events.forEach(event => {
              let eventDiv = document.createElement('li');
              eventDiv.className = 'event';
              eventDiv.innerHTML = `
                  <h2>${event.name}</h2>
                  <p>${event.description}</p>
                  <p>${event.date}</p>
              `;
              eventsContainer.appendChild(eventDiv);
          });
          console.log('Events added to the container');
      });
  });
});


// JavaScript for updating status on button click
// Select the button element from the document using its ID 'update-status'
const updateStatusButton = document.querySelector('#update-status'); 
// Attach a click event listener to the button
updateStatusButton.addEventListener('click', () => {
  // Create a query string with the order parameter
  const queryString = new URLSearchParams({ order: 123 }).toString();
  // Construct the URL for the status endpoint with query parameters
  const url = `/status?${queryString}`;

  // Send a GET request to the status endpoint
  fetch(url)
    .then(response => response.text()) // Convert the response to text
    .then(status => {
      // Update the status in the HTML element with ID 'order-status'
      document.querySelector('#order-status').innerHTML = status;
    });
});


// Fetch data from another URL and update a div with the response data
// Send a GET request to '/some-url'
fetch('/some-url')
  .then(response => response.json()) // Convert the response to JSON
  .then(responseData => {
    // Update the text content of the HTML element with ID 'my-div'
    document.querySelector('#my-div').innerText = JSON.stringify(responseData);
  });
