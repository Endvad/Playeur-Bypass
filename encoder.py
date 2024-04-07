from base64 import b64encode
import sys
import pyperclip

filename = "icon.png"
with open(filename, "rb") as f:
    pyperclip.copy(b64encode(f.read()).decode("ascii"))
    print("Copied to clipboard.")