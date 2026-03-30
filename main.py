from fastapi import FastAPI
import pickle
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

app=FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return {"message":"api is working"}

with open("model.pkl", "rb") as f:
    model = pickle.load(f)

class SessionData(BaseModel):
    avg_mouse_speed: float
    mouse_speed_variance: float
    click_interval_avg: float
    click_interval_variance: float
    typing_avg_delay: float
    typing_variance: float
    backspace_count: int
    scroll_speed: float
    hesitation_time: float
    session_duration: float
    actions_per_second: float
    idle_ratio:float
    curvature_score:float

def calibrate(prob, T=2.0):
    import math
    prob = min(max(prob, 1e-6), 1 - 1e-6)
    logit = math.log(prob / (1 - prob))
    logit /= T
    return 1 / (1 + math.exp(-logit))

@app.post("/predict")
def predict(data: SessionData):
    features = [[
        data.avg_mouse_speed,
        data.mouse_speed_variance,
        data.click_interval_avg,
        data.click_interval_variance,
        data.typing_avg_delay,
        data.typing_variance,
        data.backspace_count,
        data.scroll_speed,
        data.hesitation_time,
        data.session_duration,
        data.actions_per_second,
        data.idle_ratio,
        data.curvature_score
    ]]

    #prediction = model.predict(features)[0]
    prob=model.predict_proba(features)[0][1]
    print("old prob=",prob)
    prob = calibrate(prob, T=2.0)
    # return {
    #     "prediction": int(prediction),
    #     "result": "human" if prediction == 1 else "bot"
    # }
    rule_score = 0
    if data.backspace_count > 2:
        rule_score += 0.3

    if data.typing_variance > 0.3:
        rule_score += 0.3

    if data.idle_ratio > 0.2:
        rule_score += 0.2

    if data.curvature_score > 0.5:
        rule_score += 0.2

    final_score = 0.6 * prob + 0.4 * rule_score
    print("prob=",prob)
    print("rule_score=",rule_score)
    print("final_score=",final_score)
    return{
        "confidence":float(final_score),
        "result": "human" if final_score>0.6 else "bot" if final_score<0.3 else "suspicious"
    }