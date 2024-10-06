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

text = """
Гул затих. Я вышел на подмостки. Прислонясь к дверному косяку, Я
ловлю в далеком отголоске, Что случится на моем веку. На меня наставлен сумрак ночи Тысячью биноклей на оси. Если только можно, Aвва Oтче, Чашу эту мимо пронеси.
"""

processed_text = preprocess_text(text)

k_values = range(1, 6)
hk_over_k = []

for k in k_values:
    entropy_k = calculate_entropy_k_grams(processed_text, k)
    hk_over_k.append(entropy_k / k)


plt.figure(figsize=(10, 6))
plt.plot(k_values, hk_over_k, marker='o', linestyle='-', color='b')
plt.xlabel('k')
plt.ylabel('Hk(T) / k')
plt.title('График зависимости Hk(T) / k от k')
plt.grid(True)
plt.show()
