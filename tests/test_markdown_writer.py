from mdcrawler.content_extractor import ImageReference
from mdcrawler.crawler import Page
from mdcrawler.markdown_writer import render_markdown


def test_render_markdown_replaces_image_tokens() -> None:
    page = Page(
        url="https://example.com/docs/start",
        title="Title",
        markdown="Intro [[IMAGE_0]]",
        images=[
            ImageReference(token="[[IMAGE_0]]", url="https://example.com/image.png", alt="Logo")
        ],
    )
    page.images[0].filename = "example.com-logo.png"

    rendered = render_markdown(page, image_prefix="../images/")

    assert rendered == "Intro ![Logo](../images/example.com-logo.png)"
