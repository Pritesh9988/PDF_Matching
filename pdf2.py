import PyPDF2
import difflib
from reportlab.pdfgen import canvas
from reportlab.lib.colors import yellow

def compare_pdf(file1, file2, output_file):
    pdf1 = PyPDF2.PdfFileReader(open(file1, 'rb'))
    pdf2 = PyPDF2.PdfFileReader(open(file2, 'rb'))

    page1 = pdf1.getPage(0)
    page2 = pdf2.getPage(0)

    text1 = page1.extractText()
    text2 = page2.extractText()

    diff = difflib.ndiff(text1.split(), text2.split())
    changes = [line for line in diff if line.startswith('+') or line.startswith('-')]

    if len(changes) > 0:
        c = canvas.Canvas(output_file, pagesize=page1.mediaBox)
        c.setFillColor(yellow)

        for change in changes:
            if change.startswith('+'):
                c.setFillColor('green')
            elif change.startswith('-'):
                c.setFillColor('red')

            line = change[2:]
            c.drawString(10, 10, line)  # Draw the changed line at the top-left corner

        c.save()
    else:
        # If there are no changes, simply copy the page from the first PDF to the output PDF
        output = PyPDF2.PdfFileWriter()
        output.addPage(page1)
        with open(output_file, 'wb') as f:
            output.write(f)

# Usage
file1 = 'file1.pdf'
file2 = 'file2.pdf'
output_file = 'output.pdf'

compare_pdf(file1, file2, output_file)
