

function showToast(message) {
    const toast = document.getElementById('toast');
    toast.querySelector('.toast-content p').textContent = message;
    toast.classList.remove('hide');
    setTimeout(() => {
      toast.classList.add('hide');
    }, 3000); // Hide after 3 seconds
  }
  
  // Example usage: Call showToast when an action is completed
  // This function can be called after a fetch request or other actions
  document.getElementById('some-action-button').addEventListener('click', () => {
    showToast('Challenge marked as done!');
  });