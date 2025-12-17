import time, random
import sys 
import os 
from faker import Faker

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils.order_generator import generate_order, save_order_to_file

fake = Faker("fr_FR")
OUTPUT_DIR = "data/sources/boutique_physique/"
CANAL = "boutique"

def simulate():
    fake.unique.clear()  # réinitialise la mémoire unique
    for _ in range(1900):
        order = generate_order(CANAL)
        save_order_to_file(order, OUTPUT_DIR)
        time.sleep(random.uniform(0.1, 0.2))

if __name__ == "__main__":
    simulate()
