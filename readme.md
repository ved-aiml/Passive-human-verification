# 🛡️ PassiveGuard — Passive Human Verification System

> **Replace CAPTCHA with invisible, AI-powered behavioral biometrics.**  
> PassiveGuard silently observes how users interact with a page — mouse movement, typing rhythm, click patterns, and scrolling — and uses a trained Machine Learning model to classify them as **human** or **bot**, without ever interrupting them.

---

## 🚀 Live Demo Flow

```
User visits page → Behavioral signals collected silently → 
Click "Verify & Sign In" → Features sent to FastAPI → 
Random Forest model predicts → Result shown instantly
```

---

## ✨ Features

| Feature | Description |
|---|---|
| 🖱️ Mouse Tracking | Speed, variance, curvature score, hesitation detection |
| ⌨️ Typing Analysis | Average delay, variance between keystrokes, backspace frequency |
| 🖱️ Click Patterns | Inter-click interval average and variance |
| 📜 Scroll Behavior | Scroll speed profiling |
| ⏱️ Session Metrics | Duration, actions per second, idle ratio |
| 🤖 ML Classification | Random Forest trained on synthetic human vs bot data |
| ⚡ Real-time API | FastAPI backend serves predictions in milliseconds |
| 🎨 Passive UX | No puzzles, no friction — completely invisible to real users |

---

## 🏗️ Architecture

```                                           
┌─────────────────────────────────────────────────┐
│                  Browser (index.html)           │
│                                                 │
│  tracker.js — collects 13 behavioral features   │
│       ↓                                         │
│  POST /predict  →  FastAPI (main.py)            │
│                        ↓                        │
│               model.pkl (Random Forest)         │
│                        ↓                        │
│       { prediction: 1|0, result: "human"|"bot" }│
└─────────────────────────────────────────────────┘
```

---

## 📊 ML Pipeline

### Features Extracted (13 total)

| # | Feature | Description |
|---|---|---|
| 1 | `avg_mouse_speed` | Average pixels/ms of mouse movement |
| 2 | `mouse_speed_variance` | Variance in mouse speed (bots are too consistent) |
| 3 | `click_interval_avg` | Average time between clicks |
| 4 | `click_interval_variance` | Variance in click timing |
| 5 | `typing_avg_delay` | Average delay between keystrokes |
| 6 | `typing_variance` | Variance in keystroke timing |
| 7 | `backspace_count` | Number of corrections (bots never make mistakes) |
| 8 | `scroll_speed` | Average scroll velocity |
| 9 | `hesitation_time` | Time paused with no mouse movement |
| 10 | `session_duration` | Total session length |
| 11 | `actions_per_second` | Action density over session |
| 12 | `idle_ratio` | Fraction of session spent idle |
| 13 | `curvature_score` | Path curvature (bots move in straight lines) |

### Model

- **Algorithm:** Random Forest Classifier (scikit-learn)
- **Training Data:** 2,000 synthetic samples (1,000 human, 1,000 bot)
- **Train/Test Split:** 80/20
- **Saved as:** `model.pkl`

---

## 🗂️ Project Structure

```
captcha/
├── tracker.js          # ★ The SDK — embeddable in any website
├── index.html          # Demo page showing the SDK in action
├── style.css           # Demo page styles
├── app.js              # Demo page UI logic (indicators, result overlay)
├── main.py             # FastAPI backend with /predict endpoint
├── train_model.py      # Model training script (Random Forest)
├── data_generator.py   # Synthetic dataset generator
├── dataset.csv         # Generated training data (2000 rows)
├── model.pkl           # Trained ML model (serialized)
├── requirements.txt    # Python dependencies
└── readme.md           # This file
```

---

## ⚙️ Setup & Run

### Prerequisites

- Python 3.8+
- pip

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. (Optional) Regenerate Dataset

```bash
python data_generator.py
```

### 3. (Optional) Retrain Model

```bash
python train_model.py
```

### 4. Start the FastAPI Backend

```bash
uvicorn main:app --reload
```

> API will be available at `http://127.0.0.1:8000`

### 5. Open the Frontend

Open `index.html` directly in your browser (no server needed for the frontend).

---

## 🔌 API Reference

### `POST /predict`

Predicts whether the session belongs to a human or bot.

**Request Body:**
```json
{
  "avg_mouse_speed": 1.8,
  "mouse_speed_variance": 0.9,
  "click_interval_avg": 0.5,
  "click_interval_variance": 0.3,
  "typing_avg_delay": 0.25,
  "typing_variance": 0.15,
  "backspace_count": 3,
  "scroll_speed": 1.2,
  "hesitation_time": 800,
  "session_duration": 15000,
  "actions_per_second": 4.2,
  "idle_ratio": 0.1,
  "curvature_score": 0.85
}
```

**Response:**
```json
{
  "prediction": 1,
  "result": "human"
}
```

| `prediction` | `result` | Meaning |
|---|---|---|
| `1` | `"human"` | Verified as human |
| `0` | `"bot"` | Detected as bot |

---

## 🧠 How Bot vs Human Detection Works

| Signal | Human | Bot |
|---|---|---|
| Mouse speed variance | High (natural movement) | Very low (robotic precision) |
| Typing variance | Present (natural rhythm) | Near zero (perfectly timed) |
| Backspace usage | Occasional corrections | None |
| Curvature score | High (curved paths) | Near zero (straight lines) |
| Idle ratio | ~10–20% | Near 0% |
| Click interval variance | Natural randomness | Perfectly uniform |

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| **SDK** | Vanilla JavaScript (`tracker.js`) — zero dependencies |
| Demo Page | HTML5, CSS3 (`style.css`, `app.js`) |
| Backend API | Python · FastAPI · Uvicorn |
| ML Model | scikit-learn · Random Forest |
| Data | Synthetic CSV (pandas) |
| Serialization | pickle |

---

## 📦 Embedding the SDK

Add these **two lines** to any existing website — that's the entire integration:

```html
<!-- PassiveGuard SDK: drop into any page, before your form's submit handler -->
<script src="https://your-cdn/tracker.js"></script>
```

Then call `calculateFeatures()` before your form submits and send the result to your backend:

```js
document.querySelector('#myForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    const features = calculateFeatures();
    const res = await fetch('https://your-api/predict', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(features)
    });
    const { result } = await res.json();
    if (result === 'bot') { /* block */ } else { /* allow */ }
});
```

The SDK requires **no configuration** and is **invisible to the user**.

---

## 📈 Progress

- [x] Feature design & research
- [x] Synthetic data generation (2000 samples)
- [x] Model training & evaluation
- [x] FastAPI `/predict` endpoint
- [x] Embeddable behavioral SDK (`tracker.js`)
- [x] Demo page with real-time behavior indicators
- [ ] Confidence score (`0.0–1.0`) in API response
- [ ] Real-world data collection & model improvement
- [ ] Dashboard for monitoring verification analytics

---

## 🎯 Goal

**Replace CAPTCHA entirely.** Most CAPTCHA systems frustrate users while being increasingly solvable by AI bots. PassiveGuard flips the model — instead of making humans prove they're human, it makes it harder for bots to hide.

> *"The best security is the kind users never notice."*

---
