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

    def test_html_input_in_bytes(self):
        sample = (
            b'<html class="article" id="body">'
            b"   <body>"
            b"       <p>1234567890123456789012345</p>"
            b"   </body>"
            b"</html>"
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
        assert not "comment" in s
        assert not "aside" in s

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
