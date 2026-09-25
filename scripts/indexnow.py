"""Tell Bing and the other IndexNow search engines that pages changed (26 Sep 2026).

    python3 scripts/indexnow.py /insight-some-article.html /insights.html /index.html

Run it after a push to main has gone live, with the .html paths of every page the push changed.
The key file 25747fcf3f9fd2bc54bf5ee54d16b678.txt at the site root proves the site is ours; never delete or rename it.
It prints the response code: 200 or 202 means accepted. A failure never blocks a publish, so
report it and carry on. Google does not use IndexNow; the sitemap covers Google.
"""
import json, sys, urllib.request

KEY = "25747fcf3f9fd2bc54bf5ee54d16b678"
HOST = "www.spenceralexander.com.au"


def main(paths):
    if not paths:
        sys.exit("usage: python3 scripts/indexnow.py /page.html [/other.html ...]")
    urls = []
    for p in paths:
        p = p if p.startswith("/") else "/" + p
        if p in ("/", "/index.html"):
            urls.append("https://%s/" % HOST)
        else:
            urls.append("https://%s%s" % (HOST, p))
    body = json.dumps({"host": HOST, "key": KEY, "keyLocation": "https://%s/%s.txt" % (HOST, KEY), "urlList": urls}).encode()
    req = urllib.request.Request("https://api.indexnow.org/indexnow", data=body, headers={"Content-Type": "application/json; charset=utf-8"})
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            print("IndexNow", r.status, "for", len(urls), "URL(s)")
    except urllib.error.HTTPError as e:
        print("IndexNow refused:", e.code, e.read()[:200].decode("utf8", "replace"))
    except Exception as e:
        print("IndexNow not reached:", e)


if __name__ == "__main__":
    main(sys.argv[1:])
