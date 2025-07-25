from fetch_post import*
from summarize import*
from TTS_preprocessing import *
# from failedTTS.TTS import*
from tts_module import generate_voiceovers

if __name__ == "__main__":
    stories = fetch_valid_stories(count=5)  # Fetch 5 stories
    with open("story_list.json", "w", encoding="utf-8") as f:
        json.dump(stories, f, indent=2, ensure_ascii=False)

    print(f"\n🎉 Done! Saved {len(stories)} stories to story_list.json")

    process_stories()

    ttfpreprocessing()
    
    input_path=r'C:\Users\Aravind Kumar\Desktop\short-form-content-creation\exports'
    output_path=r'C:\Users\Aravind Kumar\Desktop\short-form-content-creation\wavfiles'
    generate_voiceovers(input_path, output_path)




