import sys
import os
import time
import re
import numpy as np

# Add the current directory to sys.path to import app
sys.path.append(os.getcwd())

from app.models.text_classifier_ensemble import ensemble_predict

# --- DATASET: 30 HUMAN SAMPLES ---
human_samples = [
    # 1-20 from Web Search
    "The history of artificial intelligence (AI) began in antiquity, with myths, stories, and rumors of artificial beings endowed with intelligence or consciousness by master craftsmen. The study of logic and formal reasoning from antiquity to the present led to the development of the programmable digital computer in the 1940s.",
    "NASA's James Webb Space Telescope has captured a stunning new image of the Pillars of Creation, where new stars are forming within dense clouds of gas and dust. Three-dimensional pillars look like majestic rock formations, but are made of cool interstellar gas and dust that appear semi-transparent in near-infrared light.",
    "Genetic variation is the diversity in gene frequencies between individuals or across groups. Such variation is a key component of evolution, acting as the raw material upon which natural selection acts. By comparing genomes across populations, researchers can pinpoint specific genetic markers.",
    "Christopher Nolan's Oppenheimer is a technical masterpiece that remains emotionally cold but visually and aurally overwhelming. The film is paced magnificently, feeling shorter than its three-hour runtime; the star-studded cast give it their all, and the constant dread and unease make it worth watching.",
    "Florence was the only Italian city I had visited before, so it felt like a beautiful reunion. Once we arrived, our guide took us to her old apartment on the way to the Duomo. We passed a wine bar, where she had befriended the entire staff. Armando, a waiter at the wine bar, saw her—and it was touching.",
    "Sourdough is a way of life but it's also a type of bread made with a natural leavening agent relying on a slow fermentation of the dough. Sourdough bread has a bit of a sour taste and is very popular in San Francisco and Paris. My life in sourdough is all about wild yeast and slow food.",
    "The match lived up to all the pre-tournament hype, with both players demonstrating incredible athleticism and shot-making ability under immense pressure. After splitting the first two sets, the intensity reached a fever pitch in the deciding set, where a single break of serve proved to be the difference.",
    "Global economic growth is projected to remain modest as high interest rates continue to dampen investment and consumption in major economies. While inflation has begun to moderate in several regions, underlying price pressures remain persistent, prompting central banks to maintain a cautious stance.",
    "The central tension in utilitarianism lies in the demand for impartiality; if one must weigh every person's well-being equally, the special obligations we hold toward friends and family can seem morally suspect. Critics argue that an ethical system requiring the sacrifice of personal connection fails.",
    "She enters the forest, her body weary, her feet slapping heavy. The change is instant. She is wrapped in cool air, grasped in its arms and sucked in, the humidity and heaviness of outside shaken and lifted off. The ground starts to absorb her steps, and she begins to move silently.",
    "As organizations shift more of their infrastructure to the cloud, the attack surface for potential threats has expanded exponentially. Cybercriminals are increasingly leveraging automated bots and AI-driven phishing campaigns to bypass traditional signature-based security defenses.",
    "A balanced diet is foundational to long-term health, providing the essential macronutrients and micronutrients necessary for metabolic function. While there is much debate surrounding specific dietary patterns, the consensus among nutritionists emphasizes the intake of whole, unprocessed foods.",
    "The Renaissance, or rebirth, was a period of time when Europeans began to question what they had been told was sacrosanct. Through art, inventions, science, literature, and theology, the separate nations of the European continent sought answers that the Roman Catholic Church was unwilling to offer.",
    "The Grantee shall have and hold the property, including all easements, appurtenances, and improvements thereon, in fee simple absolute, subject to the restrictive covenants and zoning ordinances of record. No alteration to the structure shall be undertaken without the express written consent.",
    "What if we stopped asking, 'What do you want to be when you grow up?' and started asking, 'What problem do you want to solve?' Because when you focus on the problem, you start to see the world not as a series of labels or boxes, but as a series of opportunities for impact.",
    "This season is all about the resurgence of maximalism, with bold prints, oversized silhouettes, and eclectic layering dominating the runways. While minimalism had its moment, designers are now leaning into vibrant colors and unexpected textures that demand attention.",
    "Roses are hardy plants and flourish in a wide range of conditions, but they do have a few basic requirements that you should consider before planting. They need at least six hours of direct sunlight each day for the best bloom production. Furthermore, soil drainage is critical.",
    "On his latest record, the saxophonist strips away the complex arrangements of his previous work, opting instead for a raw, improvisational exploration of blues scales. The interplay between the rhythm section is telepathic, with the drummer providing a restless, textured foundation.",
    "Networking is one of the most valuable activities you can do for your career, so make the most of it. Prepare and have a plan for what you want to achieve. Don't spend all your time talking to the colleagues you came with or people you know. Think about your network beyond the event.",
    "Understanding child development and parenting research can help us as we raise our children, but it doesn't tell us everything. Research is all about understanding the typical track of children's development. As a parent, it's useful to know approximately when your child might walk.",
    # 21-30: Manual additions (Literature/History)
    "Call me Ishmael. Some years ago—never mind how long precisely—having little or no money in my purse, and nothing particular to interest me on shore, I thought I would sail about a little and see the watery part of the world. It is a way I have of driving off the spleen and regulating the circulation.",
    "Four score and seven years ago our fathers brought forth on this continent, a new nation, conceived in Liberty, and dedicated to the proposition that all men are created equal. Now we are engaged in a great civil war, testing whether that nation, or any nation so conceived and so dedicated, can long endure.",
    "It was the best of times, it was the worst of times, it was the age of wisdom, it was the age of foolishness, it was the epoch of belief, it was the epoch of incredulity, it was the season of Light, it was the season of Darkness, it was the spring of hope, it was the winter of despair.",
    "The quick brown fox jumps over the lazy dog. This sentence contains every letter in the English alphabet. It is often used for testing keyboards and fonts. In the 19th century, it was a common exercise for students learning penmanship and typing on early mechanical typewriters.",
    "In a hole in the ground there lived a hobbit. Not a nasty, dirty, wet hole, filled with the ends of worms and an oozy smell, nor yet a dry, bare, sandy hole with nothing in it to sit down on or to eat: it was a hobbit-hole, and that means comfort. It had a perfectly round door like a porthole.",
    "Mr. Sherlock Holmes, who was usually very late in the mornings, save upon those not infrequent occasions when he was up all night, was seated at the breakfast table. I stood upon the hearth-rug and picked up the stick which our visitor had left behind him the night before.",
    "To be, or not to be, that is the question: Whether 'tis nobler in the mind to suffer The slings and arrows of outrageous fortune, Or to take arms against a sea of troubles, And by opposing end them? To die: to sleep; No more; and by a sleep to say we end The heart-ache.",
    "The sun was setting behind the rugged peaks of the Himalayas, casting long, purple shadows across the valley. Tenzing adjusted his pack, feeling the familiar weight against his shoulders. He had been climbing these trails since he was a boy, yet the mountains never failed to inspire awe.",
    "The Industrial Revolution marked a major turning point in history; almost every aspect of daily life was influenced in some way. In particular, average income and population began to exhibit unprecedented sustained growth. Some economists say that the main impact was the standard of living.",
    "Space, the final frontier. These are the voyages of the starship Enterprise. Its five-year mission: to explore strange new worlds, to seek out new life and new civilizations, to boldly go where no man has gone before. The vast emptiness of the cosmos holds secrets beyond our wildest imagination."
]

# --- DATASET: 30 AI SAMPLES ---
ai_samples = [
    "Artificial intelligence is a branch of computer science that aims to create machines capable of performing tasks that typically require human intelligence. These tasks include natural language processing, image recognition, and decision-making based on complex data sets and algorithms.",
    "The advent of large language models has significantly transformed the landscape of human-computer interaction. By leveraging massive amounts of textual data, these models can generate coherent and contextually relevant responses, making them invaluable tools for research and content creation.",
    "To optimize your React application, you should consider using techniques such as memoization, code-splitting, and lazy loading. Additionally, profiling your components with the React DevTools can help identify unnecessary re-renders and performance bottlenecks in your UI.",
    "Quantum computing utilizes the principles of superposition and entanglement to perform calculations that would be impossible for classical computers. While the technology is still in its nascent stages, it holds the potential to revolutionize fields such as cryptography and materials science.",
    "The transition to renewable energy sources is essential for mitigating the impacts of climate change. Solar and wind power have become increasingly cost-effective, providing a sustainable alternative to fossil fuels and reducing the overall carbon footprint of global energy production.",
    "Blockchain technology provides a decentralized and transparent method for recording transactions across a network. By using cryptographic hashing, it ensures that data cannot be altered retroactively without the consensus of the majority, making it ideal for financial applications.",
    "Machine learning algorithms can be categorized into three main types: supervised learning, unsupervised learning, and reinforcement learning. Each approach has its own strengths and is suited for different types of problems, from image classification to autonomous driving.",
    "The internet of things (IoT) refers to the growing network of physical objects that are connected to the internet and can share data with each other. This connectivity allows for greater automation and efficiency in various sectors, including smart homes and industrial manufacturing.",
    "Natural language processing (NLP) is a subfield of AI that focuses on the interaction between computers and human language. It involves tasks such as sentiment analysis, machine translation, and text summarization, enabling machines to understand and generate human-like text.",
    "Deep learning is a subset of machine learning that uses multi-layered neural networks to model complex patterns in data. These architectures, inspired by the structure of the human brain, have achieved state-of-the-art results in computer vision and speech recognition.",
    "The integration of AI in healthcare has the potential to improve diagnostic accuracy and patient outcomes. By analyzing medical images and patient records, AI systems can assist doctors in identifying early signs of disease and recommending personalized treatment plans.",
    "Cybersecurity is the practice of protecting systems, networks, and programs from digital attacks. These attacks are usually aimed at accessing, changing, or destroying sensitive information, extorting money from users, or interrupting normal business processes.",
    "The global supply chain is a complex network of organizations, people, activities, and resources involved in moving a product from supplier to customer. Disruptions in one part of the chain can have a ripple effect, leading to delays and increased costs for businesses and consumers.",
    "Digital marketing involves the use of online channels to promote products and services to a target audience. Strategies such as search engine optimization (SEO), social media marketing, and email campaigns are essential for building brand awareness and driving sales.",
    "The concept of the metaverse refers to a collective virtual shared space, created by the convergence of virtually enhanced physical reality and physically persistent virtual space. It represents a new frontier for social interaction, commerce, and entertainment in the digital age.",
    "Data science is an interdisciplinary field that uses scientific methods, processes, algorithms, and systems to extract knowledge and insights from structured and unstructured data. It combines techniques from statistics, computer science, and domain-specific knowledge.",
    "Cloud computing provides on-demand access to computing resources, such as servers, storage, and databases, over the internet. This model allows businesses to scale their infrastructure quickly and cost-effectively, without the need for significant upfront investment in hardware.",
    "The development of autonomous vehicles relies on a combination of sensors, cameras, and AI algorithms to navigate complex environments. These vehicles have the potential to improve road safety, reduce traffic congestion, and provide greater mobility for individuals who cannot drive.",
    "Edge computing is a distributed computing paradigm that brings computation and data storage closer to the location where it is needed. By processing data at the edge of the network, it can reduce latency and bandwidth usage for applications such as real-time video analytics.",
    "The circular economy is an economic model that emphasizes the reuse, repair, and recycling of materials to minimize waste and reduce the environmental impact of production and consumption. It represents a shift away from the traditional linear 'take-make-dispose' approach.",
    "Bioinformatics is the application of computer science and statistics to the field of biology, particularly in the analysis of large-scale biological data such as genomic sequences. It plays a crucial role in drug discovery and the study of evolutionary relationships between species.",
    "The gig economy is a labor market characterized by the prevalence of short-term contracts or freelance work as opposed to permanent jobs. While it offers flexibility for workers, it also raises concerns about job security and the lack of traditional employment benefits.",
    "Robotic process automation (RPA) involves the use of software robots to automate repetitive and rule-based tasks in business processes. By freeing up human workers for more complex and creative tasks, it can significantly improve organizational efficiency and productivity.",
    "The psychology of color explores how different hues can influence human emotions and behaviors. In marketing and design, understanding color theory is essential for creating visual experiences that resonate with the target audience and convey the desired brand message.",
    "Strategic planning is a process by which an organization defines its direction and makes decisions on allocating its resources to pursue this strategy. It involves setting goals, analyzing the competitive environment, and developing action plans to achieve long-term success.",
    "The rise of remote work has been accelerated by advancements in communication technology and a shift in organizational culture. While it offers benefits such as increased flexibility and reduced commuting time, it also presents challenges for team collaboration and maintaining work-life balance.",
    "Financial literacy is the ability to understand and effectively use various financial skills, including personal financial management, budgeting, and investing. It is a critical life skill that can help individuals make informed decisions and achieve long-term financial stability.",
    "The importance of biodiversity lies in its role in maintaining ecosystem stability and providing essential services such as pollination, water purification, and climate regulation. Loss of biodiversity can have profound consequences for the health of our planet and human well-being.",
    "Effective communication is a cornerstone of successful leadership and teamwork. It involves not only the clear expression of ideas but also active listening and the ability to adapt one's communication style to different audiences and contexts.",
    "The history of space exploration is a testament to human curiosity and the desire to push the boundaries of our knowledge. From the launch of Sputnik to the Apollo moon landings, each milestone has expanded our understanding of the universe and our place within it."
]

def run_stress_test_v3():
    print("="*60)
    print("    FAKESHIELD FINAL ACCURACY STRESS TEST (v16.0)     ")
    print("="*60)
    
    # --- PHASE 1: HUMAN ---
    print("\n--- PHASE 1: TESTING 30 HUMAN SAMPLES ---")
    human_correct = 0
    for i, text in enumerate(human_samples):
        res = ensemble_predict(text, mode="standard")
        verdict = res["verdict"]
        score = res["score"] * 100
        
        # Human Correct if verdict is LIKELY HUMAN or UNCERTAIN (below 50%)
        is_correct = verdict == "LIKELY HUMAN" or (verdict == "UNCERTAIN" and score < 50.0)
        status = "CORRECT" if is_correct else "FAIL"
        if is_correct: human_correct += 1
        
        print(f"Sample {i+1:2}: {verdict:18} | Score: {score:4.1f}% | {status}")
        
    # --- PHASE 2: AI ---
    print("\n--- PHASE 2: TESTING 30 AI SAMPLES ---")
    ai_correct = 0
    for i, text in enumerate(ai_samples):
        res = ensemble_predict(text, mode="standard")
        verdict = res["verdict"]
        score = res["score"] * 100
        
        # AI Correct if verdict is AI GENERATED, LIKELY AI, or UNCERTAIN (above 50%)
        is_correct = verdict in ["AI GENERATED", "LIKELY AI"] or (verdict == "UNCERTAIN" and score >= 50.0)
        status = "CORRECT" if is_correct else "FAIL"
        if is_correct: ai_correct += 1
        
        print(f"Sample {i+1:2}: {verdict:18} | Score: {score:4.1f}% | {status}")
        
    # --- REPORT ---
    h_acc = (human_correct / 30) * 100
    a_acc = (ai_correct / 30) * 100
    total_acc = ((human_correct + ai_correct) / 60) * 100
    
    print("\n" + "="*60)
    print("                   FINAL ACCURACY REPORT                    ")
    print("="*60)
    print(f"Human Accuracy (False Positives: {30-human_correct}): {h_acc:.1f}%")
    print(f"AI Accuracy (False Negatives: {30-ai_correct}): {a_acc:.1f}%")
    print(f"OVERALL STRESS TEST ACCURACY: {total_acc:.1f}%")
    print("="*60)

if __name__ == "__main__":
    run_stress_test_v3()
