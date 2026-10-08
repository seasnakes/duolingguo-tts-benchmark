"""Wait for this upload to become visible in this workflow run's artifact list."""
import json
import os
import time
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


def wait_for_artifact(fetch, artifact_id, *, attempts=12, interval=10, sleep=time.sleep):
    for attempt in range(1, attempts + 1):
        try:
            artifacts = fetch()
        except HTTPError as error:
            if error.code not in (408, 429, 500, 502, 503, 504):
                raise
            print(f'Artifact API temporarily unavailable (HTTP {error.code}).', flush=True)
        except (URLError, TimeoutError):
            print('Artifact API request timed out or connection failed.', flush=True)
        else:
            matches = [a for a in artifacts if a['name'] == 'github-pages']
            if len(matches) > 1:
                raise RuntimeError('Multiple github-pages artifacts found; refusing ambiguous deployment.')
            if matches:
                artifact = matches[0]
                if str(artifact['id']) == str(artifact_id):
                    if artifact.get('expired') or artifact.get('size_in_bytes', 0) <= 0:
                        raise RuntimeError('Uploaded artifact is expired or empty.')
                    print(f'Confirmed github-pages artifact {artifact_id} is ready.', flush=True)
                    return
        print(f'Waiting for uploaded artifact {artifact_id} ({attempt}/{attempts}).', flush=True)
        if attempt < attempts:
            sleep(interval)
    raise TimeoutError('Uploaded github-pages artifact did not become visible; deployment was not started.')


def main():
    artifact_id = os.environ['PAGES_ARTIFACT_ID']
    if not artifact_id.isdigit():
        raise ValueError('Upload did not return a valid artifact ID.')
    base = os.environ.get('GITHUB_API_URL', 'https://api.github.com')
    url = f"{base}/repos/{os.environ['GITHUB_REPOSITORY']}/actions/runs/{os.environ['GITHUB_RUN_ID']}/artifacts?per_page=100"
    def fetch():
        request = Request(url, headers={
            'Authorization': f"Bearer {os.environ['GH_TOKEN']}",
            'Accept': 'application/vnd.github+json',
            'X-GitHub-Api-Version': '2022-11-28',
        })
        with urlopen(request, timeout=15) as response:
            return json.load(response)['artifacts']
    wait_for_artifact(fetch, artifact_id)


if __name__ == '__main__':
    main()
