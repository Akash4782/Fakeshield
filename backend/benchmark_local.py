import requests
import time

text = """Deep learning is a specialized branch of machine learning that focuses on training artificial neural networks with many layers (hence “deep”) to learn patterns from large amounts of data. Inspired by the structure of the human brain, these neural networks consist of interconnected nodes (neurons) that process information and pass it forward. Deep learning models are particularly powerful because they can automatically learn features from raw data, reducing the need for manual feature engineering.

At the core of deep learning are artificial neural networks, which are made up of input layers, hidden layers, and output layers. Each layer transforms the data using mathematical operations, allowing the network to gradually learn complex patterns. The more layers a network has, the more abstract and high-level features it can capture. For example, in image recognition, early layers may detect edges, while deeper layers recognize objects like faces or animals.

One of the most important aspects of deep learning is the training process. During training, the model learns by adjusting its internal parameters (weights and biases) using a large dataset. This process involves a technique called backpropagation, where the model calculates the error in its predictions and updates its parameters to reduce that error. Optimization algorithms like gradient descent are commonly used to guide this learning process.

Deep learning models require large amounts of data to perform well. Unlike traditional machine learning methods, which may work with smaller datasets, deep learning thrives on big data. The availability of massive datasets, along with increased computational power from GPUs and cloud computing, has been a key factor in the rapid growth of deep learning applications.

There are several types of deep learning architectures designed for different tasks. Convolutional Neural Networks (CNNs) are widely used for image and video analysis, while Recurrent Neural Networks (RNNs) and their variants like LSTMs are used for sequential data such as text and speech. More recently, Transformer-based models have become popular for natural language processing tasks due to their ability to handle long-range dependencies efficiently.

Deep learning has revolutionized many industries by enabling breakthroughs in areas such as computer vision, natural language processing, speech recognition, and autonomous systems. Applications include facial recognition, language translation, recommendation systems, self-driving cars, and medical diagnosis. These systems can often outperform traditional approaches when given sufficient data and computational resources.

Despite its strengths, deep learning also has some limitations. It requires significant computational power, which can be expensive and resource-intensive. Training deep models can take a long time, especially for large datasets. Additionally, these models often act as “black boxes,” meaning it can be difficult to interpret how they arrive at specific decisions, which raises concerns in critical applications like healthcare and finance.

Another challenge is overfitting, where a model performs well on training data but poorly on unseen data. Techniques such as regularization, dropout, and data augmentation are used to address this issue. Moreover, deep learning models are sensitive to the quality and diversity of data; biased or insufficient data can lead to inaccurate or unfair outcomes.

The future of deep learning is promising, with ongoing research focused on improving efficiency, interpretability, and generalization. New approaches aim to reduce the dependence on large labeled datasets, such as self-supervised and unsupervised learning. There is also growing interest in combining deep learning with other fields like reinforcement learning to build more intelligent systems.

In summary, deep learning is a powerful and rapidly evolving field that has transformed how machines learn and process information. By leveraging multi-layered neural networks and large datasets, it enables systems to perform complex tasks with high accuracy. While it comes with challenges such as high resource requirements and lack of transparency, its impact across industries continues to grow, making it one of the most important technologies in modern artificial intelligence."""

url = "http://localhost:8002/api/v1/text/analyze"

print(f"Submitting text ({len(text.split())} words) to local detector...")
t0 = time.time()
try:
    response = requests.post(url, json={"text": text, "mode": "deep", "include_highlights": True})
    t1 = time.time()
    
    if response.status_code == 200:
        data = response.json().get("data")
        print(f"\nAnalysis Complete in {t1-t0:.2f}s")
        print(f"Verdict:     {data['verdict']}")
        print(f"Confidence:  {data['confidence']}%")
        print("\nSignals:")
        for k, v in data['signals'].items():
            print(f"  {k:15}: {v}%")
    else:
        print(f"Error: {response.status_code} - {response.text}")
except Exception as e:
    print(f"Connection Failed: {e}")
