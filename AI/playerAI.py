#!/usr/bin/env python

from abc import ABC, abstractmethod 
  
class PlayerAI(ABC): 

    @abstractmethod
    def __init__(self): 
        self.name = "AI"
  
    @abstractmethod
    def make_move(self, board): 
        pass