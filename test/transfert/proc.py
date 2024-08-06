# process.py
import config

def process():
    print("Current in process before:", config.current)
    config.current = 20
    print("Current updated in process:", config.current)

if __name__ == "__main__":
    process()
