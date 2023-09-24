from envs.game_env_multiRound import BFTblockchainModel
"""
In this test file, we test the multi-round game environment with different initial settings.

rate = R-c_send+kappa / 2R-2c_send+kappa

"""

if __name__ == '__main__':
    # when threshold is smaller than 0.5
    # both H and B are larger or equal to threshold, H larger than rate, then Honest Eq.
    model = BFTblockchainModel(n = 100, R = 100, c_check = 5, c_send = 5, kappa = 1, threshold = 0.4, initial_h = 0.6)
    # both H and B are larger larger or equal to threshold, H smaller than rate, then Byzantine Eq.
    model = BFTblockchainModel(n = 100, R = 100, c_check = 5, c_send = 5, kappa = 1, threshold = 0.4, initial_h = 0.49)
    # both H and B are larger larger or equal to threshold, H equal to rate, then Pooling Eq.
    # this one cannot be shown in code.
    model = BFTblockchainModel(n = 100, R = 100, c_check = 5, c_send = 5, kappa = 1, threshold = 0.4, initial_h = 96/191)
    
    # when threshold is 0.5
    # both H and B are 0.5, then Byzantine Eq. (because H is smaller than rate)
    model = BFTblockchainModel(n = 100, R = 100, c_check = 5, c_send = 5, kappa = 1, threshold = 0.5, initial_h = 0.5)
    # H larger than 0.5, then Honest Eq.
    model = BFTblockchainModel(n = 100, R = 100, c_check = 5, c_send = 5, kappa = 1, threshold = 0.5, initial_h = 0.6)
    # B larger than 0.5, then Byzantine Eq.
    model = BFTblockchainModel(n = 100, R = 100, c_check = 5, c_send = 5, kappa = 1, threshold = 0.5, initial_h = 0.4)

    # when threshold is larger than 0.5
    # H larger than threshold, then Honest Eq.
    model = BFTblockchainModel(n = 100, R = 100, c_check = 5, c_send = 5, kappa = 1, threshold = 0.55, initial_h = 0.6)
    # B larger than threshold, then Byzantine Eq.
    model = BFTblockchainModel(n = 100, R = 100, c_check = 5, c_send = 5, kappa = 1, threshold = 0.55, initial_h = 0.4)
    
    x_list = [];
    step_list = [];
    model.setup();
    while model.terminate == False:
        # print("not terminated")
        model.step();
        x_list.append(model.proportion_of_honest);
        step_list.append(model.counter);