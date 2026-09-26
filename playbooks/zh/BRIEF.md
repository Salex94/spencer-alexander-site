# Brief: the Simplified Chinese pages of spenceralexander.com.au

You are translating pages of a Melbourne law firm's live website into Simplified Chinese for Mandarin
readers in Box Hill and Melbourne's east. A lawyer at the firm who reads Mandarin will check every page
before anything is published, so write the best Chinese you can and make her review easy.

This is the brief the seven Chinese pages in `zh/` were translated to on 26 Sep 2026, kept as the
standard for every later change to them. The pages were first written outside the repository, one
translated page and one numbered review file each, and then given the shared Chinese header, menus and
footer, the zh URLs and the hreflang links by a build step. From publication, the pages in `zh/` are the
source, and any change is made in them directly under the rules below and checked by the Mandarin
reading lawyer before it is published.

## What to translate

- Everything inside <main id="main"> ... </main>: every visible string, alt text and aria-label.
- In <head>: the <title>, meta description, og:title, og:description, twitter:title and
  twitter:description, and every text value in the JSON-LD blocks, such as name, description,
  headline, FAQ questions and answers, service names and breadcrumb names. Set "inLanguage": "zh-Hans"
  where a node has inLanguage. Keep every URL, @id, @type, number and date exactly as it is.
- Leave the header, the top bar, the mobile menu, the footer and the mobile call bar in English. They
  are replaced afterwards with a shared Chinese version, so do not touch them.

## Links inside <main>

- Pages that will exist in Chinese: /, /contact, /fees and the three practice pages. Rewrite links to
  them as /zh/ (home), /zh/contact, /zh/fees, /zh/family-law, /zh/wills-and-estates and /zh/commercial-law,
  keeping any #fragment, such as /zh/contact#enquiry or /zh/family-law#svc-divorce-and-separation.
- Every other page stays in English and keeps its English link: the articles, insights, faq, about,
  resources, privacy. Translate the link text and make clear the destination is in English, for
  example "阅读英文指南：离婚" or a label ending "英文". Never pretend an English page is Chinese.
- tel: and mailto: links stay exactly as they are.

## The standard for the Chinese

- Legal accuracy comes first. Every legal statement must say exactly what the English says, with the
  same qualifications, exceptions, time limits and figures. Add nothing, drop nothing, strengthen
  nothing. If a legal term has no settled Chinese equivalent, use the plain Chinese meaning followed by
  the English term after a space, for example 遗嘱认证 Probate, the first time it appears on the page.
- Natural, warm, professional Simplified Chinese that a Mandarin reader in Melbourne would find clear
  and trustworthy. Not stiff, not machine translated. Use the terms Chinese Australians actually search
  for: 博士山 for Box Hill, 离婚律师, 遗嘱, 遗产, 遗嘱认证, 持久授权书, 家庭法律师, 商业律师.
- No dashes of any kind, including the Chinese dash ——, and no brackets of any kind, including （）,
  except the phone number (03) 9125 8355 and the jurisdiction suffixes (Vic) and (Cth) in Act titles.
  Use ，。、：； instead.
- Never call the firm or anyone at it a specialist or expert: no 专家, 专攻, 专精, 权威. Never promise an
  outcome. Never state or imply that any lawyer at the firm speaks Mandarin. Keep Spencer's name, the
  firm's name "Spencer Alexander Lawyers", addresses and phone numbers in English.
- Fixed wording: "Your first call is free, and you speak with a lawyer" is 首次通话免费，与您通话的是律师。
  "A written fee estimate before any substantive work begins" is 开始任何实质性工作之前提供书面费用估算.
  "Every matter overseen by the principal" is 每宗案件均由首席律师监督.
- Google review quotes stay in English exactly as written, with the name exactly as written. Translate
  only the words around them.
- Visible FAQ answers and their FAQPage JSON-LD text must be identical to each other in Chinese.
- Keep every HTML tag, class, id and attribute exactly as it is, apart from the translated text, the
  rewritten links above and lang attributes. Keep the same number of sections, blocks and list items.
- Title tag: the Chinese title followed by " | Spencer Alexander Lawyers", about 30 Chinese characters
  before the suffix. Meta description: about 60 to 90 Chinese characters, the same text in the meta tag,
  og:description, twitter:description and any JSON-LD description of the page.

## The review file

<page>.review.md lists, in page order, every translated string as a numbered pair:

    12. EN: the English text
        中文: the Chinese text

including the title, description and each FAQ. Where you made a choice the reviewer should know about,
such as a term with more than one common translation, add a line starting "Note:" under that pair.

Finish by checking your page: no —— or – or （ or ） anywhere in the Chinese, every <main> link rewritten as
above, and the FAQ schema text identical to the visible answers. Your final message lists the page, the
terms you chose for the key legal concepts, and anything the reviewer should look at first.
