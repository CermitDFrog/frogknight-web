
function confirmDelete(character_name) {
    // Create alert to confirm delete
    var x = confirm("Are you sure you want to delete " + character_name + "?");
    if (x) {
        document.getElementById("delete-form").submit();
    }
}