import http.client
import json
import random
import time

from data import users
from data import platters
from data.users import get_users
from data.platters import get_platters


def get_ranked_actions_for_user(user:str) -> dict:
    conn = http.client.HTTPConnection("localhost:7071")

    conn.request("GET", "/api/GetRankedActions?user={0}".format(user))

    res = conn.getresponse()
    data = res.read()

    return json.loads(data.decode("utf-8"))


def send_reward_for_action(event_id:str, reward:int) -> bool:
    conn = http.client.HTTPConnection("localhost:7071")

    payload = "event_id={0}&reward={1}".format(event_id, reward)

    conn.request("GET", "/api/RewardAction?{0}".format(payload))

    res = conn.getresponse()
    data = res.read()

    return res.status == 200


def calculateReward(user_name:str, platter_name:str) -> int:

    user = get_users().get(user_name)
    platter = get_platters().get(platter_name)
    
    if (user == None or platter == None):
        return 0
    
    if user["company_size"] == "large":
        if platter["attributes"]["qty"] >= 50:
            return 1
        else:
            return 0
        
    if user["company_size"] == "small":
        if platter["attributes"]["qty"] <= 10:
            return 1
        else:
            return 0
        
    if user["company_size"] == "medium":
        if platter["attributes"]["qty"] >= 10 and platter["attributes"]["qty"] <= 50:
            return 1
        else:
            return 0

    return 0



while(True):
    user = random.choice(["Andy", "Tim", "Chris", "Paul", "Scott"])
    rankings = get_ranked_actions_for_user(user)
    event_id = rankings.get("event_id", "")
    best_action = rankings.get("best_action", "")
    
    reward = calculateReward(user, best_action)
    
    send_reward_for_action(event_id, reward)
    
    print("User: {0}, Platter: {1}, Reward: {2}".format(user, rankings.get("best_action"), reward))
    
    time.sleep(1)

