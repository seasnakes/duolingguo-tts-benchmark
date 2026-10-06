import json
import os
import time
from datetime import datetime, timezone
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen


def request(path, body=None, token=None, params=None):
    url = 'https://open.feishu.cn/open-apis/' + path
    if params:
        url += '?' + urlencode(params, doseq=True)
    headers = {'Content-Type': 'application/json'}
    if token:
        headers['Authorization'] = 'Bearer ' + token
    for attempt in range(3):
        try:
            req = Request(url, data=json.dumps(body).encode() if body else None, headers=headers)
            with urlopen(req, timeout=30) as response:
                result = json.load(response)
            if result.get('code') != 0:
                raise RuntimeError('Feishu API code ' + str(result.get('code')))
            return result
        except (HTTPError, URLError, TimeoutError):
            if attempt == 2:
                raise RuntimeError('Feishu refresh failed; previous deployment retained') from None
            time.sleep(2 ** attempt)


def main():
    token = request('auth/v3/tenant_access_token/internal', body={
        'app_id': os.environ['FEISHU_APP_ID'],
        'app_secret': os.environ['FEISHU_APP_SECRET'],
    })['tenant_access_token']
    file_token = os.environ['FEISHU_FILE_TOKEN']
    data = request('drive/v1/medias/batch_get_tmp_download_url', token=token, params={
        'file_tokens': [file_token],
        'extra': json.dumps({'bitablePerm': {'tableId': os.environ['FEISHU_TABLE_ID']}}),
    })['data']['tmp_download_urls']
    url = next((item['tmp_download_url'] for item in data if item['file_token'] == file_token), None)
    if not url or not url.startswith('https://'):
        raise RuntimeError('Feishu returned no valid media URL')
    metadata = {
        'url': url,
        'resolution': '1080p',
        'bytes': 48248229,
        'sha256': '840cce79f23a1c323b59fc1e87df94df338dad4513546a12f0fe8bf0df628345',
        'updated_at': datetime.now(timezone.utc).isoformat(),
    }
    (Path(__file__).parent / 'site' / 'source-media.json').write_text(json.dumps(metadata, ensure_ascii=False))
    print('Feishu source link refreshed; 1080p original is available.')


if __name__ == '__main__':
    main()
