import random
import csv
data=[]
x=1000
def generate_human_sample():
    session_duration=random.randint(20, 60)
    actions = random.randint(50, 300)

    actions_per_second = actions / session_duration
    return {
  "avg_mouse_speed": random.uniform(1,3),
  "mouse_speed_variance": random.uniform(0.5,2),
  "click_interval_avg": random.uniform(0.3,1),
  "click_interval_variance": random.uniform(0.2,0.9),
  "typing_avg_delay": random.uniform(0.1,0.7),
  "typing_variance": random.uniform(0.1,0.7),
  "backspace_count": random.randint(1,10),
  "scroll_speed": random.uniform(0.5,2),
  "hesitation_time": random.uniform(0.3,3),
  "session_duration":session_duration,
  "actions_per_second":actions_per_second,
  "label": 1
}
for _ in range(1000):
    data.append(generate_human_sample())

def generate_bot_sample():
    session_duration = random.randint(5, 20)  
    actions = random.randint(200, 500)  

    return {
        "avg_mouse_speed": random.uniform(2.5, 4),  
        "mouse_speed_variance": random.uniform(0.01, 0.1), 
        "click_interval_avg": random.uniform(0.05, 0.2), 
        "click_interval_variance": random.uniform(0.001, 0.05), 
        "typing_avg_delay": random.uniform(0.01, 0.05), 
        "typing_variance": random.uniform(0.001, 0.02), 
        "backspace_count": 0, 
        "scroll_speed": random.uniform(2, 5), 
        "hesitation_time": random.uniform(0.0, 0.1), 
        "session_duration": session_duration,
        "actions_per_second": actions / session_duration,
        "label": 0
    }
for _ in range(1000):
    data.append(generate_bot_sample())

keys = data[0].keys()

with open("dataset.csv", "w", newline="") as file:
    writer = csv.DictWriter(file, fieldnames=keys)
    writer.writeheader()
    writer.writerows(data)
