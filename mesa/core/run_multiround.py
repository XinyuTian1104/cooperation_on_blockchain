from envs.game_env_multiRound import BFTblockchainModel
# import random

if __name__ == '__main__':
    model = BFTblockchainModel(n = 100, R = 100, c_check = 5, c_send = 5, kappa = 1, threshold = 0.4, initial_h = 0.55)
    x_list = [];
    step_list = [];
    model.setup();
    # print("Model setup: ", model.counter)
    while model.terminate == False:
        print("not terminated")
        model.step();
        x_list.append(model.proportion_of_honest);
        step_list.append(model.counter);