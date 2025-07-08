"""
Simple verification script to check our implementation
"""

import importlib
import sys

def verify_module(module_name):
    try:
        module = importlib.import_module(module_name)
        print(f"✅ Successfully imported {module_name}")
        return True
    except Exception as e:
        print(f"❌ Failed to import {module_name}: {str(e)}")
        return False

if __name__ == "__main__":
    modules = [
        "ai_service",
        "config",
        "conversation_handler",
        "session_manager",
        "utils",
        "validators"
    ]
    
    success_count = 0
    for module in modules:
        if verify_module(module):
            success_count += 1
    
    print(f"\nVerification complete: {success_count}/{len(modules)} modules successfully imported")
    if success_count == len(modules):
        print("✅ All modules imported successfully. Implementation looks good!")
    else:
        print("⚠️ Some modules failed to import. Please check the issues above.")
