const filterForm = document.querySelector('#filter-form');

filterForm.addEventListener('submit', (event) => {
  event.preventDefault();

  // Create a JSON object with form values
  const formData = {
    activity_id: document.querySelector('#activity_id').value,
    date: document.querySelector('#date').value
  };

  // Send a POST request with JSON data
  fetch('/filter_events', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(formData)
  })
  .then(response => response.json())
  .then(events => {
    const eventContainer = document.querySelector('#event-container');
    eventContainer.innerHTML = '';

    events.forEach(event => {
      const eventElement = document.createElement('div');
      eventElement.classList.add('event');
      eventElement.innerHTML = `
        <h2>${event.title}</h2>
        <p>${event.description}</p>
        <p>Date: ${new Date(event.date).toLocaleDateString()}</p>
        <p>Location: ${event.location}</p>
        <p>Cost: $${event.cost}</p>
      `;
      eventContainer.appendChild(eventElement);
    });
  })
  .catch(error => {
    console.error('Error:', error);
  });
});


// JavaScript for updating status on button click

// Select the button element from the document using its ID 'update-status'
const button = document.querySelector('#update-status');

// Attach a click event listener to the button
button.addEventListener('click', () => {
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

