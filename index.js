/**
 * WhatsApp Message Capture → Flask AI Classifier (via app.py)
 * -----------------------------------------------------------
 * ✅ Only reads target group(s)
 * ✅ Sends payload to Flask for classification
 * ✅ Silent for all non-target chats
 * ✅ Auto-reconnect and error-safe
 */

const { Client, LocalAuth } = require('whatsapp-web.js');
const axios = require('axios');
const qrcode = require('qrcode-terminal');

// ===== CONFIGURATION =====
const FLASK_API = 'https://whatsapp-notifier-87yb.onrender.com/classify';  // your app.py endpoint
const TARGET_GROUPS = [
  '120363421163177091@g.us',  // Replace with your real group IDs
  // Add more if needed
];

// ✅ Multiple admin numbers who will receive alerts
const ADMIN_NUMBERS = [
  '2349036180200@c.us', // Aina
  // Add more, e.g.:
  '2348068394857@c.us',
  // '2348021111111@c.us'
];

const PORT = 3001; // Express port

// ===== INITIALIZATION =====
const client = new Client({
  authStrategy: new LocalAuth(),
  puppeteer: { headless: true }
});

let isClientReady = false;

// ===== EVENTS =====
client.on('qr', qr => {
  qrcode.generate(qr, { small: true });
  console.log('📱 Scan the QR code to log in.');
});

client.on('authenticated', () => console.log('✅ Authenticated successfully!'));
client.on('auth_failure', msg => console.error('❌ Authentication failed:', msg));

client.on('ready', () => {
  console.log('🎉 WhatsApp client is ready!');
  isClientReady = true;
});

// ===== MESSAGE LISTENER =====
client.on('message', async msg => {
  // Ignore all messages that are not from your target group(s)
  if (!TARGET_GROUPS.includes(msg.from)) return;

  try {
    const sender =
      msg.author
        ? (await client.getContactById(msg.author)).pushname || msg.author.split('@')[0]
        : 'Unknown';

    console.log(`💬 New message from ${sender}: ${msg.body.slice(0, 80)}...`);

    // Send only what Flask expects
    const payload = { message: msg.body };
    const res = await axios.post(FLASK_API, payload);

    const importance = (res.data.importance || '').toLowerCase();
    console.log(`🤖 Flask classified as: ${importance}`);

    // ✅ Send DM alerts to all admins if important
    if (importance === 'important') {
      const alertText = `🚨 *IMPORTANT MESSAGE DETECTED!* 🚨\n\n👤 *From:* ${sender}\n💬 *Message:* ${msg.body}\n🕒 *Time:* ${new Date(msg.timestamp * 1000).toLocaleString()}`;

      for (const adminNumber of ADMIN_NUMBERS) {
        try {
          await client.sendMessage(adminNumber, alertText);
          console.log(`📩 Sent important alert DM to ${adminNumber}`);
        } catch (sendErr) {
          console.error(`⚠️ Failed to send alert to ${adminNumber}:`, sendErr.message);
        }
      }
    }

  } catch (err) {
    console.error('❌ Error forwarding to Flask:', err.message);
  }
});


// ===== ERROR HANDLING =====
client.on('disconnected', reason => {
  console.error('🔌 Disconnected:', reason);
  isClientReady = false;
  setTimeout(() => {
    console.log('🔄 Reconnecting WhatsApp...');
    client.initialize();
  }, 5000);
});

process.on('uncaughtException', err => {
  console.error('💥 Uncaught Exception:', err.message);
});

// ===== START =====
console.log('🚀 Starting WhatsApp client...');
client.initialize();

