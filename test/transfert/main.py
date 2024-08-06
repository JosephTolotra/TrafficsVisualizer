# main.py
import config

def main():
    print("Current in main:", config.current)
    config.current = 10
    print("Current updated in main:", config.current)

if __name__ == "__main__":
    main()
