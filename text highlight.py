import fitz
import difflib

def highlight_differences(file1, file2):
    # Open the PDF files
    pdf1 = fitz.open(file1)
    pdf2 = fitz.open(file2)

    # Iterate through the pages of the second PDF
    for page_num in range(len(pdf2)):
        page2 = pdf2[page_num]

        # Get the text from both pages
        text1 = pdf1[page_num].get_text("text")
        text2 = page2.get_text("text")

        # Compare the text using difflib
        differ = difflib.Differ()
        diff = differ.compare(text1, text2)

        # Track the positions of differences
        diff_positions = []
        pos2 = 0
        for line in diff:
            if line.startswith('-') or line.startswith('+'):
                diff_positions.append(pos2)
            if not line.startswith('-'):
                pos2 += len(line[2:])

        # Highlight the positions of differences on the second page
        for pos in diff_positions:
            highlight_rect = [pos, 0, pos+1, 1]  # Modify the height as needed
            page2.add_highlight_annot(highlight_rect)

    # Save the modified PDF
    output_path = "highlighted_differences.pdf"
    pdf2.save(output_path)
    pdf2.close()

    print(f"Differences highlighted in {output_path}")

# Compare two PDF files and highlight the positions of differences in the second PDF
file1 = "path/to/file1.pdf"
file2 = "path/to/file2.pdf"
highlight_differences(file1, file2)
