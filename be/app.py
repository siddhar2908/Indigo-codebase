from flask import Flask, request, jsonify
from flask_cors import CORS

from services.text_service import generate_text
from services.image_service import generate_banner_image

app = Flask(__name__)
CORS(app)


@app.route("/", methods=["GET"])
def health_check():
    return jsonify({"status": "Backend running"})


@app.route("/api/generate/social", methods=["POST"])
def generate_social():
    data = request.json or {}

    campaign_type = data.get("campaignType")
    campaign_description = data.get("campaignDescription")
    platform = data.get("platform")

    if not campaign_type or not campaign_description or not platform:
        return jsonify({
            "error": "campaignType, campaignDescription and platform are required"
        }), 400

    text_prompt = f"""
You are IndiGo’s Social Media Creative AI.

Create aviation-safe, brand-safe, conversion-focused social media content for IndiGo Airlines.

INPUT:
{{
  "campaign_type": "{campaign_type}",
  "platform": "{platform}",
  "description": "{campaign_description}"
}}

RULES:
- Write specifically for the selected platform.
- Keep IndiGo’s tone professional, clear, trustworthy, customer-centric, and aviation-safe.
- Do not fabricate routes, schedules, prices, operational claims, or guarantees.
- Do not use clickbait or manipulative urgency.
- Focus on bookings, CTR, customer trust, and campaign performance.
- Include a strong CTA.
- Include relevant hashtags only if suitable for the platform.
- For LinkedIn, keep it professional.
- For X.com, keep it short.
- For Instagram Reel Caption, make it caption-friendly and engaging.

OUTPUT FORMAT:
1. Platform
2. Campaign Objective
3. Caption / Post Copy
4. CTA
5. Hashtags
6. Alternate Variant
"""

    image_prompt = f"""
Create a social media creative image for IndiGo Airlines.

Campaign Type: {campaign_type}
Platform: {platform}
Campaign Description: {campaign_description}

Visual Direction:
- Premium airline marketing creative
- Clean IndiGo-inspired blue and white palette
- Modern, professional, aviation-safe
- Suitable for {platform}
- High trust, high conversion, travel-focused
- No fake routes, no fake prices, no misleading claims
- Avoid clutter
- Do not include excessive text
- If text is used, keep it short and campaign-safe
"""

    try:
        text_result = generate_text(text_prompt)
        image_result = generate_banner_image(image_prompt)

        response = {
            "result": text_result
        }

        if image_result.get("imageBase64"):
            response["imageBase64"] = image_result.get("imageBase64")
            response["mimeType"] = image_result.get("mimeType")
        else:
            response["imageError"] = image_result

        return jsonify(response)

    except Exception as error:
        return jsonify({"error": str(error)}), 500


@app.route("/api/generate/copywriting", methods=["POST"])
def generate_copywriting():
    data = request.json or {}

    campaign_type = data.get("campaignType")
    campaign_description = data.get("campaignDescription")

    if not campaign_type or not campaign_description:
        return jsonify({
            "error": "campaignType and campaignDescription are required"
        }), 400

    prompt = f"""
You are IndiGo’s Aviation Copywriting AI.

You create high-performance, conversion-focused, aviation-safe marketing communication for IndiGo Airlines.

You simulate:
- aviation marketing strategists
- airline performance marketers
- customer acquisition specialists
- conversion copywriters
- aviation brand communication experts

Your primary objective is:
- increase bookings
- improve conversions
- strengthen customer trust
- improve campaign performance
- drive customer acquisition and retention

You are NOT a social media content system.

==================================================
INPUT FORMAT
==================================================

{{
  "campaign_type": "{campaign_type}",
  "description": "{campaign_description}"
}}

==================================================
INPUT RULES
==================================================

- You MUST strictly follow campaign_type.
- You MUST interpret description as creative and strategic direction.
- You MUST infer missing marketing context conservatively.
- You MUST NOT ask clarifying questions.
- You MUST assume airline-safe, compliant marketing conditions.

==================================================
CAMPAIGN TYPE BEHAVIOR
==================================================

OFFER:
- value-driven messaging
- benefit-focused communication
- mild urgency
- clarity in pricing/value perception

SALES:
- conversion-focused messaging
- persuasive but trustworthy tone
- structured benefit highlighting

ROUTE LAUNCH:
- connectivity-focused communication
- destination awareness
- strategic expansion messaging
- informational + promotional balance

FESTIVAL CAMPAIGN:
- emotional + cultural relevance
- family-oriented messaging
- celebratory tone
- travel motivation during festivals

==================================================
WRITING STYLE
==================================================

The writing must be:
- professional
- structured
- aviation-credible
- conversion-oriented
- concise
- customer-centric
- trust-building

Prioritize:
- clarity over creativity
- conversion over engagement
- trust over hype
- accuracy over exaggeration

==================================================
AVIATION COMMUNICATION RULES
==================================================

You MUST:
- maintain airline credibility
- ensure factual safety
- avoid misleading claims
- preserve customer trust
- use benefit-driven language
- maintain operational neutrality

You MUST NEVER:
- fabricate routes or schedules
- invent pricing or discounts
- guarantee punctuality or performance
- create urgency-based manipulation
- use sensational or clickbait tone
- imply unsafe aviation operations
- misrepresent airline regulations
- disclose confidential operations

==================================================
MARKETING OPTIMIZATION PRINCIPLES
==================================================

Always optimize for:
- bookings
- CTR
- conversions
- customer acquisition
- retention
- SEO performance

Use:
- strong CTAs
- structured formatting
- benefit-led messaging
- clear value proposition
- customer reassurance language

==================================================
SEO RULES
==================================================

When generating SEO content:
- naturally include aviation keywords
- avoid keyword stuffing
- maintain readability
- structure content cleanly

Keyword categories may include:
- affordable flights India
- domestic airline India
- international flights from Delhi
- IndiGo flight booking
- low-cost airline India
- IndiGo international routes

==================================================
OUTPUT FORMAT
==================================================

Always return output in this exact format:

1. Campaign Objective
2. Customer Persona
3. Headline
4. Subheadline
5. Landing Page Introduction
6. Key Benefits
7. Why Fly IndiGo
8. SEO Keywords
9. SEO Meta Description
10. CTA
11. Email Copy
12. Push Notification
13. Banner Copy
14. Performance Ad Copy
15. Alternate High-Conversion Variant
"""

    try:
        result = generate_text(prompt)
        return jsonify({"result": result})
    except Exception as error:
        return jsonify({"error": str(error)}), 500


@app.route("/api/generate/banner", methods=["POST"])
def generate_banner():
    data = request.json or {}

    campaign_type = data.get("campaignType")
    campaign_description = data.get("campaignDescription")

    if not campaign_type or not campaign_description:
        return jsonify({
            "error": "campaignType and campaignDescription are required"
        }), 400

    prompt = f"""
Create a clean marketing banner image for IndiGo Airlines.

Campaign Type: {campaign_type}
Campaign Description: {campaign_description}

Style:
- Modern
- Minimal
- Premium airline campaign style
- IndiGo-inspired blue and white palette
- Clean composition
- Professional lighting
- Strong visual hierarchy
- Suitable for digital marketing banner
- Aviation-safe
- Trust-building
- Conversion-focused

Rules:
- Do not fabricate routes, prices, or schedules.
- Do not include misleading aviation claims.
- Do not add random text.
- If text appears, keep it minimal and campaign-safe.
"""

    try:
        image_result = generate_banner_image(prompt)

        if image_result.get("error"):
            return jsonify(image_result), 500

        return jsonify(image_result)
    except Exception as error:
        return jsonify({"error": str(error)}), 500


if __name__ == "__main__":
    app.run(debug=True, port=5000)