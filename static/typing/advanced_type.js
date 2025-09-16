document.addEventListener('DOMContentLoaded', function() {
  var testText = "Press start to fetch text from the server.";
  var ongoing = false;
  var timeStarted = null;
  var virtualBox = "";
  var incorrectCharCount = 0;
  var wordsEl = document.getElementById('words');
  var inputEl = document.getElementById('typing-input');
  var infoEl = document.getElementById('info');
  var startBtn = document.getElementById('start-btn');
  var resetBtn = document.getElementById('reset-btn');
  var wordCountEl = document.getElementById('word-count');
  var test = "tka";
  var name = document.getElementById('name').innerHTML;
  if (name === "" || name === "False") {
    window.location.href = "/onboarding";
  };

  document.getElementById('herotitle').addEventListener('click', function() {
    window.location.href = "/typing";
  });

  if (wordsEl) wordsEl.innerText = testText;
  inputEl.disabled=true;


  function sendResults(wpm, accuracy, time, mistakes, name) {
    fetch('/typing/submit_advanced', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
        'wpm': wpm,
        'accuracy': accuracy,
        'time': time,
        'name': name || 'Anonymous',
        'test': test,
        'words': testText.length
      }
      }).then(response => {
        if (response.redirected) {
          window.history.replaceState(null, "", response.url);
          window.location.href = response.url;
        }
    }).catch(error => console.error('Error:', error));
  }

  function calculateWPM(timeTakenMs, characters) {
    const minutes = timeTakenMs / 60000;
    if (!minutes || minutes <= 0) return 0;
    const words = characters / 5;
    const wpm = words / minutes;
    return Math.round(wpm);
  }

  function reset() {
    ongoing = false;
    timeStarted = null;
    virtualBox = "";
    incorrectCharCount = 0;
    inputEl.disabled=true;
    inputEl.setAttribute("placeholder", "Click start!")
    if (inputEl) inputEl.value = "";
    if (wordsEl) wordsEl.innerText = "Press start to fetch text from the server.";
    if (infoEl) infoEl.innerText = "";
    console.log('Reset was pressed! virtualBox is now:', virtualBox);
  }

  function fetchTest(test, wordCount) {
    // Corrected URL syntax to use a single '?'
    fetch(`/typing/generate_advanced?collection=${test}&word_count=${wordCount}`)
      .then(response => response.json())
      .then(data => {
        // Corrected variable name from 'textText' to 'testText'
        testText = data.text;
        console.log(data.text)
        wordsEl.innerText = testText;
        inputEl.setAttribute("placeholder", "Start typing here...");
        if (inputEl) inputEl.disabled = false;
        inputEl.focus();
      });
  }

  if (startBtn) startBtn.addEventListener('click', function() {
    reset();
    if (inputEl) inputEl.value = "";
    fetchTest(test, wordCountEl ? wordCountEl.value : 10);
    ongoing = true;
    timeStarted = new Date(); // Set timeStarted immediately on click
    if (inputEl) inputEl.focus();
  });

  if (resetBtn) resetBtn.addEventListener('click', function() { reset(); });

  if (inputEl) {
    inputEl.addEventListener('keydown', function(e) {
      if (e.ctrlKey && e.key === 'Backspace') {
        e.preventDefault();
        virtualBox = virtualBox.trimEnd();
        const lastSpaceIndex = virtualBox.lastIndexOf(' ');
        if (lastSpaceIndex !== -1) {
          virtualBox = virtualBox.substring(0, lastSpaceIndex);
        } else {
          virtualBox = "";
        }
        inputEl.value = virtualBox;
        console.log('Ctrl + Backspace was pressed! virtualBox is now:', virtualBox);
      }
    });
    let incorrectCharCount = 0;
    let incorrectCharIndexes = new Set();

    inputEl.addEventListener('input', function(e) {
      virtualBox = e.target.value;
      let highlightedText = '';
      incorrectCharIndexes.clear();

      for (let i = 0; i < testText.length; i++) {
        const char = testText[i];
        const typedChar = virtualBox[i];

        if (i < virtualBox.length) {
          if (char === typedChar) {
            highlightedText += `<span class="correct">${char}</span>`;
          } else {
            highlightedText += `<span class="incorrect">${char}</span>`;
            incorrectCharIndexes.add(i);
          }
        } else {
          highlightedText += `<span>${char}</span>`;
        }
      }

      incorrectCharCount = incorrectCharIndexes.size;

      if (wordsEl) wordsEl.innerHTML = highlightedText;

      if (virtualBox.length === testText.length && ongoing) {
        ongoing = false;
        const timeEnded = new Date();
        const timeTakenMs = timeEnded - timeStarted;
        const wpm = calculateWPM(timeTakenMs, testText.length);
        const seconds = Math.round((timeTakenMs / 1000) * 100) / 100;
        if (infoEl) infoEl.innerText = `Completed in ${seconds} seconds - ${wpm} WPM`;
        console.log('Time taken:', seconds, 'seconds');
        console.log(wpm, 'WPM');
        

        let correct = testText.length - incorrectCharIndexes.size; 
        let accuracy = Math.round((correct / testText.length) * 100);
        sendResults(wpm, accuracy, seconds, incorrectCharIndexes.size, name);
      }
    });
  }
});