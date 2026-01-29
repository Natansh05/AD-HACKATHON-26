import requests
from state.session import get_access_token

AUDIO_LIST_URL = "http://13.234.226.222/api/recordings/"
AUDIO_REVIEW_URL = "http://13.234.226.222/api/recordings/{uuid}/"

# ---------------- FETCH ----------------
def fetch_audios():
    token = get_access_token()
    if not token:
        return []

    headers = {
        "Authorization": f"Bearer {token}"
    }

    try:
        response = requests.get(
            AUDIO_LIST_URL,
            headers=headers,
            timeout=10
        )

        if response.status_code != 200:
            return []

        data = response.json()
        results = data.get("results", [])

        normalized = []

        for item in results:
            normalized.append({
                "id": item.get("uuid"),
                "language": item.get("language", {}).get("code"),
                "date": item.get("call_date", "")[:10],
                "playback_url": item.get("audio_url"),
                "feedback": "",
                "rating": 0 if not item.get("is_rated") else item.get("ratings_count", 0),
                "quality_tags": item.get("tags", [])
            })

        return normalized

    except requests.exceptions.RequestException:
        return []


# ---------------- SAVE / POST ----------------
def save_audio_review(audio_id, rating, feedback, quality_tags):
    token = get_access_token()
    if not token:
        return False, "Not authenticated"

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    payload = {
        "rating": rating,
        "feedback": feedback,
        "tags": quality_tags
    }

    try:
        response = requests.post(
            AUDIO_REVIEW_URL.format(uuid=audio_id),
            headers=headers,
            json=payload,
            timeout=10
        )

        if response.status_code in (200, 201):
            return True, "Saved successfully"
        else:
            return False, response.text

    except requests.exceptions.RequestException as e:
        return False, str(e)
