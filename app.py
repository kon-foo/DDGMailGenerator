from fastapi import FastAPI, HTTPException, Query
import requests
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

@app.get("/generate")
def generate_email(account: str = Query(...)):
    # Look up bearer token for this account
    env_key = f'BEARER_{account.upper()}'
    bearer_token = os.getenv(env_key)
    if not bearer_token:
        raise HTTPException(
            status_code=404,
            detail=f'No bearer token found for account: {account}'
        )

    # Make request to DuckDuckGo API
    try:
        response = requests.post(
            'https://quack.duckduckgo.com/api/email/addresses',
            headers={
                'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:145.0) Gecko/20100101 Firefox/145.0',
                'Accept': '*/*',
                'Accept-Language': 'en,en-US;q=0.5',
                'Accept-Encoding': 'gzip, deflate, br, zstd',
                'Referer': 'https://duckduckgo.com/',
                'Authorization': f'Bearer {bearer_token}',
                'Origin': 'https://duckduckgo.com',
                'Sec-GPC': '1',
                'Connection': 'keep-alive',
                'Sec-Fetch-Dest': 'empty',
                'Sec-Fetch-Mode': 'cors',
                'Sec-Fetch-Site': 'same-site'
            }
        )
        response.raise_for_status()  # Raises an HTTPError for bad responses (4xx, 5xx)
        asdict = response.json()
        if "address" in asdict:
            asdict["address"] = f"{asdict['address']}@duck.com"
        return asdict
    except requests.exceptions.HTTPError as e:
        raise HTTPException(status_code=e.response.status_code, detail=e.response.text)
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=500, detail="Failed to parse response")

@app.get("/health")
def health():
    return {"status": "healthy"}
