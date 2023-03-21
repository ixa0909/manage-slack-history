
function test(id) {
  var change = document.getElementById(id);

  if (change.style.display == "block") {
    change.style.display = "none";
  } else {
    change.style.display = "block";
  }
}
