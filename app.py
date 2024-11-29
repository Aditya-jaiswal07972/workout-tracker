import cv2
import numpy as np
import mediapipe as mp
import time
from flask import Flask, render_template, jsonify
from exercise_tracker import BicepCurlTracker, SquatTracker, PushUpTracker  # Import the exercise tracker classes

# Initialize Flask app
app = Flask(__name__)

# Global exercise data
exercise_data = {
    "bicep_curls": 0,
    "squats": 0,
    "push_ups": 0,
    "posture_quality": "Good",
    "workout_time": 0.0
}

# Initialize exercise trackers
bicep_curl_tracker = BicepCurlTracker()
squat_tracker = SquatTracker()
push_up_tracker = PushUpTracker()

# Route to serve the webpage
@app.route('/')
def index():
    return render_template('index.html')  # Renders the HTML page to show data

# Route to fetch exercise data
@app.route('/exercise_data')
def get_exercise_data():
    # Update exercise data (e.g., reps, posture quality, workout time)
    exercise_data['workout_time'] = bicep_curl_tracker.get_total_workout_time()
    return jsonify(exercise_data)  # Send data as JSON to frontend

# Run video capture and exercise tracking
def track_exercises():
    cap = cv2.VideoCapture(0)

    with mp.solutions.pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
        while cap.isOpened():
            ret, frame = cap.read()

            # Convert frame to RGB for Mediapipe processing
            image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            image.flags.writeable = False

            # Make pose detection
            results = pose.process(image)

            # Revert back to BGR for OpenCV
            image.flags.writeable = True
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

            # Extract landmarks and track each exercise
            try:
                landmarks = results.pose_landmarks.landmark

                # Track exercises
                bicep_curl_tracker.track(landmarks, image)
                squat_tracker.track(landmarks, image)
                push_up_tracker.track(landmarks, image)

            except Exception as e:
                print(f"Error: {e}")
                pass

            # Show the video feed
            cv2.imshow('Exercise Tracker', image)

            # Break the loop on 'q' key press
            if cv2.waitKey(10) & 0xFF == ord('q'):
                break

    # Release video capture and close windows
    cap.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    # Run the exercise tracking in a separate thread
    from threading import Thread
    exercise_thread = Thread(target=track_exercises)
    exercise_thread.start()

    # Start the Flask web server
    app.run(debug=True, use_reloader=False)
