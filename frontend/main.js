const startBtn = document.getElementById("start-btn");
const stopBtn = document.getElementById("stop-btn");
const userTextElem = document.getElementById("user-text");
const assistantTextElem = document.getElementById("assistant-text");

let currentUtterance = null;
let queryCount = 0;
const MAX_QUERIES = 5;

async function sendQuery(text) {
  if (queryCount >= MAX_QUERIES) {
    alert("You have reached the maximum number of queries for this session.");
    return;
  }
  queryCount++;
  if (queryCount >= MAX_QUERIES) {
    startBtn.disabled = true;
    if (window.speechSynthesis.speaking) {
      window.speechSynthesis.cancel();
      currentUtterance = null;
    }
  }

  console.log(`Sending query #${queryCount}: ${text}`);
  const response = await fetch("http://localhost:8080/query/", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ text }),
  });
  const data = await response.json();
  // handle response
  return data;
}

// Web Speech API for speech-to-text
const recognition = new (window.SpeechRecognition ||
  window.webkitSpeechRecognition)();
recognition.lang = "en-US";
recognition.interimResults = false;

// Start button triggers recognition
startBtn.onclick = () => {
  if (window.speechSynthesis.speaking) {
    window.speechSynthesis.cancel(); // barge-in
    currentUtterance = null;
  }
  recognition.start();
};

stopBtn.onclick = () => {
  // Stop speech recognition
  recognition.stop();

  // Cancel any ongoing speech synthesis
  if (window.speechSynthesis.speaking) {
    window.speechSynthesis.cancel();
    currentUtterance = null;
  }
};

// Handle recognition results
recognition.onresult = async (event) => {
  const text = event.results[0][0].transcript;
  userTextElem.textContent = `You: ${text}`;

  // Send query to backend
  try {
    const data = await sendQuery(text);
    if (!data || !data.answer) {
      assistantTextElem.textContent = "No response from backend.";
      return;
    }

    assistantTextElem.textContent = `Assistant: ${data.answer}`;

    // Speak the assistant response
    currentUtterance = new SpeechSynthesisUtterance(data.answer);
    currentUtterance.onend = () => {
      currentUtterance = null;
    };
    window.speechSynthesis.speak(currentUtterance);
  } catch (err) {
    assistantTextElem.textContent = "Error communicating with backend.";
    console.error(err);
  }
};

// Optional: cancel TTS if user clicks start again (barge-in)
recognition.onstart = () => {
  if (window.speechSynthesis.speaking) {
    window.speechSynthesis.cancel();
    currentUtterance = null;
  }
};
