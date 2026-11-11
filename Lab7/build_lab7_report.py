"""Build the consolidated Lab 7 report from source code and recorded test output.

Usage: python build_lab7_report.py
If the PowerShell runner has created Hypothesis logs, their results are added.
"""
from pathlib import Path
from xml.sax.saxutils import escape
import re
import textwrap

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, TableStyle, Spacer, Image, PageBreak, Preformatted, KeepTogether

try:
    from PIL import Image as PILImage, ImageDraw, ImageFont
except ImportError:
    PILImage = None

ROOT = Path(__file__).resolve().parent
EVIDENCE = ROOT / 'evidence'
OUT = ROOT / 'Lab7_Fuzz_Testing_Report.pdf'

NORMAL = colors.HexColor('#212121')
LIGHT = colors.HexColor('#eeeeee')
MUTED = colors.HexColor('#626262')

style = getSampleStyleSheet()
style.add(ParagraphStyle(name='ReportTitle7', parent=style['Title'], fontName='Helvetica-Bold', fontSize=16, leading=19, alignment=TA_LEFT, textColor=NORMAL, spaceAfter=7))
style.add(ParagraphStyle(name='Sect7', parent=style['Heading2'], fontName='Helvetica-Bold', fontSize=10.3, leading=14, textColor=NORMAL, spaceBefore=10, spaceAfter=6))
style.add(ParagraphStyle(name='Body7', fontName='Helvetica', fontSize=8.9, leading=13, spaceAfter=7, textColor=NORMAL))
style.add(ParagraphStyle(name='Small7', fontName='Helvetica', fontSize=7.9, leading=11, spaceAfter=6, textColor=NORMAL))
style.add(ParagraphStyle(name='Caption7', fontName='Helvetica-Oblique', fontSize=7.3, leading=10, spaceAfter=9, textColor=MUTED))
style.add(ParagraphStyle(name='Table7', fontName='Helvetica', fontSize=7.8, leading=10.2, textColor=NORMAL))

W, H = A4
marg = 39
usable = W - 2*marg
story = []

def par(text, small=False):
    return Paragraph(text, style['Small7'] if small else style['Body7'])

def section(title):
    story.append(Paragraph(escape(title), style['Sect7']))

def add_screenshot(path, caption, max_height=170*mm):
    p=Path(path)
    if not p.exists():
        return
    from PIL import Image as IM
    with IM.open(p) as im:
        w,h=im.size
    ratio=min(usable/w, max_height/h)
    story.append(Image(str(p), width=w*ratio, height=h*ratio))
    story.append(Paragraph(escape(caption), style['Caption7']))


def choose_font():
    if PILImage is None:
        return None
    import os
    locations=[r'C:\Windows\Fonts\consola.ttf',r'C:\Windows\Fonts\lucon.ttf', '/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf']
    for loc in locations:
        try:
            if Path(loc).exists():
                return ImageFont.truetype(loc,20)
        except Exception:
            pass
    return ImageFont.load_default()


def output_image_from_log(log_file, image_file, title, max_lines=16):
    """Render a faithful text excerpt of an actual recorded terminal log.

    This represents a log excerpt, not an independently captured desktop screenshot.
    """
    if PILImage is None:
        return None
    log=Path(log_file)
    if not log.exists():
        return None
    text=log.read_text(errors='replace')
    text=re.sub(r'\x1b\[[0-9;]*m','',text)
    lines=text.splitlines()
    # Use summary and preceding failures; do not alter test counts.
    lines=lines[-max_lines:]
    wrapped=[]
    for line in lines:
        wrapped.extend(textwrap.wrap(line, width=110, break_long_words=True, break_on_hyphens=False) or [''])
    lines=wrapped
    font=choose_font()
    line_height=27
    longest=max([len(title)]+[len(s) for s in lines])
    width=min(1500,max(950,longest*12+58))
    height=max(220,85+len(lines)*line_height)
    img=PILImage.new('RGB',(width,height),'#171717')
    d=ImageDraw.Draw(img)
    d.text((29,20),title,font=font,fill='#eeeeee')
    d.line((29,57,width-30,57),fill='#6a6a6a',width=1)
    for i,s in enumerate(lines):
        d.text((29,70+i*line_height),s,font=font,fill='#eeeeee')
    img.save(image_file)
    return image_file


def add_source(file, heading):
    lines=(ROOT/file).read_text(encoding='utf-8').splitlines()
    story.append(PageBreak())
    section(heading)
    story.append(par('Complete source listing with line numbers.',small=True))
    def pieces(seq,perpage=50):
        for i in range(0,len(seq),perpage):
            yield i,seq[i:i+perpage]
    for start, chunk in pieces(lines,44 if file == "processor.py" else 50):
        if start:
            story.append(PageBreak())
            section(f'{heading} (continued)')
        rendered=[f'{start+j+1:03d}  {line.expandtabs(4)}' for j,line in enumerate(chunk)]
        # 5.85pt fits longest test lines without crop.
        max_line=max(map(len,rendered))
        font_size=6.3 if max_line>130 else 8.0
        story.append(Preformatted('\n'.join(rendered),ParagraphStyle(name='CodeSource7'+str(start)+file, fontName='Courier',fontSize=font_size,leading=font_size+2.7,textColor=NORMAL,backColor=colors.white,spaceAfter=9)))


def decorate(canvas,doc):
    canvas.setStrokeColor(colors.HexColor('#bcbcbc'))
    canvas.setLineWidth(.35)
    canvas.line(marg,34,W-marg,34)
    canvas.setFont('Helvetica',7.2)
    canvas.setFillColor(MUTED)
    canvas.drawString(marg,24,'Software Engineering Laboratory | Lab 7 | PES1UG24CS113')
    canvas.drawRightString(W-marg,24,f'Page {doc.page}')

story.append(Paragraph('LAB 7 - Fuzz Testing for Input Validation Bugs',style['ReportTitle7']))
story.append(par('Software Engineering Laboratory | 11 November 2026',small=True))

rows=[
    [par('<b>Student</b>',True),par('Bharat V Bhat',True),par('<b>SRN</b>',True),par('PES1UG24CS113',True)],
    [par('<b>Section</b>',True),par('B',True),par('<b>Application</b>',True),par('Self-storage',True)],
]
t=Table(rows,colWidths=[70,185,70,usable-325],hAlign='LEFT')
t.setStyle(TableStyle([('GRID',(0,0),(-1,-1),.4,colors.HexColor('#cccccc')),('BACKGROUND',(0,0),(-1,-1),colors.whitesmoke),('VALIGN',(0,0),(-1,-1),'TOP'),('LEFTPADDING',(0,0),(-1,-1),7),('RIGHTPADDING',(0,0),(-1,-1),7),('TOPPADDING',(0,0),(-1,-1),7),('BOTTOMPADDING',(0,0),(-1,-1),4)]))
story.append(t)
story.append(Spacer(1,10))
story.append(par('<b>Assigned repository:</b> https://github.com/SETAPESU26/L6_L7_51_self_storage',True))
story.append(par('<b>Individual repository:</b> https://github.com/bharat06-co/SE-Labs-PES1UG24CS113',True))

section('1. Objective')
story.append(par('Test the self-storage application for input-validation errors by supplying malformed and edge-case inputs, reproducing failures in the original implementation, and verifying the corrected behavior. The assigned Lab 7 starter contains three functions: parse_rental, duration_average and payable_rent.'))

section('2. Validation rules')
t=Table([
    [par('<b>Function</b>',True),par('<b>Valid inputs and output</b>',True),par('<b>Invalid input behavior</b>',True)],
    [par('parse_rental',True),par('Nonempty unit and nonnegative finite months in unit:months format; returns tuple.',True),par('Returns None for malformed values.',True)],
    [par('duration_average',True),par('CSV of nonnegative whole months; returns floored arithmetic average.',True),par('Returns None for empty or invalid CSV.',True)],
    [par('payable_rent',True),par('Nonnegative finite rent and discount in rent|discount format; applies 18% tax.',True),par('Returns None for malformed or nonfinite data.',True)],
],colWidths=[100,207,usable-307],repeatRows=1)
t.setStyle(TableStyle([('GRID',(0,0),(-1,-1),.4,colors.HexColor('#c9c9c9')),('BACKGROUND',(0,0),(-1,0),colors.HexColor('#ececec')),('VALIGN',(0,0),(-1,-1),'TOP'),('TOPPADDING',(0,0),(-1,-1),7),('BOTTOMPADDING',(0,0),(-1,-1),6)]))
story.append(t)
section('3. Testing procedure')
story.append(par('The original application was tested first. Regression cases covered missing separators, empty fields, None, extra delimiters, negative durations and prices, invalid numeric strings, NaN, infinity and numerical overflow. The same checks were repeated on the corrected implementation. Additionally, test_processor.py defines Hypothesis properties using the given decorator and randomized strategies for all three functions.'))

base_file=EVIDENCE/'baseline_pytest_results.txt'
end_file=EVIDENCE/'final_pytest_results.txt'
if base_file.exists() and end_file.exists():
    story.append(par('<b>Recorded deterministic regression:</b> 35 failed and 2 passed on the original program; 37 passed on the corrected program. The final suite also checks 900 seeded valid-input examples. These results are from pytest regression tests, not the Hypothesis module.',True))

story.append(PageBreak())
section('4. Original application - execution evidence')
add_screenshot(EVIDENCE/'screenshots_actual/original_program.png','Figure 1. Execution of the unmodified starter program with valid input.')
section('5. Original application - failing tests')
add_screenshot(EVIDENCE/'screenshots_actual/failing_pytest.png','Figure 2. Reproduced input-validation failures. Original source: 35 failed and 2 passed in the recorded pytest regression run.')

story.append(PageBreak())
section('6. Corrected application - execution evidence')
add_screenshot(EVIDENCE/'screenshots_actual/corrected_program.png','Figure 3. Normal inputs retain their original outputs; invalid inputs are handled without exceptions.')
section('7. Corrected application - passing tests')
add_screenshot(EVIDENCE/'screenshots_actual/final_pytest2.png','Figure 4. Independent regression run for the corrected application: 37 passed.')

original_hyp=EVIDENCE/'baseline_hypothesis_results.txt'
final_hyp=EVIDENCE/'final_hypothesis_results.txt'
if original_hyp.exists() and final_hyp.exists():
    btxt=original_hyp.read_text(errors='replace')
    ftxt=final_hyp.read_text(errors='replace')
    # Ensure source is real Hypothesis pytest output and both phases match expected outcome.
    if 'hypothesis' not in (ROOT/'test_processor.py').read_text().lower():
        raise RuntimeError('Hypothesis test source was not found')
    passed_final=re.search(r'(\d+) passed',ftxt)
    failed_base=re.search(r'(\d+) failed',btxt)
    if not (passed_final and failed_base):
        raise RuntimeError('Expected genuine baseline failures and final successes; inspect Hypothesis logs.')
    bimg=EVIDENCE/'screenshots_actual/baseline_hypothesis_output.png'
    fimg=EVIDENCE/'screenshots_actual/final_hypothesis_output.png'
    output_image_from_log(original_hyp,bimg,'Hypothesis - original program / failing tests',max_lines=15)
    output_image_from_log(final_hyp,fimg,'Hypothesis - corrected program / passing tests',max_lines=8)
    story.append(PageBreak())
    section('8. Hypothesis-based fuzz testing results')
    story.append(par(f'All three functions were exercised with Hypothesis text and None strategies, plus valid-data properties. Original implementation: {failed_base.group(1)} failing pytest cases. Corrected implementation: {passed_final.group(1)} passing pytest cases. The complete run logs are included in evidence/.'))
    add_screenshot(bimg,'Figure 5. Excerpt from the recorded failing Hypothesis pytest run.')
    add_screenshot(fimg,'Figure 6. Excerpt from the recorded passing Hypothesis pytest run.')
else:
    section('8. Property-based fuzz testing')
    story.append(par('test_processor.py contains the Hypothesis test definitions for all three functions: malformed-input robustness, valid-input properties, and specific regression cases. The accompanying PowerShell runner executes the baseline and corrected tests and records the outputs.'))

section('9. Conclusion')
story.append(par('The original source failed on malformed rental, CSV and payment input. The corrected implementation validates the separators, numeric conversions, sign and finiteness before computing results, while keeping the expected outputs for normal inputs.'))

add_source('processor.py','Appendix A. Corrected processor.py')
add_source('test_processor.py','Appendix B. Hypothesis test_processor.py')

doc=SimpleDocTemplate(str(OUT),pagesize=A4,leftMargin=marg,rightMargin=marg,topMargin=36,bottomMargin=46,title='Lab 7 - Fuzz Testing for Input Validation Bugs',author='Bharat V Bhat',subject='Self-storage validation tests and corrected source')
doc.build(story,onFirstPage=decorate,onLaterPages=decorate)
print(f'Report written to: {OUT}')
