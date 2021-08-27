click_on_topics_show_more = """
-- main script
function main(splash)

  splash.private_mode_enabled = false
  assert(splash:go(splash.args.url))
  assert(splash:wait(4))
  
  splash:runjs("document.querySelector('.show-more.au-target').click();")
  
  assert(splash:wait(1))

  return {
    num = #splash:select_all('.item-phone-button'),
    html = splash:html(),
    png = splash:png(),
    har = splash:har(),
  }
end
"""
