from envs.game_env_multiRound import BFTblockchainModel
"""
In this test file, we test the multi-round game environment with different initial settings.

rate = R-c_send+kappa / 2R-2c_send+kappa

Setting #1: Both Honest and Byzantine are larger than threshold. (both has pivotality)
- If Honest larger than rate, Honest Equilibrium.
- If Honest smaller than rate, Byzantine Equilibrium.
- If Honest equal to rate, Pooling Equilibrium.

Setting #2: Honest is larger than threshold, Byzantine is smaller than threshold.


"""

if __name__ == '__main__':
    model = BFTblockchainModel(n = 100, R = 100, c_check = 5, c_send = 5, kappa = 1, threshold = 0.4, initial_h = 0.503)
    x_list = [];
    step_list = [];
    model.setup();
    while model.terminate == False:
        print("not terminated")
        model.step();
        x_list.append(model.proportion_of_honest);
        step_list.append(model.counter);