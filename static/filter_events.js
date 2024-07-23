// tada

const activityFilter = document.getElementById('activity_id');
const applyFiltersButton = document.querySelector('#filter-form button');
const eventsContainer = document.getElementById('event-container');

  // list of events displayed on the page based on the selected activity
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
      })
  })
