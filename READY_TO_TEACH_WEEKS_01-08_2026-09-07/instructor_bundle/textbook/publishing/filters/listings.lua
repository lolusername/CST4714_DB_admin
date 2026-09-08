local listing_number = 0

local labels = {
  sql = "SQL",
  postgresql = "SQL",
  javascript = "MongoDB shell / JavaScript",
  js = "MongoDB shell / JavaScript",
  json = "JSON",
  python = "Python",
  py = "Python",
  bash = "Shell",
  shell = "Shell",
  sh = "Shell",
  text = "Text",
  plaintext = "Text",
  markdown = "Markdown",
  yaml = "YAML",
  dot = "Graphviz DOT"
}

function CodeBlock(block)
  listing_number = listing_number + 1
  local language = "Code"
  if block.classes and #block.classes > 0 then
    language = labels[block.classes[1]] or string.upper(block.classes[1])
  end

  local caption = pandoc.Para({
    pandoc.Span(
      {pandoc.Str("Listing " .. listing_number .. ". " .. language)},
      pandoc.Attr("", {"listing-caption"}, {})
    )
  })

  return {caption, block}
end
