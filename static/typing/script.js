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

  if (wordsEl) wordsEl.innerText = testText;

  function sendResults(wpm, accuracy, time, mistakes) {
    document.getElementById("wpm-field").value = wpm;
    document.getElementById("accuracy-field").value = accuracy;
    document.getElementById("time-field").value = time;
    document.getElementById("mistakes-field").value = mistakes;
    document.getElementById("results-form").submit();
}


  function parseText(text = testText, wordCount = 10) {
    const words = (text || "").split(',');
    const limitedWords = words.slice(0, Number(wordCount) || 10);
    return limitedWords.join(' ');
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
    if (inputEl) inputEl.value = "";
    if (wordsEl) wordsEl.innerText = "Press start to fetch text from the server.";
    if (infoEl) infoEl.innerText = "";
    console.log('Reset was pressed! virtualBox is now:', virtualBox);
  }

  if (startBtn) startBtn.addEventListener('click', function() {
    reset();
    if (inputEl) inputEl.value = "";
    fetch('/typing/generate?collection=food')
      .then(response => response.json())
      .then(data => {
        testText = parseText(data.text[0], wordCountEl ? wordCountEl.value : 10);
        if (wordsEl) wordsEl.innerText = testText;
      });
    ongoing = true;
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

    inputEl.addEventListener('input', function(e) {
      virtualBox = e.target.value;
      if (!timeStarted && virtualBox.length > 0) timeStarted = new Date();
      let highlightedText = '';
      for (let i = 0; i < testText.length; i++) {
        const char = testText[i];
        const typedChar = virtualBox[i];
        if (i < virtualBox.length) {
          if (char === typedChar) {
            highlightedText += `<span class="correct">${char}</span>`;
          } else {
            highlightedText += `<span class="incorrect">${char}</span>`;
            incorrectCharCount += 1;
          }
        } else {
          highlightedText += `<span>${char}</span>`;
        }
      }
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
        let correct = testText.length - incorrectCharCount;
        let accuracy = Math.round((correct / testText.length) * 100);
        //let mistakesDisplay = `${incorrectCharCount}/${testText.length}`;
        sendResults(wpm, accuracy, seconds, incorrectCharCount);
      }
    });
  }
});
