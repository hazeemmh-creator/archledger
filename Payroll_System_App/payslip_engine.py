import os
import re
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT

# --- PAGE BORDER FUNCTION ---
def draw_page_border(canvas, doc):
    canvas.saveState()
    canvas.setStrokeColor(colors.black)
    canvas.setLineWidth(1.5) 
    canvas.rect(15, 15, A4[0] - 30, A4[1] - 30)
    canvas.restoreState()

def generate_live_payslip(staff_data=None, month_name="FEBRUARY", year="2026"):
    if staff_data is None: staff_data = {}
    
    # --- FOLDER ORGANIZATION UPGRADE ---
    base_dir = "output"
    staff_name = str(staff_data.get("STAFF NAME", "Preview_Staff"))
    
    # THE PDF CRASH SHIELD: Strips out \ / : * ? " < > | completely
    safe_name = re.sub(r'[\\/*?:"<>|]', "", staff_name).strip().replace(" ", "_")
    
    staff_folder = os.path.join(base_dir, safe_name)
    if not os.path.exists(staff_folder): 
        os.makedirs(staff_folder)
        
    # --- THE MISSING LINK FIX ---
    # We must define the exact file name and path before creating the document
    pdf_filename = f"{safe_name}_{month_name}_{year}.pdf"
    pdf_file = os.path.join(staff_folder, pdf_filename)
    
    doc = SimpleDocTemplate(pdf_file, pagesize=A4, rightMargin=40, leftMargin=40, topMargin=25, bottomMargin=25)
    elements = []

    INSTITUTION_BLUE = colors.HexColor("#000080") 
    INSTITUTION_RED = colors.HexColor("#FF0000")  
    HEADER_BG_BLUE = colors.HexColor("#DDEBF7")   
    TEXT_COLOR = colors.black                     
    GRID_COLOR = colors.black                     

    styles = getSampleStyleSheet()
    
    title_style = ParagraphStyle(name="TitleStyle", fontName="Helvetica-Bold", fontSize=12, alignment=TA_CENTER, textColor=INSTITUTION_BLUE)
    sub_title_style = ParagraphStyle(name="SubTitle", fontName="Helvetica-Bold", fontSize=11, alignment=TA_CENTER, textColor=INSTITUTION_RED)
    period_style = ParagraphStyle(name="Period", fontName="Helvetica-Bold", fontSize=11, alignment=TA_CENTER, textColor=TEXT_COLOR)
    sign_title_style = ParagraphStyle(name="SignTitle", fontName="Helvetica-Bold", fontSize=10, alignment=TA_LEFT, textColor=TEXT_COLOR)
    sign_sub_style = ParagraphStyle(name="SignSub", fontName="Helvetica-Bold", fontSize=10, alignment=TA_LEFT, textColor=TEXT_COLOR)

    # --- LOGO ---
    logo_path = "logo.png" if os.path.exists("logo.png") else "logo.jpg"
    if os.path.exists(logo_path):
        logo_img = Image(logo_path, width=55, height=55) 
        logo_img.hAlign = 'CENTER'
        elements.append(logo_img)
    else:
        elements.append(Paragraph("<font color='black'><b>[ INSTITUTIONAL LOGO ]</b></font>", ParagraphStyle(name="L", alignment=TA_CENTER, fontName="Helvetica")))

    elements.append(Spacer(1, 3))
    
    # --- THE PERFECTLY STACKED HEADER ---
    elements.append(Paragraph("NATIONAL INSTITUTE FOR LEGISLATIVE AND DEMOCRATIC STUDIES (NILDS)", title_style))
    elements.append(Spacer(1, 1)) 
    elements.append(Paragraph("NATIONAL ASSEMBLY", sub_title_style))
    
    elements.append(Spacer(1, 5)) 
    elements.append(Paragraph(f"PAY-SLIP FOR THE MONTH OF: {str(month_name).title()} {year}", period_style))
    elements.append(Spacer(1, 10))

    def get_text(col_name): return str(staff_data.get(col_name, ""))
    def get_money(col_name):
        val = staff_data.get(col_name, "")
        if val == "" or val == 0 or val == "0" or val is None or str(val).lower() == 'nan': return ""
        try: return f"{float(val):,.2f}"
        except: return "0.00"

    # --- STAFF INFO ---
    acct_string = f"{get_text('BANK')} {get_text('ACCT NO')}".strip()
    info_data = [
        ["NAME", "JOB TITLE", "GRADE LEVEL"],
        [get_text("STAFF NAME"), get_text("DESIGNATION"), get_text("GRADE LEVEL")],
        ["FIRS TIN NO.", "PFA NO.", "BANK / ACCT NO."],
        [get_text("TIN"), get_text("PFA"), acct_string if acct_string else ""]
    ]
    info_table = Table(info_data, colWidths=[225, 180, 110])
    info_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), HEADER_BG_BLUE), 
        ('BACKGROUND', (0,2), (-1,2), HEADER_BG_BLUE), 
        ('FONTNAME', (0,0), (-1,-1), 'Helvetica-Bold'), 
        ('FONTSIZE', (0,0), (-1,-1), 9), 
        ('TEXTCOLOR', (0,0), (-1,-1), TEXT_COLOR),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('GRID', (0,0), (-1,-1), 0.75, GRID_COLOR),    
        ('TOPPADDING', (0,0), (-1,-1), 2), 
        ('BOTTOMPADDING', (0,0), (-1,-1), 2), 
    ]))
    elements.append(info_table)
    elements.append(Spacer(1, 10)) 

    # --- FINANCIALS: ENGINE ALIGNMENT ---
    fin_data = [
        ["DETAILS", "(N)", "(N)"],
        ["GROSS INCOME (Monthly)", get_money("GROSS SALARY"), ""],
        ["ALLOWANCES:", "", ""],
        ["BASIC SALARY", get_money("BASIC SALARY"), ""],
        ["28 DAYS IN LIEU OF ACCOM. ARREARS", get_money("28 DAYS IN LIEU OF ACCOM. ARREARS"), ""],
        ["RENT ALLOWANCE", get_money("RENT ALLOWANCE"), ""],
        ["UTILITY ALLOWANCE", get_money("UTILITY ALLOWANCE"), ""],
        ["DOMESTIC ALLOWANCE", get_money("DOMESTIC ALLOWANCE"), ""],
        ["ENTERTAINMENT ALLOWANCE", get_money("ENTERTAINMENT ALLOWANCE"), ""],
        ["FURNITURE ALLOWANCE", get_money("FURNITURE ALLOWANCE"), ""],
        ["MOTOR/FUEL ALLOWANCE", get_money("MOTOR/FUEL ALLOWANCE"), ""],
        ["RESEARCH ALLOWANCE", get_money("RESEARCH ALLOWANCE"), ""],
        ["HARDSHIP ALLOWANCE", get_money("HARDSHIP ALLOWANCE"), ""],
        ["LEAVE ALLOWANCE", get_money("LEAVE ALLOWANCE"), ""],
        ["OUTFIT ALLOWANCE", get_money("OUTFIT ALLOWANCE"), ""],
        ["LEGISLATIVE DUTY ALLOWANCE", get_money("LEGISLATIVE DUTY ALLOWANCE"), ""],
        ["SALARY ARREARS", get_money("SALARY ARREARS"), ""],
        ["", "", ""], 
        ["DEDUCTIONS:", "", ""], 
        ["EMPLOYEE PENSIONS", "", get_money("EMPLOYEE PENSIONS")],
        ["NHF", "", get_money("NHF DED.")],
        ["PAYE", "", get_money("PAYE")],
        ["COOPERATIVE 1", "", get_money("COOP 1 CONTR/SPEC SAVINGS")],
        ["COOP 1 LOAN RECOVERY", "", get_money("COOP 1 LOAN RECOVERY")],
        ["COOPERATIVE 2", "", get_money("COOP 2 CONTR/SPEC SAVINGS")],
        ["COOP 2 LOAN RECOVERY", "", get_money("COOP 2 LOAN RECOVERY")], 
        ["AUCTION", "", get_money("AUCTION")],
        ["", "", ""], 
        ["TOTAL DEDUCTIONS", "", get_money("TOTAL DEDUCTION")],
        ["", "", ""], 
        ["NET PAY", get_money("NET PAY"), ""],
    ]
    deductions_row_idx = 0
    for i, row in enumerate(fin_data):
        if row[0] == "DEDUCTIONS:":
            deductions_row_idx = i
            break

    fin_table = Table(fin_data, colWidths=[275, 120, 120])
    fin_table.setStyle(TableStyle([
        ('FONTNAME', (0,0), (-1,-1), 'Helvetica'),
        ('FONTSIZE', (0,0), (-1,-1), 9), 
        ('TEXTCOLOR', (0,0), (-1,-1), TEXT_COLOR),
        ('GRID', (0,0), (-1,-1), 0.75, GRID_COLOR), 
        ('BACKGROUND', (0,0), (-1,0), HEADER_BG_BLUE),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('FONTSIZE', (0,0), (-1,0), 10), 
        ('ALIGN', (0,0), (0,0), 'LEFT'),
        ('ALIGN', (1,0), (2,0), 'CENTER'),
        ('FONTNAME', (0,2), (0,2), 'Helvetica-Bold'),
        ('FONTNAME', (0,deductions_row_idx), (0,deductions_row_idx), 'Helvetica-Bold'),
        ('BACKGROUND', (0,deductions_row_idx), (-1,deductions_row_idx), HEADER_BG_BLUE), 
        ('FONTNAME', (0,1), (-1,1), 'Helvetica-Bold'),   
        ('FONTNAME', (0,-3), (-1,-3), 'Helvetica-Bold'), 
        ('FONTNAME', (0,-1), (-1,-1), 'Helvetica-Bold'), 
        ('ALIGN', (1,1), (2,-1), 'RIGHT'),
        ('TOPPADDING', (0,0), (-1,-1), 2), 
        ('BOTTOMPADDING', (0,0), (-1,-1), 2), 
    ]))
    elements.append(fin_table)
    
    # --- SIGNATURE AREA ---
    elements.append(Spacer(1, 35)) 
    
    elements.append(Paragraph("SIGNED: DIRECTOR", sign_title_style))
    elements.append(Spacer(1, 2))
    elements.append(Paragraph("FINANCE & ACCOUNTS", sign_sub_style))
    
    doc.build(elements, onFirstPage=draw_page_border, onLaterPages=draw_page_border)
    
    return os.path.abspath(pdf_file)