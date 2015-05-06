from bs4 import UnicodeDammit

def get_encoding(page):
    # Pass in html to UnicodeDammit for encoding detection
    page = UnicodeDammit(page)
    enc = page.original_encoding
    return enc

# def custom_decode(encoding):
#     """Overrides encoding when charset declaration
#        or charset determination is a subset of a larger
#        charset.  Created because of issues with Chinese websites"""
#     encoding = encoding.lower()
#     alternates = {
#         'big5': 'big5hkscs',
#         'gb2312': 'gb18030',
#         'ascii': 'utf-8',
#         'MacCyrillic': 'cp1251',
#     }
#     if encoding in alternates:
#         return alternates[encoding]
#     else:
#         return encoding
