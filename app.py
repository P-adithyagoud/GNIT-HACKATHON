import sys
import os

# Ensure the root directory is in the path
sys.path.append(os.path.dirname(__file__))

# Import the factory from the explicitly named 'core' package
try:
    from core import create_app
    app = create_app()
except Exception as e:
    # This helps diagnose boot errors in the Vercel logs
    print(f"CRITICAL BOOT ERROR: {str(e)}")
    raise e

if __name__ == '__main__':
    app.run(debug=True, port=5000)
