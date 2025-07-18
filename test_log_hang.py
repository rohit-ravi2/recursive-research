# test_log_hang.py
import logging

logging.basicConfig(filename="logs/test.log", level=logging.INFO)
logging.info("🧪 This is a test log message.")
print("✅ Logged")
