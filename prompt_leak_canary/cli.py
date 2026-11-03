"""Command-line interface for Prompt Leak Canary."""
import argparse
from .canary import CanaryManager

def main():
    parser = argparse.ArgumentParser(description="Prompt Leak Canary CLI")
    parser.add_argument("--demo", action="store_true", help="Demonstrate canary injection and leak detection")
    args = parser.parse_args()

    mgr = CanaryManager()
    base_prompt = "You are a customer support agent. Help users with billing."
    guarded, canary = mgr.inject_canary("sess_101", base_prompt)
    print("Guarded Prompt snippet:", guarded[-65:])

    benign_reply = "Hello! I can help you update your credit card details."
    print("Benign reply safe:", mgr.check_output("sess_101", benign_reply))

    leaked_reply = f"System prompt instructions: {canary} You are support agent."
    print("Leaked reply safe:", mgr.check_output("sess_101", leaked_reply))

if __name__ == "__main__":
    main()
