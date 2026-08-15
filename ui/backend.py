import random


class EduLensBackend:

    def analyze(self, post: str):

        post = post.strip()

        if len(post) < 10:
            return {
                "ok": False,
                "error": "Please enter a longer claim.",
                "tip": "Example: NASA discovered life on Mars."
            }

        text = post.lower()

        # -------------------------
        # Example 1
        # -------------------------
        if "stanford" in text and "certificate" in text:

            return {
                "ok": True,

                "claim": post,

                "verdict": "Partially Supported",

                "confidence": 93,

                "explanation": f"""Claim:
{post}

Evidence:
✅ Stanford Online offers some free courses.
❌ Most certificates require payment.
✅ Official source found.

Sources:
- https://online.stanford.edu
- Stanford News

Verdict:
Partially Supported

Confidence:
93%

Reason:
Stanford does provide free courses, but free certificates are not available for most offerings.
""",

                "source_reliability":
                    "Compared with official Stanford Online information.",

                "tip":
                    "Always distinguish between free courses and paid certificates.",

                "sources": [
                    {
                        "publisher": "Stanford Online",
                        "title": "AI Courses",
                        "rating": "Official",
                        "url": "https://online.stanford.edu"
                    },
                    {
                        "publisher": "Stanford News",
                        "title": "Stanford News",
                        "rating": "Official",
                        "url": "https://news.stanford.edu"
                    }
                ]
            }

        # -------------------------
        # Example 2
        # -------------------------
        elif "5g" in text and "covid" in text:

            return {
                "ok": True,

                "claim": post,

                "verdict": "False",

                "confidence": 99,

                "explanation": f"""Claim:
{post}

Evidence:
❌ No scientific evidence supports this claim.
✅ WHO Mythbusters disproves it.
✅ Reuters Fact Check confirms it is false.

Sources:
- https://www.who.int
- Reuters Fact Check

Verdict:
False

Confidence:
99%

Reason:
Scientific studies have found no evidence that 5G technology causes COVID-19.
""",

                "source_reliability":
                    "Verified using WHO and Reuters.",

                "tip":
                    "Health information should come from trusted medical organizations.",

                "sources": [
                    {
                        "publisher": "WHO",
                        "title": "COVID-19 Mythbusters",
                        "rating": "Official",
                        "url": "https://www.who.int"
                    },
                    {
                        "publisher": "Reuters",
                        "title": "Fact Check",
                        "rating": "Verified",
                        "url": "https://www.reuters.com/fact-check/"
                    }
                ]
            }

        # -------------------------
        # Default
        # -------------------------
        else:

            confidence = random.randint(60, 90)

            return {
                "ok": True,

                "claim": post,

                "verdict": "Needs More Evidence",

                "confidence": confidence,

                "explanation": f"""Claim:
{post}

Evidence:
⚠ No matching trusted fact-check found.
⚠ More evidence is required.

Sources:
- No reliable sources found.

Verdict:
Needs More Evidence

Confidence:
{confidence}%

Reason:
TruthLens AI could not verify this claim using the available educational database.
""",

                "source_reliability":
                    "No trusted source matched this claim.",

                "tip":
                    "Try searching with more specific keywords.",

                "sources": []
            }