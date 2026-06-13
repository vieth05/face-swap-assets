import json
import re
from pathlib import Path

BASE_URL = "https://raw.githubusercontent.com/vieth05/face-swap-assets/main"

ROOT = Path(__file__).parent

config = {
    "face2face": {"categories": []},
    "smile": {"items": []},
    "hair": {"categories": []},
    "ai_art": {"categories": []},
    "eyeglasses": {"items": []}
}


def get_url(path: Path):
    relative = path.relative_to(ROOT).as_posix()
    return f"{BASE_URL}/{relative}"


def extract_number(name: str):
    match = re.search(r'\d+', name)
    return int(match.group()) if match else 999999


# =========================
# FACE2FACE IMAGE
# =========================
image_root = ROOT / "face2face" / "image"

if image_root.exists():
    for category in sorted(image_root.iterdir()):
        if not category.is_dir():
            continue

        items = []

        images = sorted(
            [f for f in category.iterdir()
             if f.is_file() and f.suffix.lower() in [".png", ".jpg", ".jpeg"]],
            key=lambda x: extract_number(x.stem)
        )

        for image in images:
            if image.name.startswith("."):
                continue

            items.append({
                "id": image.stem,
                "name": "",
                "thumbnail": get_url(image),
                "url": get_url(image)
            })

        config["face2face"]["categories"].append({
            "id": category.name,
            "name": category.name.replace("_", " ").title(),
            "type": "image",
            "items": items
        })


# =========================
# FACE2FACE VIDEO
# =========================
video_root = ROOT / "face2face" / "video"

if video_root.exists():
    for category in sorted(video_root.iterdir()):
        if not category.is_dir():
            continue

        items = []

        # Make Photo Sing
        if category.name == "makephotosing":

            videos = sorted(
                category.glob("*.mp4"),
                key=lambda x: extract_number(x.stem)
            )

            for video in videos:
                items.append({
                    "id": video.stem,
                    "name": "",
                    "thumbnail": get_url(video),
                    "url": get_url(video)
                })

            config["face2face"]["categories"].append({
                "id": category.name,
                "name": "Make Photo Sing",
                "type": "video",
                "thumbnailType": "video",
                "items": items
            })

        # Normal video categories
        else:

            gifs = {f.stem: f for f in category.glob("*.gif")}
            videos = {f.stem: f for f in category.glob("*.mp4")}

            ids = sorted(
                set(gifs.keys()) & set(videos.keys()),
                key=extract_number
            )

            for item_id in ids:
                items.append({
                    "id": item_id,
                    "name": "",
                    "thumbnail": get_url(gifs[item_id]),
                    "url": get_url(videos[item_id])
                })

            config["face2face"]["categories"].append({
                "id": category.name,
                "name": category.name.replace("_", " ").title(),
                "type": "video",
                "thumbnailType": "gif",
                "items": items
            })


# =========================
# SMILE
# =========================
smile_root = ROOT / "smile"

if smile_root.exists():
    images = sorted(
        [f for f in smile_root.iterdir()
         if f.is_file() and f.suffix.lower() in [".png", ".jpg", ".jpeg"]],
        key=lambda x: extract_number(x.stem)
    )

    for image in images:
        if image.name.startswith("."):
            continue

        config["smile"]["items"].append({
            "id": str(extract_number(image.stem)),
            "name": "",
            "thumbnail": get_url(image),
            "url": get_url(image)
        })


# =========================
# EYEGLASSES
# =========================
eye_root = ROOT / "eyeglasses"

if eye_root.exists():
    images = sorted(
        [f for f in eye_root.iterdir()
         if f.is_file() and f.suffix.lower() in [".png", ".jpg", ".jpeg"]],
        key=lambda x: extract_number(x.stem)
    )

    for image in images:
        if image.name.startswith("."):
            continue

        config["eyeglasses"]["items"].append({
            "id": image.stem,
            "name": "",
            "thumbnail": get_url(image),
            "url": get_url(image)
        })


# =========================
# HAIR
# =========================
hair_root = ROOT / "hair"

for folder in ["hair_style", "hair_color"]:

    path = hair_root / folder

    if not path.exists():
        continue

    items = []

    for image in sorted(path.glob("*.png")):

        if image.name.startswith("."):
            continue

        name = image.stem

        if folder == "hair_color":
            display_name = name.replace("color_", "")
        else:
            display_name = name

        display_name = display_name.replace("_", " ").title()

        items.append({
            "id": name,
            "name": display_name,
            "thumbnail": get_url(image),
            "url": get_url(image)
        })

    config["hair"]["categories"].append({
        "id": folder,
        "name": folder.replace("_", " ").title(),
        "items": items
    })


# =========================
# AI ART
# =========================
ai_root = ROOT / "ai_art"

if ai_root.exists():
    for category in sorted(ai_root.iterdir()):

        if not category.is_dir():
            continue

        items = []

        images = sorted(
            [f for f in category.iterdir()
             if f.is_file() and f.suffix.lower() in [".png", ".jpg", ".jpeg"]],
            key=lambda x: extract_number(x.stem)
        )

        for image in images:
            if image.name.startswith("."):
                continue

            items.append({
                "id": image.stem,
                "name": "",
                "thumbnail": get_url(image),
                "url": get_url(image)
            })

        config["ai_art"]["categories"].append({
            "id": category.name,
            "name": category.name.replace("_", " ").title(),
            "items": items
        })


# =========================
# SAVE JSON
# =========================
output = ROOT / "config" / "config.json"

output.parent.mkdir(exist_ok=True)

with open(output, "w", encoding="utf-8") as f:
    json.dump(config, f, ensure_ascii=False, indent=2)

print(f"Generated: {output}")