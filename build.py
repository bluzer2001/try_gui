import sys
import os

def get_running_directory():
    if hasattr(sys, 'frozen'):
        # The application is frozen (running as an executable)
        running_dir = os.path.dirname(sys.executable)
    else:
        # The application is not frozen (running as a script)
        running_dir = os.path.dirname(os.path.abspath(__file__))
    return running_dir

def main():
    running_dir = get_running_directory()
    print(f"The executable is running from: {running_dir}")

    # Example of using the running directory to load a configuration file
    config_path = os.path.join(running_dir, 'config.json')
    if os.path.exists(config_path):
        print(f"Configuration file found at: {config_path}")
    else:
        print(f"No configuration file found at: {config_path}")

if __name__ == "__main__":
    main()
