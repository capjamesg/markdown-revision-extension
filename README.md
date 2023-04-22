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

Here is an example Revision Type tree:

```
{'pending': {'suggestions': [{'uuid': 'ea750efc-c274-43f8-a003-584f5288b36d', 'text': '[S: Perhaps "thought?"]', 'index': 70}], 'revisions': [{'uuid': '3a626e37-36ee-4bc2-8626-663ad56f42b5', 'text': '[R: /on Billions/on the television show Billions/]', 'index': 1285}], 'deletions': []}, 'accepted': {'suggestions': [], 'revisions': [], 'deletions': []}}
```

### Comments

To parse a comment, search for the following text in a document:

```
[S: This is a comment.]
```

The text after the colon (`:`) and before the closing square bracket `]` is the comment.

### Revision

To parse a revision, search for the following text in a document:

```
[R: /old text/new text/]
```

Implementations MUST enforce the `/old text/new text/` syntax with a forward slash at the beginning and end of the revision string.

## Implementations

This repository contains an example markdown document that contains comments, revisions, and deletions per the specification Syntax.

Accomapanying this document, there is an implementation of a Markdown Revisions parser.

## Authors

- capjamesg

## References

[^1]: Markdown Specification: https://daringfireball.net/projects/markdown
