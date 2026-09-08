-- Source chapters live in textbook/, while exports live two folders deeper.
function Link(link)
  local companion = link.target:match("^%.%./notebooks/")
    or link.target:match("^%.%./datasets/")
    or link.target:match("^%.%./weeks/")
  if not companion then
    return nil
  end

  if FORMAT:match("epub") then
    link.target = "#companion-materials"
  else
    link.target = "../../" .. link.target
  end
  return link
end
