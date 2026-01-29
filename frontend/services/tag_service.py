import requests
from state.session import get_access_token

TAG_LIST_URL = "http://13.234.226.222/api/rating-tags/"

# ---------------- GET TAGS ----------------
def fetch_rating_tags():
    token = get_access_token()
    if not token:
        return []

    headers = {
        "Authorization": f"Bearer {token}"
    }

    try:
        response = requests.get(
            TAG_LIST_URL,
            headers=headers,
            timeout=10
        )

        if response.status_code != 200:
            return []

        data = response.json()
        results = data.get("results", [])

        # Only return tag names (what UI needs)
        return [tag["name"] for tag in results]

    except requests.exceptions.RequestException:
        return []


# ---------------- POST TAG ----------------
def create_rating_tag(tag_name: str):
    token = get_access_token()
    if not token:
        return False, "Not authenticated"

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    payload = {
        "name": tag_name
    }

    try:
        response = requests.post(
            TAG_LIST_URL,
            headers=headers,
            json=payload,
            timeout=10
        )

        if response.status_code in (200, 201):
            return True, "Tag created"
        else:
            return False, response.text

    except requests.exceptions.RequestException as e:
        return False, str(e)
