import requests

cookies = {
    '_ga': 'GA1.1.1758841131.1699815037',
    '_ym_uid': '1699815043535990768',
    'tmr_lvid': '42020b6262a3b7c506df491c0e2b9d61',
    'tmr_lvidTS': '1699815043818',
    'buyer_laas_location': '637640',
    'srv_id': '-LkiX2ycHrvoqPzz.nbHHZailC7APHJu0EmgP_EVkl0n1ssSCf5Wo4RUNpLLzUXVzL1NMe9uX4nK437Q=.wUL2HaM-6lc3D4zPwGFm88wuMUjLB5bNatNXbKhHs7w=.web',
    'u': '372tvu4o.1keu6c.1utxkak6wht00',
    'v': '1746093160',
    'luri': 'moskva',
    'buyer_location_id': '637640',
    '_ym_d': '1746093163',
    '_ym_isad': '1',
    '_gcl_au': '1.1.1114664964.1746093163',
    'cookie_consent_shown': '1',
    'uxs_uid': '06b77920-2672-11f0-af75-292c6c0c3994',
    'SEARCH_HISTORY_IDS': '1%2C%2C4%2C0',
    '_ym_visorc': 'b',
    'gMltIuegZN2COuSe': 'EOFGWsm50bhh17prLqaIgdir1V0kgrvN',
    'domain_sid': '9_oQd5sze73mdi3gYLLbD%3A1746093164488',
    'f': '5.d908952b446ec0dbdc134d8a1938bf88a68643d4d8df96e9a68643d4d8df96e9a68643d4d8df96e9a68643d4d8df96e94f9572e6986d0c624f9572e6986d0c624f9572e6986d0c62ba029cd346349f36c1e8912fd5a48d0283bac648e6e6724346b8ae4e81acb9fa1a2a574992f83a9246b8ae4e81acb9fa46b8ae4e81acb9fa143114829cf33ca7af305aadb1df8ceb48bdd0f4e425aba7085d5b6a45ae867378ba5f931b08c66a91e52da22a560f550df103df0c26013a2ebf3cb6fd35a0ac71e7cb57bbcb8e0ff0c77052689da50ddc5322845a0cba1aba0ac8037e2b74f92da10fb74cac1eab2da10fb74cac1eab2da10fb74cac1eabdc5322845a0cba1a0df103df0c26013a037e1fbb3ea05095de87ad3b397f946b4c41e97fe93686ad7f8a51fce9ad1b8534546485ab5795f75d3d12014bda85a4fa1a39d59040462b7eab1d806ffda0e8aff5a88f928bb65f47c0ddde4b32a689c772035eab81f5e146b8ae4e81acb9fa46b8ae4e81acb9faf5b8e78c6f0f62a37b460a273915f338796b219c9e7f9d4e2da10fb74cac1eab2da10fb74cac1eabc98d1c3ab1f148dc7b2a336b51bc37401fd23d3d1b9f6ec4',
    'ft': '"Q6CeYaiWbd+1td6oE5TscrCKkF1vBBIItyZQiQc5QY8AqgtdIoGn8QFs7Jy9olhx4/Q1AjArQzFhRg50u17AudZKnJgQlrM2U7yqjZScS/521iFtdp556doETLuXBPCi4SHICWidqnQ62R8++wHikNLyTbzSOXOlCLrGIV56N5n4ZoPkO1pzJtA3DqGj8Os0"',
    'cssid': 'ebd084c2-f09d-4c38-8c12-ab2a20c9571c',
    'cssid_exp': '1746098343407',
    'dfp_group': '38',
    'sx': 'H4sIAAAAAAAC%2F1zOz0ozMRAA8HfJeQ%2BZyWQm2dt3%2BNQiKP7pYr0lmQQFC7prpW7ZdxcPC8UX%2BPE7GZ%2B8gMuBSkSMPqakpUHVCFQrSzb9yXyZ3oxXI03X88PuaHf7UYvpTDU9CDEEsj4unUmFWYC9R5DIJaaiKlasC9pyo7BS3%2B%2Fb7f5lKHHIN6%2FD4%2BGcAgC3dKZhFZ%2BQvFMS51QhYcHoq8UcrPJKHan8s25j6%2Fy2eYKL%2F39W9pdSZuGM0hgzcfOYa7AkChySVbdSyu3u8Dl%2FpMvp%2Fvl2qmeURAmwLD8BAAD%2F%2F9x0XBItAQAA',
    'abp': '0',
    '_ga_M29JC28873': 'GS1.1.1746093163.20.1.1746097660.42.0.0',
    'tmr_detect': '1%7C1746097660978',
    'buyer_from_page': 'catalog',
    'csprefid': 'f75d2465-fcae-4c72-bce3-18f95be7dfc6',
}

headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'ru,en;q=0.9',
    'cache-control': 'max-age=0',
    # 'cookie': '_ga=GA1.1.1758841131.1699815037; _ym_uid=1699815043535990768; tmr_lvid=42020b6262a3b7c506df491c0e2b9d61; tmr_lvidTS=1699815043818; buyer_laas_location=637640; srv_id=-LkiX2ycHrvoqPzz.nbHHZailC7APHJu0EmgP_EVkl0n1ssSCf5Wo4RUNpLLzUXVzL1NMe9uX4nK437Q=.wUL2HaM-6lc3D4zPwGFm88wuMUjLB5bNatNXbKhHs7w=.web; u=372tvu4o.1keu6c.1utxkak6wht00; v=1746093160; luri=moskva; buyer_location_id=637640; _ym_d=1746093163; _ym_isad=1; _gcl_au=1.1.1114664964.1746093163; cookie_consent_shown=1; uxs_uid=06b77920-2672-11f0-af75-292c6c0c3994; SEARCH_HISTORY_IDS=1%2C%2C4%2C0; _ym_visorc=b; gMltIuegZN2COuSe=EOFGWsm50bhh17prLqaIgdir1V0kgrvN; domain_sid=9_oQd5sze73mdi3gYLLbD%3A1746093164488; f=5.d908952b446ec0dbdc134d8a1938bf88a68643d4d8df96e9a68643d4d8df96e9a68643d4d8df96e9a68643d4d8df96e94f9572e6986d0c624f9572e6986d0c624f9572e6986d0c62ba029cd346349f36c1e8912fd5a48d0283bac648e6e6724346b8ae4e81acb9fa1a2a574992f83a9246b8ae4e81acb9fa46b8ae4e81acb9fa143114829cf33ca7af305aadb1df8ceb48bdd0f4e425aba7085d5b6a45ae867378ba5f931b08c66a91e52da22a560f550df103df0c26013a2ebf3cb6fd35a0ac71e7cb57bbcb8e0ff0c77052689da50ddc5322845a0cba1aba0ac8037e2b74f92da10fb74cac1eab2da10fb74cac1eab2da10fb74cac1eabdc5322845a0cba1a0df103df0c26013a037e1fbb3ea05095de87ad3b397f946b4c41e97fe93686ad7f8a51fce9ad1b8534546485ab5795f75d3d12014bda85a4fa1a39d59040462b7eab1d806ffda0e8aff5a88f928bb65f47c0ddde4b32a689c772035eab81f5e146b8ae4e81acb9fa46b8ae4e81acb9faf5b8e78c6f0f62a37b460a273915f338796b219c9e7f9d4e2da10fb74cac1eab2da10fb74cac1eabc98d1c3ab1f148dc7b2a336b51bc37401fd23d3d1b9f6ec4; ft="Q6CeYaiWbd+1td6oE5TscrCKkF1vBBIItyZQiQc5QY8AqgtdIoGn8QFs7Jy9olhx4/Q1AjArQzFhRg50u17AudZKnJgQlrM2U7yqjZScS/521iFtdp556doETLuXBPCi4SHICWidqnQ62R8++wHikNLyTbzSOXOlCLrGIV56N5n4ZoPkO1pzJtA3DqGj8Os0"; cssid=ebd084c2-f09d-4c38-8c12-ab2a20c9571c; cssid_exp=1746098343407; dfp_group=38; sx=H4sIAAAAAAAC%2F1zOz0ozMRAA8HfJeQ%2BZyWQm2dt3%2BNQiKP7pYr0lmQQFC7prpW7ZdxcPC8UX%2BPE7GZ%2B8gMuBSkSMPqakpUHVCFQrSzb9yXyZ3oxXI03X88PuaHf7UYvpTDU9CDEEsj4unUmFWYC9R5DIJaaiKlasC9pyo7BS3%2B%2Fb7f5lKHHIN6%2FD4%2BGcAgC3dKZhFZ%2BQvFMS51QhYcHoq8UcrPJKHan8s25j6%2Fy2eYKL%2F39W9pdSZuGM0hgzcfOYa7AkChySVbdSyu3u8Dl%2FpMvp%2Fvl2qmeURAmwLD8BAAD%2F%2F9x0XBItAQAA; abp=0; _ga_M29JC28873=GS1.1.1746093163.20.1.1746097660.42.0.0; tmr_detect=1%7C1746097660978; buyer_from_page=catalog; csprefid=f75d2465-fcae-4c72-bce3-18f95be7dfc6',
    'dnt': '1',
    'priority': 'u=0, i',
    'referer': 'https://www.avito.ru/moskva/kvartiry/prodam/studii-ASgBAgICAkSSA8YQygj~WA?context=H4sIAAAAAAAA_wEjANz_YToxOntzOjg6ImZyb21QYWdlIjtzOjc6ImNhdGFsb2ciO312FITcIwAAAA',
    'sec-ch-ua': '"Not A(Brand";v="8", "Chromium";v="132", "YaBrowser";v="25.2", "Yowser";v="2.5"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"macOS"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 YaBrowser/25.2.0.0 Safari/537.36',
}

params = {
    'context': 'H4sIAAAAAAAA_wEjANz_YToxOntzOjg6ImZyb21QYWdlIjtzOjc6ImNhdGFsb2ciO312FITcIwAAAA',
}

response = requests.get(
    'https://www.avito.ru/moskva/kvartiry/prodam/1-komnatnye-ASgBAgICAkSSA8YQygiAWQ',
    params=params,
    cookies=cookies,
    headers=headers,
)

USER_AGENTS = [
    # Windows + Chrome
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    
    # macOS + Safari
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Safari/605.1.15',
    
    # Linux + Firefox
    'Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/115.0',
    
    # iPhone
    'Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1',
    
    # Android
    'Mozilla/5.0 (Linux; Android 13; SM-S901B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Mobile Safari/537.36'
]

