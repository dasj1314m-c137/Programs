from collections import Counter

def median(numbers):
    n = len(numbers)
    sorted_list = sorted(numbers)
    mid = n // 2
    if n % 2 == 0:
        med = (sorted_list[mid - 1] + sorted_list[mid]) / 2
    else:
        med = sorted_list[mid]
    return med

def mean(numbers):
    return round(sum(numbers) / len(numbers), 2)

def mode(numbers):
    frequencyA = Counter(numbers)
    max_freq = max(frequencyA.values())
    modes = [str(key) for key, value in frequencyA.items() if value == max_freq]
    if len(modes) == len(frequencyA):
        return None
    return modes

def calculate_all_measures(numbers):
    return {
        "mean": mean(numbers),
        "median": median(numbers),
        "mode": mode(numbers)
    }
