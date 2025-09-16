document.addEventListener('DOMContentLoaded', function() {
    document.getElementById('seconds-left').innerText = 15;
    setInterval(() => {
        let current = parseInt(document.getElementById('seconds-left').innerText);
        if (current === 1) {
            location.reload();
        }
        document.getElementById('seconds-left').innerText = current - 1;
    }, 1000);
      document.getElementById('herotitle').addEventListener('click', function() {
    window.location.href = "/typing";
  });
});