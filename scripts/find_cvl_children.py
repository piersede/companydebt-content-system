"""Find WP pages whose parent is /liquidation/creditors-voluntary-liquidation/."""
import sys, json
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from wp_publish import get_credentials, create_authenticated_session

creds = get_credentials(prod=False)
session, api = create_authenticated_session(creds)

# Step 1: find CVL page id
r = session.get(f"{api}/pages", params={"slug": "creditors-voluntary-liquidation", "per_page": 5}, timeout=30)
r.raise_for_status()
pages = r.json()
if not pages:
    print("CVL page not found")
    sys.exit(1)
cvl_id = pages[0]["id"]
print(f"CVL page id: {cvl_id}  link: {pages[0]['link']}")

# Step 2: list children
children = []
page_num = 1
while True:
    r = session.get(f"{api}/pages", params={"parent": cvl_id, "per_page": 100, "page": page_num, "status": "publish,draft,private"}, timeout=30)
    if r.status_code == 400:
        break
    r.raise_for_status()
    batch = r.json()
    if not batch:
        break
    children.extend(batch)
    if len(batch) < 100:
        break
    page_num += 1

print(f"\nFound {len(children)} children:\n")
for c in children:
    print(f"  id={c['id']}  slug={c['slug']}  status={c['status']}  title={c['title']['rendered'][:80]}")
