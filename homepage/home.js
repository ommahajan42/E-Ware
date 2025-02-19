const scrollArea = document.getElementById("scrollArea");
let isDown = false;
let startX;
let scrollLeft;

scrollArea.addEventListener("mousedown", (e) => {
    isDown = true;
    scrollArea.style.cursor = "grabbing";
    startX = e.pageX - scrollArea.offsetLeft;
    scrollLeft = scrollArea.scrollLeft;
});

scrollArea.addEventListener("mouseleave", () => {
    isDown = false;
    scrollArea.style.cursor = "grab";
});

scrollArea.addEventListener("mouseup", () => {
    isDown = false;
    scrollArea.style.cursor = "grab";
});

scrollArea.addEventListener("mousemove", (e) => {
    if (!isDown) return;
    e.preventDefault();
    const x = e.pageX - scrollArea.offsetLeft;
    const walk = (x - startX) * 2;
    scrollArea.scrollLeft = scrollLeft - walk;
});
function toggleDropdown() {
    var dropdown = document.getElementById("dropdownMenu");
    dropdown.style.display = dropdown.style.display === "block" ? "none" : "block";
}
window.onclick = function(event) {
    if (!event.target.closest('.profile-container')) {
        document.getElementById("dropdownMenu").style.display = "none";
    }
}
