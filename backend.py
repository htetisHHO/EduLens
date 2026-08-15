"""Evidence lookup backend for the TruthLens educational chatbot.

Set GOOGLE_FACTCHECK_API_KEY to enable live lookups from the Google Fact
Check Tools API. Results are always shown as evidence to review, never as an
automatic declaration that a post is fake.
"""
import json
import os
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen


API_URL = "https://factchecktools.googleapis.com/v1alpha1/claims:search"


def _label(rating: str) -> str:
    value = rating.lower()
    if any(word in value for word in ("false", "incorrect", "pants on fire", "misleading")):
        return "Not supported by this fact check"
    if any(word in value for word in ("mixed", "partly", "partially", "half true")):
        return "Needs more context"
    if any(word in value for word in ("true", "correct", "accurate", "verified")):
        return "Supported by this fact check"
    return "A relevant fact check was found"


def analyze_claim(post: str) -> dict:
    """Find existing fact checks for a user-supplied claim."""
    claim = " ".join(post.split())
    if len(claim) < 12:
        return {"ok": False, "error": "Please enter a longer claim or social-media post."}

    api_key = os.environ.get("GOOGLE_FACTCHECK_API_KEY")
    if not api_key:
        return {
            "ok": False,
            "error": "Live source lookup is not configured yet.",
            "tip": "Add a Google Fact Check Tools API key to enable real fact-check source searches.",
        }

    query = urlencode({"query": claim, "key": api_key, "languageCode": "en-US", "pageSize": 5})
    request = Request(f"{API_URL}?{query}", headers={"Accept": "application/json"})
    try:
        with urlopen(request, timeout=15) as response:
            payload = json.load(response)
    except HTTPError as exc:
        return {"ok": False, "error": f"Source lookup failed (HTTP {exc.code})."}
    except URLError:
        return {"ok": False, "error": "Could not reach the source lookup service. Check your internet connection."}

    claims = payload.get("claims", [])
    sources = []
    for item in claims:
        for review in item.get("claimReview", []):
            publisher = review.get("publisher", {})
            sources.append({
                "publisher": publisher.get("name", "Fact-check publisher"),
                "url": review.get("url", ""),
                "title": review.get("title", item.get("text", "Fact check")),
                "rating": review.get("textualRating", "Rating not provided"),
                "reliability": "Published fact-check source",
            })

    if not sources:
        return {
            "ok": True,
            "claim": claim,
            "verdict": "Unable to verify yet",
            "explanation": "No matching published fact check was returned. This does not prove the post is true or false.",
            "sources": [],
            "source_reliability": "No matching published fact check was found.",
            "tip": "Try a shorter, specific claim and check the original source, date, and context.",
        }

    first = sources[0]
    return {
        "ok": True,
        "claim": claim,
        "verdict": _label(first["rating"]),
        "explanation": f"A published fact check from {first['publisher']} rated a related claim as: {first['rating']}.",
        "sources": sources,
        "source_reliability": "The evidence comes from published ClaimReview fact checks returned by the source search.",
        "tip": "Open the original fact check and compare its date, wording, and scope with the social-media post.",
    }
