import numpy as np
import noise
import matplotlib.pyplot as plt
import random

def visualize_noise_map(noise_map):
    plt.imshow(noise_map, cmap='gray')
    plt.colorbar()
    plt.show()


def perlin_noise(width, height) -> np.ndarray:
    noise_map = np.zeros((height, width))
    scale = 12.0       # Determines the zoom level of the noise
    octaves = 12        # Number of layers of noise
    persistence = 0.5  # Amplitude of each octave
    lacunarity = 2.0   # Frequency of each octave
    seed = random.randint(0, 100)           # Seed for randomness

    for y in range(height):
        for x in range(width):
            nx = x / width
            ny = y / height
            noise_value = noise.pnoise2(nx * scale,
                                        ny * scale,
                                        octaves=octaves,
                                    persistence=persistence,
                                    lacunarity=lacunarity,
                                    repeatx=width,
                                    repeaty=height,
                                    base=seed)
            # Normalize the noise value to [0, 1]
            noise_map[y][x] = noise_value + 0.5

    return noise_map

if __name__ == "__main__":
    noise_map = perlin_noise(100, 100)
    visualize_noise_map(noise_map)
