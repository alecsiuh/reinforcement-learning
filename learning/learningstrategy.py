from abc import ABC, abstractmethod

import numpy as np

from agent.episode import Episode
from environment.environment import Environment


class LearningStrategy(ABC):
    """
    Implementations of this class represent a Learning Method
    This class is INCOMPLETE
    """

    env: Environment

    def __init__(self, environment: Environment, λ, γ, t_max) -> None:
        self.total_rewards = 0
        self.env = environment
        self.λ = λ  # exponential decay rate used for exploration/exploitation (given)
        self.γ = γ  # discount rate for exploration (given)
        self.ε_max = 1.0  # Exploration probability at start (given)
        self.ε_min = 0.0005  # Minimum exploration probability (given)

        self.ε = self.ε_max # (decaying) probability of selecting random action according to ε-soft policy
        self.t_max = t_max  # upper limit voor episode
        self.t = 0  # episode time step
        self.τ = 0  # overall time step

    @abstractmethod
    def next_action(self, state):
        pass

    @abstractmethod
    def learn(self, episode: Episode):
        # at this point subclasses insert their implementation
        # see for example be\kdg\rl\learning\tabular\tabular_learning.py
        self.t += 1
        self.τ += 1

    @abstractmethod
    def on_learning_start(self):
        """
        Implements all necessary initialization that needs to be done at the start of new Episode
        Each subclasse learning algorithm should decide what to do here
        """
        pass

    def on_learning_end(self):
        self.τ += 1
        self.decay()

    def done(self):
        return self.t > self.t_max

    def decay(self):
        # Reduce epsilon ε, because we need less and less exploration as time progresses
        # alternative code for decay

        # 'self.ε' is the probability that a random action will be taken
        # '1- self.ε' is the probability that the best action will be taken
        # decreases with every episode !!! (whenever an episode ends, the agent will explore less and less
        self.ε = self.ε_min + (self.ε_max - self.ε_min) * np.exp(-self.λ * self.τ)
