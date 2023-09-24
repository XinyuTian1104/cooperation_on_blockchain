from envs.game_agents import Agent
import random

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
    print("setup: ", self.counter)
    self.terminate = False;

  def step(self) -> None:
    # generate proposer
    proposer = random.randint(0, self.num_agent - 1);

    # update payoff per round
    rewards = [];
    for i in range(self.num_agent):
      r = self.agents[i].get_reward(self.proportion_of_honest, self.agents[proposer].strategy, self.threshold, self.R, self. c_check, self.c_send, self.kappa)
      # print(i)
      rewards.append(r);
    print("The rewards of the agents: ", rewards)
    # rewards = [self.agents[i].get_reward() for i in range(self.num_agent)];

    # NEW ROUND: new choice of strategy, update proportion_of_honest
    self.counter = self.counter + 1;
    print("The round of game: ", self.counter)

    # calculate total reward of honest agents
    total_r_honest = sum([rewards[i] for i in range(self.num_agent) if self.agents[i].strategy == 0]);

    # calculate total reward of Byzantine agents
    total_r_bynzantine = sum([rewards[i] for i in range(self.num_agent) if self.agents[i].strategy == 1]);
    print("The total rewards of Honest and Byzantine: ", (total_r_honest, total_r_bynzantine))

    # update strategy
    for i in range(self.num_agent):
      # print(rewards[i], total_r_honest, total_r_bynzantine, self.proportion_of_honest);
      self.agents[i].update_strategy(total_r_honest, total_r_bynzantine, self.proportion_of_honest);

    # update proportion_of_honest
    proportion_of_honest = sum([self.agents[i].strategy for i in range(self.num_agent)]) / self.num_agent;
    print("The proportion of honest: ", proportion_of_honest)

    # terminate if any equlibrium is reached
    if self.proportion_of_honest == proportion_of_honest:
      # self.proportion_of_honest = proportion_of_honest;
      self.terminate = True;
      print("TERMINATED! The final proportion of honest is: ", proportion_of_honest, "The total rounds of game is: ", self.counter)
    else:
      self.proportion_of_honest = proportion_of_honest;
    return self.counter, proportion_of_honest, self.terminate