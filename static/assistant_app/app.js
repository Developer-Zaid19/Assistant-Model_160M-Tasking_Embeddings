const modeButtons = document.querySelectorAll(".mode-button");
const panels = {
  chat: document.querySelector("#chat-panel"),
  embedding: document.querySelector("#embedding-panel"),
  task: document.querySelector("#task-panel"),
};

const chatForm = document.querySelector("#chat-form");
const chatInput = document.querySelector("#chat-input");
const conversation = document.querySelector("#conversation");
const embeddingForm = document.querySelector("#embedding-form");
const embeddingInput = document.querySelector("#embedding-input");
const vectorPreview = document.querySelector("#vector-preview");
const copyButton = document.querySelector("#copy-vector");
const taskingForm = document.querySelector("#tasking-form");
const taskingInput = document.querySelector("#tasking-input");
const taskingPreview = document.querySelector("#tasking-preview");

let currentVector = "";

function csrfToken() {
  return document.querySelector("[name=csrfmiddlewaretoken]").value;
}

function setMode(mode) {
  modeButtons.forEach((button) => button.classList.toggle("active", button.dataset.mode === mode));
  Object.entries(panels).forEach(([key, panel]) => panel.classList.toggle("active", key === mode));
}

function addBubble(role, text, meta = "") {
  const bubble = document.createElement("div");
  bubble.className = `bubble ${role}`;
  bubble.innerHTML = `<span class="label">${meta || (role === "user" ? "You" : "Model")}</span><p></p>`;
  bubble.querySelector("p").textContent = text;
  conversation.appendChild(bubble);
  conversation.scrollTop = conversation.scrollHeight;
}

async function postJson(url, payload) {
  const response = await fetch(url, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": csrfToken(),
    },
    body: JSON.stringify(payload),
  });

  const data = await response.json();
  if (!response.ok) {
    throw new Error(data.error || "Request failed");
  }
  return data;
}

modeButtons.forEach((button) => {
  button.addEventListener("click", () => setMode(button.dataset.mode));
});

chatForm.addEventListener("submit", async (event) => {
  event.preventDefault();
  const message = chatInput.value.trim();
  if (!message) return;

  const button = chatForm.querySelector("button");
  button.disabled = true;
  button.textContent = "Thinking...";
  addBubble("user", message, "You");
  chatInput.value = "";

  try {
    const data = await postJson("/api/chat/", { message });
    addBubble("assistant", data.reply, `${data.model} - ${data.generation_time_ms} ms`);
  } catch (error) {
    addBubble("assistant", error.message, "Error");
  } finally {
    button.disabled = false;
    button.textContent = "Send";
  }
});

embeddingForm.addEventListener("submit", async (event) => {
  event.preventDefault();
  const text = embeddingInput.value.trim();
  if (!text) return;

  const button = embeddingForm.querySelector("button");
  button.disabled = true;
  button.textContent = "Generating...";
  copyButton.disabled = true;
  vectorPreview.textContent = "Generating embedding...";

  try {
    const data = await postJson("/api/embed/", { text });
    currentVector = JSON.stringify(data.embedding);
    vectorPreview.textContent = `${data.model} - ${data.dimension} dimensions - ${data.generation_time_ms} ms\n${data.preview}`;
    copyButton.disabled = false;
  } catch (error) {
    currentVector = "";
    vectorPreview.textContent = error.message;
  } finally {
    button.disabled = false;
    button.textContent = "Generate Embedding";
  }
});

taskingForm.addEventListener("submit", async (event) => {
  event.preventDefault();
  const text = taskingInput.value.trim();
  if (!text) return;

  const button = taskingForm.querySelector("button");
  button.disabled = true;
  button.textContent = "Running...";
  taskingPreview.textContent = "Generating task embedding and matching...";

  try {
    const data = await postJson("/api/task/", { text });
    const summary = data.wikipedia_summary ? `\nWikipedia: ${data.wikipedia_summary}` : "";
    taskingPreview.textContent = [
      `${data.model} - ${data.generation_time_ms} ms`,
      `Matched: ${data.matched_task.task}`,
      `Type: ${data.matched_task.type}`,
      `Cosine similarity: ${data.similarity}`,
      `Action: ${data.action_result}${summary}`,
    ].join("\n");
  } catch (error) {
    taskingPreview.textContent = error.message;
  } finally {
    button.disabled = false;
    button.textContent = "Run Task";
  }
});

copyButton.addEventListener("click", async () => {
  if (!currentVector) return;
  await navigator.clipboard.writeText(currentVector);
  copyButton.textContent = "Copied";
  setTimeout(() => {
    copyButton.textContent = "Copy Vector";
  }, 1200);
});
