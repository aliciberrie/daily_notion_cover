import requests, random, os

# Notion credentials ... os.getenv()
NOTION_TOKEN = "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"  # Or paste token directly (not recommended)
DATABASE_ID = "26152b919b8080a2b262dc9817020768" 
PAGE_ID = "26152b919b808080982efe21d3d7a1a4"

headers = {
    "Authorization": f"Bearer {NOTION_TOKEN}",
    "Notion-Version": "2022-06-28",
    "Content-Type": "application/json" # what is this?
}

# Step 1: Query database for image URLs
query_url = f"https://api.notion.com/v1/databases/{DATABASE_ID}/query"
res = requests.post(query_url, headers=headers)

if res.status_code != 200:
    print("❌ Error querying database:", res.text)
    exit()

data = res.json()

# Extract URLs from "Image URL" property
images = []
for row in data["results"]:
    try:
        url = row["properties"]["Image URL"]["url"]
        if url:
            images.append(url)
    except KeyError:
        pass

if not images:
    print("⚠️ No images found in database")
    exit()

# Step 2: Pick random image
image_url = random.choice(images)

# Step 3: Update Notion page cover
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