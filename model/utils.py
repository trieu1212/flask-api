import math

def cosine_distance(x1, x2):
    mag1 = 0.0
    mag2 = 0.0
    product = 0.0

    for i in range(len(x1)):
        mag1 += x1[i] ** 2
        mag2 += x2[i] ** 2
        product += x1[i] * x2[i]

    mag1 = math.sqrt(mag1)
    mag2 = math.sqrt(mag2)

    result = product / (mag1 * mag2)
    print(f"Result: {result}")

    return result