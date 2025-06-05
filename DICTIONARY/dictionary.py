import requests
import tkinter as tk
from tkinter import messagebox

def get_meaning():
    word = entry.get().strip()
    if not word:
        messagebox.showwarning("Input Error", "Please enter a word.")
        return

    url = f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}"
    response = requests.get(url)

    result_text.delete("1.0", tk.END)  # clear previous text

    if response.status_code == 200:
        data = response.json()
        meanings = data[0].get("meanings", [])
        if not meanings:
            result_text.insert(tk.END, f"No meanings found for '{word}'.")
            return

        result_text.insert(tk.END, f"Meanings for '{word}':\n\n")
        for meaning in meanings:
            part_of_speech = meaning.get("partOfSpeech", "unknown")
            definitions = meaning.get("definitions", [])
            for i, definition in enumerate(definitions[:3], 1):  # show up to 3
                meaning_text = definition.get("definition")
                result_text.insert(tk.END, f"{i}. ({part_of_speech}) {meaning_text}\n\n")
    else:
        result_text.insert(tk.END, f"Word {word} not found in the dictionary.")

# GUI Setup
root = tk.Tk()
root.title("Dictionary App")
root.geometry("500x400")
root.resizable(False, False)

tk.Label(root, text="Enter a word:", font=("Arial", 12)).pack(pady=10)
entry = tk.Entry(root, font=("Arial", 14), width=30)
entry.pack()

tk.Button(root, text="Get Meaning", command=get_meaning, font=("Arial", 12)).pack(pady=10)

result_text = tk.Text(root, wrap=tk.WORD, font=("Arial", 12), height=15, width=60)
result_text.pack(padx=10, pady=10)

root.mainloop()
