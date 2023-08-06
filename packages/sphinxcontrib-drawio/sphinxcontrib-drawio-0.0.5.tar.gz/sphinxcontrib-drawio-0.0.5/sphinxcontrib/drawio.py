import os.path
import platform
import posixpath
import subprocess
from hashlib import sha1
from typing import Dict, Any, List

import sphinx
from docutils import nodes
from docutils.nodes import Node
from docutils.parsers.rst import directives
from sphinx.application import Sphinx
from sphinx.errors import SphinxError
from sphinx.util import logging, ensuredir
from sphinx.util.docutils import SphinxDirective, SphinxTranslator
from sphinx.util.fileutil import copy_asset
from sphinx.writers.html import HTMLTranslator

logger = logging.getLogger(__name__)

VALID_OUTPUT_FORMATS = ("png", "jpg", "svg")


class DrawIOError(SphinxError):
    category = 'DrawIO Error'


def align_spec(argument: Any) -> str:
    return directives.choice(argument, ("left", "center", "right"))


# noinspection PyPep8Naming
class DrawIONode(nodes.General, nodes.Inline, nodes.Element):
    pass


class DrawIO(SphinxDirective):
    has_content = False
    required_arguments = 1
    optional_arguments = 1
    final_argument_whitespace = True
    option_spec = {
        "alt"  : directives.unchanged,
        "align": align_spec,
    }

    def run(self) -> List[Node]:
        if self.arguments:
            rel_filename, filename = self.env.relfn2path(self.arguments[0])
            self.env.note_dependency(rel_filename)
            if not os.path.exists(filename):
                return [self.state.document.reporter.warning(
                    "External draw.io file {} not found.".format(filename),
                    lineno=self.lineno
                )]

        else:
            return [self.state_machine.reporter.warning(
                "Ignoring 'drawio' directive without argument.",
                line=self.lineno,
            )]

        node = DrawIONode()
        node["filename"] = filename
        if "alt" in self.options:
            node["alt"] = self.options["alt"]
        if "align" in self.options:
            node["align"] = self.options["align"]

        node["doc_name"] = self.env.docname

        self.add_name(node)
        return [node]


def render_drawio(self: SphinxTranslator, node: DrawIONode, in_filename: str,
                  output_format: str) -> str:
    """Render drawio file into an output image file."""

    # Any directive options which would change the output file would go here
    unique_values = (
        # This ensures that the same file hash is generated no matter the build directory
        # Mainly useful for pytest, as it creates a new build directory every time
        node["filename"].replace(self.builder.srcdir, ""),
    )
    hash_key = "\n".join(unique_values)
    sha_key = sha1(hash_key.encode()).hexdigest()
    filename = "drawio-{}.{}".format(sha_key, output_format)
    file_path = posixpath.join(self.builder.imgpath, filename)
    out_file_path = os.path.join(self.builder.outdir, self.builder.imagedir,
                                 filename)

    if os.path.isfile(out_file_path):
        return file_path

    ensuredir(os.path.dirname(out_file_path))

    if self.builder.config.drawio_binary_path:
        binary_path = self.builder.config.drawio_binary_path
    elif platform.system() == "Windows":
        binary_path = r"C:\Program Files\draw.io\draw.io.exe"
    else:
        binary_path = "/opt/draw.io/drawio"

    drawio_args = [
        binary_path,
        "--no-sandbox",
        "--export",
        "--format",
        output_format,
        "--output",
        out_file_path,
        in_filename,
    ]

    if self.builder.config.drawio_headless:
        # This can only be added if true, an empty string is bad
        drawio_args.insert(0, "xvfb-run")

    doc_name = node.get("doc_name", "index")
    cwd = os.path.dirname(os.path.join(self.builder.srcdir, doc_name))

    try:
        ret = subprocess.run(drawio_args, stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE, cwd=cwd, check=True)
        if not os.path.isfile(out_file_path):
            raise DrawIOError("draw.io did not produce an output file:"
                              "\n[stderr]\n{}\n[stdout]\n{}"
                              .format(ret.stderr, ret.stdout))
        return file_path
    except OSError as exc:
        raise DrawIOError("draw.io ({}) exited with error:\n{}"
                          .format(" ".join(drawio_args), exc))
    except subprocess.CalledProcessError as exc:
        raise DrawIOError("draw.io ({}) exited with error:\n[stderr]\n{}"
                          "\n[stdout]\n{}".format(" ".join(drawio_args),
                                                  exc.stderr, exc.stdout))


def render_drawio_html(self: HTMLTranslator, node: DrawIONode) -> None:
    output_format = self.builder.config.drawio_output_format
    filename = node["filename"]
    try:
        if output_format not in VALID_OUTPUT_FORMATS:
            raise DrawIOError("drawio_output_format must be one of {}, but is {}"
                              .format(", ".join(VALID_OUTPUT_FORMATS),
                                      output_format))
        file_path = render_drawio(self, node, filename, output_format)
    except DrawIOError as e:
        logger.warning("drawio filename: {}: {}".format(filename, e))
        raise nodes.SkipNode

    alt = node.get("alt", file_path)
    if "align" in node:
        self.body.append('<div align="{0}" class="align-{0}">'.format(node["align"]))

    if output_format == "svg":
        self.body.append('<div class="drawio">')
        self.body.append('<object data="{}" type="image/svg+xml"'
                         'class="drawio">\n'.format(file_path))
        self.body.append('<p class="warning">{}</p>'.format(alt))
        self.body.append('</object></div>\n')
    else:
        self.body.append('<div class="drawio">')
        self.body.append('<img src="{}" alt="{}" class="drawio" />'
                         .format(file_path, alt))

    if "align" in node:
        self.body.append('</div>\n')

    raise nodes.SkipNode


def on_build_finished(app: Sphinx, exc: Exception) -> None:
    if exc is None:
        this_file_path = os.path.dirname(os.path.realpath(__file__))
        src = os.path.join(this_file_path, "drawio.css")
        dst = os.path.join(app.outdir, "_static")
        copy_asset(src, dst)


def setup(app: Sphinx) -> Dict[str, Any]:
    app.add_node(DrawIONode, html=(render_drawio_html, None))
    app.add_directive("drawio", DrawIO)
    app.add_config_value("drawio_output_format", "png", "html")
    app.add_config_value("drawio_binary_path", None, "html")
    app.add_config_value("drawio_headless", True, "html")

    # Add CSS file to the HTML static path for add_css_file
    app.connect("build-finished", on_build_finished)
    app.add_css_file("drawio.css")

    # TODO: Check for parallel read and write safe
    return {"version": sphinx.__display_version__}
