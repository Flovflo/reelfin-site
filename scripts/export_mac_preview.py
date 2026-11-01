#!/usr/bin/env python3
"""Export a certified native Mac app capture; no additional crop or UI retouch."""
import argparse
import hashlib
import json
from pathlib import Path
from PIL import Image


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--capture', type=Path, required=True)
    parser.add_argument('--evidence', type=Path, required=True)
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[1]
    image = Image.open(args.capture).convert('RGB')
    evidence = json.loads(args.evidence.read_text())
    capture = next(c for c in evidence['captures'] if c['name'] == 'home')
    expected = capture['sha256']
    assert expected == sha(args.capture), (expected, sha(args.capture))
    assert capture['pixelEquality'] and capture['noResample'] and capture['originalUntouched']
    assert image.size == (2048, 1472)
    output = root / 'assets/media/devices'
    metadata = {
        'platform': 'Mac', 'releaseStatus': 'in_development', 'presentationOnly': True,
        'uiRetouched': False, 'additionalCrop': False, 'sourceSize': list(image.size),
        'sourceSha256': sha(args.capture), 'evidenceSha256': sha(args.evidence),
        'originalAscSha256': capture['originalSHA256'], 'approvedSourceCrop': evidence['cropBoxPixels'],
        'sourcePixelEqualityVerifiedByCaptureAgent': True, 'variants': [],
    }
    for width in (480, 640, 960, 1600):
        size = (width, round(image.height * width / image.width))
        name = 'mac-home.webp' if width == 1600 else f'mac-home-{width}.webp'
        path = output / name
        image.resize(size, Image.Resampling.LANCZOS).save(path, lossless=True, method=6)
        metadata['variants'].append({'file': name, 'width': size[0], 'height': size[1], 'sha256': sha(path)})
        print(name, size, path.stat().st_size)
    (output / 'mac-preview.json').write_text(json.dumps(metadata, indent=2) + '\n')
    native_path = root / 'assets/media/cinema/native-captures.json'
    native = json.loads(native_path.read_text())
    native['unavailablePlatforms'] = [p for p in native.get('unavailablePlatforms', []) if p['platform'] != 'mac']
    native['captures'] = [c for c in native['captures'] if c.get('platform') != 'mac']
    native['captures'].append({'platform': 'mac', 'file': '../devices/mac-home.webp', 'width': 1600, 'height': 1150,
        'source': 'presentation-captures/mac/home.png', 'sourceSha256': sha(args.capture),
        'presentationOnly': True, 'uiRetouched': False, 'releaseStatus': 'in_development'})
    native_path.write_text(json.dumps(native, indent=2) + '\n')


if __name__ == '__main__':
    main()
