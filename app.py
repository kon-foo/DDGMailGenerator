from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import HTMLResponse
import requests
import os
from dotenv import load_dotenv

load_dotenv()
app = FastAPI()

def _generate_email_logic(account: str):
    """Shared logic for generating emails"""
    env_key = f'BEARER_{account.upper()}'
    bearer_token = os.getenv(env_key)

    if not bearer_token:
        raise HTTPException(
            status_code=404,
            detail=f'No bearer token found for account: {account}'
        )

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
        response.raise_for_status()
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

@app.get("/generate")
def generate_email(account: str = Query(...)):
    """JSON API endpoint"""
    return _generate_email_logic(account)

@app.get("/generate-ui", response_class=HTMLResponse)
def generate_email_ui(account: str = Query(...)):
    """HTML UI endpoint with copy button"""
    result = _generate_email_logic(account)
    email = result.get("address", "")

    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Email Generated</title>
        <style>
            body {{
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
                max-width: 600px;
                margin: 50px auto;
                padding: 20px;
                background: #f5f5f5;
            }}
            .container {{
                background: white;
                padding: 30px;
                border-radius: 12px;
                box-shadow: 0 2px 8px rgba(0,0,0,0.1);
            }}
            .email-display {{
                background: #f8f9fa;
                padding: 15px;
                border-radius: 8px;
                font-family: 'Courier New', monospace;
                font-size: 16px;
                word-break: break-all;
                margin: 20px 0;
                border: 2px solid #e9ecef;
            }}
            .copy-btn {{
                background: #0066cc;
                color: white;
                border: none;
                padding: 12px 24px;
                border-radius: 8px;
                font-size: 16px;
                cursor: pointer;
                width: 100%;
                margin-top: 10px;
            }}
            .copy-btn:hover {{
                background: #0052a3;
            }}
            .copy-btn.copied {{
                background: #28a745;
            }}
            h1 {{
                color: #333;
                margin-top: 0;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>✉️ New Email Generated</h1>
            <div class="email-display" id="email">{email}</div>
            <button class="copy-btn" id="copyBtn" onclick="copyEmail()">
                Copy to Clipboard
            </button>
        </div>

        <script>
            function copyEmail() {{
                const email = document.getElementById('email').textContent;
                const btn = document.getElementById('copyBtn');

                navigator.clipboard.writeText(email).then(() => {{
                    btn.textContent = '✓ Copied!';
                    btn.classList.add('copied');
                    setTimeout(() => {{
                        btn.textContent = 'Copy to Clipboard';
                        btn.classList.remove('copied');
                    }}, 2000);
                }}).catch(err => {{
                    btn.textContent = 'Failed to copy';
                    setTimeout(() => {{
                        btn.textContent = 'Copy to Clipboard';
                    }}, 2000);
                }});
            }}
        </script>
    </body>
    </html>
    """
    return html

@app.get("/health")
def health():
    return {"status": "healthy"}
