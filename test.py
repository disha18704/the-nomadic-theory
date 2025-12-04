import llama_index.llms.google_genai as lib
import pkg_resources

print("--- DIAGNOSTIC REPORT ---")

# 1. Check Version
try:
    version = pkg_resources.get_distribution("llama-index-llms-google-genai").version
    print(f"Installed Version: {version}")
except:
    print("Could not detect version.")

# 2. Inspect the Library
print("\nAvailable classes in 'llama_index.llms.google_genai':")
available_items = dir(lib)

# Filter out the boring internal stuff (starts with __)
clean_items = [x for x in available_items if not x.startswith("__")]
print(clean_items)

print("-------------------------")