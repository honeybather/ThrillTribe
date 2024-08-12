console.log('hi');
const activityFilter = document.getElementById('category_id');
const applyFiltersButton = document.querySelector('#filter-form button');
const activitiesContainer = document.getElementById('activity-container');

applyFiltersButton.addEventListener('click', (event) => {
  event.preventDefault();
  const categoryId = activityFilter.value;
  console.log('Selected Category ID:', categoryId);

  fetch('/filter_activities', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({ category_id: categoryId })
  })
  .then(response => {
    console.log('Response status:', response.status); 
    return response.json();
  })
  .then(activities => {
    console.log('Filtered activities:', activities);
    // check if activitiesContainer exists before clearing
    if (activitiesContainer) {
      // clear existing activities
      activitiesContainer.innerHTML = '';
      
      // display filtered activities with links and images
      activities.forEach(activity => { 
        let activityDiv = document.createElement('div');
        activityDiv.className = 'gallery'; 
        activityDiv.innerHTML = `
          <a href="/activities/${activity.id}">
            <img src="${activity.imgURL}" alt="${activity.name}">
            <div class="desc">${activity.name}</div>
          </a>
        `;
        activitiesContainer.appendChild(activityDiv);
      });
      console.log('Activities added to the container');
    } else {
      console.error('Activity container not found');
    }
  });
});