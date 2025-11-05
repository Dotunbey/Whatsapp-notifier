
---

## 🚀 WhatsApp Web3 Intel Detector (AI-Powered)

This project connects a **WhatsApp message listener** to a **Flask-based AI classifier** that detects *important Web3 or crypto-related announcements* in real time.

It uses:

* **Node.js** + [whatsapp-web.js](https://github.com/pedroslopez/whatsapp-web.js) for WhatsApp message fetching
* **Python Flask** + **Gemini AI** for message classification
* **Render** or any VPS (optional) for free live deployment

---

## 🧩 Project Overview

The system automatically scans messages from selected WhatsApp groups and uses a **custom Gemini model prompt** to classify them as either:

* `important` → credible or event-based Web3 announcements
* `not important` → general chat, spam, or speculation

This helps filter high-signal Web3 intelligence in real time, e.g. *airdrops, mints, TGEs, testnets,* etc.

---

## 🏗️ Architecture

```bash
WhatsApp Group  →  Node.js (whatsapp-web.js)
                     ↓
                  Express Server
                     ↓
           Flask API (Gemini AI Classifier)
                     ↓
          JSON Output (important / not important)
```

---

## 🧠 AI Classification Logic

The **Gemini model** is prompted with a detailed rule-based system that ensures only *credible*, *event-oriented*, or *officially-toned* messages are flagged as “important”.

### Examples of "important"

* `🚨 Mint is LIVE on Solana: https://mint.xyz`
* `Momentum Airdrop Wave 1 now open: https://airdrop.mmt.finance`
* `Creek Finance Testnet is live — connect wallet to claim faucet`

### Examples of "not important"

* `Anyone minted yet?`
* `LFG 🚀🚀`
* `Probably next week`

---

## 🧰 Tech Stack

| Component           | Technology                             |
| ------------------- | -------------------------------------- |
| Backend AI          | **Flask (Python)**                     |
| AI Model            | **Google Gemini 2.5 Flash**            |
| WhatsApp Automation | **Node.js + whatsapp-web.js**          |
| API Communication   | **Axios**                              |
| Deployment          | **Render** (or Replit / Railway / VPS) |

---

## ⚙️ Installation Guide

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/<your-username>/whatsapp-web3-intel.git
cd whatsapp-web3-intel
```

---

### 2️⃣ Setup Python Backend (Flask)

#### 📁 `app.py`

This file runs your AI classification API.
Make sure you have your **Gemini API key**.

#### 🧪 Install dependencies:

```bash
pip install flask python-dotenv requests
```

#### 🔑 Create `.env`

```bash
GEMINI_API_KEY=your_gemini_api_key_here
GEMINI_MODEL=gemini-2.5-flash
PORT=8000
```

#### ▶️ Run Flask API

```bash
python app.py
```

Your classifier runs on:
👉 `http://localhost:8000/classify`

---

### 3️⃣ Setup Node.js WhatsApp Bot

#### 📁 `index.js`

This file listens to messages and sends them to your Flask classifier.

#### 📦 Install dependencies:

```bash
npm install
```

#### 🔑 Environment variables

Create a `.env` file:

```bash
FLASK_API_URL=http://localhost:8000/classify
```

#### ▶️ Run the bot:

```bash
npm run dev
```

* A QR code appears in your terminal.
* Scan it with your WhatsApp mobile app to authenticate.
* The bot will connect and start reading messages.

---

## 🌐 Deployment (Free on Render)

You can host both the Flask API and the Node bot for free on [Render](https://render.com/):

### For Flask API

1. Create a new **Web Service** → Upload your `app.py`.
2. Set the start command:

   ```bash
   gunicorn app:app
   ```
3. Add environment variable `GEMINI_API_KEY`.

### For Node Bot

1. Create another **Web Service**.
2. Use this start command:

   ```bash
   npm start
   ```
3. Add environment variable `FLASK_API_URL` (your Flask API’s public URL).

---

## 📂 Recommended Folder Structure

```
📁 whatsapp-web3-intel/
│
├── 📄 app.py                  # Flask + Gemini AI classifier
├── 📄 bot.js                  # WhatsApp group fetcher
├── 📄 index.js                # Main bot logic
├── 📄 package.json            # Node dependencies
├── 📄 requirements.txt        # Python dependencies
├── 📄 .env                    # API keys and settings
└── 📄 README.md               # Documentation
```

---

## 🧪 Example API Call

### POST Request

```bash
curl -X POST http://localhost:8000/classify \
-H "Content-Type: application/json" \
-d '{"message": "🚨 Mint is LIVE on Solana: https://mint.xyz"}'
```

### Response

```json
{
  "importance": "important"
}
```

---

## 🔒 Security Notes

* **Never share your `.env` file** publicly.
* Use **LocalAuth** for WhatsApp sessions (it saves credentials locally, not online).
* Avoid running this bot on shared/public servers unless isolated.

---

## 👨‍💻 Author

**Aina Adoption Oluwasomidotun**
📍 Data Scientist | AI Engineer | Automation Specialist
🔗 [LinkedIn](#) | [GitHub](#) | [Email](#)

---

## 🧾 License

This project is licensed under the **MIT License** — free to use and modify with attribution.

---

