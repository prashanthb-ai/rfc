---
authors: Prashanth.B <prashanthb-ai@wadhwaniai.org>
state: prototype
discussion: https://github.com/prashanthb-ai/rfc/issues/4
---

# RFC 0002: Using GitHub actions to keep RFCs updated

Github actions can run on every pr, so we use them to help PR authors keep their
RFCs up to date. If you're working on a Solution at WadhwaniAI you can set this
up as follows:

1. Create a directory called `.github/workflows` and copy the yaml contents of
   the same directory in this repo into it.
2. Upload a PR and wait for the actions to complete. This should leave a comment
   on your PR.
3. If the comment indicates an RFC, update it.

## Linking RFCs to PRs

Github exposes a REST api through which we can access the "discussion issue".
Eg:
```console
$ curl https://api.github.com/repos/prashanthb-ai/rfc/issues
[
  {
    "url": "https://api.github.com/repos/prashanthb-ai/rfc/issues/5",
    "repository_url": "https://api.github.com/repos/prashanthb-ai/rfc",
    "labels_url": "https://api.github.com/repos/prashanthb-ai/rfc/issues/5/labels{/name}",
    "comments_url": "https://api.github.com/repos/prashanthb-ai/rfc/issues/5/comments",
    "events_url": "https://api.github.com/repos/prashanthb-ai/rfc/issues/5/events",
    "html_url": "https://github.com/prashanthb-ai/rfc/pull/5",
    "id": 894100225,
    "node_id": "MDExOlB1bGxSZXF1ZXN0NjQ2NTE1NTM2",
    "number": 5,
    "title": "RFC 0000: Using Github actions to keep RFCs updated",
    "user": {
      "login": "prashanthb-ai",
        ...
       },
    "labels": [

    ],
    "state": "open",
    "locked": false,
    "assignee": null,
    "assignees": [

    ],
    "milestone": null,
    "comments": 0,
    "created_at": "2021-05-18T08:06:30Z",
    "updated_at": "2021-05-18T08:06:30Z",
    "closed_at": null,
    "author_association": "OWNER",
    "active_lock_reason": null,
    "pull_request": {
      "url": "https://api.github.com/repos/prashanthb-ai/rfc/pulls/5",
      "html_url": "https://github.com/prashanthb-ai/rfc/pull/5",
      "diff_url": "https://github.com/prashanthb-ai/rfc/pull/5.diff",
      "patch_url": "https://github.com/prashanthb-ai/rfc/pull/5.patch"
    },
    "body": "",
  },
```
Note that `linked pull requests` is available directly through this api.

### Option 1

Follow this DAG
```console
        v----------------------v--------------|
RFC -> discussion issue -> other issues -> Linked pull requests
```
This means every PR related to the RFC needs to reference the discussion issue
AND its parent issue.

### Option 2

Follow this DAG
```console
RFC -> discussion issue -> Other issues -> Linked pull requests
```
This means every PR related to the RFC only needs to reference its parent issue.
What makes this challenging is we now need to either use:
* Comments on the dicussion issue OR
* Update history of the discussion issue

To link PR-linked-issues to discussion issues.

For the sake of simplicity in implementation, we are going with Option 1.

## Getting Filenames from PRs

The url for the PRs is available in the discussion issues link.
```console
$ curl https://api.github.com/repos/prashanthb-ai/rfc/pulls/3
...
  "created_at": "2021-05-16T11:44:47Z",
  "updated_at": "2021-05-16T11:47:22Z",
  "closed_at": "2021-05-16T11:47:22Z",
  "merged_at": "2021-05-16T11:47:22Z",
  "merge_commit_sha": "85d7e40d15c0ab2a9271905395427ce9a49fc7ee",
  "assignee": null,
...
```
Wait till the PR is checked in (i.e `merged: true`) then run
```console
$ git diff --name-only 85d7e40d15c0ab2a9271905395427ce9a49fc7ee
README.md
```

## Finding if a PR references a RFC

Any new PR in a repo, do the following
1. Parse all `state: published` RFCs for discussion issues in your repo
2. Find all PRs for each discussion issue
3. See if there's an overlap with one or more files in a given pr
4. Comment on this PR with a link to the parent RFC for the overlapping files

To achieve this, we need the following in the GitHub action container:
1. list of files in this new PR
2. name of the Solution repo (used to search the RFC repo for discussion
   issues)

## Appendix

* [PyGithub](https://github.com/PyGithub/PyGithub)
* [GhAPI tool](https://github.blog/2020-12-18-learn-about-ghapi-a-new-third-party-python-client-for-the-github-api/)
* [Github API](https://blog.exploratory.io/analyzing-issue-data-with-github-rest-api-63945017dedc)
