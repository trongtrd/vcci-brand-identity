--[[ VCCI memo. YAML keys: recipient, sender, copy-to (to/from are Pandoc's own format keys), date, title (subject),
  priority, status, signature {name, title}, attachments.

  In Word: the routing block (to, from, cc, date, subject) opens the body; signature and attachments
  close it. The PDF builds the same parts in typst-template.typ. Pandoc's own title block is not used. ]]

local LABELS = {
  vi = { memo = 'Tờ trình', to = 'Gửi', from = 'Từ', cc = 'Đồng gửi', date = 'Ngày', subject = 'Về việc', attachments = 'Tài liệu kèm theo' },
  en = { memo = 'Memo', to = 'To', from = 'From', cc = 'Cc', date = 'Date', subject = 'Subject', attachments = 'Attachments' },
}

local function str(v) return v and pandoc.utils.stringify(v) or nil end

local function line(label, value)
  return pandoc.Para({ pandoc.Strong(pandoc.Str(label .. ':')), pandoc.Space(), pandoc.Str(value) })
end

-- Word: a memo's headings one level smaller than a report's chapters (Heading 2 for '#')
function Header(el)
  if quarto.doc.is_format('docx') then el.level = el.level + 1; return el end
end

function Pandoc(doc)
  if not quarto.doc.is_format('docx') then return nil end
  local m = doc.meta
  local lang = m.lang and str(m.lang):sub(1, 2) or 'vi'
  local L = LABELS[lang] or LABELS.en
  local from = str(m.sender)
  if not from and m.author then
    local names = {}
    for _, a in ipairs(m.author) do table.insert(names, str(a.name and (a.name.literal or a.name) or a)) end
    from = table.concat(names, ', ')
  end
  local front = {}
  -- no string.upper: it works on bytes and breaks Vietnamese letters; the VCCI Label style sets capitals itself
  local label = str(m['memo-label']) or L.memo
  if m.priority then label = label .. '  ·  ' .. str(m.priority) end
  table.insert(front, pandoc.Div(pandoc.Para({ pandoc.Str(label) }), { ['custom-style'] = 'VCCI Label' }))
  for _, row in ipairs({ { L.to, str(m.recipient) }, { L.from, from }, { L.cc, str(m['copy-to']) }, { L.date, str(m.date) } }) do
    if row[2] and row[2] ~= '' then table.insert(front, line(row[1], row[2])) end
  end
  if m.title then table.insert(front, pandoc.Header(2, { pandoc.Str(L.subject .. ': ' .. str(m.title)) }, { class = 'unnumbered' })) end
  for i = #front, 1, -1 do table.insert(doc.blocks, 1, front[i]) end

  if m.signature and m.signature.name then
    table.insert(doc.blocks, pandoc.Para({ pandoc.Strong(pandoc.Str(str(m.signature.name))) }))
    if m.signature.title then
      table.insert(doc.blocks, pandoc.Div(pandoc.Para({ pandoc.Str(str(m.signature.title)) }), { ['custom-style'] = 'VCCI Small' }))
    end
  end
  if m.attachments then
    table.insert(doc.blocks, pandoc.Div(pandoc.Para({ pandoc.Str(L.attachments) }), { ['custom-style'] = 'VCCI Label' }))
    local items = {}
    for _, a in ipairs(m.attachments) do table.insert(items, { pandoc.Plain({ pandoc.Str(str(a)) }) }) end
    table.insert(doc.blocks, pandoc.OrderedList(items))
  end
  -- the routing block replaces Pandoc's title block
  doc.meta.title, doc.meta.subtitle, doc.meta.author, doc.meta.date = nil, nil, nil, nil
  return doc
end
