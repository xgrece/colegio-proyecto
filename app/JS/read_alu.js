function showUpdateForm(id) {
  document.getElementById("updateId").value = id;
  document.getElementById("updateForm").style.display = "block";
  document.getElementById("deleteForm").style.display = "none";
}

function showDeleteForm(id) {
  document.getElementById("deleteId").value = id;
  document.getElementById("deleteForm").style.display = "block";
  document.getElementById("updateForm").style.display = "none";
}

function hideUpdateForm() {
  document.getElementById("updateForm").style.display = "none";
}

function hideDeleteForm() {
  document.getElementById("deleteForm").style.display = "none";
}
