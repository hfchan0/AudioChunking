import subprocess
from multiprocessing import Process, Pool
import os, time
import sys
import librosa

def output_audio(original_audio_file, timeslot):
    start, end = timeslot
    os.system(f"ffmpeg -ss {start} -to {start + end} -i {original_audio_file} audio_{start}.wav")

def chunking(original_audio_file, min_secs, max_secs):
    # debug
    return [(0,100), (100,200), (200,300)]

def video2audio(video_file, output_file_extension = "wav"):
    filename, file_extension = os.path.splitext(video_file)
    subprocess.call(["ffmpeg", "-y", "-i", video_file, f"{filename}.{output_file_extension}"], 
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.STDOUT)
    return filename + output_file_extension

def main():
    # Check if arguments are valid
    if len(sys.argv) != 4:
        print("Not enough or too much argument(s).")
        print('Number of arguments:', len(sys.argv), 'arguments.')
        print('Argument List:', str(sys.argv))
    
    # Check if the type of input file is supported
    original_audio_file = ""
    file_type = -1
    supported_video_extension = [".mp4", ".webm", ".ts"]
    supported_audio_extension = [".mp3", ".wav"]
    for ext in supported_video_extension:
        if ext in sys.argv[1]:
            file_type = 1
            print("The input file is a video")
            original_audio_file = video2audio(sys.argv[1])
            break
    for ext in supported_audio_extension:
        if ext in sys.argv[1]:
            file_type = 2
            print("The input file is an audio")
            original_audio_file = sys.argv[1]
            break
    if file_type == -1:
        print("The file type is not supported.")
        print("Supported formats: \nVideo: ", str(supported_video_extension), "\nAudio: ", str(supported_audio_extension))
    
    # Record the minimum duration and maximum duration of the audio chunk
    min_secs = sys.argv[2]
    max_secs = sys.argv[3]

    # Start chunking
    timeslots = chunking(original_audio_file, min_secs, max_secs)
    
    # Ouput audio files with multiprocessing
    cpus = os.cpu_count()
    pool = Pool(cpus)
    pool_outputs = pool.starmap(output_audio, [original_audio_file , timeslots])
    