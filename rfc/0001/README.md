---
authors: Prashanth.B <prashanthb-ai@wadhwaniai.org>
state: draft
discussion: https://github.com/prashanthb-ai/rfc/issues/1
---

# RFC 0001: RFCs for Greater Justice

Writing down ideas on engineering design while they are still fresh allows for
actionable technical discussion. We capture these in a Request For Comments
(RFC). The spirit of an RFC is best described by [IETF RFC
3](https://datatracker.ietf.org/doc/html/rfc3)

> The content of a note may be any thought, suggestion, etc. related to the software or other aspect of the network. Notes are encouraged to be timely rather than polished. Philosophical positions without examples or other specifics, specific suggestions or implementation techniques without introductory or background explication, and explicit questions without any attempted answers are all acceptable. The minimum length for a note is one sentence.

> These standards (or lack of them) are stated explicitly for two reasons. First, there is a tendency to view a written statement as ipso facto authoritative, and we hope to promote the exchange and discussion of considerably less than authoritative ideas. Second, there is a natural hesitancy to publish something unpolished, and we hope to ease this inhibition.

In other words the RFC serves as a vector for discussion that converges to an
authoritative explanation of the new design.
This style of development is similar to how owls are drawn.

![](owl.jpg)


## RFC lifecycle

All RFCs open with a paragraph of
[python-markdown2](https://github.com/trentm/python-markdown2/wiki/metadata)
formatted metadata.  The `state` field in this metadata must be one of the
following:

* __Draft__: quickly write something to solicit feedback. The tone and language
  of the doc at this stage should convey - "here's what I'm thinkig.. is it
worth doing? are we all on the same page about the basics?".

* __Issues__: once you have buy-in, identify 2 or 3 other engineers who can help
  you break the RFC into issues in _your own_ github repo. Continue discussion
in smaller groups on the issues. Make sure you add all issues to the "Linked
Issues" section of the "Discussion Issue" in your RFC PR.

* __Prototype__: Sometimes it helps to add a prototype with an RFC. Do not
  stress on code clarity - no one is going to maintain it.  Use your words to
describe these aspects of the design instead. Your prototype should convey
_functional_ ideas.

* __Published__: consolidate discussion from issues back into the doc. Ask for a
  final round of reviews and check it in. At this point your RFC should contain
all/most of the considerations in the [design doc template](https://docs.google.com/document/d/1lv27VCZldYMT5XLoUwYhJ4kT_DRBP7avXFq2AxZCMO8/edit).

* __Abandoned__: blockers were raised making the proposal untenable. _Do not_
  delete this RFC. It contains valuable insight. Check it in with `state:
Abandoned`.

Between the `draft` and `published` states you should go through one or more
design review sessions with the wider engineering team. If you have a prototype,
demo it.

## Creating an RFC

Create a RFC any time you want a third opinion.

1. Create the Discussion issue in your own repo. Title it `RFC <number>:
   <Title>` just like the RFC.
2. Allocate an RFC number
```
$ mkdir -p rfc/0001
$ cp skeleton.md rfc/0001/README.md
$
```
3. Modify the title/authors/discussion issue section of the RFC template. Commit
   and upload.
4. Start the discussion. Notify people by at-ing/slacking/emailing them.

## Updating the RFC

Once the RFC is in a published state, you and your team should begin working on
the Issues listed in the "Linked Issues" comment. This might be a good time to
start tracking progress through Asana/sprints. Note that at this point, your
RFC/Repo/Issues/Code interact in the following way:
```
Repo: RFC               Repo: TB
--------                --------
RFC 1916
Discussion issue:
TB/123 ---------------> Issue 123
  ^                     Linked PRs:
  |                     TB/01
  |                      |
  |                      v
  |                     PR 01
  |                     Linked Issues:
  |                     TB/01
  |                     Files:
  |-------------------- src/adherence.py
```

It is best to maintain a single authoritative source of the design in the RFC.
Versions are recoverable via git. So update the single RFC document through a PR
whenever:
* Timelines and other constraints change the behavior significantly from what
  was captured in the RFC
* The source (`src/adherence.py` in the example) goes through significant
  behavioral changes

The pre-submit hooks proposed in this RFC should help you do so.

## Integrating with Google Docs

If you'd rather work in Google Docs, you can. Just create a RFC following the
format described here and add a link to your Doc. As long as you link PRs to the
discussion issue, subsequent changes to those files will get a comment
mentioning your RFC/Doc. In the future these "shell RFCs" might get auto created
for Docs added to a specific shared gdrive.

### Soliciting feedback through a Google Doc

The best way to comment on an RFC is to directly comment on the open PR, however
this does require a GitHub account. To solicit comments from a non tech audience
you can convert the RFC to a Google Doc ([eg](https://docs.google.com/document/d/1l8lzVDO7rx7dkAFsAwM_Ro4Gyrl6WmaL/edit#bookmark=id.gjdgxs)).

1. Install pandoc
2. Run pandoc
```
$ pandoc --from markdown --to docx ./README.md > /tmp/README.docx
```
3. Reflect changes back on the PR before checking it in

For larger designs you are encouraged to do this at least once, after all the
comments on the PR have been resolved, but before flipping the state of the RFC
to `published`.

## Proposed Code Changes

1. GH hook to nudge authors of a change (in another repo) to update the relevant
   RFCs in this repo.
2. GH hook to update the index section of the README in this repo with new
   additions to `rfc/` (also in this repo)
3. Slack integration to quickly lookup open RFCs with a fuzzy text search (???
   this should be easy to implement ???)

When implemented correctly, a RFC should hold all the information an engineer
needs to explain their work in layman terms (come performance review time, or to
third party integrators).

