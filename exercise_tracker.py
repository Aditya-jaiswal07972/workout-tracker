import numpy as np
import mediapipe as mp

# Initialize Mediapipe Pose Class
mp_pose = mp.solutions.pose

# Base class for exercises
class ExerciseTracker:
    def __init__(self, name, joint_points):
        self.name = name
        self.joint_points = joint_points
        self.counter = 0
        self.stage = None
        self.previous_position = None
        self.start_time = None

    def calculate_angle(self, a, b, c):
        a = np.array(a)  # First point
        b = np.array(b)  # Middle point
        c = np.array(c)  # Last point
        radians = np.arctan2(c[1] - b[1], c[0] - b[0]) - np.arctan2(a[1] - b[1], a[0] - b[0])
        angle = np.abs(radians * 180.0 / np.pi)
        if angle > 180.0:
            angle = 360 - angle
        return angle

    def count_reps(self, angle, angle_threshold, stage_up, stage_down):
        if angle > angle_threshold and self.stage == stage_down:
            self.stage = stage_up
        if angle < angle_threshold and self.stage == stage_up:
            self.stage = stage_down
            self.counter += 1

    def display_counter(self, image):
        cv2.putText(image, f'{self.name}: {self.counter}', (10, 60),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)

    def get_total_workout_time(self):
        return time.time() - self.start_time if self.start_time else 0

# Bicep Curl Class
class BicepCurlTracker(ExerciseTracker):
    def __init__(self):
        super().__init__('Bicep Curl', ['LEFT_SHOULDER', 'LEFT_ELBOW', 'LEFT_WRIST'])

    def track(self, landmarks, image):
        shoulder = [landmarks[mp_pose.PoseLandmark[self.joint_points[0]].value].x,
                    landmarks[mp_pose.PoseLandmark[self.joint_points[0]].value].y]
        elbow = [landmarks[mp_pose.PoseLandmark[self.joint_points[1]].value].x,
                 landmarks[mp_pose.PoseLandmark[self.joint_points[1]].value].y]
        wrist = [landmarks[mp_pose.PoseLandmark[self.joint_points[2]].value].x,
                 landmarks[mp_pose.PoseLandmark[self.joint_points[2]].value].y]
        
        left_angle = self.calculate_angle(shoulder, elbow, wrist)
        
        # Count bicep curls based on angle change
        self.count_reps(left_angle, 30, 'up', 'down')
        
        # Update exercise data
        exercise_data['bicep_curls'] = self.counter

# Squat Class
class SquatTracker(ExerciseTracker):
    def __init__(self):
        super().__init__('Squat', ['LEFT_HIP', 'LEFT_KNEE', 'LEFT_ANKLE'])

    def track(self, landmarks, image):
        hip = [landmarks[mp_pose.PoseLandmark[self.joint_points[0]].value].x,
               landmarks[mp_pose.PoseLandmark[self.joint_points[0]].value].y]
        knee = [landmarks[mp_pose.PoseLandmark[self.joint_points[1]].value].x,
                landmarks[mp_pose.PoseLandmark[self.joint_points[1]].value].y]
        ankle = [landmarks[mp_pose.PoseLandmark[self.joint_points[2]].value].x,
                 landmarks[mp_pose.PoseLandmark[self.joint_points[2]].value].y]
        
        squat_angle = self.calculate_angle(hip, knee, ankle)
        
        # Count squats based on angle change
        self.count_reps(squat_angle, 90, 'up', 'down')
        
        # Update exercise data
        exercise_data['squats'] = self.counter

# Push-up Class
class PushUpTracker(ExerciseTracker):
    def __init__(self):
        super().__init__('Push-up', ['LEFT_SHOULDER', 'LEFT_ELBOW', 'LEFT_WRIST'])

    def track(self, landmarks, image):
        shoulder = [landmarks[mp_pose.PoseLandmark[self.joint_points[0]].value].x,
                    landmarks[mp_pose.PoseLandmark[self.joint_points[0]].value].y]
        elbow = [landmarks[mp_pose.PoseLandmark[self.joint_points[1]].value].x,
                 landmarks[mp_pose.PoseLandmark[self.joint_points[1]].value].y]
        wrist = [landmarks[mp_pose.PoseLandmark[self.joint_points[2]].value].x,
                 landmarks[mp_pose.PoseLandmark[self.joint_points[2]].value].y]
        
        pushup_angle = self.calculate_angle(shoulder, elbow, wrist)
        
        # Count push-ups based on angle change
        self.count_reps(pushup_angle, 160, 'up', 'down')
        
        # Update exercise data
        exercise_data['push_ups'] = self.counter
