document.getElementById("analyzeBtn").addEventListener("click", async () => {
  const comment = document.getElementById("comment").value.trim();
  const resultBox = document.getElementById("result");
  const emoji = document.getElementById("emoji");
  const progress = document.getElementById("progress");
  const confidenceText = document.getElementById("confidence");

  if (!comment) return alert("Please type a comment!");

  resultBox.classList.remove("hidden");
  emoji.textContent = "🔍";
  progress.style.width = "0%";
  confidenceText.textContent = "Analyzing...";

  const response = await fetch("http://127.0.0.1:8000/predict", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ text: comment }),
  });

  const data = await response.json();

  const confidence = (data.confidence * 100).toFixed(1);
  const isToxic = data.is_toxic;

  // Emoji
  emoji.textContent = isToxic ? "😡" : "😇";

  // Progress bar
  progress.style.width = confidence + "%";
  progress.style.background = isToxic
    ? "linear-gradient(to right, #f87171, #dc2626)"
    : "linear-gradient(to right, #4ade80, #16a34a)";

  // Confidence text
  confidenceText.textContent = `${confidence}% ${isToxic ? "Toxic" : "Clean"}`;
});
