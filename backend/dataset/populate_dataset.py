import os

# AI Samples
ai_essays = [
    "Artificial intelligence is a branch of computer science that deals with the creation of intelligent agents, which are systems that can reason, learn, and act autonomously. AI has the potential to revolutionize many aspects of our lives, from healthcare and transportation to education and entertainment.",
    "The industrial revolution was a period of significant social and economic change that began in Great Britain in the late 18th century. It was characterized by the transition from manual labor to machine-based manufacturing, leading to a massive increase in productivity and the growth of cities.",
    "Climate change is one of the most pressing challenges facing our planet today. It is caused by the release of greenhouse gases into the atmosphere, which trap heat and cause the Earth's temperature to rise. The consequences of climate change are already being felt around the world, from more frequent and intense heatwaves to rising sea levels."
]

ai_technical = [
    "A neural network is a type of machine learning model that is inspired by the structure and function of the human brain. It consists of layers of interconnected nodes, called neurons, that process information and learn patterns from data.",
    "Backpropagation is an algorithm used to train neural networks by calculating the gradient of the loss function with respect to the weights of the network. This gradient is then used to update the weights in a way that minimizes the loss.",
    "Convolutional neural networks (CNNs) are a type of neural network that is particularly well-suited for image processing tasks. They use convolutional layers to extract features from images, such as edges and textures, which are then used to classify the images."
]

ai_casual = [
    "Hey! I just wanted to check in and see how you're doing. I haven't heard from you in a while, so I hope everything is going well. Let me know if you want to catch up sometime soon!",
    "I'm so sorry I missed your call earlier. I was in a meeting and couldn't step out. Is everything okay? Give me a shout when you have a minute.",
    "Just saw that news about the new space mission. How cool is that? I can't believe we're actually going back to the moon. We should definitely go see a launch sometime!"
]

ai_stories = [
    "Once upon a time, in a land far, far away, there lived a young princess named Elara. She was kind, clever, and loved exploring the enchanted forest that surrounded her kingdom. One day, while she was wandering through the woods, she came across a mysterious talking fox who told her of a hidden treasure...",
    "The old clock on the mantelpiece ticked steadily, a reminder of the passing time. Elias sat in his armchair, staring into the flickering flames of the fireplace. He was thinking about the life he had lived, the choices he had made, and the people he had loved. He knew that his time was coming to an end, but he felt a sense of peace...",
    "The spaceship hummed as it hurtled through the vast emptiness of space. Captain Nova sat at the controls, her eyes fixed on the distant stars. She was on a mission to find a new home for humanity, a planet that could sustain life and provide a future for her people."
]

# Human Samples (from search results and knowledge)
human_essays = [
    "Climate change, a significant global challenge, refers to long-term shifts in weather patterns, encompassing changes in temperature, rainfall, and the frequency of extreme weather events. While the Earth's climate has naturally evolved over millennia, the current rapid warming trend is predominantly attributed to human activities.",
    "The impact of climate change on biodiversity is a critical issue. As global temperatures rise, many species face habitat loss, leading to a decline in population. The industrial revolution led to a substantial increase in greenhouse gases like CO2, primarily from burning fossil fuels for energy.",
    "Addressing the climate crisis requires a collective effort. Transitioning to CO2-free energy and more efficient energy use is essential. Policy changes to reduce fossil fuel production and promote clean technology are also necessary to protect the planet's ecological balance."
]

human_technical = [
    "A neural network is a computational system loosely modeled after the human brain, designed to process information and learn patterns from data. It consists of layers of interconnected nodes, often called neurons, which perform bulk processing tasks.",
    "Neural network layers typically include an input layer, hidden layers, and an output layer. Each neuron in a hidden layer receives inputs, multiplies them by weights, adds a bias, and applies an activation function. This process allows the network to model complex relationships.",
    "Deep learning involves training neural networks with many hidden layers. The adjustment of weights and biases happens through backpropagation to minimize error. This capability allows networks to make generalizations from unstructured data like images or text."
]

human_casual = [
    "Hey, just saw your message. Sorry for the late reply, had a crazy day at work. Would love to grab coffee this weekend and catch up on everything. Let me know what time works best for you!",
    "Can't believe it's already Friday! This week flew by. Are we still on for the game tomorrow? I'm really looking forward to it. Hope you've had a good one.",
    "Did you see the latest update on the project? Looks like we've got some work to do. Let's touch base on Monday morning to go over the details and make a plan moving forward."
]

human_stories = [
    "My best friend disappeared in 1998, only to be 'found' years later inside a tree. The encounter turned unsettlingly supernatural, with a plea for 'blood' to free him. It was a moment that stayed with me forever, haunting my dreams.",
    "My friend vanished nineteen years ago from a place they've never returned to. I still experience unsettling occurrences that suggest something is trying to lure me back to that same location. The memory of that night is as fresh as ever.",
    "I searched for my best friend for four years, leading to a reunion with a dramatically changed person. They revealed a bizarre, lifelong attachment to a malevolent entity that had controlled their actions all that time."
]

def save_samples(base_path, samples_dict):
    for category, samples in samples_dict.items():
        cat_dir = os.path.join(base_path, category)
        os.makedirs(cat_dir, exist_ok=True)
        for i, sample in enumerate(samples):
            file_path = os.path.join(cat_dir, f"{category}_{i+1}.txt")
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(sample)
    print(f"Saved samples to {base_path}")

save_samples("backend/dataset/ai", {
    "essay": ai_essays,
    "technical": ai_technical,
    "casual": ai_casual,
    "story": ai_stories
})

save_samples("backend/dataset/human", {
    "essay": human_essays,
    "technical": human_technical,
    "casual": human_casual,
    "story": human_stories
})
