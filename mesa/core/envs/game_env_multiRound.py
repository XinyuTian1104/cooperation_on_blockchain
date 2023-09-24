from envs.game_agents import Agent
import random
import numpy as np

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

    super().__init__()

  def setup(self) -> None:
    self.proportion_of_honest = self.initial_h;
    self.agents = [];
    for i in range(self.num_agent):
      # generate strategy with weight initial_h
      if random.random() <= self.initial_h:
        strategy = 0;
      else:
        strategy = 1;
      self.agents.append(Agent(strategy));
    self.counter = self.counter + 1;
    # print("setup: ", self.counter)
    self.terminate = False;

  def step(self) -> None:
    # one step of game contains 100 rounds
    rewards = np.array([0 for i in range(100)]);
    for i in range(100000):
      # generate proposer
      proposer = random.randint(0, self.num_agent - 1);
      # update payoff per round
      reward = np.array([0 for i in range(self.num_agent)]);
      for j in range(self.num_agent):
        r = self.agents[j].get_reward(self.proportion_of_honest, self.agents[proposer].strategy, self.threshold, self.R, self. c_check, self.c_send, self.kappa)
        reward[j] = r;
      rewards = rewards + reward;
    rewards = rewards / 100000;
    # print("The rewards of the agents: ", rewards)

    # NEW ROUND: new choice of strategy, update proportion_of_honest
    self.counter = self.counter + 1;
    print("The round of game: ", self.counter)

    # calculate total reward of honest agents
    total_r_honest = sum([rewards[i] for i in range(self.num_agent) if self.agents[i].strategy == 0]);

    # calculate total reward of Byzantine agents
    total_r_byzantine = sum([rewards[i] for i in range(self.num_agent) if self.agents[i].strategy == 1]);
    # print("The total rewards of Honest and Byzantine: ", (total_r_honest, total_r_byzantine))

    # update strategy
    tmp = (self.proportion_of_honest * total_r_honest)/(self.proportion_of_honest * total_r_honest + (1 - self.proportion_of_honest) * total_r_byzantine);
    print("tmp: ", tmp)
    probability = 1 / (1 + np.exp(-(tmp-0.5)*10));
    print("The probability of being honest: ", probability)
    for i in range(self.num_agent):
      self.agents[i].update_strategy(probability);

    # update proportion_of_honest
    proportion_of_honest = 1 - (sum([self.agents[i].strategy for i in range(self.num_agent)]) / self.num_agent);
    print("The proportion of honest: ", proportion_of_honest)

    # terminate if any equlibrium is reached
    if self.proportion_of_honest == proportion_of_honest:
      self.terminate = True;
      print("TERMINATED! The final proportion of honest is: ", self.proportion_of_honest, "The total rounds of game is: ", self.counter)
    elif tmp == 1:
      self.terminate = True;
      self.proportion_of_honest = 1;
      print("TERMINATED! The final proportion of honest is: ", self.proportion_of_honest, "The total rounds of game is: ", self.counter)
    else:
      self.proportion_of_honest = proportion_of_honest;
    
    # self.proportion_of_honest = proportion_of_honest;
    return self.counter, proportion_of_honest, self.terminate