import PyPDF2
from reportlab.pdfgen import canvas
from reportlab.lib.colors import yellow

def compare_pdf(file1, file2, output_file):
    pdf1 = PyPDF2.PdfReader(open(file1, 'rb'))
    pdf2 = PyPDF2.PdfReader(open(file2, 'rb'))

    output = PyPDF2.PdfWriter()

    if len(pdf1.pages) != len(pdf2.pages):
        print("The number of pages in the PDFs is different.")
        return

    for page_num in range(len(pdf1.pages)):
        page1 = pdf1.pages[page_num]
        page2 = pdf2.pages[page_num]

        if page1.extract_text() != page2.extract_text():
            c = canvas.Canvas(output_file, pagesize=page1.mediabox)
            c.setFillColor(yellow)

            text1 = page1.extract_text().splitlines()
            text2 = page2.extract_text().splitlines()

            for index, (line1, line2) in enumerate(zip(text1, text2)):
                if line1 != line2:
                    y = page1.mediabox[3] - (index * 12)  # Assuming a font size of 12
                    c.rect(0, y, page1.mediabox[2], y - 12, fill=True, stroke=False)
                    c.drawString(10, y - 10, line2)  # Highlight the modified line

            c.save()
            output.addPage(page2)
        else:
            output.addPage(page1)

    with open(output_file, 'wb') as f:
        output.write(f)

# Usage
file1 = 'file1.pdf'
file2 = 'file2.pdf'
output_file = 'output.pdf'

compare_pdf(file1, file2, output_file)
