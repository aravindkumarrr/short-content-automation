import json
from openai import OpenAI

# Load Groq API key and base URL from config
with open("config.json", "r", encoding="utf-8") as f:
    cfg = json.load(f)

# ✅ Initialize OpenAI-compatible client for Groq
client = OpenAI(
    api_key=cfg["groq"]["key"],
    base_url=cfg["groq"]["base_url"]
)

def generate_hook(title, body, model="llama3-70b-8192"):
    prompt = f"""
You are a viral content writer for YouTube Shorts and TikTok. Your job is to write a short, shocking, emotional, or dramatic HOOK for a Reddit story that makes people want to keep watching.

Write 1–2 sentences. End with: "Here's the full story."

Title: {title}

Body: {body[:1000]}
"""

    try:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "user", "content": prompt}
            ],
            temperature=0.9
        )
        content = response.choices[0].message.content
        if content:
            return content.strip()
        else:
            print("⚠️ Empty response content.")
            return None

    except Exception as e:
        print(f"❌ Error generating hook: {e}")
        return None

def process_stories(input_file="story_list.json", output_file="hooked_stories.json"):
    try:
        with open(input_file, "r", encoding="utf-8") as f:
            stories = json.load(f)
    except Exception as e:
        print(f"❌ Error loading {input_file}: {e}")
        return

    hooked_stories = []
    for i, story in enumerate(stories):
        print(f"\n🪝 [{i+1}/{len(stories)}] Generating hook for: {story['title'][:60]}...")
        hook = generate_hook(story["title"], story["body"])
        if hook:
            story["hook"] = hook
            hooked_stories.append(story)
        else:
            print("⚠️ Skipping story due to error or empty hook.")

    try:
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(hooked_stories, f, indent=2, ensure_ascii=False)
        print(f"\n✅ Done! Saved {len(hooked_stories)} hooked stories to {output_file}")
    except Exception as e:
        print(f"❌ Error saving to {output_file}: {e}")

# if __name__ == "__main__":
#     process_stories()
