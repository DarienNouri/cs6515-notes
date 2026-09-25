import os
import re

REPOS = [
    "/Users/darien/projects/cs6515-notes",
    "/Users/darien/projects/cs6515-github-pages"
]

WEEKS = [
    {"dir": "W01_DP1-DP2", "short": "W01 DP"},
    {"dir": "W02_DC3-DC1", "short": "W02 D&C"},
    {"dir": "W03_DC2", "short": "W03 Median"},
    {"dir": "W04_DP3-GR1-GR2_EXAM1", "short": "W04 Graphs & SCC"},
    {"dir": "W05_GR3", "short": "W05 MST"},
    {"dir": "W06_MF1-MF2", "short": "W06 Max-Flow"},
    {"dir": "W07_MF4_EXAM2", "short": "W07 Edmonds-Karp"},
    {"dir": "W08_NP1-NP2-NP3", "short": "W08 NP-Complete"},
    {"dir": "W09_LP1-LP2-LP3", "short": "W09 Linear Prog"},
    {"dir": "W10_LP4-NP4-NP5_EXAM3", "short": "W10 Approx & Halting"},
    {"dir": "W11_Advanced-FFT-Crypto-Bloom", "short": "W11 Advanced"},
]

def update_week_files(repo):
    print(f"Updating week files in {repo}...")
    for idx, wk in enumerate(WEEKS):
        filepath = os.path.join(repo, "01_by_week", wk["dir"], "index.html")
        if not os.path.exists(filepath):
            print(f"  Missing: {filepath}")
            continue
        with open(filepath, "r", encoding="utf-8") as f:
            html = f.read()

        # Match legacy blockquote
        pattern = r"<blockquote>\s*<p>((?:(?!</p>).)*?)</p>\s*<p>(?:<a[^>]+>.*?(?:weeks|◀|▶).*?)</p>\s*</blockquote>"
        m = re.search(pattern, html, re.DOTALL | re.IGNORECASE)
        if not m:
            print(f"  Could not find legacy blockquote in {wk['dir']}")
            continue

        raw_desc = m.group(1)
        desc = re.sub(r"\s+", " ", raw_desc).strip()

        # Prev button
        if idx > 0:
            prev_wk = WEEKS[idx - 1]
            prev_html = (
                f'<a class="btn btn--prev" href="../{prev_wk["dir"]}/index.html">\n'
                f'      <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><line x1="19" y1="12" x2="5" y2="12"></line><polyline points="12 19 5 12 12 5"></polyline></svg>\n'
                f'      <span>{prev_wk["short"]}</span>\n'
                f'    </a>'
            )
        else:
            prev_html = '<span class="btn btn--disabled" aria-disabled="true">← Start</span>'

        # Next button
        if idx < len(WEEKS) - 1:
            next_wk = WEEKS[idx + 1]
            next_html = (
                f'<a class="btn btn--next" href="../{next_wk["dir"]}/index.html">\n'
                f'      <span>{next_wk["short"]}</span>\n'
                f'      <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><line x1="5" y1="12" x2="19" y2="12"></line><polyline points="12 5 19 12 12 19"></polyline></svg>\n'
                f'    </a>'
            )
        else:
            next_html = '<span class="btn btn--disabled" aria-disabled="true">End →</span>'

        replacement = (
            f'<div class="module-subtitle">\n'
            f'  <span>{desc}</span>\n'
            f'</div>\n'
            f'<nav class="top-nav-bar" data-top-nav aria-label="Top page navigation">\n'
            f'  <div class="top-nav-bar__left">\n'
            f'    {prev_html}\n'
            f'  </div>\n'
            f'  <div class="top-nav-bar__center">\n'
            f'    <a class="btn" href="../index.html">All Weeks</a>\n'
            f'    <a class="btn" href="../../00_START_HERE/COURSE_ROADMAP.html">Roadmap</a>\n'
            f'    <a class="btn" href="../../00_START_HERE/INDEX.html">Master Index</a>\n'
            f'    <a class="btn" href="../../module-week-schedule.html">Schedule</a>\n'
            f'  </div>\n'
            f'  <div class="top-nav-bar__right">\n'
            f'    {next_html}\n'
            f'  </div>\n'
            f'</nav>'
        )

        new_html = html[:m.start()] + replacement + html[m.end():]
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(new_html)
        print(f"  Updated {wk['dir']}")

def update_all_in_one(repo):
    print(f"Updating all-in-one.html in {repo}...")
    filepath = os.path.join(repo, "01_by_week", "all-in-one.html")
    if not os.path.exists(filepath):
        print(f"  Missing: {filepath}")
        return

    with open(filepath, "r", encoding="utf-8") as f:
        html = f.read()

    # 1. Update top intro blockquote
    top_intro_pattern = (
        r"<blockquote>\s*<p>Every weekly study page is stacked here for continuous review[^<]*</p>\s*"
        r"<p><a href=\"index\.html\">All weeks</a> · <a href=\"\.\./index\.html\">Home</a></p>\s*</blockquote>"
    )
    top_replacement = (
        '<p class="lead">Every weekly study page is stacked here for continuous review. Use the outline sidebar for fast navigation, or search with <kbd>Cmd K</kbd>.</p>\n'
        '<nav class="top-nav-bar" data-top-nav aria-label="Top page navigation">\n'
        '  <div class="top-nav-bar__left">\n'
        '    <a class="btn btn--prev" href="../index.html">\n'
        '      <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><line x1="19" y1="12" x2="5" y2="12"></line><polyline points="12 19 5 12 12 5"></polyline></svg>\n'
        '      <span>Home</span>\n'
        '    </a>\n'
        '  </div>\n'
        '  <div class="top-nav-bar__center">\n'
        '    <a class="btn" href="index.html">All Weeks Grid</a>\n'
        '    <a class="btn" href="../00_START_HERE/COURSE_ROADMAP.html">Roadmap</a>\n'
        '    <a class="btn" href="../00_START_HERE/INDEX.html">Master Index</a>\n'
        '    <a class="btn" href="../module-week-schedule.html">Schedule</a>\n'
        '  </div>\n'
        '  <div class="top-nav-bar__right">\n'
        '    <a class="btn btn--next" href="W01_DP1-DP2/index.html">\n'
        '      <span>Start Week 1</span>\n'
        '      <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><line x1="5" y1="12" x2="19" y2="12"></line><polyline points="12 5 19 12 12 19"></polyline></svg>\n'
        '    </a>\n'
        '  </div>\n'
        '</nav>'
    )
    html, n_top = re.subn(top_intro_pattern, top_replacement, html, count=1, flags=re.DOTALL)
    print(f"  Replaced top intro blockquote (count: {n_top})")

    # 2. Update all week header blockquotes in all-in-one.html
    def sub_bq(match):
        raw_desc = match.group(1)
        desc = re.sub(r"\s+", " ", raw_desc).strip()
        return f'<div class="module-subtitle">\n  <span>{desc}</span>\n</div>'

    pattern = r"<blockquote>\s*<p>((?:(?!</p>).)*?)</p>\s*<p>(?:<a[^>]+>.*?(?:weeks|◀|▶).*?)</p>\s*</blockquote>"
    html, count = re.subn(pattern, sub_bq, html, flags=re.DOTALL | re.IGNORECASE)
    print(f"  Replaced {count} section blockquotes with module-subtitle badges")

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(html)

for repo in REPOS:
    update_week_files(repo)
    update_all_in_one(repo)

print("All updates completed successfully!")
