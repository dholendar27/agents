import os
from typing import Any, Dict

import requests
from dotenv import load_dotenv

load_dotenv()

GOOGLE_MAPS_KEY = os.getenv("GOOGLE_MAPS_KEY")
if not GOOGLE_MAPS_KEY:
    print("Please Enter Google Maps Key")
    exit()


def map_search(query: str, location_bias: str = None) -> Dict[str, Any]:
    """
    Search for places using Google Places API (Text Search).

    Args:
        query: Natural language search query
               (e.g., "Aadhar Seva Kendra in Nashik Maharashtra")
        location_bias: Optional city or region to bias results
                       (e.g., "Nashik, Maharashtra")

    Returns:
        JSON response from Google Places API with place details
    """
    url = "https://places.googleapis.com/v1/places:searchText"

    headers = {
        "Content-Type": "application/json",
        "X-Goog-Api-Key": GOOGLE_MAPS_KEY,
        "X-Goog-FieldMask": (
            "places.displayName,"
            "places.formattedAddress,"
            "places.location,"
            "places.rating,"
            "places.userRatingCount,"
            "places.regularOpeningHours,"
            "places.internationalPhoneNumber,"
            "places.websiteUri,"
            "places.googleMapsUri"
        ),
    }

    data: Dict[str, Any] = {"textQuery": query}

    if location_bias:
        data["locationBias"] = {
            "circle": {
                "center": {"textQuery": location_bias},
                "radius": 50000.0,  # 50 km radius
            }
        }

    try:
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        result = response.json()

        # ✅ Return a clean, agent-friendly summary
        places = result.get("places", [])
        if not places:
            return {
                "status": "no_results",
                "message": f"No places found for query: '{query}'. "
                "Try a broader search term or different location.",
            }

        formatted = []
        for place in places:
            formatted.append(
                {
                    "name": place.get("displayName", {}).get("text", "N/A"),
                    "address": place.get("formattedAddress", "N/A"),
                    "phone": place.get("internationalPhoneNumber", "N/A"),
                    "rating": place.get("rating", "N/A"),
                    "maps_link": place.get("googleMapsUri", "N/A"),
                    "website": place.get("websiteUri", "N/A"),
                    "opening_hours": (
                        place.get("regularOpeningHours", {}).get(
                            "weekdayDescriptions", []
                        )
                    ),
                }
            )

        return {"status": "success", "count": len(formatted), "places": formatted}

    except requests.exceptions.HTTPError as e:
        return {"error": f"HTTP error: {e.response.status_code} - {e.response.text}"}
    except requests.exceptions.RequestException as e:
        return {"error": f"Request failed: {str(e)}"}
