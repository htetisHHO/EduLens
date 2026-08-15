import json
from ollama import chat


class EduLensChatbot:

    def analyze(self, user_claim):

        prompt = f"""
You are EduLens AI.

You ONLY verify educational claims.

Return ONLY valid JSON.

Example:

{{
    "claim":"...",
    "verdict":"Supported",
    "confidence":95,
    "reason":"...",
    "evidence":[
        "Evidence 1",
        "Evidence 2"
    ],
    "sources":[
        {{
            "publisher":"UNESCO",
            "url":"https://www.unesco.org"
        }},
        {{
            "publisher":"Harvard Online",
            "url":"https://pll.harvard.edu"
        }}
    ]
}}

Claim:

{user_claim}
"""

        try:

            response = chat(
                model="llama3.2:3b",
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            )

            data = json.loads(response.message.content)

            return {
                "ok": True,
                **data
            }

        except Exception as e:

            return {
                "ok": False,
                "error": str(e),
                "tip": "The AI could not understand the response."
            }
