import os
import requests
from flask import Flask, request, jsonify
from dotenv import load_dotenv

# ------------------------------
# Setup
# ------------------------------
load_dotenv()
app = Flask(__name__)

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")  # ✅ Latest stable model
BASE_URL = f"https://generativelanguage.googleapis.com/v1beta/models/{GEMINI_MODEL}:generateContent"

if not GEMINI_API_KEY:
    raise RuntimeError("❌ GEMINI_API_KEY not set in environment or .env file.")

# ------------------------------
# AI Classification Prompt
# ------------------------------

SYSTEM_PROMPT = """
You are an elite Web3 intel detector — a precision analyst scanning high-volume group chats for genuine, time-sensitive updates that demand immediate action. Your sole task is to flag ONLY verifiable or clearly event-based announcements — not casual chatter or hype. Prioritize actionable signals and credible tone.

---

### ✅ CRITERIA FOR "IMPORTANT" (ANY of the following count)
1. Announces or hints at a **specific, real-time Web3 event** — even if no link is included:
   - Mentions like “mint live”, “TGE next”, “claim open”, “airdrop started”, “whitelist now”, “presale active”, “launch soon”, “snapshot taken”, “testnet live”, “connect wallet”, “subscribe”, “claim your spot”
   - Short alerts using keywords of Web3 actions are important by intent, even without links.

2. Contains **credible or official links**, which automatically make it important:
   - Domains like `x.com`, `.app`, `.finance`, `.xyz`, `.io`, `.org`, `.eth`
   - Tweets, mints, claim pages, or blog links from known Web3 sources
   - Messages such as “Thanks for your attention — https://x.com/StableAfrika” are always important.

3. Uses an **official, directive, or informative tone** typical of announcements:
   - “Check eligibility”, “Claim here”, “TGE is next”, “Reflect money on Solana”, “Follow and turn on notifications”
   - Even polite closings like “Thanks for your attention”, “Follow for more info” are important when related to Web3 news.

---

### 🧾 EXAMPLES OF "IMPORTANT"
- “🚨 Mint is LIVE on Solana: https://mint.xyz”
- “TGE is next”
- “Reflect money on Solana, super early on this one”
- “Momentum Airdrop Wave 1 now open: https://airdrop.mmt.finance”
- “If you were nominated for Momentum Finance Title Deeds, check if you got in — https://deed.mmt.finance”
- “Creek Finance Testnet (SUI) is live — connect SUI wallet and claim faucet”
- “https://x.com/StableAfrika/status/1983389792986452067 — Thanks for your attention to this matter”
- “Follow and turn on notis — https://x.com/humidifi_”
- “FCFS 3k Farcaster claim spot — https://farcaster.xyz/bammyict/0xd35c91ef”

---

### 🚫 CRITERIA FOR "NOT IMPORTANT"
- Questions: “Anyone minted yet?”, “Is this real?”, “When is the drop?”
- Speculative chatter: “Might launch soon”, “Probably next week”
- Hype or memes: “LFG fam 🚀🔥”, “GM”, “Alpha dropping soon”
- Reposts or stale info: “Mint was live yesterday”
- Off-topic or personal messages

---

### ⚙️ RULES
- If there’s **a credible link**, classify as **important**.
- If **no link**, still classify as **important** if event-language appears (mint, claim, launch, TGE, presale, whitelist, drop, etc.).
- Do not overfit on emojis or tone — focus on *intent* and *keywords of action*.
- Default to “important” when a message could reasonably alert users to a real Web3 event.

---

### 🧩 RESPONSE FORMAT
Output only one lowercase word:
- `important`
- `not important`
"""



# ------------------------------
# Gemini API Query
# ------------------------------
def query_gemini(prompt: str) -> str:
    headers = {"Content-Type": "application/json"}
    params = {"key": GEMINI_API_KEY}
    payload = {
        "contents": [
            {
                "role": "user",
                "parts": [{"text": prompt}]
            }
        ]
    }

    try:
        print("🌐 Sending request to Gemini...")
        response = requests.post(BASE_URL, headers=headers, params=params, json=payload, timeout=30)
        print(f"🔢 Status code: {response.status_code}")

        # If API failed
        if response.status_code != 200:
            print(f"📦 Raw error: {response.text[:400]}")
            raise RuntimeError(f"Gemini API error ({response.status_code}): {response.text}")

        data = response.json()

        # Extract model output
        text = ""
        if "candidates" in data and data["candidates"]:
            parts = data["candidates"][0].get("content", {}).get("parts", [])
            if parts and "text" in parts[0]:
                text = parts[0]["text"].strip()

        if not text:
            return "not important"

        print(f"🧠 Gemini output: {text}")
        return text.lower()

    except Exception as e:
        print(f"❌ Gemini API request failed: {e}")
        raise RuntimeError(f"Gemini API request failed: {e}")

# ------------------------------
# Flask Route
# ------------------------------
@app.route("/classify", methods=["POST"])
def classify_message():
    payload = request.get_json(silent=True) or {}
    message = (payload.get("message") or "").strip()

    if not message:
        return jsonify({"error": "No message provided"}), 400

    prompt = f"{SYSTEM_PROMPT}\n\nClassify this message:\n{message}\nClassification:"

    try:
        print(f"🔎 Received message:\n{message}\n")
        gemini_output = query_gemini(prompt)
        print(f"🤖 Gemini classification: {gemini_output}")

        return jsonify({"importance": gemini_output}), 200

    except Exception as exc:
        print(f"⚠️ Error classifying: {exc}")
        return jsonify({"error": str(exc)}), 500

# ------------------------------
# Run Flask Server
# ------------------------------
if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    print(f"🚀 Running Gemini classifier on http://0.0.0.0:{port} using model {GEMINI_MODEL}")
    app.run(host="0.0.0.0", port=port, debug=True)
