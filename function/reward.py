prev_exp = 0

def get_reward(current_exp):
    global prev_exp
    reward = current_exp - prev_exp
    prev_exp = current_exp
    return reward