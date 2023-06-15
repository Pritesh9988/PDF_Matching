import PyPDF2
import difflib
from reportlab.pdfgen import canvas
from reportlab.lib.colors import yellow

def compare_pdf(file1, file2, output_file):
    pdf1 = PyPDF2.PdfReader(open(file1, 'rb'))
    pdf2 = PyPDF2.PdfReader(open(file2, 'rb'))

    output = PyPDF2.PdfWriter()

    num_pages = min(len(pdf1.pages), len(pdf2.pages))

    for page_num in range(num_pages):
        page1 = pdf1.pages[page_num]
        page2 = pdf1.pages[page_num]

        c = canvas.Canvas('temp.pdf', pagesize=page2.mediabox)

        text1 = page1.extract_text()
        text2 = page2.extract_text()

        diff = difflib.ndiff(text1.split(), text2.split())
        changes = [line for line in diff if line.startswith('+') or line.startswith('-')]
        
        print(changes)

        if len(changes) > 0:
            c.setFillColor(yellow)

            lines1 = text1.splitlines()
            lines2 = text2.splitlines()

            for line_num, (line1, line2) in enumerate(zip(lines1, lines2)):
                diff = difflib.ndiff(line1.split(), line2.split())
                changes = [change for change in diff if change.startswith('+') or change.startswith('-')]
                if len(changes) > 0:
                    y = page2.mediabox[3] - (line_num * 12)  # Assuming a font size of 12
                    c.rect(0, y, page2.mediabox[2], y - 12, fill=True, stroke=False)
                    c.drawString(10, y - 10, line2)  # Highlight the modified line

        c.showPage()
        c.save()

        temp_pdf = PyPDF2.PdfFileReader(open("temp.pdf", 'rb'))
        output.addPage(temp_pdf.getPage(0))

    with open(output_file, 'wb') as f:
        output.write(f)

# Usage
file1 = 'file1.pdf'
file2 = 'file2.pdf'
output_file = 'output.pdf'

compare_pdf(file1, file2, output_file)
