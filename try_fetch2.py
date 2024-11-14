import requests
import pandas as pd
import json

# 登录和认证设置
api_key = ''
username = ''
password = ''
headers = {
    'Content-Type': 'application/json',
    'Accept': 'application/json',
    'X-IG-API-KEY': api_key,
    'Version': '3',
    'X-SECURITY-TOKEN': 'f397cd0b31f6ec1f8e7d4758d331b43341fc9b91bca127daa0c86b6309a8fcCD01114',
    'CST': '627c1c9acb0d848e3ccdf83a1c867eedebd3e7783a3e4266bd05a91817cf64CC01115'

}
data = json.dumps({'identifier': username, 'password': password})
login_url = 'https://api.ig.com/gateway/deal/session'
response = requests.post(login_url, headers=headers, data=data)


df = pd.DataFrame()

if response.status_code == 200:
    access_token = response.json()['oauthToken']['access_token']
    headers['Authorization'] = f'Bearer {access_token}'

    epic = 'IX.D.DAX.IFA.IP'
    resolution = 'MINUTE'
    page_size = 100
    total_pages = 2


    data_url = f'https://api.ig.com/gateway/deal/prices/{epic}?resolution={resolution}&pageSize={page_size}&pageNumber={total_pages}'

    data_response = requests.get(data_url, headers=headers)
    if data_response.status_code == 200:
        
        page_data = pd.DataFrame(data_response.json()['prices'])
        df = pd.concat([df, page_data], ignore_index=True)
    else:
        print(f"Failed to retrieve data for page {total_pages}: {data_response.status_code} {data_response.text}")
        print("Request URL:", data_url)
        print("Headers:", headers)
        print("Response:", data_response.text)

    df.to_csv('dax_data.csv', index=False)
    print("Data saved to 'dax_data.csv'.")
else:
    print("Login failed:", response.status_code, response.text)
