--[[ VCCI Working Paper metadata.

  abstract-en / keywords-en (Vietnamese paper) or abstract-vi / keywords-vi (English paper) become the second
  abstract in the other language. In Word, series and number join the date line of the title block, and the
  title-page details that Pandoc does not place itself (keywords, second abstract, JEL codes, suggested citation,
  disclaimer) are written at the start of the body.
]]

local LABELS = {
  vi = { number = 'số', abstract = 'Tóm tắt', keywords = 'Từ khóa', jel = 'Mã JEL', citation = 'Trích dẫn đề nghị',
         city = 'Hà Nội', org = 'Liên đoàn Thương mại và Công nghiệp Việt Nam',
         disclaimer = 'Quan điểm trong bài là của tác giả, không nhất thiết phản ánh quan điểm của Liên đoàn Thương mại và Công nghiệp Việt Nam.' },
  en = { number = 'No.', abstract = 'Abstract', keywords = 'Keywords', jel = 'JEL classification', citation = 'Suggested citation',
         city = 'Hanoi', org = 'Vietnam Chamber of Commerce and Industry',
         disclaimer = 'The views expressed are those of the authors and do not necessarily reflect the views of the Vietnam Chamber of Commerce and Industry.' },
}

local function doc_lang(m)
  local l = m.lang and pandoc.utils.stringify(m.lang):sub(1, 2) or 'vi'
  return LABELS[l] and l or 'en'
end

local function join(list, sep)
  local out = {}
  for _, v in ipairs(list or {}) do table.insert(out, pandoc.utils.stringify(v)) end
  return table.concat(out, sep)
end

function Meta(m)
  local alt = doc_lang(m) == 'vi' and 'en' or 'vi'
  if m['abstract-' .. alt] then m['vcci-abstract-alt'] = m['abstract-' .. alt] end
  if m['keywords-' .. alt] then m['vcci-keywords-alt'] = m['keywords-' .. alt] end
  return m
end

local function styled(style, inlines)
  return pandoc.Div(pandoc.Para(inlines), { ['custom-style'] = style })
end

local function labelled(label, text)
  return pandoc.Para({ pandoc.Strong(pandoc.Str(label .. ':')), pandoc.Space(), pandoc.Str(text) })
end

function Pandoc(doc)
  if not quarto.doc.is_format('docx') then return nil end
  local m = doc.meta
  local lang = doc_lang(m)
  local alt = lang == 'vi' and 'en' or 'vi'
  local L, A = LABELS[lang], LABELS[alt]
  local series = m['wp-series'] and pandoc.utils.stringify(m['wp-series']) or 'VCCI Working Paper'
  local number = m['wp-number'] and pandoc.utils.stringify(m['wp-number'])
  local series_number = number and (series .. ' ' .. L.number .. ' ' .. number) or series
  -- series and number go on the date line of Pandoc's title block, so they sit above the abstract
  local date = m.date and pandoc.utils.stringify(m.date) or nil
  doc.meta.date = pandoc.MetaInlines({ pandoc.Str((date and (date .. ' · ') or '') .. series_number) })
  local front = {}
  if m.keywords then table.insert(front, labelled(L.keywords, join(m.keywords, '; '))) end
  if m['vcci-abstract-alt'] then
    table.insert(front, styled('Abstract Title', { pandoc.Str(A.abstract) }))
    local alt_blocks = m['vcci-abstract-alt']
    if alt_blocks.t == 'MetaBlocks' or type(alt_blocks) == 'table' and alt_blocks[1] and alt_blocks[1].t then
      for _, b in ipairs(alt_blocks) do
        table.insert(front, pandoc.Div(b.t and b or pandoc.Para(b), { ['custom-style'] = 'Abstract' }))
      end
    else
      table.insert(front, styled('Abstract', { pandoc.Str(pandoc.utils.stringify(alt_blocks)) }))
    end
    if m['vcci-keywords-alt'] then table.insert(front, labelled(A.keywords, join(m['vcci-keywords-alt'], '; '))) end
  end
  if m.jel then table.insert(front, labelled(L.jel, join(m.jel, ', '))) end
  local citation = m['citation-text'] and pandoc.utils.stringify(m['citation-text'])
  if not citation then
    local names = {}
    for _, a in ipairs(m.author or {}) do
      local n = a.name and (a.name.literal or a.name) or a
      table.insert(names, pandoc.utils.stringify(n))
    end
    local year = (date or ''):match('%d%d%d%d') or 'n.d.'
    citation = (#names > 0 and table.concat(names, ', ') or L.org) .. ' (' .. year .. '). ' ..
      pandoc.utils.stringify(m.title or '') .. '. ' .. series_number .. '. ' .. L.city .. ': ' .. L.org .. '.'
  end
  table.insert(front, styled('VCCI Small', { pandoc.Strong(pandoc.Str(L.citation .. ':')), pandoc.Space(), pandoc.Str(citation) }))
  local disclaimer = m.disclaimer and pandoc.utils.stringify(m.disclaimer) or L.disclaimer
  table.insert(front, styled('VCCI Small', { pandoc.Str(disclaimer) }))
  for i = #front, 1, -1 do table.insert(doc.blocks, 1, front[i]) end
  return doc
end
