import numpy as np
import random
from game_env import BFTblockchainModel

class Agent():

  def __init__(self, strategy, reward) -> None:
    super().__init__()
    self.strategy = strategy;
    self.reward = reward;
  
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
            # if proposer_strategy == 0: # Honest proposer
            #     if self.strategy == 0: # Honest agent, {HH}
            #        reward = 0;
            #     elif self.strategy == 1: # Byzantine agent, {BH}
            #        reward = 0;
            #     else:
            #        raise ValueError;
            # elif proposer_strategy == 1: # Byzantine proposer
            #     if self.strategy == 0: # Honest agent, {HB}
            #        reward = 0;
            #     elif self.strategy == 1: # Byzantine agent, {BB}
            #        reward = 0;
            #     else:
            #        raise ValueError;
            # else:
            #     raise ValueError;
        else:
            raise ValueError;
    
    
    return reward
    
  def update_strategy(self, total_r_honest, total_r_byzantine, proportion_of_honest) -> None:
    """
        Strategy Update Rule:
            For agent i, the probability of being honest is
                x_i(t+1) = x_i(t) * sum_u_honest / (x_i(t) * sum_u_honest + (1-x_i(t)) * sum_u_byzantine)
            the probability of being Byzantine is 1 - x_i(t+1)
            where
                sum_u_honest = p{HH}V_{HH} + p{HB}V_{HB}
                sum_u_byzantine = p{BH}V_{BH} + p{BB}V_{BB}
    """
    if random.random() <= proportion_of_honest:
      strategy = 0; 
    else:
      strategy = 1;

  