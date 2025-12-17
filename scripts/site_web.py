import time, random
import sys 
import os 

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils.order_generator import generate_order, save_order_to_file

OUTPUT_DIR = "data/sources/site_web/"
CANAL = "web"

def simulate():
    for _ in range(1900):
        order = generate_order(CANAL)
        save_order_to_file(order, OUTPUT_DIR)
        time.sleep(random.uniform(0.1, 0.2))  # accéléré pour générer 500 rapidement

if __name__ == "__main__":
    simulate()
