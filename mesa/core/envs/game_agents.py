import numpy as np
import random
from game_env import BFTblockchainModel

class Agent():

  def __init__(self, strategy, reward) -> None:
    super().__init__()
    self.strategy = strategy;
    self.reward = reward;
  
  def get_reward(self, proportion_of_honest, proposer_strategy, threshold) -> None:
    """
        If Byzantine majority:
            If Honest majority, then V_{HH} = R-c_{check}-c_{send}, 
                                V_{HB} = -c_{check}-c_{send}, 
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
                  reward = 
                return self.balance * (1 - self.m) * (0 - self.c_check) + (self.m + (1 - self.m) * (1 - self.x)) * (self.R - self.c_check - self.c_send);
    
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

  def utilityH(self):
    """
    The utility function for a player with Honest strategy
    """
    if self.n * (1 - self.x) >= self.v:
      if self.n * self.x >= self.v:
        utility = (self.m + (1 - self.m) * self.x) * (self.R - self.c_check - self.c_send) + (1 - self.m) * (1 - self.x) * (0 - self.c_check - self.kappa);
      else:
        utility = (self.m + (1 - self.m) * self.x) * (0 - self.c_check - self.c_send) + (1 - self.m) * (1 - self.x) * (0 - self.c_check - self.kappa);
    else:
      if self.n * self.x >= self.v:
        utility = (self.m + (1 - self.m) * self.x) * (self.R - self.c_check - self.c_send) + (1 - self.m) * (1 - self.x) * (0 - self.c_check);
      else:
        utility = (self.m + (1 - self.m) * self.x) * (0 - self.c_check - self.c_send) + (1 - self.m) * (1 - self.x) * (0 - self.c_check);
    return utility

  def utilityB(self):
    """
    The utility function for a player with Byzantine strategy
    """
    if self.n * (1 - self.x) >= self.v:
      if self.n * self.x >= self.v:
        utility = self.x * (1 - self.m) * (0 - self.c_check) + (self.m + (1 - self.m) * (1 - self.x)) * (self.R - self.c_check - self.c_send);
      else:
        utility = self.x * (1 - self.m) * (0 - self.c_check) + (self.m + (1 - self.m) * (1 - self.x)) * (self.R - self.c_check - self.c_send);
    else:
      if self.n * self.x >= self.v:
        utility = self.x * (1 - self.m) * (0 - self.c_check) + (self.m + (1 - self.m) * (1 - self.x)) * (0 - self.c_check - self.c_send);
      else:
        utility = self.x * (1 - self.m) * (0 - self.c_check) + (self.m + (1 - self.m) * (1 - self.x)) * (0 - self.c_check - self.c_send);
    return utility

  def StrategyChangeH(self):
    """
    The strategy change function for a player
    """
    x = self.x * self.utilityH() / (self.x * self.utilityH() + (1 - self.x) * self.utilityB());
    if self.x * self.utilityH() > 0:
      if (self.x * self.utilityH() + (1 - self.x) * self.utilityB()) != 0:
        if x > 1:
          x = 1;
        elif x > 0:
          x = x;
        else:
          x = 1;
      else:
        x = 1;
    elif self.x * self.utilityH() < 0:
      if (self.x * self.utilityH() + (1 - self.x) * self.utilityB()) != 0:
        if x < 0:
          x = 0;
        elif x > 0:
          x = 1 - x;
      else:
        x = 0;
    else:
      x = x;
    return x
