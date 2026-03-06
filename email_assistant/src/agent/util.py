import json
import re
from typing import Dict


def convert_response_to_json(data: str) -> Dict:

    match = re.search(r"\{.*\}", data, re.DOTALL)

    if match:
        json_response = json.loads(match.group())
        return json_response
    else:
        raise ValueError("No JSON found in response")
