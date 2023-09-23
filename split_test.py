import PyPDF2

# Open the PDF file
pdf_file = open('/Users/fermibot/Downloads/chapter6.pdf', 'rb')

# Create a PDF reader object
reader = PyPDF2.PdfReader(pdf_file)

# Get the number of pages in the PDF file
num_pages = len(reader.pages)

# Create a list to store the chapter titles
chapter_titles = []

# Iterate over the pages in the PDF file
print(reader.pages[1].extract_text())
for i in range(num_pages):
    # Get the text on the current page
    text = reader.pages[i].extract_text()

    # Find the chapter title in the text
    chapter_title = text.split('\n')[0]

    # Add the chapter title to the list
    chapter_titles.append(chapter_title)

# Close the PDF file
pdf_file.close()

if __name__ == '__main__':
    # Print the chapter titles
    print(chapter_titles)
