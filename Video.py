import cv2
import time
from ffpyplayer.player import MediaPlayer

# Function to handle audio playback
def get_audio_player(video_path):
    return MediaPlayer(video_path)

# Function to sync audio with video playback
def sync_audio(player, frame_time):
    audio_time = player.get_pts()
    if audio_time is not None and frame_time > audio_time:
        time.sleep(frame_time - audio_time)

def format_time(seconds):
    minutes, secs = divmod(int(seconds), 60)
    return f"{minutes:02d}:{secs:02d}"

# Mouse callback function to pause/unpause video
def mouse_click(event, x, y, flags, param):
    global paused, resume_time
    if event == cv2.EVENT_LBUTTONDOWN:  # Left-click to toggle pause/unpause
        if paused:
            resume_time = time.time()
            audio_player.set_pause(False)  # Resume audio when video resumes
        else:
            audio_player.set_pause(True)  # Pause audio when video pauses
        paused = not paused
        print("Paused" if paused else "Resumed")

# Function to check if current time is near a pause point
def is_near_pause_point(current_time, pause_times, threshold=0.1):
    return any(abs(current_time - pause_time) < threshold for pause_time in pause_times)

# Load the video
video_path = "data/Video.mp4"
cap = cv2.VideoCapture(video_path)

# Get audio player for the video
audio_player = get_audio_player(video_path)

# Define pause times (in seconds)
#TODO - these are just examples but ideally we would insert timeframes from major topics.
pause_times = {10, 20, 25, 40}  # Set of pause times

# Check if video opened successfully
if not cap.isOpened():
    print("Error: Could not open video.")
    exit()

# Get the frame rate (fps) of the video
fps = cap.get(cv2.CAP_PROP_FPS)

# Initialize variables
paused = False
last_update = time.time()
resume_time = 0
resume_buffer = 1  # 1 second buffer after resuming

# Set up mouse callback for the video window
cv2.namedWindow('Video')
cv2.setMouseCallback('Video', mouse_click)

while True:
    if not paused:
        ret, frame = cap.read()
        if not ret:
            print("End of video or error.")
            break

    # Get the current frame number and calculate the current time
    current_frame = cap.get(cv2.CAP_PROP_POS_FRAMES)
    current_time = current_frame / fps

    # Update time display every second
    if time.time() - last_update >= 1:
        print(f"Current time: {format_time(current_time)}")
        last_update = time.time()

    # Display the video frame
    cv2.imshow('Video', frame)

    # Sync the audio with the video
    sync_audio(audio_player, current_time)

    # Pause the video near specified times, but not immediately after resuming
    if is_near_pause_point(current_time, pause_times) and not paused and time.time() - resume_time > resume_buffer:
        print(f"Pausing video at {format_time(current_time)}")
        paused = True
        audio_player.set_pause(True)  # Pause audio

    # Handle key presses
    key = cv2.waitKey(25) & 0xFF  # Adjusting waitKey for better responsiveness

    if key == ord('q'):  # Press 'q' to exit
        break
    elif key == ord(' '):  # Press spacebar to pause/unpause
        if paused:
            resume_time = time.time()
            new_frame = current_frame + fps * 0.2  # Move forward by 0.2 seconds
            cap.set(cv2.CAP_PROP_POS_FRAMES, new_frame)
            audio_player.set_pause(False)  # Resume audio
        else:
            audio_player.set_pause(True)  # Pause audio
        paused = not paused
        print("Paused" if paused else "Resumed")
    elif key == ord('r'):  # Press 'r' to rewind 5 seconds
        new_frame = max(0, current_frame - 5 * fps)
        cap.set(cv2.CAP_PROP_POS_FRAMES, new_frame)
        audio_player.seek(new_frame / fps, relative=False)  # Rewind audio
        paused = False  # Resume after rewinding
        resume_time = time.time()
    elif key == ord('f'):  # Press 'f' to fast forward 5 seconds
        new_frame = min(cap.get(cv2.CAP_PROP_FRAME_COUNT), current_frame + 5 * fps)
        cap.set(cv2.CAP_PROP_POS_FRAMES, new_frame)
        audio_player.seek(new_frame / fps, relative=False)  # Fast forward audio
        paused = False  # Resume after fast-forwarding
        resume_time = time.time()

    # Introduce a small delay to control playback speed (skipped if paused)
    if not paused:
        # Do not use time.sleep() to maintain responsiveness
        pass

# Release the video capture object and close windows
cap.release()
cv2.destroyAllWindows()

# Close the audio player
audio_player.close_player()