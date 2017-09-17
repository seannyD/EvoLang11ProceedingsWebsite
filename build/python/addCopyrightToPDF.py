from pyPdf import PdfFileWriter, PdfFileReader
from pyPdf.generic import NameObject, createStringObject
import StringIO
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter



def addCopyrightToPDF(pdf_file_location, pdf_file_destination,copyrightText, drawText=True, title="",authors=""):
    packet = StringIO.StringIO()
    # create a new PDF with Reportlab
    can = canvas.Canvas(packet, pagesize=letter)
    can.setFont("Times-Roman",7)
    ctext = copyrightText.split("\n")
    if drawText:
        can.drawString(30, 40, ctext[0])
        can.drawString(30, 50, ctext[1])
    else:
        can.drawString(30, 50, "")
    can.save()

    #move to the beginning of the StringIO buffer
    packet.seek(0)
    new_pdf = PdfFileReader(packet)
    # read your existing PDF
    existing_pdf = PdfFileReader(file(pdf_file_location, "rb"))
    output = PdfFileWriter()
    npagesorig = existing_pdf.getNumPages()
    #print npagesorig
    for i in range(npagesorig):
        page = existing_pdf.getPage(i)
        # if last page
        if i == (npagesorig-1):
            #print "HERE",copyrightText,drawText
            page.mergePage(new_pdf.getPage(0))
        output.addPage(page)

    infoDict = output._info.getObject()
    infoDict.update({
        NameObject('/Title'): createStringObject(title),
        NameObject('/Author'): createStringObject(authors)
    })

    # finally, write "output" to a real file
    outputStream = file(pdf_file_destination, "wb")
    output.write(outputStream)
    outputStream.close()
