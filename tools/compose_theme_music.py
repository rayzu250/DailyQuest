"""Render DailyQuest's original synthesized instrumental theme loops.

Requires numpy and soundfile. No recordings, external samples or model calls.
Run from the repository root; existing tracks require an explicit --replace.
"""
from pathlib import Path
import argparse
import json
import sys
import math
import hashlib
import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent / ".audio-deps"))
import soundfile as sf

SR = 32000
# name, title, tempo, bars, tonic, chord roots, melody scale degrees, lead voice
TRACKS = [
    ("forest", "Senderos tranquilos", 70, 40, 60, [0, 5, 2, 4], [4, 2, 0, 7, 4, 9, 7, 2], "keys"),
    ("ocean", "Corrientes suaves", 64, 40, 62, [0, 7, 5, 2], [7, 9, 4, 2, 0, 4, 2, 7], "bell"),
    ("sunset", "Luz de la tarde", 76, 40, 57, [0, 5, 9, 7], [0, 4, 7, 9, 7, 4, 2, 0], "pluck"),
    ("night", "Órbita serena", 62, 40, 59, [9, 5, 0, 7], [11, 7, 4, 2, 4, 9, 7, 4], "pad"),
    ("prehistoric", "Valle del alba", 74, 40, 55, [0, 2, 5, 7], [0, 7, 4, 2, 7, 9, 4, 0], "marimba"),
    ("garden", "Brotes de luz", 68, 40, 65, [0, 5, 4, 2], [4, 7, 9, 7, 2, 4, 0, 2], "pluck"),
    ("robots", "Pequeños circuitos", 80, 40, 60, [9, 5, 0, 7], [9, 7, 4, 0, 2, 4, 7, 11], "keys"),
    ("secondary/mecha", "Horizonte Atlas", 108, 64, 57, [9, 5, 0, 7], [9, 12, 16, 14, 12, 7, 9, 4], "synth"),
    ("secondary/arcane", "Páginas del cielo", 98, 56, 62, [2, 9, 5, 0], [2, 5, 9, 12, 11, 9, 5, 4], "bell"),
    ("secondary/stage", "Antes del escenario", 114, 64, 60, [0, 7, 9, 5], [4, 7, 12, 11, 9, 7, 4, 2], "keys"),
]
CHORDS = {0: [0, 4, 7, 11], 2: [2, 5, 9, 12], 4: [4, 7, 11, 14],
          5: [5, 9, 12, 16], 7: [7, 11, 14, 17], 9: [9, 12, 16, 19]}


def tone(note, seconds, voice):
    t = np.arange(max(8, round(seconds * SR)), dtype=np.float64) / SR
    f = 440 * 2 ** ((note - 69) / 12)
    phase = 2 * np.pi * f * t
    if voice == "pad":
        signal = (np.sin(phase) + .30 * np.sin(phase * 1.002)
                  + .16 * np.sin(2 * phase)) / 1.46
        envelope = (1 - np.exp(-t / .14)) * np.minimum(1, (seconds - t) / .30)
    elif voice == "bass":
        signal = np.sin(phase) + .13 * np.sin(2 * phase)
        envelope = (1 - np.exp(-t / .012)) * np.exp(-t * 1.3)
    elif voice == "synth":
        signal = sum(np.sin(phase * h) / h ** 1.8 for h in range(1, 7))
        envelope = (1 - np.exp(-t / .018)) * np.exp(-t * 2.2)
    elif voice == "bell":
        signal = np.sin(phase) + .22 * np.sin(phase * 2.001) * np.exp(-t * 3)
        envelope = (1 - np.exp(-t / .012)) * np.exp(-t * 2.1)
    elif voice == "marimba":
        signal = np.sin(phase) + .20 * np.sin(phase * 4) * np.exp(-t * 12)
        envelope = (1 - np.exp(-t / .006)) * np.exp(-t * 4.6)
    else:
        signal = np.sin(phase) + .22 * np.sin(2 * phase) * np.exp(-t * 3)
        signal += .09 * np.sin(3 * phase) * np.exp(-t * 5)
        envelope = (1 - np.exp(-t / .009)) * np.exp(-t * (3.2 if voice == "pluck" else 1.8))
    envelope *= np.clip((seconds - t) / .035, 0, 1)
    return (signal * envelope).astype(np.float32)


def percussion(kind, rng):
    duration = {"kick": .32, "snare": .18, "hat": .07, "shaker": .12}[kind]
    t = np.arange(round(duration * SR)) / SR
    noise = rng.normal(0, 1, len(t))
    if kind == "kick":
        phase = 2 * np.pi * (48 * t + 3.6 * (1 - np.exp(-t * 24)))
        signal = np.sin(phase) * np.exp(-t * 16)
    elif kind == "snare":
        smooth = np.convolve(noise, np.ones(5) / 5, mode="same")
        signal = (.45 * smooth + .28 * np.sin(2 * np.pi * 180 * t)) * np.exp(-t * 28)
    else:
        high = noise - np.convolve(noise, np.ones(13) / 13, mode="same")
        signal = .18 * high * np.exp(-t * (70 if kind == "hat" else 40))
    signal *= np.minimum(1, t / .002) * np.clip((duration - t) / .012, 0, 1)
    return signal.astype(np.float32)


def render(spec, root, replace):
    name, title, bpm, bars, tonic, progression, motif, lead = spec
    target = root / (name + ".ogg")
    if target.exists() and not replace:
        raise FileExistsError(f"Refusing to replace {target}; use --replace after review.")
    beat = 60 / bpm
    frames = round(bars * 4 * beat * SR)
    audio = np.zeros((frames, 2), dtype=np.float32)
    seed = int.from_bytes(hashlib.sha256(name.encode()).digest()[:4], "little")
    rng = np.random.default_rng(seed)
    secondary = name.startswith("secondary/")
    cache = {}

    def add(signal, seconds, gain, pan=0):
        start = round(seconds * SR) % frames
        weights = np.array([math.sqrt((1 - pan) / 2), math.sqrt((1 + pan) / 2)])
        sample = signal[:, None] * (gain * weights).astype(np.float32)
        end = min(len(signal), frames - start)
        audio[start:start + end] += sample[:end]
        if end < len(signal):
            audio[:len(signal) - end] += sample[end:]

    def note(pitch, position, length, voice, gain, pan=0, echo=False):
        key = (pitch, round(length * beat, 4), voice)
        if key not in cache:
            cache[key] = tone(pitch, length * beat, voice)
        signal = cache[key]
        add(signal, position * beat, gain, pan)
        if echo:
            add(signal, (position + .75) * beat, gain * .18, -pan)
            add(signal, (position + 1.5) * beat, gain * .07, pan)

    drums = {kind: percussion(kind, rng) for kind in ("kick", "snare", "hat", "shaker")}
    for bar in range(bars):
        position = bar * 4
        root_degree = progression[(bar // 2) % 4]
        chord = CHORDS[root_degree]
        section = (bar // 8) % 4
        # Los bloques alternan densidad; las notas y colas se mezclan circularmente.
        density = [0.75, 1.0, 0.65, .9][section]
        for k, degree in enumerate(chord):
            note(tonic + degree, position + k * .035, 4.4, "pad", .065, (k - 1.5) * .26)
            if bar % 2 == 0 or secondary:
                note(tonic + degree, position + .12 + k * .045, 2.8, "keys", .10, (k - 1.5) * .18)
        bass_note = tonic + root_degree - 24
        for offset in ([0, 1.5, 2.5, 3.5] if secondary else [0, 2.5]):
            note(bass_note, position + offset, .85 if secondary else 1.5, "bass", .22)
        melody_slots = [0.5, 1.75, 2.5, 3.25] if secondary else [.5, 2.25]
        if section == 2 and bar % 2:
            melody_slots = melody_slots[:1]
        for k, offset in enumerate(melody_slots):
            degree = motif[(bar * 2 + k) % len(motif)]
            if section == 1 and bar % 4 == 3:
                degree = chord[(k + 1) % 4]
            note(tonic + 12 + degree, position + offset, 1.3, lead,
                 .13 * density, .18 * (-1 if k % 2 else 1), True)
        if secondary or name in ("robots", "prehistoric", "garden"):
            for k in range(8 if secondary else 4):
                note(tonic + chord[k % 4] + 12, position + k * (0.5 if secondary else 1),
                     .45, "pluck", .040 * density, .38 * (-1 if k % 2 else 1), secondary)
        drum_gain = .65 if secondary else .38
        if name == "night":
            drum_gain *= .4
        for offset in ([0, 1.5, 2, 3.5] if secondary else [0, 2.5]):
            add(drums["kick"], (position + offset) * beat, .40 * drum_gain)
        for offset in [1, 3]:
            add(drums["snare"], (position + offset + .035) * beat, .23 * drum_gain, -.06)
        for k in range(8):
            swing = .07 if k % 2 and not secondary else 0
            add(drums["shaker" if not secondary else "hat"],
                (position + k * .5 + swing) * beat,
                .17 * drum_gain * (1 if k % 2 else .75), .30)
    # Nivel RMS común, margen de pico y sin silencios añadidos al bucle.
    rms = float(np.sqrt(np.mean(audio.astype(np.float64) ** 2)))
    peak = float(np.max(np.abs(audio)))
    gain = min(10 ** (-21 / 20) / rms, .88 / peak)
    audio *= gain
    target.parent.mkdir(parents=True, exist_ok=True)
    # Bloques pequeños evitan desbordar la pila del codificador Vorbis en Windows.
    with sf.SoundFile(target, "w", samplerate=SR, channels=2, format="OGG", subtype="VORBIS") as output:
        for start in range(0, len(audio), 4096):
            output.write(audio[start:start + 4096])
    decoded, rate = sf.read(target, dtype="float32")
    assert rate == SR and decoded.shape == audio.shape
    assert np.isfinite(decoded).all() and np.max(np.abs(decoded)) < 1
    report = {"file": str(target.as_posix()), "title": title, "bpm": bpm,
              "seconds": round(frames / SR, 3), "sample_rate": SR,
              "peak_dbfs": round(float(20 * np.log10(np.max(np.abs(decoded)))), 2),
              "rms_dbfs": round(float(20 * np.log10(np.sqrt(np.mean(decoded ** 2)))), 2),
              "seam_delta": round(float(np.max(np.abs(decoded[0] - decoded[-1]))), 6),
              "sha256": hashlib.sha256(target.read_bytes()).hexdigest()}
    print(json.dumps(report, ensure_ascii=False), flush=True)
    return report


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--replace", action="store_true")
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[1]
    reports = [render(spec, root / "game/audio/themes", args.replace) for spec in TRACKS]
    for report in reports:
        report["file"] = str(Path(report["file"]).relative_to(root).as_posix())
    (root / "docs/MUSIC_MANIFEST.json").write_text(
        json.dumps(reports, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
