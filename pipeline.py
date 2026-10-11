import subprocess
import sys

def run_script(script_name):
    print(f"--- Running {script_name} ---")
    try:
        # Using sys.executable to ensure we use the same python interpreter
        result = subprocess.run([sys.executable, script_name], check=True, capture_output=True, text=True)
        print(result.stdout)
    except subprocess.CalledProcessError as e:
        print(f"Error occurred while running {script_name}:")
        print(e.stderr)
        sys.exit(1)

def main():
    scripts = ["extract.py", "transform.py", "load.py", "cleanup.py", "build_marts.py"]
    
    for script in scripts:
        run_script(script)
        
    print("Pipeline executed successfully.")

if __name__ == "__main__":
    main()
