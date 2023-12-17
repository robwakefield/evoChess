#!/usr/bin/env python

from abc import ABC, abstractmethod 
  
class PlayerAI(ABC): 
  
    @abstractmethod
    def make_move(self, board): 
        pass