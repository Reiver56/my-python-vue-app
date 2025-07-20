# da cambiare in produzione, in quanto poco sicuro.
import subprocess

def run_code(code: str) -> str:
    try:
        # Execute the code using Python's subprocess module
      result = subprocess.run(
          ["python3", "-c", code],
          capture_output=True, text=True, timeout=5
      )
      return result.stdout or result.stderr
    except Exception as e:
      return f"Code execution failed: {e}"