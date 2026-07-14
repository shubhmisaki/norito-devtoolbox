(function () {
  const els = {
    text: document.getElementById("textInput"),
    words: document.getElementById("statWords"),
    sentences: document.getElementById("statSentences"),
    paragraphs: document.getElementById("statParagraphs"),
    readingTime: document.getElementById("statReadingTime"),
    speakingTime: document.getElementById("statSpeakingTime"),
    chars: document.getElementById("statChars"),
  };

  const WORDS_PER_MINUTE_READING = 225;
  const WORDS_PER_MINUTE_SPEAKING = 130;

  function fmtMinutes(words, wpm) {
    const totalSeconds = Math.round((words / wpm) * 60);
    if (totalSeconds < 60) return `${totalSeconds} sec`;
    const mins = Math.floor(totalSeconds / 60);
    const secs = totalSeconds % 60;
    return secs === 0 ? `${mins} min` : `${mins} min ${secs} sec`;
  }

  function update() {
    const text = els.text.value;
    const trimmed = text.trim();
    const words = trimmed ? trimmed.split(/\s+/).length : 0;
    // Sentence boundary: a run of . ! or ? followed by whitespace or end of
    // string. Not linguistically perfect (abbreviations like "Mr." will
    // over-count), but a reasonable approximation without a full NLP model.
    const sentences = trimmed ? (trimmed.match(/[^.!?]+[.!?]+(\s|$)/g) || (trimmed ? [trimmed] : [])).length : 0;
    const paragraphs = trimmed ? trimmed.split(/\n\s*\n/).filter((p) => p.trim()).length : 0;

    els.words.textContent = words.toLocaleString();
    els.sentences.textContent = sentences.toLocaleString();
    els.paragraphs.textContent = paragraphs.toLocaleString();
    els.chars.textContent = text.length.toLocaleString();
    els.readingTime.textContent = words ? fmtMinutes(words, WORDS_PER_MINUTE_READING) : "0 sec";
    els.speakingTime.textContent = words ? fmtMinutes(words, WORDS_PER_MINUTE_SPEAKING) : "0 sec";
  }

  els.text.addEventListener("input", update);
  update();
})();
