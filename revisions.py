# Markdown Annotation
# An extension to the markdown language that supports inline suggestions and revisions
# The syntax for the language is:
# [S: ] - Suggestion
# [R: /old text/new text/] - Revise
# [D: ] - Delete
# This document contains a parser for the new language.
# Written by capjamesg

import re
import uuid

VOCAB = {
    "suggestions": {"exec": lambda x: re.findall(r"\[S: (.*?)\]", x), "pattern": "S"},
    "revisions": {"exec": lambda x: re.findall(r"\[R: (.*?)\]", x), "pattern": "R"},
    "deletions": {"exec": lambda x: re.findall(r"\[D: (.*?)\]", x), "pattern": "D"},
}


class Document:
    def __init__(self, contents=""):
        self.contents = contents

    def read_from_file(self, file_path):
        with open(file_path, "r") as file:
            self.contents = file.read()

    def _last_occuring_instance(self, string, substring):
        return string.rindex(substring)

    def parse_document(self):
        tree = {}

        for key, _ in VOCAB.items():
            tree[key] = VOCAB[key]["exec"](self.contents)

            # remove blank
            tree[key] = [t for t in tree[key] if t not in ("", " ", "//")]

            # surround each object in its pattern
            tree[key] = [f"[{VOCAB[key]['pattern'].upper()}: {t}]" for t in tree[key]]

            # apply uuids
            tree[key] = [
                {"uuid": str(uuid.uuid4()), "text": t, "index": self.contents.index(t)}
                for t in tree[key]
            ]

        changes = {"pending": tree, "accepted": {k: [] for k in tree.keys()}}

        self.changes = changes

    def accept(self, revision):
        is_suggestion = revision["uuid"] in [
            s["uuid"] for s in self.changes["pending"]["suggestions"]
        ]
        is_revision = revision["uuid"] in [
            r["uuid"] for r in self.changes["pending"]["revisions"]
        ]

        if not is_suggestion and not is_revision:
            raise ValueError("Revision not found in document.")

        if is_suggestion:
            self.changes["pending"]["suggestions"] = [
                s
                for s in self.changes["pending"]["suggestions"]
                if s["uuid"] != revision["uuid"]
            ]
            self.changes["accepted"]["suggestions"].append(revision)

        if is_revision:
            self.changes["pending"]["revisions"] = [
                r
                for r in self.changes["pending"]["revisions"]
                if r["uuid"] != revision["uuid"]
            ]

            revision_index = revision["index"]

            second_instance = revision["text"].split("/")[1]

            # get index of first newline after revision
            end_of_revision = self._last_occuring_instance(
                self.contents[:revision_index], second_instance
            )

            # remove revision from document

            # replace end of revision with new text
            text = revision["text"].split("/")[2]

            new_text = (
                self.contents[:end_of_revision]
                + text
                + self.contents[end_of_revision + len(second_instance) :]
            )

            # get index of [R: /old text/new text/]
            index_of_text = new_text.index(revision["text"])

            # remove revision["text"] from new_text
            revision_text = revision["text"]

            # -1 for space character length

            new_text = (
                new_text[: index_of_text - 1]
                + new_text[index_of_text + len(revision_text) :]
            )

            self.contents = new_text

            self.changes["accepted"]["revisions"].append(revision)

    def save_document(self, file_path):
        with open(file_path, "w") as file:
            file.write(self.contents)

    def _get_sentence(self, full_doc, text):
        # get index of text
        index = full_doc.index(text)

        # get index of first newline after text
        end_of_text = full_doc.index("\n", index)

        # get index of last newline before text
        start_of_text = full_doc.rindex("\n", 0, index)

        # get sentence
        sentence = full_doc[start_of_text:end_of_text]

        return sentence

    def interactive_accept(self, items):
        if "revisions" in items:
            for revision in document.changes["pending"]["revisions"]:
                # get sentence of revision
                while True:
                    print(self._get_sentence(document.contents, revision["text"]))

                    current = revision["text"].split("/")[1]
                    new = revision["text"].split("/")[2]

                    print(f"\nCurrent: {current}")
                    print(f"New: {new}\n")

                    accept = input("Accept? (y/n/i): ").lower()

                    # if accept == "i", print suggestion then ask again
                    if accept == "i":
                        print(revision)

                    if accept == "y" or accept == "yes":
                        document.accept(revision)
                        break

                print()

        if "suggestions" in items:
            for suggestion in document.changes["pending"]["suggestions"]:
                # get sentence of suggestion
                print(self._get_sentence(document.contents, suggestion["text"]))

                accept = input("Finished reviewing? (y/n): ").lower()

                if accept == "y" or accept == "yes":
                    document.accept(suggestion)

                print()


document = Document()

document.read_from_file("/Users/James/Documents/The Song Part II.md")

document.parse_document()

document.interactive_accept(["revisions", "suggestions"])

document.save_document("annotate_test.md")
