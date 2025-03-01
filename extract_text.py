import requests
from bs4 import BeautifulSoup

# URL of "The Time Machine" text file
url = "https://www.gutenberg.org/files/35/35-0.txt"

# Fetch the content
response = requests.get(url)

# Ensure request was successful
if response.status_code == 200:
    text = response.text

    # Gutenberg books have header/footer text we should remove
    start_marker = "*** START OF THIS PROJECT GUTENBERG EBOOK THE TIME MACHINE ***"
    end_marker = "*** END OF THIS PROJECT GUTENBERG EBOOK THE TIME MACHINE ***"

    start_idx = text.find(start_marker)
    end_idx = text.find(end_marker)

    if start_idx != -1 and end_idx != -1:
        text = text[start_idx + len(start_marker):end_idx].strip()

    # Save cleaned text to a file
    with open("Selected_Document.txt", "w", encoding="utf-8") as file:
        file.write(text)

    print("Document saved as Selected_Document.txt")

else:
    print("Failed to download the document. Status code:", response.status_code)
