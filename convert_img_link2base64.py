import os
import re
import base64

import sys
sys.path.append("/home/jurgis/Dokumentai/OLD\ PC/FTP\ \ GALVOSUKYKLA.LT/moodle\ quiz\ imgs")

fname = "moodle.coding/questions.xml"
with open(fname) as f:
    xml_in = f.read()

xml_out = xml_in[:]

results = []
etc_links = []
for url in re.findall(r'img src="([^"]+)"', xml_in):
    if url.lower().startswith('data:image'):
        continue

    if not url.startsiwth('http://galvosukykla.lt/moodle_code_quiz.img/'):
        etc_links.append(url)


    url = url.replace('%20', ' ')
    local_path = url.replace("http://galvosukykla.lt/moodle_code_quiz.img/", "moodle_code_quiz.img/")
    print(local_path)

    try:
        encoded = base64.b64encode(open(local_path, "rb").read())
        dataurl = replacement = f"data:image/png;base64,{encoded.decode()}"
        results.append([local_path, dataurl])

        print(len(results), local_path, dataurl[:70])
        xml_out = xml_out.replace(url, dataurl)
    except FileNotFoundError as e:
        print(len(results), "ERR", e)


with open('out.xml', 'w') as f:
    f.write(xml_out)



html = ""
for nr, (url, dataurl) in enumerate(results):
    html += f"\n<tr><td>nr</td><td>{url}<br> <img src='{url}'> </td> " \
            f"<td> <img src='{dataurl}'> </td> </tr>"

html = f"<html><body><table>{html}</table></body></html>"

with open('out.html', 'w') as f:
    f.write(html)


print(f"{etc_links=}")