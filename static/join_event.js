function joinEvent(eventId) {
  console.log('Joining event with ID:', eventId);

  fetch(`/join_event/${eventId}`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({}), 
  })
  .then(response => response.json())
  .then(data => {
    if (data.success) {
      alert(data.message);  // Use the message from the JSON response
    } else {
      alert('Failed to join the event: ' + data.message);
    }
  })
  .catch(error => {
    console.error('Error joining event:', error);
    alert('An error occurred while joining the event.');
  });
}
  