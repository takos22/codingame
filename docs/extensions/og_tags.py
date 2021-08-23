# credits to: Takayuki Shimizukawa @ Sphinx-users.jp
# based on:
# https://github.com/sphinx-contrib/ogp/blob/master/sphinxcontrib_ogp/ext.py

import os
from typing import Any, Dict, List, Tuple
from urllib.parse import urlparse, urlunparse
from docutils import nodes
from sphinx import addnodes
from sphinx.application import Sphinx, Config
from urllib.parse import urljoin


class Visitor:
    def __init__(self, document: nodes.Node, config: Config):
        self.document = document
        self.config = config
        self.text_list = []
        self.images = []
        self.n_sections = 0

    def dispatch_visit(self, node):
        # skip toctree
        if isinstance(node, addnodes.compact_paragraph) and node.get("toctree"):
            raise nodes.SkipChildren

        # collect images
        if isinstance(node, nodes.image):
            self.images.append(node)

        # collect 3 first sections
        if self.n_sections < 3:

            # collect text
            if isinstance(node, nodes.paragraph):
                self.text_list.append(node.astext())

            # add depth
            if isinstance(node, nodes.section):
                self.n_sections += 1

    def dispatch_departure(self, node):
        pass

    def get_og_description(self):
        text = " ".join(self.text_list)
        desc_length = self.config["og_desc_length"]
        if len(text) > desc_length:
            text = text[: desc_length - 3] + "..."
        return text

    def get_og_image_url(self, page_url: str):
        if self.images:
            return urljoin(page_url, self.images[0]["uri"])
        else:
            return None


def get_og_tags(context: Dict[str, Any], doctree: nodes.Node, config: Config):
    if os.getenv("READTHEDOCS") and config["og_site_url"] is None:
        if config["html_baseurl"] is None:
            raise EnvironmentError(
                "ReadTheDocs did not provide a valid canonical URL!"
            )

        # readthedocs uses html_baseurl for sphinx > 1.8
        parse_result = urlparse(config["html_baseurl"])

        # Grab root url from canonical url
        config["og_site_url"] = urlunparse(
            (
                parse_result.scheme,
                parse_result.netloc,
                parse_result.path,
                "",
                "",
                "",
            )
        )

    # page_url
    site_url = config["og_site_url"]
    page_url = urljoin(site_url, context["pagename"] + context["file_suffix"])

    # collection
    visitor = Visitor(doctree, config)
    doctree.walkabout(visitor)

    # og:title
    og_title = config["og_title"] or context["title"]

    # og:site_name
    og_site_name = config["og_site_name"] or context["shorttitle"]

    # og:description
    og_desc = config["og_desc"] or visitor.get_og_description()

    # og:image
    og_image = config["og_image"] or visitor.get_og_image_url(page_url)

    # OG tags
    tags = """
    <meta property="og:title" content="{title}">
    <meta property="og:description" content="{desc}">
    <meta property='og:url' content="{page_url}">
    <meta property="og:site_name" content="{site_name}">
    <meta name="twitter:card" content="summary" />
    """.format(
        title=og_title,
        desc=og_desc,
        page_url=page_url,
        site_name=og_site_name,
    )
    if og_image:
        tags += '<meta property="og:image" content="{url}">'.format(
            url=og_image
        )
    return tags


def html_page_context(
    app: Sphinx,
    pagename: str,
    templatename: str,
    context: Dict[str, Any],
    doctree,
):
    if not doctree:
        return

    context["metatags"] += get_og_tags(context, doctree, app.config)


def setup(app: Sphinx) -> Dict[str, Any]:
    app.add_config_value("og_site_url", None, "html")
    app.add_config_value("og_title", None, "html")
    app.add_config_value("og_site_name", None, "html")
    app.add_config_value("og_desc", None, "html")
    app.add_config_value("og_desc_length", 200, "html")
    app.add_config_value("og_image", None, "html")
    app.connect("html-page-context", html_page_context)
    return {
        "version": "0.1.0",
        "parallel_read_safe": True,
        "parallel_write_safe": True,
    }
