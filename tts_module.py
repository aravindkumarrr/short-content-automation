# ==============================================================================
# INSTRUCTIONS FOR USING THIS MODULE:
# ==============================================================================
# 1. Ensure necessary libraries are installed:
#    pip install kokoro-tts soundfile resampy numpy torch
# 2. Import and call the function from another script:
#    from tts_module import generate_voiceovers
#    generate_voiceovers('path/to/input_folder', 'path/to/output_folder')
# 3. The function will process all .txt files in the input folder and save .wav files to the output folder.
# ==============================================================================

# Import the necessary libraries
from kokoro import KPipeline
import soundfile as sf
import resampy
import numpy as np
import warnings
import os

def generate_voiceovers(input_folder, output_folder):
    """
    Iterates over .txt files in the input folder, reads their content,
    generates TTS audio with speed adjustment, and saves combined .wav files to the output folder.
    
    Args:
        input_folder (str): Path to the folder containing .txt files.
        output_folder (str): Path to the folder where .wav files will be saved.
    """



    if not os.path.isdir(input_folder):
        print(f"Error: '{input_folder}' is not a valid directory.")
        return

    # Create output folder if it doesn't exist
    os.makedirs(output_folder, exist_ok=True)

    # Initialize the TTS pipeline once (outside the loop for efficiency).
    try:
        # Use 'a' for American English (valid code); adjust if needed for other languages
        warnings.filterwarnings("ignore", category=UserWarning, module="torch.nn.modules.rnn")
        pipeline = KPipeline(lang_code='a', repo_id='hexgrad/Kokoro-82M')
    except Exception as e:
        print(f"Error initializing KPipeline. Have you accepted the model license on Hugging Face Hub?")
        print(f"Original error: {e}")
        raise

    # Define constants
    original_sample_rate = 24000
    speed_factor = 1.1
    target_sample_rate = int(original_sample_rate / speed_factor)

    # Check for matching files
    matching_files = [f for f in os.listdir(input_folder) if f.endswith('.txt')]
    if not matching_files:
        print(f"No .txt files found in '{input_folder}'. Nothing to process.")
        return

    # Iterate over files in the input folder
    for filename in matching_files:
        file_path = os.path.join(input_folder, filename)

        voicelist = ['af_heart', 'af_bella', 'af_nicole', 'af_aoede', 'af_kore', 'af_sarah', 'af_nova', 'af_sky', 'af_alloy', 'af_jessica', 'af_river', 'am_michael', 'am_fenrir', 'am_puck', 'am_echo', 'am_eric', 'am_liam', 'am_onyx', 'am_santa', 'am_adam', 'bf_emma', 'bf_isabella', 'bf_alice', 'bf_lily', 'bm_george', 'bm_fable', 'bm_lewis', 'bm_daniel']
        voice = np.random.choice(voicelist)
        try:
            # Read the file content
            with open(file_path, 'r', encoding='utf-8') as f:
                text = f.read().strip()
            
            if not text:
                print(f"Skipping empty file: {filename}")
                continue

            print(f"\nProcessing file: {filename}")
            print("Starting audio generation...")

            # Generate audio chunks (use a valid voice matching lang_code='a')
            generator = pipeline(text, voice
                                 #='af_heart'
                                 )  # Valid American English voice

            # List to hold processed audio segments
            all_audio_segments = []

            # Loop through each generated audio segment
            for i, (gs, ps, audio_original) in enumerate(generator):
                print(f"Processing segment {i}... Global Step: {gs}, Phoneme Step: {ps}")

                # Convert Tensor to NumPy array
                audio_original_np = audio_original.cpu().numpy()

                # Ensure floating-point format for resampling
                if audio_original_np.dtype != np.float32 and audio_original_np.dtype != np.float64:
                    audio_original_np = audio_original_np.astype(np.float32) / np.iinfo(audio_original_np.dtype).max

                # Resample to adjust speed
                audio_speed_up = resampy.resample(
                    audio_original_np,
                    sr_orig=original_sample_rate,
                    sr_new=target_sample_rate,
                    filter='kaiser_best'
                )

                # Add to segments list
                all_audio_segments.append(audio_speed_up)
                print(f"Segment {i} processed and added to the queue.")
                print("-" * 20)

            # Combine and save if segments exist
            if all_audio_segments:
                print("All segments processed. Combining into a single audio file...")
                final_audio = np.concatenate(all_audio_segments)

                # Define output filename based on input file
                base_name = os.path.splitext(filename)[0]
                output_filename = f'{base_name}_speed_{speed_factor}.wav'
                output_path = os.path.join(output_folder, output_filename)

                # Save the audio
                sf.write(output_path, final_audio, original_sample_rate)

                print("\n==================================================")
                print("✅ Audio for this file processed and saved successfully!")
                print(f"Find your audio file here: {os.path.abspath(output_path)}")
                print("==================================================")
            else:
                print(f"No audio segments generated for {filename}. Check input text, voice, and model compatibility.")

        except Exception as e:
            print(f"Error processing {filename}: {e}")

    print("\nAll files in the input folder have been processed.")

# Optional: For testing the module standalone
if __name__ == "__main__":
    # Example usage with your paths
    input_path = r'C:\Users\Aravind Kumar\Desktop\short-form-content-creation\exports'
    output_path = r'C:\Users\Aravind Kumar\Desktop\short-form-content-creation\wavfiles'
    generate_voiceovers(input_path, output_path)

