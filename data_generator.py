import random
import csv

data = []

def add_noise(value, noise_level):
    return value + random.uniform(-noise_level, noise_level)


# 🟢 HUMAN
def generate_human_sample():
    session_duration = random.uniform(30, 100)
    actions = random.randint(100, 500)
    actions_per_second = actions / session_duration

    avg_mouse_speed = add_noise(random.uniform(0.8, 2.2), 0.2)
    mouse_speed_variance = add_noise(random.uniform(0.6, 2.5), 0.3)

    click_interval_avg = add_noise(random.uniform(0.4, 1.5), 0.2)
    click_interval_variance = add_noise(random.uniform(0.3, 1.2), 0.2)

    typing_avg_delay = add_noise(random.uniform(0.2, 0.9), 0.1)
    typing_variance = add_noise(random.uniform(0.4, 1.2), 0.2)

    backspace_count = random.randint(3, 15)

    scroll_speed = add_noise(random.uniform(0.5, 2.5), 0.3)

    hesitation_time = add_noise(random.uniform(0.5, 4.0), 0.5)

    idle_ratio = add_noise(random.uniform(0.2, 0.6), 0.1)

    curvature_score = add_noise(random.uniform(0.7, 2.5), 0.3)

    return {
        "avg_mouse_speed": max(0, avg_mouse_speed),
        "mouse_speed_variance": max(0, mouse_speed_variance),
        "click_interval_avg": max(0, click_interval_avg),
        "click_interval_variance": max(0, click_interval_variance),
        "typing_avg_delay": max(0, typing_avg_delay),
        "typing_variance": max(0, typing_variance),
        "backspace_count": backspace_count,
        "scroll_speed": max(0, scroll_speed),
        "hesitation_time": max(0, hesitation_time),
        "session_duration": session_duration,
        "actions_per_second": actions_per_second,
        "idle_ratio": max(0, idle_ratio),
        "curvature_score": max(0, curvature_score),
        "label": 1
    }


# 🔴 BOT
def generate_bot_sample():
    session_duration = random.uniform(5, 30)
    actions = random.randint(200, 600)
    actions_per_second = actions / session_duration

    # Slight overlap introduced deliberately
    avg_mouse_speed = add_noise(random.uniform(1.8, 4.0), 0.2)
    mouse_speed_variance = add_noise(random.uniform(0.01, 0.3), 0.05)

    click_interval_avg = add_noise(random.uniform(0.05, 0.5), 0.1)
    click_interval_variance = add_noise(random.uniform(0.001, 0.2), 0.05)

    typing_avg_delay = add_noise(random.uniform(0.02, 0.2), 0.05)
    typing_variance = add_noise(random.uniform(0.01, 0.3), 0.05)

    # smart bots (rarely make mistakes)
    backspace_count = random.choice([0, 0, 0, 1])

    scroll_speed = add_noise(random.uniform(2.0, 6.0), 0.5)

    hesitation_time = add_noise(random.uniform(0.0, 0.5), 0.1)

    idle_ratio = add_noise(random.uniform(0.0, 0.15), 0.05)

    curvature_score = add_noise(random.uniform(0.0, 0.5), 0.1)

    return {
        "avg_mouse_speed": max(0, avg_mouse_speed),
        "mouse_speed_variance": max(0, mouse_speed_variance),
        "click_interval_avg": max(0, click_interval_avg),
        "click_interval_variance": max(0, click_interval_variance),
        "typing_avg_delay": max(0, typing_avg_delay),
        "typing_variance": max(0, typing_variance),
        "backspace_count": backspace_count,
        "scroll_speed": max(0, scroll_speed),
        "hesitation_time": max(0, hesitation_time),
        "session_duration": session_duration,
        "actions_per_second": actions_per_second,
        "idle_ratio": max(0, idle_ratio),
        "curvature_score": max(0, curvature_score),
        "label": 0
    }


# Generate dataset
for _ in range(1000):
    data.append(generate_human_sample())

for _ in range(1000):
    data.append(generate_bot_sample())


# Save CSV
keys = data[0].keys()

with open("dataset.csv", "w", newline="") as file:
    writer = csv.DictWriter(file, fieldnames=keys)
    writer.writeheader()
    writer.writerows(data)