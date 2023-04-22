# Markdown Revisions Specification

## Abstract

Markdown Revisions is a proposed extension to Markdown [^1] that provides a plain-text syntax for annotations and comments on a markdown document.

## Syntax

Revisions adds three inline comment types, herein referred to as Revision Types:

- `[S: ]`: Provide a comment.
- `[R: /old text/new text/]`: Suggest a revision.
- `[D: /text/]`: Suggest a deletion.

Markdown revisions are designed to be human-readable, providing authors with the ability to annotate on a document without requiring any software other than a text editor.

## Parsing

In this section, we discuss how to parse each Markdown Revision.

All Markdown Revision Types -- comments, revisions, and deletions -- should be parsed into a tree with the following structure:

- pending
- accepted

A third branch may be created called `rejected` that lists rejected suggestions.

Each instance of a Revision Type in the tree should contain the following pieces of information:

- `uuid`: A UUID for the Revision;
- `text`: The Revision text, in full (example: `[S: This is a suggestion]`), and;
- `index`: The index at which the Revision text starts in the document.

### Comments

To parse a comment, search for the following text in a document:

- `[S: ]`:

## Implementations

This repository contains an example markdown document that contains comments, revisions, and deletions per the specification Syntax.

Accomapanying this document, there is an implementation of a Markdown Revisions parser.

## Authors

- capjamesg

## References

[^1]: Markdown Specification: https://daringfireball.net/projects/markdown
