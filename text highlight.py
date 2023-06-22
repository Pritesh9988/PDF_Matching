import PyPDF2
import aspose.words as aw
from datetime import date

def split_pdf_into_pages(input_path,input_path2):
    # Open the PDF file
    pdf = PyPDF2.PdfReader(input_path)
    pdf2 = PyPDF2.PdfReader(input_path2)

    # Iterate through each page
    for page_num in range(len(pdf.pages)):
        # Create a new PDF writer
        pdf_writer = PyPDF2.PdfWriter()
        pdf_writer2 = PyPDF2.PdfWriter()
        # Add the current page to the writer
        pdf_writer.add_page(pdf.pages[page_num])
        pdf_writer2.add_page(pdf2.pages[page_num])
        # Create the output file path
        output_path = f"page_{page_num+1}.pdf"
        output_path2 = f"page2_{page_num+1}.pdf"
        # Write the output file
        with open(output_path, "wb") as output_file:
            pdf_writer.write(output_file)
            
        with open(output_path2, "wb") as output_file2:
            pdf_writer.write(output_file2)

        print(f"Page {page_num+1} saved as {output_path}")
        print(f"Page {page_num+1} saved as {output_path2}")
        
        


# Load PDF files
        PDF1 = aw.Document(output_path)
        PDF2 = aw.Document(output_path2)

        # Convert PDF files to Word format
        PDF1.save("first.docx", aw.SaveFormat.DOCX)
        PDF2.save("second.docx", aw.SaveFormat.DOCX)

        # Load converted Word documents 
        DOC1 = aw.Document("first.docx")
        DOC2 = aw.Document("second.docx")

# Set comparison options
        options = aw.comparing.CompareOptions()            


        # DOC1 will contain changes as revisions after comparison
        DOC1.compare(DOC2, "user", date.today(), options)

        if (DOC1.revisions.count >= 0):
            # Save resultant file as PDF
            DOC1.save(f"compare_op_{page_num+1}.pdf", aw.SaveFormat.PDF)
        else:
            print("Documents are equal")
        
        
        
        
# Provide the input PDF file path
input_file = "file1.pdf"
input_file2 = "file2.pdf"
# Split the PDF into separate pages
split_pdf_into_pages(input_file,input_file2)