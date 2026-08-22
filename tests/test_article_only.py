import os
import time
import unittest

from readability import Document
from functools import wraps


class TimeoutException(Exception):
    """Exception raised when a function exceeds its time limit."""
    pass


def timeout(seconds):
    """Decorator to enforce a timeout on function execution."""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            start_time = time.perf_counter()
            result = func(*args, **kwargs)
            end_time = time.perf_counter()
            elapsed_time = end_time - start_time
            if elapsed_time > seconds:
                raise TimeoutException(
                    f"Function '{func.__name__}' exceeded time limit of {seconds} seconds "
                    f"with an execution time of {elapsed_time:.4f} seconds"
                )
            return result
        return wrapper
    return decorator


SAMPLES = os.path.join(os.path.dirname(__file__), "samples")


def load_sample(filename):
    """Helper to get the content out of the sample files"""
    with open(os.path.join(SAMPLES, filename)) as f:
        html = f.read()
    return html


class TestArticleOnly(unittest.TestCase):
    """The option to not get back a full html doc should work

    Given a full html document, the call can request just divs of processed
    content. In this way the developer can then wrap the article however they
    want in their own view or application.

    """

    def test_si_sample(self):
        """Using the si sample, load article with only opening body element"""
        sample = load_sample("si-game.sample.html")
        doc = Document(
            sample,
            url="http://sportsillustrated.cnn.com/baseball/mlb/gameflash/2012/04/16/40630_preview.html",
        )
        res = doc.summary()
        self.assertEqual("<html><body><div><div class", res[0:27])

    def test_si_sample_html_partial(self):
        """Using the si sample, make sure we can get the article alone."""
        sample = load_sample("si-game.sample.html")
        doc = Document(
            sample,
            url="http://sportsillustrated.cnn.com/baseball/mlb/gameflash/2012/04/16/40630_preview.html",
        )
        res = doc.summary(html_partial=True)
        self.assertEqual('<div><div class="', res[0:17])

    def test_too_many_images_sample_html_partial(self):
        """Using the too-many-images sample, make sure we still get the article."""
        sample = load_sample("too-many-images.sample.html")
        doc = Document(sample)
        res = doc.summary(html_partial=True)
        self.assertEqual('<div><div class="post-body', res[0:26])

    def test_wrong_link_issue_49(self):
        """We shouldn't break on bad HTML."""
        sample = load_sample("the-hurricane-rubin-carter-denzel-washington.html")
        doc = Document(sample)
        res = doc.summary(html_partial=True)
        self.assertEqual('<div><div class="content__article-body ', res[0:39])

    def test_best_elem_is_root_and_passing(self):
        sample = (
            '<html class="article" id="body">'
            "   <body>"
            "       <p>1234567890123456789012345</p>"
            "   </body>"
            "</html>"
        )
        doc = Document(sample)
        doc.summary()

    def test_correct_cleanup(self):
        sample = """
        <html>
            <body>
                <section>test section</section>
                <article class="">
<p>Lot of text here.</p>
                <div id="advertisement"><a href="link">Ad</a></div>
<p>More text is written here, and contains punctuation and dots.</p>
</article>
                <aside id="comment1"/>
                <div id="comment2">
                    <a href="asd">spam</a>
                    <a href="asd">spam</a>
                    <a href="asd">spam</a>
                </div>
                <div id="comment3"/>
                <aside id="comment4">A small comment.</aside>
                <div id="comment5"><p>The comment is also helpful, but it's
                    still not the correct item to be extracted.</p>
                    <p>It's even longer than the article itself!"</p></div>
            </body>
        </html>
        """
        doc = Document(sample)
        s = doc.summary()
        # print(s)
        assert "punctuation" in s
        assert "comment" not in s
        assert "aside" not in s

    def test_preserves_comments_in_code_blocks(self):
        article_text = "Reliable article sentence with punctuation. " * 20
        sample = f"""
        <html><body><article>
            <pre><code>value = 1
                <span class="comment"># keep this comment</span>
                print(value)
            </code></pre>
            <p>{article_text}</p>
        </article></body></html>
        """

        summary = Document(sample).summary()

        self.assertIn("# keep this comment", summary)

    def test_preserves_inline_links_in_paragraph(self):
        article_text = "This is ordinary article text with punctuation. " * 8
        sample = f"""
        <html><body><div class="article">
            Games include <a href="/one">MMORPG</a> and
            <a href="/two">MOBA</a>. {article_text}
        </div></body></html>
        """

        summary = Document(sample).summary(html_partial=True)

        self.assertIn('<p class="article">', summary)
        self.assertIn('<a href="/one">MMORPG</a>', summary)
        self.assertNotIn("</p><a ", summary)

    def test_preserves_inline_elements_in_mixed_div(self):
        article_text = "This is ordinary article text with punctuation. " * 8
        sample = f"""
        <html><body><div class="article">
            Before <i>important words</i> after them. {article_text}
            <br><br>Another article paragraph. {article_text}
            <div class="clear"></div>
        </div></body></html>
        """

        summary = Document(sample).summary(html_partial=True)

        self.assertIn("Before <i>important words</i> after them.", summary)
        self.assertNotIn("</p><i>", summary)

    def test_removes_inline_display_none(self):
        article_text = "This is ordinary article text with punctuation. " * 8
        sample = f"""
        <html><body><article>
            <div style="color: red; DISPLAY: none !important">Hidden content</div>
            <p>{article_text}</p>
        </article></body></html>
        """

        summary = Document(sample).summary()

        self.assertNotIn("Hidden content", summary)
        self.assertIn("ordinary article text", summary)

    def test_removes_noscript_content(self):
        article_text = "This is ordinary article text with punctuation. " * 8
        fallback_text = "Encoded advertising fallback content. " * 20
        sample = f"""
        <html><body><article>
            <p>{article_text}</p>
            <noscript><div><p>{fallback_text}</p></div></noscript>
        </article></body></html>
        """

        summary = Document(sample).summary()

        self.assertIn("ordinary article text", summary)
        self.assertNotIn("advertising fallback", summary)

    def test_preserves_main_inside_sidebar_layout(self):
        article_text = "This is the primary article with useful information. " * 10
        sample = f"""
        <html><body>
            <div class="container sidebar-right">
                <header>Site navigation and branding</header>
                <main><div class="article-content"><p>{article_text}</p></div></main>
                <aside>Unrelated sidebar</aside>
            </div>
        </body></html>
        """

        summary = Document(sample).summary()

        self.assertIn("primary article", summary)
        self.assertNotIn("Site navigation and branding", summary)

    def test_preserves_article_inside_unlikely_wrapper(self):
        article_text = (
            "This is the primary medical article, with useful details, facts, "
            "and explanatory context. " * 16
        )
        modal_text = "Privacy settings and modal information, " * 12
        sample = f"""
        <html><body>
            <div class="row site_header">
                <article><div class="article-body"><p>{article_text}</p></div></article>
            </div>
            <div class="modal-body container"><p>{modal_text}</p></div>
        </body></html>
        """

        summary = Document(sample).summary()

        self.assertIn("primary medical article", summary)
        self.assertNotIn("Privacy settings", summary)

    def test_recovers_editorial_lead_from_article(self):
        article_text = (
            "This is the primary article with useful information. " * 10
        )
        sample = f"""
        <html><body><article>
            <header>
                <p class="article__subhead">
                    A concise introduction that explains the story before
                    the body.
                </p>
            </header>
            <div class="layout"><div class="article-content">
                <p>{article_text}</p>
            </div></div>
        </article></body></html>
        """

        summary = Document(sample).summary()

        self.assertIn("concise introduction", summary)
        self.assertIn("primary article", summary)

    def test_recovers_hyphenated_story_lead(self):
        article_text = (
            "This is the primary article with useful information. " * 10
        )
        sample = f"""
        <html><body><main>
            <div class="views-field-field-news-story-lead">
                A newsroom lead placed outside the scored body container.
            </div>
            <div class="layout"><div class="article-content">
                <p>{article_text}</p>
            </div></div>
        </main></body></html>
        """

        summary = Document(sample).summary()

        self.assertIn("newsroom lead", summary)
        self.assertIn("primary article", summary)

    def test_does_not_recover_linked_editorial_promo(self):
        article_text = (
            "This is the primary article with useful information. " * 10
        )
        sample = f"""
        <html><body><article>
            <div class="subtitle">
                <a href="/newsletter">Subscribe to our daily newsletter</a>
            </div>
            <div class="layout"><div class="article-content">
                <p>{article_text}</p>
            </div></div>
        </article></body></html>
        """

        summary = Document(sample).summary()

        self.assertNotIn("daily newsletter", summary)
        self.assertIn("primary article", summary)

    def test_merges_segmented_article_containers(self):
        first_segment = "First segment of the article with useful details. " * 10
        second_segment = "Second segment continues the same article. " * 8
        related_links = "Related navigation link. " * 12
        sample = f"""
        <html><body><article>
            <section><div class="article-text">
                <p>{first_segment}</p>
            </div></section>
            <section><div class="article-text">
                <p>{second_segment}</p>
            </div></section>
            <section><div class="article-text">
                <p><a href="/related">{related_links}</a></p>
            </div></section>
        </article></body></html>
        """

        summary = Document(sample).summary()

        self.assertIn("First segment", summary)
        self.assertIn("Second segment", summary)
        self.assertNotIn("Related navigation", summary)

    def test_merges_segments_in_positive_container(self):
        first_segment = "First independent section with substantial article text. " * 12
        second_segment = "Second independent section continuing the same story. " * 10
        sample = f"""
        <html><body><div class="postBody">
            <section><div><div class="post__content article-text">
                <p>{first_segment}</p>
            </div></div></section>
            <section><div><div class="post__content article-text">
                <p>{second_segment}</p>
            </div></div></section>
        </div></body></html>
        """

        summary = Document(sample).summary()

        self.assertIn("First independent section", summary)
        self.assertIn("Second independent section", summary)

    def test_prefers_list_based_article_to_service_form(self):
        list_items = "".join(
            "<li>Article release note number {} with substantial useful "
            "information and punctuation.</li>".format(index)
            for index in range(30)
        )
        form_text = "Newsletter preferences, subscription options, " * 8
        sample = f"""
        <html><body><main>
            <article><div class="entry-content"><ul>{list_items}</ul></div></article>
            <aside><form><div class="form-contents">
                <p>{form_text}</p>
            </div></form></aside>
        </main></body></html>
        """

        summary = Document(sample).summary()

        self.assertIn("Article release note number 29", summary)
        self.assertNotIn("Newsletter preferences", summary)

    def test_recovers_heading_preamble_sibling(self):
        article_text = (
            "This is the primary article with useful information. " * 10
        )
        sample = f"""
        <html><body><article><div class="layout">
            <div class="hero">
                <h2>A substantial introductory heading before the article body.</h2>
            </div>
            <div class="article-content"><p>{article_text}</p></div>
        </div></article></body></html>
        """

        summary = Document(sample).summary()

        self.assertIn("introductory heading", summary)
        self.assertIn("primary article", summary)

    def test_does_not_recover_linked_heading_preamble(self):
        article_text = (
            "This is the primary article with useful information. " * 10
        )
        sample = f"""
        <html><body><article><div class="layout">
            <div class="hero"><h2><a href="/related">
                Read more stories selected for you in this related section.
            </a></h2></div>
            <div class="article-content"><p>{article_text}</p></div>
        </div></article></body></html>
        """

        summary = Document(sample).summary()

        self.assertNotIn("selected for you", summary)
        self.assertIn("primary article", summary)

    def test_removes_linked_calls_to_action(self):
        article_text = "This is ordinary article text with punctuation. " * 10
        sample = f"""
        <html><body><article>
            <p>{article_text}</p>
            <p><a href="/newsletter">Sign up for the weekly newsletter</a>,
                delivered to your inbox.</p>
            <div><a href="/app">Get the latest news. Download the app.</a></div>
            <p><a href="/release">www.python.org/downloads/release/</a></p>
        </article></body></html>
        """

        summary = Document(sample).summary()

        self.assertNotIn("weekly newsletter", summary)
        self.assertNotIn("Download the app", summary)
        self.assertIn("www.python.org/downloads/release/", summary)

    # Many spaces make some regexes run forever
    @timeout(3)
    def test_many_repeated_spaces(self):
        long_space = " " * 1000000
        sample = "<html><body><p>foo" + long_space + "</p></body></html>"

        doc = Document(sample)
        s = doc.summary()

        assert "foo" in s

    def test_not_self_closing(self):
        sample = '<h2><a href="#"></a>foobar</h2>'
        doc = Document(sample)
        assert (
            '<body id="readabilityBody"><h2><a href="#"></a>foobar</h2></body>'
            == doc.summary()
        )

    def test_utf8_kanji(self):
        """Using the UTF-8 kanji sample, load article which is written in kanji"""
        sample = load_sample("utf-8-kanji.sample.html")
        doc = Document(sample)
        res = doc.summary()
        assert 0 < len(res) < 10000

    def test_bytes_input_issue_194(self):
        html = b"""
        <html>
            <head><title>Bytes input</title></head>
            <body><article><p>
                This is article content supplied as bytes, with enough text for
                encoding detection.
            </p></article></body>
        </html>
        """
        doc = Document(html)

        self.assertEqual("Bytes input", doc.title())
        self.assertIn("article content supplied as bytes", doc.summary())

    def test_get_clean_html_parses_document(self):
        doc = Document("<html><body><p>Clean content</p></body></html>")

        self.assertIn("Clean content", doc.get_clean_html())

    def test_xpath_does_not_change_retry_length(self):
        main_text = "Main article sentence with enough words and punctuation. " * 3
        retained_text = "Important retained paragraph from the same article. " * 4
        html = f"""
        <html><body><div class="article">
            <p>{main_text}</p>
            <p class="comment">{retained_text}</p>
        </div></body></html>
        """

        plain_ruthless = Document(html, retry_length=0).summary(html_partial=True)
        xpath_ruthless = Document(html, retry_length=0, xpath=True).summary(
            html_partial=True
        )
        retry_length = (len(plain_ruthless) + len(xpath_ruthless)) // 2

        plain = Document(html, retry_length=retry_length).summary(html_partial=True)
        with_xpath = Document(html, retry_length=retry_length, xpath=True).summary(
            html_partial=True
        )

        self.assertIn(retained_text, plain)
        self.assertIn(retained_text, with_xpath)
        self.assertIn('x="/html/body/div"', with_xpath)

    def test_author_present(self):
        sample = load_sample("the-hurricane-rubin-carter-denzel-washington.html")
        doc = Document(sample)
        assert 'Alex von Tunzelmann' == doc.author()

    def test_author_absent(self):
        sample = load_sample("si-game.sample.html")
        doc = Document(sample)
        assert '[no-author]' == doc.author()

    def test_keep_images_present(self):
        sample = load_sample("summary-keep-all-images.sample.html")

        doc = Document(sample)

        assert "<img" in doc.summary(keep_all_images=True)

    def test_keep_images_absent(self):
        sample = load_sample("summary-keep-all-images.sample.html")

        doc = Document(sample)

        assert "<img" not in doc.summary(keep_all_images=False)

    def test_keep_images_absent_by_defautl(self):
        sample = load_sample("summary-keep-all-images.sample.html")

        doc = Document(sample)

        assert "<img" not in doc.summary()

    def test_cjk_summary(self):
        """Check we can extract CJK text correctly."""
        html = """
        <html>
            <head>
                <title>这是标题</title>
            </head>
            <body>
                <div>一些无关紧要的内容</div>
                <div class="article-content">
                    <h1>主要文章标题</h1>
                    <p>这是主要内容的第一段。</p>
                    <p>これはコンテンツの第2段落です。</p>
                    <p>이것은 콘텐츠의 세 번째 단락입니다.</p>
                    <p>This is the fourth paragraph.</p>
                </div>
                <div>More irrelevant stuff</div>
            </body>
        </html>
        """
        doc = Document(html)
        summary = doc.summary()
        # Check that the main CJK content is present in the summary
        self.assertTrue("这是主要内容的第一段" in summary)
        self.assertTrue("これはコンテンツの第2段落です" in summary)
        self.assertTrue("이것은 콘텐츠의 세 번째 단락입니다" in summary)
        # Check that irrelevant content is mostly gone
        self.assertFalse("一些无关紧要的内容" in summary)

    def test_shorten_title_delimiter_bug(self):
        """Test that shorten_title handles delimiters correctly when the last part is valid.

        This specifically targets a potential bug where 'p1' might be used instead of 'pl'.
        """
        html = """
        <html>
            <head>
                <title>Short Part | これは長いです</title>
            </head>
            <body>
                <div>Content</div>
            </body>
        </html>
        """
        doc = Document(html)
        # With the bug, this call might raise NameError: name 'p1' is not defined
        # With the fix, it should correctly return the last part.
        short_title = doc.short_title()
        self.assertEqual(short_title, "これは長いです")
