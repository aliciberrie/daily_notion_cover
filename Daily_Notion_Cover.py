import requests, random, os
from datetime import date

# -----------------------------
# Notion credentials
# -----------------------------
NOTION_TOKEN = os.getenv("NOTION_TOKEN")  # Or paste token directly
DATABASE_ID = "26152b919b8080a2b262dc9817020768"
PAGE_ID = "26152b919b808080982efe21d3d7a1a4"

headers = {
    "Authorization": f"Bearer {NOTION_TOKEN}",
    "Notion-Version": "2022-06-28",
    "Content-Type": "application/json"
}

# -----------------------------
# Step 1: Query database for pages
# -----------------------------
query_url = f"https://api.notion.com/v1/databases/{DATABASE_ID}/query"
res = requests.post(query_url, headers=headers)

if res.status_code != 200:
    print("❌ Error querying database:", res.text)
    exit()

data = res.json()

# -----------------------------
# Step 2: Extract cover image URLs
# Pull the "cover" field from each page in the image database.
# -----------------------------
images = []
for row in data["results"]:
    try:
        cover = row.get("cover")
        if cover and cover.get("type") == "external":
            images.append(cover["external"]["url"])
        elif cover and cover.get("type") == "file":
            images.append(cover["file"]["url"])
    except KeyError:
        pass

if not images:
    print("⚠️ No cover images found in database")
    exit()

# -----------------------------
# Step 3: Pick random image based on today's date
# -----------------------------
today_str = date.today().isoformat()  # e.g., '2025-09-02'
random.seed(today_str)                # Seed with today's date
image_url = random.choice(images)     # Deterministic per day

# -----------------------------
# Step 4: Update target page cover
# -----------------------------
page_url = f"https://api.notion.com/v1/pages/{PAGE_ID}"
payload = {
    "cover": {
        "external": {
            "url": image_url
        }
    }
}

res = requests.patch(page_url, headers=headers, json=payload)

if res.status_code == 200:
    print(f"✅ Cover updated to {image_url}")
else:
    print(f"❌ Error updating cover: {res.status_code} - {res.text}")
