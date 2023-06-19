import fitz
import difflib

def highlight_differences(file1, file2):
    # Open the PDF files
    pdf1 = fitz.open(file1)
    pdf2 = fitz.open(file2)

    # Iterate through the pages of the second PDF
    for page_num in range(len(pdf2)):
        page2 = pdf2[page_num]
        page1 = pdf1[page_num]

        # Get the text from both pages
        text1 = page1.get_text("text")
        text2 = page2.get_text("text")

        # Perform text comparison
        differ = difflib.Differ()
        diff = differ.compare(text1, text2)

        # Highlight the first occurrence of each difference on the second page
        pos2 = 0
        for line in diff:
            if line.startswith('+'):
                word2 = line[2:]
                start = text2.find(word2, pos2)
                if start != -1:
                    end = start + len(word2)
                    page2.add_highlight_annot(fitz.Rect(start, 0, end, 0))
                    pos2 = end

    # Save the modified PDF
    output_path = "highlighted_differences.pdf"
    pdf2.save(output_path)
    pdf2.close()

    print(f"Differences highlighted in {output_path}")

# Compare two PDF files and highlight differences in the second PDF
file1 = "path/to/file1.pdf"
file2 = "path/to/file2.pdf"
highlight_differences(file1, file2)
