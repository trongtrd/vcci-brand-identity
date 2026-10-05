"""VCCI table styles for the Word templates.

Injected into word/styles.xml (and VCCI Table set as the document's default table style in word/settings.xml):
  VCCI Table        data tables: blue header row, hairline rows, Ivory total row, blue rule below
  VCCI Table Light  simple lists: bronze uppercase header label, hairline rows, no fills
  VCCI Table Tint   highlight boxes (key figures, notes): Blue Tint cells separated by white gutters
"""
import re

BLUE, GOLD, BRONZE_INK, TINT, STONE, IVORY, PAPER, INK, SLATE = '264896', 'FFCD00', '9C570C', 'E7ECF6', 'E6E1D5', 'F4F0E6', 'FBF9F4', '161A26', '5C6478'
SANS, SANS_SEMI = 'Be Vietnam Pro', 'Be Vietnam Pro SemiBold'

def fonts(name): return f'<w:rFonts w:ascii="{name}" w:hAnsi="{name}" w:cs="{name}" w:eastAsia="{name}"/>'
def border(side, val='single', sz=4, color=STONE): return f'<w:{side} w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>' if val != 'nil' else f'<w:{side} w:val="nil"/>'
def cell_mar(t, l, b, r): return (f'<w:tblCellMar><w:top w:w="{t}" w:type="dxa"/><w:left w:w="{l}" w:type="dxa"/>'
                                  f'<w:bottom w:w="{b}" w:type="dxa"/><w:right w:w="{r}" w:type="dxa"/></w:tblCellMar>')
def shd(fill): return f'<w:shd w:val="clear" w:color="auto" w:fill="{fill}"/>'

def style(sid, name, ppr, rpr, tblpr, tcpr, conds, ui):
    return (f'<w:style w:type="table" w:customStyle="1" w:styleId="{sid}"><w:name w:val="{name}"/><w:basedOn w:val="TableNormal"/>'
            f'<w:uiPriority w:val="{ui}"/><w:qFormat/><w:pPr>{ppr}</w:pPr><w:rPr>{rpr}</w:rPr><w:tblPr>{tblpr}</w:tblPr>'
            f'<w:tcPr>{tcpr}</w:tcPr>{conds}</w:style>')

def cond(kind, ppr='', rpr='', tcpr=''):
    return (f'<w:tblStylePr w:type="{kind}">' + (f'<w:pPr>{ppr}</w:pPr>' if ppr else '') + (f'<w:rPr>{rpr}</w:rPr>' if rpr else '')
            + '<w:tblPr/>' + (f'<w:tcPr>{tcpr}</w:tcPr>' if tcpr else '') + '</w:tblStylePr>')

PPR = '<w:spacing w:before="0" w:after="0" w:line="264" w:lineRule="auto"/>'
RPR = fonts(SANS) + f'<w:color w:val="{INK}"/><w:sz w:val="19"/><w:szCs w:val="19"/>'

VCCI_TABLE = style('VCCITable', 'VCCI Table', PPR, RPR,
    '<w:tblStyleRowBandSize w:val="1"/><w:tblStyleColBandSize w:val="1"/><w:tblBorders>'
    + border('top', 'nil') + border('left', 'nil') + border('bottom', sz=8, color=BLUE) + border('right', 'nil')
    + border('insideH', sz=4, color=STONE) + border('insideV', 'nil') + '</w:tblBorders>' + cell_mar(96, 142, 96, 142),
    '<w:vAlign w:val="center"/>',
    cond('firstRow', rpr=fonts(SANS_SEMI) + '<w:color w:val="FFFFFF"/><w:sz w:val="17"/><w:szCs w:val="17"/>',
         tcpr=f'<w:tcBorders>{border("top", sz=4, color=BLUE)}{border("bottom", sz=4, color=BLUE)}</w:tcBorders>' + shd(BLUE))
    + cond('lastRow', rpr=fonts(SANS_SEMI),
           tcpr=f'<w:tcBorders>{border("top", sz=8, color=BLUE)}</w:tcBorders>' + shd(IVORY))
    + cond('firstCol', rpr=fonts(SANS_SEMI))
    + cond('band2Horz', tcpr=shd(PAPER)), 40)

VCCI_TABLE_LIGHT = style('VCCITableLight', 'VCCI Table Light', PPR, RPR,
    '<w:tblStyleRowBandSize w:val="1"/><w:tblStyleColBandSize w:val="1"/><w:tblBorders>'
    + border('top', 'nil') + border('left', 'nil') + border('bottom', sz=4, color=STONE) + border('right', 'nil')
    + border('insideH', sz=4, color=STONE) + border('insideV', 'nil') + '</w:tblBorders>' + cell_mar(80, 0, 80, 170),
    '<w:vAlign w:val="top"/>',
    cond('firstRow', rpr=fonts(SANS_SEMI) + f'<w:caps/><w:color w:val="{BRONZE_INK}"/><w:spacing w:val="24"/><w:sz w:val="15"/><w:szCs w:val="15"/>',
         tcpr=f'<w:tcBorders>{border("bottom", sz=8, color=BLUE)}</w:tcBorders>')
    + cond('firstCol', rpr=fonts(SANS_SEMI) + f'<w:color w:val="{BLUE}"/>'), 41)

VCCI_TABLE_TINT = style('VCCITableTint', 'VCCI Table Tint', PPR, RPR,
    '<w:tblStyleRowBandSize w:val="1"/><w:tblStyleColBandSize w:val="1"/><w:tblBorders>'
    + border('top', 'nil') + border('left', 'nil') + border('bottom', 'nil') + border('right', 'nil')
    + border('insideH', sz=24, color='FFFFFF') + border('insideV', sz=24, color='FFFFFF') + '</w:tblBorders>' + cell_mar(170, 170, 170, 170),
    shd(TINT) + '<w:vAlign w:val="top"/>',
    cond('firstRow', rpr=f'<w:color w:val="{BLUE}"/>'), 42)

STYLES = [('VCCITable', VCCI_TABLE), ('VCCITableLight', VCCI_TABLE_LIGHT), ('VCCITableTint', VCCI_TABLE_TINT)]

def strip_direct_borders(doc_xml):
    """docx-js writes explicit table borders on every table; on VCCI-styled tables they would override the style."""
    def fix(m):
        pr = m.group(0)
        return re.sub(r'<w:tblBorders>.*?</w:tblBorders>', '', pr, flags=re.S) if 'w:tblStyle w:val="VCCITable' in pr else pr
    return re.sub(r'<w:tblPr>.*?</w:tblPr>', fix, doc_xml, flags=re.S)

def inject(files):
    """files: dict of part name -> bytes (modified in place)."""
    files['word/document.xml'] = strip_direct_borders(files['word/document.xml'].decode('utf-8')).encode('utf-8')
    st = files['word/styles.xml'].decode('utf-8')
    for sid, xml in STYLES:
        st = re.sub(r'<w:style w:type="table"[^>]*w:styleId="' + sid + r'".*?</w:style>', '', st, flags=re.S)
    st = st.replace('</w:styles>', ''.join(x for _, x in STYLES) + '</w:styles>')
    files['word/styles.xml'] = st.encode('utf-8')

    se = files['word/settings.xml'].decode('utf-8')
    se = re.sub(r'<w:defaultTableStyle[^>]*/>', '', se)
    tag = '<w:defaultTableStyle w:val="VCCITable"/>'
    # CT_Settings order: defaultTableStyle precedes evenAndOddHeaders and every element after it
    later = ['evenAndOddHeaders', 'bookFold', 'drawingGrid', 'displayHorizontalDrawingGridEvery', 'displayVerticalDrawingGridEvery',
             'doNotUseMarginsForDrawingGridOrigin', 'doNotShadeFormData', 'noPunctuationKerning', 'characterSpacingControl',
             'printTwoOnOne', 'strictFirstAndLastChars', 'noLineBreaks', 'savePreviewPicture', 'doNotValidateAgainstSchema',
             'saveInvalidXml', 'ignoreMixedContent', 'alwaysShowPlaceholderText', 'doNotDemarcateInvalidXml', 'saveXmlDataOnly',
             'useXSLTWhenSaving', 'saveThroughXslt', 'showXMLTags', 'alwaysMergeEmptyNamespace', 'updateFields', 'hdrShapeDefaults',
             'footnotePr', 'endnotePr', 'compat', 'docVars', 'rsids']
    hits = [i for i in (se.find('<w:' + n) for n in later) if i >= 0]
    pos = min(hits) if hits else se.rindex('</w:settings>')
    se = se[:pos] + tag + se[pos:]
    files['word/settings.xml'] = se.encode('utf-8')
