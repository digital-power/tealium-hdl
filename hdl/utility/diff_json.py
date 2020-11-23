import json
from diff_match_patch import diff_match_patch


def diff_json(old, new):
    """Diffs JSON as text, and returns the diff as HTML"""
    old_text = json.dumps(old, indent=4)
    new_text = json.dumps(new, indent=4)

    dmp = diff_match_patch()
    diff = dmp.diff_main(old_text, new_text)

    dmp.diff_cleanupSemantic(diff)

    html = dmp.diff_prettyHtml(diff).replace(
        '    ', '&nbsp;&nbsp;&nbsp;&nbsp;').replace('&para;', '')

    return html
