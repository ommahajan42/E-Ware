
function toggleDropdown() {
    var dropdown = document.getElementById("dropdownMenu");
    dropdown.style.display = dropdown.style.display === "block" ? "none" : "block";
}
window.onclick = function(event) {
    if (!event.target.closest('.profile-container')) {
        document.getElementById("dropdownMenu").style.display = "none";
    }
}