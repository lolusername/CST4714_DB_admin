function Div(div)
  if not div.classes:includes("pagebreak") then
    return nil
  end

  if FORMAT:match("docx") then
    return pandoc.RawBlock(
      "openxml",
      '<w:p><w:r><w:br w:type="page"/></w:r></w:p>'
    )
  end

  if FORMAT:match("html") or FORMAT:match("epub") then
    return pandoc.RawBlock(
      "html",
      '<div class="pagebreak" aria-hidden="true"></div>'
    )
  end

  return pandoc.RawBlock("latex", "\\newpage")
end
