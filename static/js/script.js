const deleteModal = new bootstrap.Modal(document.getElementById("deleteModal"));
const deleteButtons = document.getElementsByClassName("btn-delete");
const deleteConfirm = document.getElementById("deleteConfirm");
for (let button of deleteButtons) {
  button.addEventListener("click", (e) => {
    let postSlug = e.target.getAttribute("data-post_id");
    deleteConfirm.href = `${postSlug}/delete/`;
    deleteModal.show();
  });
}