from envs.game_agents import Agent
import random
import numpy as np

np.random.seed(2023)

class BFTblockchainModel():
  def __init__(self, n, R, c_check, c_send, kappa, threshold, initial_h):
    self.num_agent = n;
    self.agents = [];
    self.R = R;
    self.c_check = c_check;
    self.c_send = c_send;
    self.kappa = kappa;
    self.threshold = threshold;
    self.initial_h = initial_h;
    self.proportion_of_honest = initial_h;
    self.counter = 0;
    self.terminate = False;
    # self.rewards = np.array([0 for i in range(n)]);
    self.r_honest_at_round = [];
    self.r_byzantine_at_round = [];

    super().__init__()

  def setup(self) -> None:
    self.proportion_of_honest = self.initial_h;
    self.agents = [];
    for i in range(self.num_agent):
      if np.random.rand() <= self.initial_h:
        strategy = 0;
      else:
        strategy = 1;
      self.agents.append(Agent(strategy));
    self.rewards = np.array([0 for i in range(self.num_agent)]);
    # self.counter = self.counter + 1;
    # print("setup: ", self.counter)
    self.terminate = False;

  def step(self) -> None:
    rewards = np.array([0 for i in range(self.num_agent)]);
    for i in range(1000):

      # generate proposer
      proposer = np.random.randint(0, self.num_agent);

      # update payoff per round
      reward = np.array([0 for i in range(self.num_agent)]);
      for j in range(self.num_agent):
        r = self.agents[j].get_reward(self.proportion_of_honest, self.agents[proposer].strategy, self.threshold, self.R, self. c_check, self.c_send, self.kappa)
        reward[j] = r;
      rewards = rewards + reward;
    self.rewards = rewards / 1000;

    # NEW ROUND: new choice of strategy, update proportion_of_honest
    self.counter = self.counter + 1;

    # calculate total reward of honest agents
    self.r_honest_at_round = [self.rewards[i] for i in range(self.num_agent) if self.agents[i].strategy == 0];
    total_r_honest = sum(self.r_honest_at_round);
    
    # calculate total reward of Byzantine agents
    self.r_byzantine_at_round = [self.rewards[i] for i in range(self.num_agent) if self.agents[i].strategy == 1];
    total_r_byzantine = sum(self.r_byzantine_at_round);
    print("The total rewards of Honest at round ", self.counter, " is: ", total_r_honest, "The total rewards of Byzantine at round ", self.counter, " is: ", total_r_byzantine)

    # update strategy
    tmp = (total_r_honest)/(total_r_honest + total_r_byzantine);
    print("tmp: ", tmp)
    # use softmax function to update the strategy
    print('total_r_honest: ', total_r_honest, 'total_r_byzantine: ', total_r_byzantine )
    probability = 1 / (1 + np.exp(0.00005 * (total_r_byzantine - total_r_honest)));
    print("The probability of being honest: ", probability)
    for i in range(self.num_agent):
      self.agents[i].update_strategy(probability);

    # update proportion_of_honest
    proportion_of_honest = 1 - (sum([self.agents[i].strategy for i in range(self.num_agent)]) / self.num_agent);
    print("The proportion of honest: ", proportion_of_honest)

    # terminate if any equlibrium is reached
    # if self.proportion_of_honest == proportion_of_honest:
    #   self.terminate = True;
    #   print("TERMINATED! The final proportion of honest is: ", self.proportion_of_honest, "The total rounds of game is: ", self.counter)
    if tmp == 1:
      self.terminate = True;
      self.proportion_of_honest = 1;
      print("TERMINATED! The final proportion of honest is: ", self.proportion_of_honest, "The total rounds of game is: ", self.counter)
    elif tmp <= 0:
      self.terminate = True;
      self.proportion_of_honest = 0;
      print("TERMINATED! The final proportion of honest is: ", self.proportion_of_honest, "The total rounds of game is: ", self.counter)
    else:
      self.proportion_of_honest = proportion_of_honest;
  