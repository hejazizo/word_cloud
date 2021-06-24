import json
from pathlib import Path
from hazm import *
from pprint import pprint

with Path("./result.json").open() as f:
    conv = json.load(f)

with Path('./chat_before_2.html').open() as f:
    chat_before = f.read()

with Path('./chat_after_2.html').open() as f:
    chat_after = f.read()

ignore_list = [
    "این پیامت ☝️ رو دید!",
    "📬 شما یک پیام ناشناس جدید دارید !\n\nجهت دریافت کلیک کنید 👈 ",
    "☝️ در حال پاسخ دادن به فرستنده این پیام هستی ... ؛ منتظریم بفرستی :)",
    "پیام شما ارسال شد 😊\n\nچه کاری برات انجام بدم؟",
    "متوجه نشدم :/\n\nچه کاری برات انجام بدم؟",
    "حله!\n\nچه کاری برات انجام بدم؟",
    "در حال ارسال پیام ناشناس به samaneh هستی.\n\nمی‌تونی هر حرف یا انتقادی که تو دلت هست رو بگی چون پیامت به صورت کاملا ناشناس ارسال می‌شه!",
    "انصراف",
    "راهنما",
    "🏆 افزایش امتیاز",
    "💌 به مخاطب خاصم وصلم کن!",
    """برای اینکه بتونم به مخاطب خاصت بطور ناشناس وصلت کنم، یکی از این ۲ کار رو انجام بده:"""
]

receiver = {
    'name': 'Ali',
    'image': "https://pbs.twimg.com/profile_images/1294419611371188224/o3fJPsuT_400x400.jpg",
    "id": 73106435
}

sender = {
    'name': 'Sama',
    'image': "https://pbs.twimg.com/profile_images/1293331018238160898/87no1XY0_400x400.jpg",
    "id": 395365604
}

template_left = """
<li class="sent">
    <img src="{image}" alt="" />
    <p dir="rtl" style="text-align:right;">{spans}</p>
</li>
"""
template_right = """
<li class="replies">
    <img src="{image}" alt="" />
    <p dir="rtl" style="text-align:right;">{spans}</p>
</li>
"""

audio_template = """<audio controls>
  <source src="{src}" type="{type}">
</audio></br>"""

image_template_left = """<img src="{src}" alt="" width="250px" max-width="40%" style="padding-left: 50px; padding-bottom: 20px;"/></br>"""
image_template_right = """<img src="{src}" alt="" width="250px" max-width="40%" style="float: right; padding-right: 40px; padding-bottom: 20px;"/></br><div style="clear:both"></div>"""

span = """<p class="uk-margin-remove">{text}</p>"""

html = chat_before


text = ""
from collections import Counter
c = Counter()

for msg in conv['messages']:

    if msg.get("media_type"):
        if msg["media_type"] == "animation" and msg.get("thumbnail"):
            if msg.get("from_id") == receiver['id']:
                html += image_template_left.format(src=msg["thumbnail"])
            else:
                html += image_template_right.format(src=msg["thumbnail"])

        elif msg["media_type"] == "voice_message":
            html += audio_template.format(src=msg["file"], type=msg["mime_type"])

    if type(msg.get("text")) == str:
        if msg.get("text") not in ignore_list and not msg.get("text").startswith("برای اینکه بتونم به مخاطب خاصت بطور"):
            if msg.get("text"):
                spans = ""
                for line in msg.get("text").strip().split('\n'):
                    spans += f"{line}</br>"
                if msg.get("from_id") == receiver['id']:
                    html += template_left.format(spans=spans, image=receiver.get("image"))
                    c += Counter(word_tokenize(msg.get("text")))
                    text += " ".join(word_tokenize(msg.get("text")))
                else:
                    html += template_right.format(spans=msg.get("text").replace('\u200c', '').strip(), image=sender.get("image"))

        if msg.get("photo"):
            if msg.get("from_id") == receiver['id']:
                html += image_template_left.format(src=msg["photo"])
            else:
                html += image_template_right.format(src=msg["photo"])


html += chat_after

with Path('./final.html').open('w') as f:
    f.write(html)


###############################################
################ WORD CLOUD ###################
import os
import codecs
from wordcloud import WordCloud
import arabic_reshaper
from bidi.algorithm import get_display

# get data directory (using getcwd() is needed to support running example in generated IPython notebook)
d = os.path.dirname(__file__) if "__file__" in locals() else os.getcwd()

# remove stop words
with open('./stop_words.txt') as f:
    stop_words = f.read().split('\n')

# Read the whole text.
tokens = word_tokenize(text)
tokens = [w for w in tokens if w not in stop_words]
text = ' '.join(tokens)

# Read the whole text.
# f = codecs.open(os.path.join(d, 'arabicwords.txt'), 'r', 'utf-8')
pprint(Counter(tokens).most_common(100))
with open('./stats.txt', 'w') as f:
    most_common = [f'{w[0]}: {w[1]}' for w in Counter(tokens).most_common(100)]

    f.write('\n'.join(most_common))

# Make text readable for a non-Arabic library like wordcloud
text = arabic_reshaper.reshape(text)
text = get_display(text)

# Generate a word cloud image
wordcloud = WordCloud(background_color="white", width=900, height=400, font_path='fonts/NotoNaskhArabic/NotoNaskhArabic-Regular.ttf').generate(text)

# Export to an image
wordcloud.to_file("sama.png")
pprint(c)


# links
pattern = """(?i)\b((?:https?:(?:/{1,3}|[a-z0-9%])|[a-z0-9.\-]+[.](?:com|net|org|edu|gov|mil|aero|asia|biz|cat|coop|info|int|jobs|mobi|museum|name|post|pro|tel|travel|xxx|ac|ad|ae|af|ag|ai|al|am|an|ao|aq|ar|as|at|au|aw|ax|az|ba|bb|bd|be|bf|bg|bh|bi|bj|bm|bn|bo|br|bs|bt|bv|bw|by|bz|ca|cc|cd|cf|cg|ch|ci|ck|cl|cm|cn|co|cr|cs|cu|cv|cx|cy|cz|dd|de|dj|dk|dm|do|dz|ec|ee|eg|eh|er|es|et|eu|fi|fj|fk|fm|fo|fr|ga|gb|gd|ge|gf|gg|gh|gi|gl|gm|gn|gp|gq|gr|gs|gt|gu|gw|gy|hk|hm|hn|hr|ht|hu|id|ie|il|im|in|io|iq|ir|is|it|je|jm|jo|jp|ke|kg|kh|ki|km|kn|kp|kr|kw|ky|kz|la|lb|lc|li|lk|lr|ls|lt|lu|lv|ly|ma|mc|md|me|mg|mh|mk|ml|mm|mn|mo|mp|mq|mr|ms|mt|mu|mv|mw|mx|my|mz|na|nc|ne|nf|ng|ni|nl|no|np|nr|nu|nz|om|pa|pe|pf|pg|ph|pk|pl|pm|pn|pr|ps|pt|pw|py|qa|re|ro|rs|ru|rw|sa|sb|sc|sd|se|sg|sh|si|sj|Ja|sk|sl|sm|sn|so|sr|ss|st|su|sv|sx|sy|sz|tc|td|tf|tg|th|tj|tk|tl|tm|tn|to|tp|tr|tt|tv|tw|tz|ua|ug|uk|us|uy|uz|va|vc|ve|vg|vi|vn|vu|wf|ws|ye|yt|yu|za|zm|zw)/)(?:[^\s()<>{}\[\]]+|\([^\s()]*?\([^\s()]+\)[^\s()]*?\)|\([^\s]+?\))+(?:\([^\s()]*?\([^\s()]+\)[^\s()]*?\)|\([^\s]+?\)|[^\s`!()\[\]{};:'".,<>?«»“”‘’])|(?:(?<!@)[a-z0-9]+(?:[.\-][a-z0-9]+)*[.](?:com|net|org|edu|gov|mil|aero|asia|biz|cat|coop|info|int|jobs|mobi|museum|name|post|pro|tel|travel|xxx|ac|ad|ae|af|ag|ai|al|am|an|ao|aq|ar|as|at|au|aw|ax|az|ba|bb|bd|be|bf|bg|bh|bi|bj|bm|bn|bo|br|bs|bt|bv|bw|by|bz|ca|cc|cd|cf|cg|ch|ci|ck|cl|cm|cn|co|cr|cs|cu|cv|cx|cy|cz|dd|de|dj|dk|dm|do|dz|ec|ee|eg|eh|er|es|et|eu|fi|fj|fk|fm|fo|fr|ga|gb|gd|ge|gf|gg|gh|gi|gl|gm|gn|gp|gq|gr|gs|gt|gu|gw|gy|hk|hm|hn|hr|ht|hu|id|ie|il|im|in|io|iq|ir|is|it|je|jm|jo|jp|ke|kg|kh|ki|km|kn|kp|kr|kw|ky|kz|la|lb|lc|li|lk|lr|ls|lt|lu|lv|ly|ma|mc|md|me|mg|mh|mk|ml|mm|mn|mo|mp|mq|mr|ms|mt|mu|mv|mw|mx|my|mz|na|nc|ne|nf|ng|ni|nl|no|np|nr|nu|nz|om|pa|pe|pf|pg|ph|pk|pl|pm|pn|pr|ps|pt|pw|py|qa|re|ro|rs|ru|rw|sa|sb|sc|sd|se|sg|sh|si|sj|Ja|sk|sl|sm|sn|so|sr|ss|st|su|sv|sx|sy|sz|tc|td|tf|tg|th|tj|tk|tl|tm|tn|to|tp|tr|tt|tv|tw|tz|ua|ug|uk|us|uy|uz|va|vc|ve|vg|vi|vn|vu|wf|ws|ye|yt|yu|za|zm|zw)\b/?(?!@)))"""
import re
