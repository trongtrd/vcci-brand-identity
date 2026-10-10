#show: doc => vcci-report(
$if(title)$
  title: [$title$],
$endif$
$if(subtitle)$
  subtitle: [$subtitle$],
$endif$
$if(report-label)$
  label: [$report-label$],
$endif$
$if(client)$
  client: [$client$],
$endif$
$if(version)$
  version: [$version$],
$endif$
$if(status)$
  status: [$status$],
$endif$
$if(hero)$
  hero: "$hero$",
$endif$
$if(short-title)$
  short-title: [$short-title$],
$endif$
$if(team)$
  team: [$team$],
$endif$
$if(citation-text)$
  citation: [$citation-text$],
$endif$
$if(disclaimer)$
  disclaimer: [$disclaimer$],
$endif$
$if(contact)$
  contact: [$contact$],
$endif$
$if(vcci-no-cover)$
  cover: false,
$endif$
$if(vcci-no-back-cover)$
  back-cover: false,
$endif$
$if(by-author)$
  authors: (
$for(by-author)$
$if(it.name.literal)$
    ( name: [$it.name.literal$],
      affiliation: [$for(it.affiliations)$$it.name$$sep$, $endfor$] ),
$endif$
$endfor$
  ),
$endif$
$if(date)$
  date: [$date$],
$endif$
$if(abstract)$
  abstract: [$abstract$],
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
$if(toc)$
  toc: $toc$,
$endif$
$if(toc-title)$
  toc_title: [$toc-title$],
$endif$
  toc_depth: $toc-depth$,
  doc,
)
