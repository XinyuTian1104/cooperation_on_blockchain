import numpy as np
# import random
np.random.seed(2023)
# from game_env import BFTblockchainModel

class Agent():

  def __init__(self, strategy) -> None:
    super().__init__()
    self.strategy = strategy;

  def get_reward(self, proportion_of_honest, proposer_strategy, threshold, R, c_check, c_send, kappa) -> None:
    """
        If Byzantine majority:
            If Honest majority, then V_{HH} = R-c_{check}-c_{send},
                                V_{HB} = -c_{check}-k,
                                V_{BH} = -c_{check},
                                V_{BB} = R-c_{check}-c_{send};
            If Honest minority, then V_{HH} = 0,
                                V_{HB} = -k,
                                V_{BH} = -c_{check},
                                V_{BB} = R-c_{check}-c_{send};
        If Byzantine minority:
            If Honest majority, then V_{HH} = R-c_{check}-c_{send},
                                V_{HB} = -c_{check},
                                V_{BH} = 0,
                                V_{BB} = 0;
            If Honest minority, then all 0.
    """
    if (1 - proportion_of_honest) >= threshold: # Byzantine majority
        if proportion_of_honest >= threshold: # Honest majority
            if proposer_strategy == 0: # Honest proposer
                if self.strategy == 0: # Honest agent, {HH}
                  reward = R - c_check - c_send;
                elif self.strategy == 1: # Byzantine agent, {BH}
                   reward = - c_check;
                else:
                   raise ValueError;
            elif proposer_strategy == 1: # Byzantine proposer
                if self.strategy == 0: # Honest agent, {HB}
                   reward = - c_check - kappa;
                elif self.strategy == 1: # Byzantine agent, {BB}
                   reward = R - c_check - c_send
                else:
                   raise ValueError;
            else:
                raise ValueError;
        elif proportion_of_honest < threshold: # Honest minority
            if proposer_strategy == 0: # Honest proposer
                if self.strategy == 0: # Honest agent, {HH}
                   reward = 0;
                elif self.strategy == 1: # Byzantine agent, {BH}
                   reward = - c_check;
                else:
                   raise ValueError;
            elif proposer_strategy == 1: # Byzantine proposer
                if self.strategy == 0: # Honest agent, {HB}
                   reward = - kappa;
                elif self.strategy == 1: # Byzantine agent, {BB}
                   reward = R - c_check - c_send;
                else:
                   raise ValueError;
            else:
                raise ValueError;
        else:
            raise ValueError;
    elif (1 - proportion_of_honest) < threshold: # Byzantine minority
        if proportion_of_honest >= threshold: # Honest majority
            if proposer_strategy == 0: # Honest proposer
                if self.strategy == 0: # Honest agent, {HH}
                  reward = R - c_check - c_send;
                elif self.strategy == 1: # Byzantine agent, {BH}
                   reward = 0;
                else:
                   raise ValueError;
            elif proposer_strategy == 1: # Byzantine proposer
                if self.strategy == 0: # Honest agent, {HB}
                   reward = - c_check;
                elif self.strategy == 1: # Byzantine agent, {BB}
                   reward = 0;
                else:
                   raise ValueError;
            else:
                raise ValueError;
        elif proportion_of_honest < threshold: # Honest minority
            reward = 0;
        else:
            raise ValueError;

    return reward

  def update_strategy(self, probability) -> None:
    """
        Strategy Update Rule:
            For agent i, the probability of being honest is
                x_i(t+1) = x_i(t) * sum_u_honest / (x_i(t) * sum_u_honest + (1-x_i(t)) * sum_u_byzantine)
            the probability of being Byzantine is 1 - x_i(t+1)
         
         Update:
            Now we use logistic function to update the strategy.
    """
    random_number = np.random.rand();
    if random_number <= probability:
      self.strategy = 0;
    else:
      self.strategy = 1;



  