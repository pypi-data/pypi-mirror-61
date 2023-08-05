# coding: utf8

from auditorium import Show
from typing import List
from auditorium.utils import path


def load_markdown_demo():
    return Show.load(path("./static/md/demo.md"))


class MarkdownLoader:
    def __init__(self, path, instance_name="ctx"):
        self.path = path
        self.instance_name = instance_name

    def parse(self):
        slides = []
        current_slide = []

        with open(self.path) as fp:
            for line in fp:
                line = line.strip("\n")

                if line.startswith("## ") and current_slide:
                    slides.append(current_slide)
                    current_slide = []

                current_slide.append(line)

            if current_slide:
                slides.append(current_slide)

        show = Show()

        for i, slide in enumerate(slides):
            show.slide(func=MarkdownSlide(show, slide), id="slide-%i" % (i + 1))

        return show


class MarkdownSlide:
    def __init__(self, show: Show, content):
        self.show = show
        self.content: List[Content] = []

        state = "markdown"  # or 'code'
        language = ""
        code_start = ""
        split: List[str] = []

        for line in content:
            if state == "markdown":
                if line.startswith("```") or line.startswith("~~~"):
                    if split:
                        self.content.append(MarkdownContent(split))

                    split = []
                    state = "code"
                    code_start = line[:3]
                    language = line[3:].split()[0]
                    tags = line[3:].split()[1:]
                else:
                    split.append(line)

            elif state == "code":
                if line == code_start:
                    if split:
                        self.content.append(CodeContent(split, language, tags))

                    split = []
                    state = "markdown"
                else:
                    split.append(line)

        if split:
            if state == "markdown":
                self.content.append(MarkdownContent(split))
            else:
                raise ValueError("Didn't closed a code line...")

    def __call__(self, ctx):
        global_context = dict(ctx=ctx)

        for content in self.content:
            content(ctx, global_context)


class Content:
    def __call__(self, show, global_context):
        self._call(show, global_context)


class MarkdownContent(Content):
    def __init__(self, lines):
        self.lines = "\n".join(lines)

    def _call(self, show, global_context):
        show.markdown(self.lines.format(**global_context))


class CodeContent(Content):
    def __init__(self, lines, language, tags):
        self.lines = "\n".join(lines)
        self.tags = tags
        self.language = language

    def _call(self, show, global_context):
        run = ":run" in self.tags
        echo = not run or ":echo" in self.tags
        persist = ":persist" in self.tags

        local_context = dict()

        if run:
            exec(self.lines, global_context, local_context)

        if echo:
            show.code(self.lines, self.language)

        if persist:
            global_context.update(local_context)
