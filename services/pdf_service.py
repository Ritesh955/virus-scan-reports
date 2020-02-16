from fpdf import FPDF


def create_report_pdf(report,report_file_path):
    pdf = FPDF()
    pdf.add_page()
    page_width = pdf.w - 2 * pdf.l_margin

    pdf.set_font('Times','B',1) 
    pdf.cell(page_width, 0.0, 'Virus Scan Report', align='C')
    pdf.ln(10)

    pdf.set_font('Courier', '', 8)
    col_width = page_width/4
    pdf.ln(1)
    th = pdf.font_size

    col_width1 = pdf.get_string_width(str(report[0]['hash_value']))+2*pdf.c_margin
    col_width2 = pdf.get_string_width(report[0]['detection_name'])+6*pdf.c_margin
    col_width3 = pdf.get_string_width('Number of Engines')+2*pdf.c_margin
    col_width4 = pdf.get_string_width(str(report[0]['scan_date']))+2*pdf.c_margin

    pdf.cell(col_width1, th, 'Resource', border=1)
    pdf.cell(col_width2, th, 'Detection Name', border=1)
    pdf.cell(col_width3, th, 'Number of Engines', border=1)
    pdf.cell(col_width4, th, 'Scan Date', border=1)
    pdf.ln(th)  

    for row in report:
        if row  and len(row.values()) > 4:
            pdf.cell(col_width1, th, str(row['hash_value']), border=1)
            pdf.cell(col_width2, th, str(row['detection_name']), border=1)
            pdf.cell(col_width3, th, str(row['number_of_engines']), border=1)
            pdf.cell(col_width4, th, str(row['scan_date']), border=1)
            pdf.ln(th)
    pdf.ln(10)

    pdf.set_font('Times','',10.0) 
    pdf.cell(page_width, 0.0, '- end of report -', align='C')
    
    return pdf.output(report_file_path).encode('latin-1')