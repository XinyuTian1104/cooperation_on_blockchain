from game_agents import Agent
import random

class BFTblockchainModel():
  def __init__(self, n, R, c_check, c_send, kappa, v, initial_h, initial_u, m):
    self.num_agent = n;
    self.agents = [];
    self.R = R;
    self.c_check = c_check;
    self.c_send = c_send;
    self.kappa = kappa;
    self.v = v;
    self.initialH = initial_h;
    self.proportion_of_honest = initial_h;
    # self.initial_u = initial_u;
    self.m = m;
    self.counter = 0;
  
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
      reward = 0;
      self.agents.append(Agent(strategy, reward));
      self.counter = self.counter + 1;

  def step(self) -> None:
    # generate proposer
    proposer = random.randint(0, self.num_agent - 1);
    # update payoff per round
    rewards = [self.agents[i].get_reward(self.proportion_of_honest, self.agents[proposer].strategy, self.v, self.R, self. c_check, self.c_send, self.kappa) for i in range(self.num_agent)];
    
    # NEW ROUND: new choice of strategy, update proportion_of_honest
    self.counter = self.counter + 1;
    # calculate total reward of honest agents
    total_r_honest = sum([rewards[i] for i in range(self.num_agent) if self.agents[i].strategy == 0]);
    # calculate total reward of Byzantine agents
    total_r_bynzantine = sum([rewards[i] for i in range(self.num_agent) if self.agents[i].strategy == 1]);
    # update strategy
    for i in range(self.num_agent):
      self.agents[i].update_strategy(rewards[i], total_r_honest, total_r_bynzantine, self.proportion_of_honest);
    # update proportion_of_honest
    proportion_of_honest = sum([self.agents[i].strategy for i in range(self.num_agent)]) / self.num_agent;
    # terminate if any equlibrium is reached
    terminate = False;
    if self.proportion_of_honest == proportion_of_honest:
      terminate = True;
    return self.counter, proportion_of_honest, terminate