from pathlib import Path
import hashlib,json
root=Path(__file__).parent
for item in json.loads((root/'media-manifest.json').read_text()):
    data=b''.join((root/part).read_bytes() for part in item['parts'])
    assert len(data)==item['size'] and hashlib.sha256(data).hexdigest()==item['sha256'],item['path']
    target=root/'site'/item['path'];target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes(data)
print('Media restored and verified.')
