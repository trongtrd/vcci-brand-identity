--[[ VCCI block styles shared by every format.

  ::: lead        two or three sentences carrying the main message   (Typst: vcci-lead,    Word: "VCCI Lead")
  ::: highlight   box with a blue left rule; optional title="…"      (Typst: vcci-callout, Word: "VCCI Callout")
  ::: label       small uppercase label above a heading              (Typst: vcci-label,   Word: "VCCI Label")
  ::: figures     key figures, one per line: "67,4 | Điểm PCI trung vị"
                  (Typst: vcci-figures cards, Word: number in "VCCI Figure Number", label in "VCCI Small")

  Metadata: `cover: false` / `back-cover: false` become flags the Typst template can read (Pandoc templates cannot
  tell false from unset).
]]

local STYLES = {
  lead = { typst = 'vcci-lead', docx = 'VCCI Lead' },
  highlight = { typst = 'vcci-callout', docx = 'VCCI Callout' },
  label = { typst = 'vcci-label', docx = 'VCCI Label' },
}

local function typst_string(s)
  return '"' .. s:gsub('\\', '\\\\'):gsub('"', '\\"') .. '"'
end

-- "67,4 | Điểm PCI trung vị" lines from the paragraphs (or list items) of a ::: figures block
local function figure_items(el)
  local lines = {}
  local function add_inlines(inlines)   -- consecutive lines form one paragraph: split it at the line breaks
    local cur = {}
    for _, il in ipairs(inlines) do
      if il.t == 'SoftBreak' or il.t == 'LineBreak' then
        table.insert(lines, pandoc.utils.stringify(cur)); cur = {}
      else
        table.insert(cur, il)
      end
    end
    table.insert(lines, pandoc.utils.stringify(cur))
  end
  for _, b in ipairs(el.content) do
    if b.t == 'Para' or b.t == 'Plain' then add_inlines(b.content)
    elseif b.t == 'BulletList' or b.t == 'OrderedList' then
      for _, item in ipairs(b.content) do table.insert(lines, pandoc.utils.stringify(item)) end
    end
  end
  local items = {}
  for _, line in ipairs(lines) do
    local value, label = line:match('^%s*(.-)%s*|%s*(.-)%s*$')
    if value and value ~= '' then table.insert(items, { value, label }) end
  end
  return items
end

function Meta(m)
  -- Word: Quarto titles the bibliography only in PDF; give it the same title in the document language
  if quarto.doc.is_format('docx') and not m['reference-section-title'] then
    local lang = m.lang and pandoc.utils.stringify(m.lang):sub(1, 2) or 'vi'
    m['reference-section-title'] = lang == 'vi' and 'Tài liệu tham khảo' or 'References'
  end
  -- Word: Pandoc's own Vietnamese abstract title is "Tóm tắt nội dung"; the PDF says "Tóm tắt"
  if quarto.doc.is_format('docx') and not m['abstract-title'] then
    local lang = m.lang and pandoc.utils.stringify(m.lang):sub(1, 2) or 'vi'
    if lang == 'vi' then m['abstract-title'] = 'Tóm tắt' end
  end
  if m.cover == false then m['vcci-no-cover'] = true end
  if m['back-cover'] == false then m['vcci-no-back-cover'] = true end
  return m
end

function Div(el)
  if el.classes:includes('figures') then
    local items = figure_items(el)
    if quarto.doc.is_format('typst') then
      local parts = {}
      for _, it in ipairs(items) do
        table.insert(parts, '(' .. typst_string(it[1]) .. ', ' .. typst_string(it[2]) .. ')')
      end
      return pandoc.RawBlock('typst', '#vcci-figures((' .. table.concat(parts, ', ') .. ',))')
    elseif quarto.doc.is_format('docx') then
      local out = {}
      for _, it in ipairs(items) do
        table.insert(out, pandoc.Div(pandoc.Para(pandoc.Str(it[1])), { ['custom-style'] = 'VCCI Figure Number' }))
        table.insert(out, pandoc.Div(pandoc.Para(pandoc.Str(it[2])), { ['custom-style'] = 'VCCI Small' }))
      end
      return out
    end
  end
  for cls, style in pairs(STYLES) do
    if el.classes:includes(cls) then
      if quarto.doc.is_format('typst') then
        local args = ''
        if el.attributes.title then args = '(title: ' .. typst_string(el.attributes.title) .. ')' end
        local out = { pandoc.RawBlock('typst', '#' .. style.typst .. args .. '[') }
        for _, b in ipairs(el.content) do table.insert(out, b) end
        table.insert(out, pandoc.RawBlock('typst', ']'))
        return out
      elseif quarto.doc.is_format('docx') then
        local content = el.content
        if el.attributes.title then
          table.insert(content, 1, pandoc.Para({ pandoc.Strong(pandoc.Str(el.attributes.title)) }))
        end
        return pandoc.Div(content, { ['custom-style'] = style.docx })
      end
    end
  end
end
