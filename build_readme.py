import feedparser
import pathlib
import re


def replace_chunk(content, marker, chunk, inline=False):
    r = re.compile(
        r"<!\-\- {} starts \-\->.*<!\-\- {} ends \-\->".format(marker, marker),
        re.DOTALL,
    )
    if not inline:
        chunk = "\n{}\n".format(chunk)
    chunk = "<!-- {} starts -->{}<!-- {} ends -->".format(marker, chunk, marker)
    return r.sub(chunk, content)


def fetch_blog_entries():
    entries = feedparser.parse(
        r"https://www.msleigh.io/feed_rss_created.xml"
    )
    return (
        entries.feed.title,
        entries.feed.link,
        entries.feed.description,
        entries.feed.updated,
        [
            {
                "title": entry["title"],
                "url": entry["link"].split("#")[0],
                "published": entry["published"],
            }
            for entry in entries.entries
        ],
    )


if __name__ == "__main__":
    root = pathlib.Path(__file__).parent.resolve()
    readme = root / "README.md"
    readme_contents = readme.open().read()
    entries = fetch_blog_entries()
    entries_md = (
        f"Latest posts on [{entries[0]}]({entries[1]}) (updated {entries[3]}):\n"
        + "\n".join(
            [
                "- [{title}]({url}) - {published}".format(**entry)
                for entry in entries[4][:6]
            ]
        )
    )
    print(entries_md)
    rewritten = replace_chunk(readme_contents, "blog", entries_md)
    readme.open("w").write(rewritten)
