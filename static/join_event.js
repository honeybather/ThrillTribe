console.log('hey')
function joinEvent(eventId) {
    // implement the join event functionality
    console.log('Joining event with ID:', eventId);
    fetch(`/join_event/${eventId}`, {  // use backtick, to take value and plot it to the string 
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({  }), // can pass in variable 
    })
    .then(response => response.json())
    .then(data => {
      if (data.success) {
        alert('You have successfully joined the event!');
      } else {
        alert('Failed to join the event.' + data.message);
      }
    })
  }
  