from game_agents import Agent

class BFTblockchainModel():
  def __init__(self, n, R, c_check, c_send, kappa, v, initial_h, initialU):
    super().__init__()
    self.num_agent = n;
    self.agents = [];
    self.R = R;
    self.c_check = c_check;
    self.c_send = c_send;
    self.kappa = kappa;
    self.v = v;
    self.initialH = initial_h;
    self.initialU = initialU;
  
  def setup(self) -> None:
    self.agents = [];
    for i in range(self.num_agent):
      
      a = Agent(i, self);
      self.agents.append(a);

  def step(self) -> None:
    self.schedule.step()

