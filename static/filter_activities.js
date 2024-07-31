const activityFilter = document.getElementById('category_id');
const applyFiltersButton = document.querySelector('#filter-form button');
const activitiesContainer = document.getElementById('activity-container');

// Apply filters on button click
applyFiltersButton.addEventListener('click', (event) => {
  event.preventDefault();
  const categoryId = activityFilter.value;
  console.log('Selected Category ID:', categoryId);

  // Make AJAX request to fetch filtered activities
  fetch('/filter_activities', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({ category_id: categoryId })
  })
  .then(response => {
    console.log('Response status:', response.status); // Log status
    return response.json();
  })
  .then(activities => {
    console.log('Filtered activities:', activities);
    // Check if activitiesContainer exists before clearing
    if (activitiesContainer) {
      // Clear existing activities
      activitiesContainer.innerHTML = '';
      // Continue with populating the container
    } else {
      console.error('Activity container not found');
    }

    // Display filtered activities
    activities.forEach(activity => { // Changed from 'event' to 'activity'
      let activityDiv = document.createElement('li');
      activityDiv.className = 'activity'; // Changed from 'event' to 'activity'
      activityDiv.innerHTML = `
        <h2>${activity.name}</h2>
        <p>${activity.description}</p>
      `;
      activitiesContainer.appendChild(activityDiv);
    });
    console.log('Activities added to the container');
  });
});