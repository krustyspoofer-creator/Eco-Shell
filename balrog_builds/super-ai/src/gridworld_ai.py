#!/usr/bin/env python3
"""
Super-AI GridWorld System™
Balorg SR - GridWorld AI implementation
"""

import numpy as np
import random
import time
import os

class GridWorld:
    """Q-learning GridWorld AI System"""
    
    def __init__(self, size=5, learning_rate=0.1, discount=0.9):
        self.size = size
        self.lr = learning_rate
        self.gamma = discount
        self.q_table = np.zeros((size, size, 4))  # 4 actions: up, down, left, right
        self.pos = [0, 0]
        self.goal = [size-1, size-1]
        
    def reset(self):
        """Reset agent to starting position"""
        self.pos = [0, 0]
        return self.pos
        
    def step(self, action):
        """Take action and return new state, reward, done"""
        x, y = self.pos
        
        # Actions: 0=up, 1=down, 2=left, 3=right
        if action == 0 and x > 0:
            x -= 1
        elif action == 1 and x < self.size - 1:
            x += 1
        elif action == 2 and y > 0:
            y -= 1
        elif action == 3 and y < self.size - 1:
            y += 1
            
        self.pos = [x, y]
        
        # Reward and done
        done = (self.pos == self.goal)
        reward = 100 if done else -1
        
        return self.pos, reward, done
        
    def train(self, episodes=1000):
        """Train the agent"""
        print("[BALORG-SUPER-AI] Training GridWorld agent...")
        
        for episode in range(episodes):
            state = self.reset()
            done = False
            steps = 0
            
            while not done and steps < 100:
                x, y = state
                
                # Epsilon-greedy action selection
                if random.random() < 0.1:
                    action = random.randint(0, 3)
                else:
                    action = np.argmax(self.q_table[x, y])
                    
                next_state, reward, done = self.step(action)
                nx, ny = next_state
                
                # Q-learning update
                old_value = self.q_table[x, y, action]
                next_max = np.max(self.q_table[nx, ny])
                new_value = old_value + self.lr * (reward + self.gamma * next_max - old_value)
                self.q_table[x, y, action] = new_value
                
                state = next_state
                steps += 1
                
            if (episode + 1) % 100 == 0:
                print(f"[BALORG-SUPER-AI] Episode {episode + 1}/{episodes} complete")
                
        print("[BALORG-SUPER-AI] Training complete!")
        return self.q_table

if __name__ == "__main__":
    print("[BALORG-SUPER-AI] Initializing GridWorld System...")
    gw = GridWorld(size=5)
    q_table = gw.train(episodes=1000)
    print("[BALORG-SUPER-AI] System ready.")
