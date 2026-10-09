--[[ VCCI block styles shared by every format.

  ::: lead        two or three sentences carrying the main message   (Typst: vcci-lead,    Word: "VCCI Lead")
  ::: highlight   box with a blue left rule; optional title="…"      (Typst: vcci-callout, Word: "VCCI Callout")
  ::: label       small uppercase label above a heading              (Typst: vcci-label,   Word: "VCCI Label")
]]

local STYLES = {
  lead = { typst = 'vcci-lead', docx = 'VCCI Lead' },
  highlight = { typst = 'vcci-callout', docx = 'VCCI Callout' },
  label = { typst = 'vcci-label', docx = 'VCCI Label' },
}

local function typst_string(s)
  return '"' .. s:gsub('\\', '\\\\'):gsub('"', '\\"') .. '"'
end

function Div(el)
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
