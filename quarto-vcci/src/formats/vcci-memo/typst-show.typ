#show: doc => vcci-memo(
$if(title)$
  title: [$title$],
$endif$
$if(memo-label)$
  label: [$memo-label$],
$endif$
$if(recipient)$
  to: [$recipient$],
$endif$
$if(sender)$
  from: [$sender$],
$endif$
$if(copy-to)$
  cc: [$copy-to$],
$endif$
$if(date)$
  date: [$date$],
$endif$
$if(priority)$
  priority: [$priority$],
$endif$
$if(status)$
  status: [$status$],
$endif$
$if(signature.name)$
  signature-name: [$signature.name$],
$endif$
$if(signature.title)$
  signature-title: [$signature.title$],
$endif$
$if(attachments)$
  attachments: ($for(attachments)$[$attachments$],$endfor$),
$endif$
$if(by-author)$
  authors: (
$for(by-author)$
$if(it.name.literal)$
    ( name: [$it.name.literal$], ),
$endif$
$endfor$
  ),
$endif$
$if(lang)$
  lang: "$lang$",
$endif$
$if(region)$
  region: "$region$",
$endif$
$if(fontsize)$
  fontsize: $fontsize$,
$endif$
  doc,
)
