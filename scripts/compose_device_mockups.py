#!/usr/bin/env python3
"""Compose native UI in licensed Apple artwork. No downloads, mounts or software execution.

Use only after the owner has accepted the Apple resource licences. Source artwork
stays local; the public output depicts ReelFin's UI, never a standalone bezel.
"""
import argparse
import hashlib
import json
import re
from collections import deque
from pathlib import Path

from PIL import Image, ImageChops

ROOT = Path(__file__).resolve().parents[1]


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def connected_mask(binary, seed):
    width, height = binary.size
    free = binary.tobytes()
    visited = bytearray(width * height)
    pending = deque([seed])
    while pending:
        x, y = pending.popleft()
        if visited[y * width + x] or not free[y * width + x]:
            continue
        row = free[y * width:(y + 1) * width]
        left = row.rfind(b'\x00', 0, x + 1) + 1
        right = row.find(b'\x00', x)
        if right < 0:
            right = width
        visited[y * width + left:y * width + right] = b'\xff' * (right - left)
        for adjacent in (y - 1, y + 1):
            if not 0 <= adjacent < height:
                continue
            segment = free[adjacent * width + left:adjacent * width + right]
            for run in re.finditer(b'\xff+', segment):
                seed = left + run.start()
                if not visited[adjacent * width + seed]:
                    pending.append((seed, adjacent))
    return Image.frombytes('L', binary.size, bytes(visited))


def screen_mask(frame):
    """Select the internal transparent aperture, excluding exterior corners."""
    free = frame.getchannel('A').point(lambda value: 255 if value == 0 else 0)
    return connected_mask(free, (frame.width // 2, frame.height // 2))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--iphone', type=Path, required=True)
    parser.add_argument('--duo', type=Path, required=True)
    parser.add_argument('--tv', type=Path, required=True)
    parser.add_argument('--captures', type=Path, required=True)
    args = parser.parse_args()
    output = ROOT / 'assets/media/devices'
    output.mkdir(parents=True, exist_ok=True)

    frames = {
        'iphone': (args.iphone / 'PNG/iPhone 18 Pro Max/iPhone 18 Pro Max - Black - Portrait.png', (75, 66, 1395, 2934)),
        'tv': (args.tv / 'PNG/Apple TV - 4K.png', (103, 119, 3943, 2279)),
        'duo-open': (args.duo / 'PNG/iPhone Duo - Night Sky - Inner Open Landscape.png', (120, 120, 2973, 2127)),
        'duo-closed': (args.duo / 'PNG/iPhone Duo - Night Sky - Outer Closed Portrait.png', (88, 80, 1486, 2114)),
    }
    shots = [
        ('iphone-home', 'iphone', 'iphone/home.png'),
        ('iphone-series', 'iphone', 'iphone/series.png'),
        ('tv-home', 'tv', 'tv4k/home.png'),
        ('tv-series', 'tv', 'tv4k/series.png'),
        ('tv-detail', 'tv', 'tv4k/detail.png'),
        ('duo-open-home', 'duo-open', 'duo-inner/home.png'),
        ('duo-closed-series', 'duo-closed', 'duo-outer/series.png'),
    ]
    manifest = {
        'sourcePage': 'https://developer.apple.com/design/resources/',
        'guidelines': 'https://developer.apple.com/app-store/marketing/guidelines/',
        'ownerLicenceAcceptanceDate': '2026-11-01',
        'resourceUse': 'ReelFin native UI depictions only. Apple artwork may not be extracted or reused independently.',
        'bezelTreatment': {'productHardwareCropped': False, 'rotation': 0, 'addedShadow': False, 'animation': False},
        'mockups': [],
    }
    for name, kind, capture_name in shots:
        frame_path, aperture = frames[kind]
        frame = Image.open(frame_path).convert('RGBA')
        source_artwork_size = frame.size
        selected_bounds = (0, 0, frame.width, frame.height)
        if kind == 'tv':
            hardware = frame.getchannel('A').point(lambda value: 255 if value > 0 else 0)
            row_y = frame.height // 3
            row = hardware.crop((0, row_y, frame.width, row_y + 1)).tobytes()
            selected_bounds = connected_mask(hardware, (row.index(255), row_y)).getbbox()
            # This is the whole disconnected television product, not a partial
            # hardware crop. The separate box and remote are outside its bounds.
            frame = frame.crop(selected_bounds)
            aperture = tuple(value - selected_bounds[index % 2] for index, value in enumerate(aperture))
        mask = screen_mask(frame)
        assert all(abs(a - b) <= 2 for a, b in zip(mask.getbbox(), aperture)), (kind, mask.getbbox(), aperture)
        capture_path = args.captures / capture_name
        capture = Image.open(capture_path).convert('RGBA')
        x0, y0, x1, y1 = aperture
        target = (x1 - x0, y1 - y0)
        # Integer dimension rounding is the documented 1px Duo source tolerance.
        assert abs(capture.width / capture.height - target[0] / target[1]) < .0003
        screen = capture if capture.size == target else capture.resize(target, Image.Resampling.LANCZOS)
        underlay = Image.new('RGBA', frame.size)
        underlay.paste(screen, (x0, y0))
        underlay.putalpha(ImageChops.multiply(underlay.getchannel('A'), mask))
        composite = Image.alpha_composite(underlay, frame)
        opaque = frame.getchannel('A').point(lambda value: 255 if value == 255 else 0)
        unchanged = ImageChops.multiply(ImageChops.difference(composite.convert('RGB'), frame.convert('RGB')), opaque.convert('RGB')).getbbox() is None
        assert unchanged, 'Opaque hardware pixels must remain byte-identical.'
        export_width = {'iphone': 900, 'tv': 2200, 'duo-open': 1800, 'duo-closed': 900}[kind]
        export_size = (export_width, round(frame.height * export_width / frame.width))
        web_composite = composite.resize(export_size, Image.Resampling.LANCZOS)
        file = output / f'{name}.webp'
        web_composite.save(file, lossless=True, exact=True, method=6)
        decoded = Image.open(file).convert('RGBA')
        assert ImageChops.difference(decoded, web_composite).getbbox() is None
        entry = {
            'file': file.name, 'sha256': sha(file), 'width': export_size[0], 'height': export_size[1],
            'sourceArtworkSize': list(source_artwork_size), 'selectedProductBounds': list(selected_bounds),
            'selectedProductSize': list(frame.size), 'uniformWebExportScale': export_width / frame.width,
            'appleFile': frame_path.relative_to(frames[kind][0].parents[2] if kind == 'iphone' else frames[kind][0].parents[1]).as_posix(),
            'applePngSha256': sha(frame_path), 'nativeCapture': capture_name,
            'nativeCaptureSha256': sha(capture_path), 'nativeSize': list(capture.size),
            'screenAperture': list(aperture), 'screenOutputSize': list(target),
            'screenResampled': capture.size != target, 'opaqueHardwarePixelsUnchangedBeforeUniformWebExport': unchanged,
            'fullSelectedProductBoundsPreserved': True,
        }
        widths = {'iphone': [450], 'tv': [640, 1100], 'duo-open': [640, 900], 'duo-closed': [450]}[kind]
        entry['responsive'] = []
        for width in widths:
            size = (width, round(frame.height * width / frame.width))
            variant = output / f'{name}-{width}.webp'
            composite.resize(size, Image.Resampling.LANCZOS).save(variant, lossless=True, exact=True, method=6)
            entry['responsive'].append({'file': variant.name, 'width': size[0], 'height': size[1], 'sha256': sha(variant)})
        # The overlay contains only our UI pixels. Every Apple hardware pixel,
        # including antialiasing, is excluded so it remains fixed during a fade.
        if name in {'iphone-series', 'tv-series'}:
            screen.putalpha(mask.crop(aperture))
            overlay = Image.new('RGBA', frame.size)
            overlay.paste(screen, (x0, y0))
            overlay = overlay.resize(export_size, Image.Resampling.LANCZOS)
            hardware = frame.getchannel('A').resize(export_size, Image.Resampling.BOX).point(lambda value: 255 if value > 0 else 0)
            overlay.putalpha(ImageChops.multiply(overlay.getchannel('A'), ImageChops.invert(hardware)))
            overlay_path = output / f'{name}-screen.webp'
            overlay.save(overlay_path, lossless=True, method=6)
            variants = []
            for width in widths:
                size = (width, round(frame.height * width / frame.width))
                small = overlay.resize(size, Image.Resampling.LANCZOS)
                hardware = frame.getchannel('A').resize(size, Image.Resampling.BOX).point(lambda value: 255 if value > 0 else 0)
                small.putalpha(ImageChops.multiply(small.getchannel('A'), ImageChops.invert(hardware)))
                variant = output / f'{name}-screen-{width}.webp'
                small.save(variant, lossless=True, method=6)
                variants.append({'file': variant.name, 'width': size[0], 'height': size[1], 'sha256': sha(variant)})
            entry['uiOnlyOverlay'] = {'file': overlay_path.name, 'sha256': sha(overlay_path), 'excludesEveryNontransparentHardwarePixel': True, 'responsive': variants}
        manifest['mockups'].append(entry)
        print(file.name, export_size, file.stat().st_size, 'full artwork preserved')

    sources = []
    for filename in ['ReelFin-Bezel-iPhone-Duo.dmg', 'ReelFin-Bezel-iPhone-18.dmg', 'ReelFin-Bezel-Apple-TV.dmg']:
        path = Path('/tmp') / filename
        if path.exists():
            sources.append({'file': filename, 'bytes': path.stat().st_size, 'sha256': sha(path), 'download': 'https://devimages-cdn.apple.com/design/resources/download/' + filename.removeprefix('ReelFin-')})
    manifest['archives'] = sources
    (output / 'provenance.json').write_text(json.dumps(manifest, indent=2) + '\n')


if __name__ == '__main__':
    main()
