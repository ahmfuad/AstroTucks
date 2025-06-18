# 🌅 AstroTucks

AstroTucks is a Telegram bot that provides **precise sunrise and sunset times (down to the second)** based on a user’s **live location**, built using **Telegram Bot API**


## 📜 Background

This bot was created as a **side project** during our team’s research into:

* **Astronomical event tracking**
* **Iftar and Sehri timing differences** based on micro-regional location shifts during Ramadan
* The importance of **second-level accuracy** for religious observances and astronomical study

Most timing tables or local calendars round off to the nearest minute — but this bot delivers timing **with exact seconds**, which can be crucial in high-precision scenarios.

---

## ✨ Features

* Accepts live location from user
* Responds with sunrise and sunset times (to the second)
* This simpler version uses free `sunrisesunset.io` API (which unofficially appears to be based on **US Naval Observatory** calculations)
* Built on **Python 3**, **Flask** and **Telegram Bot API**
* Uses **webhook** (not polling) for efficient, real-time message handling

---

## 🛠️ How It Works (Technically)

### 🔁 1. Webhook-based Communication

Instead of polling Telegram for updates, this bot uses **webhooks**:

* You set a webhook URL (`https://yourdomain.com/webhook`) using Telegram's `setWebhook` method.
* Telegram sends a POST request to this URL **every time a user sends a message** to the bot.
* Server (a Flask app or similar) receives this request, parses it, and responds accordingly.


## 📷 Sample Usage

1. Start the bot and send your desired command (eg. **“/Sunrise”**).
2. Then from 📎 (attachment) select and send the location.
2. You will receive a message like:

```
Sunset Time Today is: XX:XX:XX AM/PM
(All times in local timezone)
```

### Find some images 

<div style="display: flex; gap: 20px; align-items: center;">
  <img src="https://raw.githubusercontent.com/ahmfuad/AstroTucks/refs/heads/main/images/bot_intro.png" width="45%">
  <img src="https://raw.githubusercontent.com/ahmfuad/AstroTucks/refs/heads/main/images/bot_usage.png" width="45%">
</div>

Try it out: [🌅 AstroTucks](https://t.me/astucks_bot) (Vastly running during Ramadan and other moon-based events.)

---

## 🧪 Tech Stack

* **Python 3.13**
* **python-telegram-bot v13.0.0**
* **Flask v2.3.3** (for webhook server)
