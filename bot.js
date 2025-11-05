/**
 * WhatsApp Group Fetcher — Safe Version (no EvaluationError)
 * Compatible with: whatsapp-web.js v1.34.1, Node ≥20
 */

const { Client, LocalAuth } = require('whatsapp-web.js');
const qrcode = require('qrcode-terminal');

const client = new Client({
  authStrategy: new LocalAuth(),
  puppeteer: {
    headless: true, // set to false if you want to see browser window
    args: ['--no-sandbox', '--disable-setuid-sandbox'],
  },
});

console.log('🚀 Launching WhatsApp client...');

client.on('qr', (qr) => {
  qrcode.generate(qr, { small: true });
  console.log('📱 Scan this QR code with WhatsApp (expires in 30s)');
});

client.on('authenticated', () => {
  console.log('✅ Authenticated successfully!');
});

client.on('ready', async () => {
  console.log('✅ Client is ready!');
  console.log('⏳ Fetching groups safely...');

  // --- Fetch groups safely with retry ---
  let attempts = 0;
  const MAX_ATTEMPTS = 5;

  while (attempts < MAX_ATTEMPTS) {
    try {
      const chats = await client.getChats();
      const groups = chats.filter(c => c.isGroup);

      console.log(`🎯 Found ${groups.length} groups:`);
      groups.forEach((g, i) => {
        console.log(`${i + 1}. ${g.name} — ${g.id._serialized}`);
      });

      console.log('\n✅ Copy the group ID(s) you want into your main index.js');
      break; // success
    } catch (err) {
      attempts++;
      console.warn(`⚠️ Attempt ${attempts}: Failed to fetch chats — retrying in 3s...`);
      await new Promise(res => setTimeout(res, 3000));
    }
  }

  if (attempts === MAX_ATTEMPTS) {
    console.error('❌ Could not fetch groups after multiple attempts. Try restarting the script.');
  }

  process.exit(0);
});

client.on('disconnected', (reason) => {
  console.error('🔌 Disconnected:', reason);
});

client.initialize();
