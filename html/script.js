function test(id) {
  var change = document.getElementById(id);

  if (change.style.display == "none") {
    change.style.display = "block";
    
  } else {
    change.style.display = "none";
    
  }
}

function attachments_display(id) {
  var attachments_change = document.getElementById(id);

  if (attachments_change.style.display == "none") {
    attachments_change.style.display = "flex";
  } else {
    attachments_change.style.display = "none";
  }
}
