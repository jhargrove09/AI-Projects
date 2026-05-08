import json
import boto3

bedrock = boto3.client("bedrock-runtime", region_name="us-east-1")

PERSONAS = {
    "wise_sensei": (
        "You are a wise, calm yoga sensei. Speak with warmth and quiet wisdom. "
        "Use gentle metaphors from nature and ancient teachings. "
        "Your tone is unhurried, peaceful, and deeply encouraging."
    ),
    "hype_coach": (
        "You are an intense, high-energy anime hype coach. "
        "You believe every yoga session is a training arc. "
        "Speak with fire and passion — every pose is a power-up!"
    ),
    "mysterious_guide": (
        "You are a mysterious, cool anime guide. Speak minimally but meaningfully. "
        "Every word carries weight. You are like Kakashi — calm, cryptic, legendary."
    ),
    "gentle_healer": (
        "You are a soft, nurturing healer. Your voice is like warm light. "
        "You celebrate every small effort. No rush, no judgment — only kindness."
    ),
}

def build_prompt(persona_key, mood, goal, duration):
    persona_desc = PERSONAS.get(persona_key, PERSONAS["wise_sensei"])
    return f"""
{persona_desc}

A student has come to you for a yoga session with the following details:
- Current mood / energy level: {mood}
- Session goal: {goal}
- Duration: {duration} minutes

Generate a complete, personalized yoga flow. Structure it like this:

1. Opening message (2-3 sentences in your persona's voice)
2. Warm-up poses (2-3 poses)
3. Main flow poses (4-6 poses, suited to the goal)
4. Cool-down poses (2-3 poses)
5. Final relaxation (savasana or breathing exercise)
6. Closing message (1-2 sentences)

For each pose include:
- Pose name (English and Sanskrit)
- How long to hold it
- A breathing cue
- A short motivational note in your persona's voice

Keep the total session within {duration} minutes.
"""

def lambda_handler(event, context):
    try:
        body = json.loads(event.get("body", "{}"))
        persona  = body.get("persona",  "wise_sensei")
        mood     = body.get("mood",     "neutral")
        goal     = body.get("goal",     "stress relief")
        duration = body.get("duration", 20)

        prompt = build_prompt(persona, mood, goal, duration)

        response = bedrock.invoke_model(
            modelId="anthropic.claude-3-sonnet-20240229-v1:0",
            contentType="application/json",
            accept="application/json",
            body=json.dumps({
                "anthropic_version": "bedrock-2023-05-31",
                "max_tokens": 2048,
                "messages": [{"role": "user", "content": prompt}],
            }),
        )

        result = json.loads(response["body"].read())
        flow_text = result["content"][0]["text"]

        return {
            "statusCode": 200,
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*",
            },
            "body": json.dumps({"flow": flow_text}),
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "headers": {"Access-Control-Allow-Origin": "*"},
            "body": json.dumps({"error": str(e)}),
        }