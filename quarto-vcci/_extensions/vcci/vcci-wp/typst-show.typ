#show: doc => vcci-wp(
$if(title)$
  title: [$title$],
$endif$
$if(subtitle)$
  subtitle: [$subtitle$],
$endif$
$if(wp-series)$
  series: [$wp-series$],
$endif$
$if(wp-number)$
  number: [$wp-number$],
$endif$
$if(by-author)$
  authors: (
$for(by-author)$
$if(it.name.literal)$
    ( name: [$it.name.literal$],
      affiliation: [$for(it.affiliations)$$it.name$$sep$; $endfor$],
      email: [$it.email$],
      corresponding: $if(it.attributes.corresponding)$true$else$false$endif$ ),
$endif$
$endfor$
  ),
$endif$
$if(date)$
  date: [$date$],
$endif$
$if(version)$
  version: [$version$],
$endif$
$if(status)$
  status: [$status$],
$endif$
$if(short-title)$
  short-title: [$short-title$],
$endif$
$if(abstract)$
  abstract: [$abstract$],
$endif$
$if(vcci-abstract-alt)$
  abstract-alt: [$vcci-abstract-alt$],
$endif$
$if(keywords)$
  keywords: ($for(keywords)$"$keywords$",$endfor$),
$endif$
$if(vcci-keywords-alt)$
  keywords-alt: ($for(vcci-keywords-alt)$"$vcci-keywords-alt$",$endfor$),
$endif$
$if(jel)$
  jel: ($for(jel)$"$jel$",$endfor$),
$endif$
$if(thanks)$
  thanks: [$thanks$],
$endif$
$if(citation-text)$
  citation: [$citation-text$],
$endif$
$if(disclaimer)$
  disclaimer: [$disclaimer$],
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
