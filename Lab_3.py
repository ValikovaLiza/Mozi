import re
from collections import Counter
import numpy as np
import matplotlib.pyplot as plt

def preprocess_text(text):
    return re.sub(r'[^а-яА-Я]', '', text).lower()

# Расчет энтропии k-грамм
def calculate_entropy_k_grams(text, k):
    k_grams = [text[i:i+k] for i in range(len(text) - k + 1)]
    total_k_grams = len(k_grams)
    
    k_gram_counts = Counter(k_grams)
    
    probabilities = [count / total_k_grams for count in k_gram_counts.values()]
    
    entropy = -sum(p * np.log2(p) for p in probabilities)
    return entropy

file = open("text3.txt", "r", encoding="utf-8")
text = file.read()

processed_text = preprocess_text(text)

k_values = range(1, 6)
hk_over_k = []

for k in k_values:
    entropy_k = calculate_entropy_k_grams(processed_text, k)
    hk_over_k.append(entropy_k / k)
print(hk_over_k)

plt.figure(figsize=(10, 6))
plt.plot(k_values, hk_over_k, marker='o', linestyle='-', color='b', label='Hk(T) / k')

for i, (k, hk_k) in enumerate(zip(k_values, hk_over_k)):
    plt.text(k+0.3, hk_k + 0.1, f'({k}, {hk_k:.2f})', fontsize=9, ha='right', va='bottom')

plt.xlabel('k')
plt.ylabel('Hk(T) / k')
plt.title('График зависимости Hk(T) / k от k')
plt.xticks(ticks=k_values)
plt.grid(True)
plt.legend()
plt.show()
file.close()
