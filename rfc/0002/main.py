import argparse
import json
import os
import re
import requests
import subprocess

from bs4 import BeautifulSoup

# TODO: Find a python markdown parser lib and avoid shelling.
def shell(command, **kwargs):
    # TODO: handle streaming output/exit codes/subprocess.poll
    print("\n%s %s" % (command, kwargs.get("input", b"").decode("utf-8")))
    process = subprocess.Popen(
        command,
        shell=True,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    output = process.communicate(**kwargs)
    print("STDOUT %s\nSTDERR %s" % (output[0], output[1]))
    return {
            "returncode": process.returncode,
            "stdout": output[0],
            "stderr": output[1]
    }

# Helper class to parse RFCs.
class RFC:

    md = "*.md"
    discussion = "discussion:"

    # Returns a list of discussion issues for the given solution.
    def get_discussion_issues(root, sol):
        cmd = 'grep -ir "%s" $(find %s -iname "%s") | awk -F" " \'{print $2}\'' % (
                RFC.discussion, root, RFC.md)
        if sol != "":
            cmd += " | grep -i %s" % sol

        output = shell(cmd)
        if output["returncode"] != 0:
            raise RuntimeError(
                    "Non zero return code from running %s: %s" %
                    (cmd, output["returncode"]))

        # TODO: make this a dict keyed on RFC.
        return [s.decode("utf-8")
                for s in output["stdout"].rstrip(b"\n").split(b"\n")]

# Helper class to manage GitHub.
class GitHub:

    api = "https://api.github.com/repos"
    gh = "https://github.com"
    protocol = "http"
    # See _classify for example usage
    url_rgx = 'https://[a-z,.]+/[a-z,/,-]+/([a-z]+)/(issue|pull)s?/?([0-9+])?'

    def _get(url):
        resp = None
        try:
            resp = requests.get(url)
        except requests.exceptions.ConnectionError as e:
            print(e)
        if resp and resp.ok is not True:
            print("Failed to fetch %s: %s" % (p, resp))
        return resp

    # Construct "https://api.github.com/repos/${sol}/pulls/${pr#}"
    # into {"solution": ${sol}, "type": "pull", "id": ${pr#}}
    def _classify(url):
        x = re.search(GitHub.url_rgx, url)
        if x:
            g = x.groups()
            return {"solution": g[0], "type": g[1], "id": g[2]}
        return {"solution": None, "type": None, "id": None}

    # Parses the html in issues for their linked PRs.
    # Returns headless pr links so callers can append the right domain.
    # eg: { "https://rfc/issue/2": ["/wadhwaniai/rfc/pull/5", ...] }
    def get_prs(issues):
        prs = {}
        for i in issues:
            resp = GitHub._get(i)
            if resp == None:
                continue
            soup = BeautifulSoup(resp.text, 'html.parser')
            links = soup.find("form", {"aria-label": re.compile('Link issues')})
            prs[i] = [l["href"] for l in links.find_all("a")]
        return prs

    # Parses a list of prs and returns the files in each.
    # eg: { "rfc": { "file/name/one.py": set([2, 3 ...]) } }
    # Where 2, 3 are the discussion issues for rfcs 2 and 3, "rfc" is the github
    # repo/solution name and one.py is part of the prs that fixed issues 2, 3.
    def get_files(issues_to_prs):
        # Construct "https://api.github.com/repos/${sol}/pulls/${pr#}/files"
        sol_to_files = {}
        for i, prs in issues_to_prs.items():

            c = GitHub._classify(i)
            sol = c["solution"]
            issue_id = c["id"]
            sol_to_files[sol] = {}
            files_to_issues = {}

            for p in prs:
                # TODO: remove all this and just work with sol + number +
                # template url.
                if not p.startswith(GitHub.protocol):
                    p = os.path.join(GitHub.api, p.strip("/"))
                if not p.endswith("files"):
                    p = os.path.join(p, "files")

                # This doesn't seem to be an issue with html parsing. The same
                # happens via the GH api for issues.
                p = p.replace("/pull/", "/pulls/")
                resp = GitHub._get(p)
                if resp == None:
                    continue

                for f in [j["filename"] for j in json.loads(resp.text)]:
                    issues = files_to_issues.get(f, set([]))
                    issues.add(i)
                    files_to_issues[f] = issues

            sol_to_files[sol] = files_to_issues

        return sol_to_files

if __name__ == "__main__":
    p = argparse.ArgumentParser(description='RFC parser cli')
    p.add_argument(
            '--root',
            action='store',
            type=str,
            help='The root directory for the RFC repo',
            required=True)
    p.add_argument(
            '--solution',
            action='store',
            type=str,
            help='The name of a solution, eg: pest_management_system. Note ' +
                'this needs to match the name in the solution\'s GitHub URL',
            default='')
    args = p.parse_args()

    issues = RFC.get_discussion_issues(args.root, args.solution)
    prs = GitHub.get_prs(issues)
    files = GitHub.get_files(prs)
    print("Current mapping of files in PRs to RFCs for this repo:\n%s" %
            files["rfc"])



