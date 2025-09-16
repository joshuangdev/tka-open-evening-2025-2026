/*document.addEventListener('DOMContentLoaded', function() {
    if (Boolean("{{askname}}") === true) {
        var name = prompt("Please enter your name:", "Anonymous");
        document.getElementById("name").innerHTML = name || "Anonymous";
    }
})*/

document.getElementById('herotitle').addEventListener('click', function() {
    window.location.href = "/typing";
  });

document.getElementById("tryagain-btn").addEventListener("click", function() {
    window.location.href = `/typing?name=${document.getElementById("name").innerHTML}`;
});
document.getElementById("startover-btn").addEventListener("click", function() {
    window.location.href = "/onboarding";
});