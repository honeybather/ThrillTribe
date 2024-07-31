function markAsCompleted(bucketListId) {
    fetch(`/bucket_list/complete/${bucketListId}`, {
        method: 'POST',
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            document.getElementById(`bucket-list-${bucketListId}`).checked = true;
            showSnackbar();
        }
    })
    .catch(error => console.error('Error:', error));
}

function showSnackbar() {
    var x = document.getElementById("snackbar");
    x.className = "show";
    setTimeout(function(){ x.className = x.className.replace("show", ""); }, 3000);
}


function myFunction() {
    // Get the snackbar DIV
    var x = document.getElementById("snackbar");
  
    // Add the "show" class to DIV
    x.className = "show";
  
    // After 3 seconds, remove the show class from DIV
    setTimeout(function(){ x.className = x.className.replace("show", ""); }, 3000);
  }