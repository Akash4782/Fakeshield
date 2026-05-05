import sys
import os

# Add the current directory to sys.path to import app
sys.path.append(os.getcwd())

from app.models.binoculars import Binoculars

# Human Samples
human_samples = [
    "Present-day climate change includes both global warming...",
    "It is revealed in recent literature on quantum foundations...",
    "There’s nowhere in the world like Japan...",
    "The year 2026 marks a pivotal transition as AI moves...",
    "The history of Rome represents one of the most influential...",
    "Two roads diverged in a yellow wood...",
    "We the People of the United States...",
    "Hypertension, also known as high blood pressure...",
    "Preheat your oven to 350 degrees...",
    "The 2026 NBA Finals reached a thrilling conclusion...",
    "Interstellar is a breathtaking exploration of space...",
    "Introducing the new iPhone 17...",
    "Existence precedes essence...",
    "Apple's success can be attributed to its tight integration...",
    "The French Revolution was a period of far-reaching...",
    "The James Webb Space Telescope has captured its most...",
    "The annual Oakwood Community Fair returned this weekend...",
    "I have a dream that my four little children...",
    "It is a truth universally acknowledged...",
    "React makes it painless to create interactive UIs...",
    "Iceland is a land of fire and ice...",
    "Minimalism isn't just about getting rid of stuff...",
    "Start your workout with five minutes of light cardio...",
    "Diversification is the key to a healthy retirement...",
    "The cat sat on the windowsill...",
    "NASA's latest rover has discovered evidence of ancient...",
    "When I'm preparing for a role, I try to find a personal...",
    "To be, or not to be, that is the question...",
    "Winter is actually a great time to start planning...",
    "The food at Little Italy was absolutely divine..."
]

def diagnose():
    bino = Binoculars()
    print("Binoculars Raw Scores for Human Samples:")
    for i, text in enumerate(human_samples):
        score = bino.compute_score(text)
        print(f"Sample {i+1:2}: {score:.4f}")

if __name__ == "__main__":
    diagnose()
