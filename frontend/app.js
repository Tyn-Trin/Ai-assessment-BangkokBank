const form = document.getElementById("query-form");
const input = document.getElementById("query-input");
const submitBtn = document.getElementById("submit-btn");
const result = document.getElementById("result");
const evidencePanel = document.getElementById("evidence-panel");
const sampleQueries = document.getElementById("sample-queries");
const kbToggle = document.getElementById("kb-toggle");
const kbRegister = document.getElementById("kb-register");

const EMPTY_EVIDENCE_HTML =
  '<p class="state-empty" style="border:none; padding:0;">ยังไม่มีคำถาม — เมื่อมีคำตอบ ระบบจะแสดงต้นฉบับนโยบายที่ใช้ตอบไว้ที่นี่</p>';

kbRegister.innerHTML = KNOWLEDGE_BASE_CHUNKS.map(
  (chunk, i) => `
    <div class="kb-clause">
      <span class="kb-clause-number">${String(i + 1).padStart(2, "0")}</span>
      <p class="kb-clause-text">${chunk}</p>
    </div>
  `
).join("");

kbToggle.addEventListener("click", () => {
  const isOpen = kbRegister.classList.toggle("open");
  kbToggle.textContent = isOpen ? "ซ่อนคลังนโยบาย" : "แสดงคลังนโยบาย";
  kbToggle.setAttribute("aria-expanded", String(isOpen));
});

async function runQuery(query) {
  submitBtn.disabled = true;
  submitBtn.textContent = "กำลังค้นหา...";
  result.innerHTML = `
    <div class="state-loading">
      <span class="spinner" aria-hidden="true"></span>
      กำลังค้นหาและสรุปคำตอบจากนโยบายบริษัท...
    </div>
  `;
  evidencePanel.innerHTML = EMPTY_EVIDENCE_HTML;

  try {
    const res = await fetch("/query", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ query }),
    });

    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    const data = await res.json();

    result.innerHTML = `
      <div class="answer-card">
        <p class="field-label">คำตอบ</p>
        <div class="answer-body">${data.final_answer}</div>
      </div>
    `;

    if (data.snippets.length) {
      evidencePanel.innerHTML = `
        <p class="evidence-count">อ้างอิงจากนโยบาย ${data.snippets.length} ข้อที่ใกล้เคียงที่สุด</p>
        ${data.snippets
          .map(
            (s, i) => `
              <div class="evidence-item">
                <span class="evidence-index">${i + 1}</span>
                <div>${s}</div>
              </div>
            `
          )
          .join("")}
      `;
    } else {
      evidencePanel.innerHTML =
        '<p class="state-empty" style="border:none; padding:0;">ไม่พบนโยบายที่เกี่ยวข้อง</p>';
    }
  } catch (err) {
    result.innerHTML = `<div class="state-error">เกิดข้อผิดพลาด: ${err.message}</div>`;
  } finally {
    submitBtn.disabled = false;
    submitBtn.textContent = "ถาม";
  }
}

form.addEventListener("submit", (e) => {
  e.preventDefault();
  const query = input.value.trim();
  if (!query) return;
  runQuery(query);
});

sampleQueries.addEventListener("click", (e) => {
  const chip = e.target.closest(".sample-chip");
  if (!chip) return;
  input.value = chip.textContent;
  runQuery(chip.textContent);
});
