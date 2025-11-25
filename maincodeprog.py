import json 
import os
import sys
JSON_FILENAME="tech" \
"_terms.json"

def load_dictionary_from_json(filename=JSON_FILENAME):
    """Loading words from JSON file into a dictionary"""
    words = {}
    try:
        if os.path.exists(filename):
            with open(filename, 'r', encoding='utf-8') as file:
                words = json.load(file)
            print(f"Loaded {len(words)} words from JSON")
        else:
            print(f"JSON file '{filename}' not found.")
    except Exception as e:
        print(f"Error loading JSON: {e}")
    return words

def save_word_to_json(word_data, filename=JSON_FILENAME):
    """Save dictionary to JSON file"""
    try:
        # First load existing data
        existing_data = {}
        if os.path.exists(filename):
            with open(filename, 'r', encoding='utf-8') as file:
                existing_data = json.load(file)
        
        # Add new word
        existing_data[word_data['word']] = {
            'meaning': word_data['meaning'],
            'example': word_data['example'],
            'synonyms': word_data['synonyms']
        }
        
        # Save back to file
        with open(filename, 'w', encoding='utf-8') as file:
            json.dump(existing_data, file, indent=4)
        
        return True
    except Exception as e:
        print(f"Error saving to JSON: {e}")
        return False

def menu():
    """Display the main menu options to the user"""
    print("\n" + "="*50)
    print("        THE TECHNICAL DIARY")
    print("="*50)
    print("1. Search for a word")
    print("2. Add a new word")
    print("3. View all words")
    print("4. Exit")
    print("="*50)

def choose():
    """Ask user what he would want to do"""
    try:
        choice = int(input("Enter your choice (1-4): "))
        return choice
    except ValueError:
        print("Please enter a valid number")

def word_search(dictionary):
    word = input("Enter the word to search: ").strip().lower()
    if not word:
        print("Please enter a valid word!")
        return
    result = dictionary.get(word)
    if result:
        print(f" Word found: {word.upper()}")
        print(f"Meaning: {result['meaning']}")
        if result['example']:
            print(f"Example: {result['example']}")
        if result['synonyms']:
            print(f"Synonyms: {', '.join(result['synonyms'])}")
    else:
        print(f"Word '{word}' not found in dictionary")
        suggestions = [w for w in dictionary.keys() if word in w]
        if suggestions:
            print(f"Did you mean: {', '.join(suggestions[:3])}?")

def add_word(dictionary):
    """Adding a new word to dictionary"""
    word = input("Enter the new word: ").strip().lower()
    if not word:
        print("Word absent")
        return
    if word in dictionary:
        print(f"Word '{word}' already exists in dictionary")
        return
    meaning = input("Enter the meaning: ").strip()
    if not meaning:
        print("Meaning cannot be empty")
        return
    
    example = input("Enter an example sentence (optional): ").strip()
    synonyms_input = input("Enter synonyms (comma separated, optional): ").strip()
    
    synonyms = []
    if synonyms_input:
        synonyms = [s.strip() for s in synonyms_input.split(',')]
    
    dictionary[word] = {
        'meaning': meaning,
        'example': example,
        'synonyms': synonyms
    }
    
    success = save_word_to_json({  
        'word': word,
        'meaning': meaning,
        'example': example,
        'synonyms': synonyms
    })
    
    if success:
        print(f"Word '{word}' added successfully!")
    else:
        print(f"Failed to save word '{word}' to file!")

def view_all_words(dictionary):
    """Display all words in the dictionary"""
    if not dictionary:
        print("Dictionary is empty!")
        return
    
    print(f"Total words in dictionary: {len(dictionary)}")
    print("\n" + "-"*50)
    for i, word in enumerate(dictionary.keys(), 1):
        print(f"{i}. {word}")
    print("-"*50)

def main():
    """Main function of the dictionary application"""
    print("Starting Dictionary Application")
    
    dictionary = load_dictionary_from_json() 
    
    while True:
        menu()
        choice = choose()
        
        if choice == 1:
            word_search(dictionary)
        elif choice == 2:
            add_word(dictionary)
        elif choice == 3:
            view_all_words(dictionary)
        elif choice == 4:
            print("Thank you for using Dictionary Application.")
            break
        else:
            print("Invalid choice! Please select 1-4.")
        
        input("\nPress Enter to continue...")

if __name__ == "__main__":
    main()
