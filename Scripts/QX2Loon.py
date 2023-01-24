#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# @File    :   QX2Loon.py
# @Time    :   2023/01/16 19:01:27
# @Author  :   Howie Hye
# @Contact :   howiehye@163.com
# @Desc    :   None


import re
import requests


url_list = [
    "https://raw.githubusercontent.com/ddgksf2013/Rewrite/master/AdBlock/Amap.conf",
    "https://raw.githubusercontent.com/ddgksf2013/Rewrite/master/AdBlock/Applet.conf",
    "https://raw.githubusercontent.com/ddgksf2013/Rewrite/master/AdBlock/AppletAds.conf",
    "https://raw.githubusercontent.com/ddgksf2013/Rewrite/master/AdBlock/Bilibili.conf",
    "https://raw.githubusercontent.com/ddgksf2013/Rewrite/master/AdBlock/KeepStyle.conf",
    "https://raw.githubusercontent.com/ddgksf2013/Rewrite/master/AdBlock/StartUp.conf",
    "https://raw.githubusercontent.com/ddgksf2013/Rewrite/master/AdBlock/Weibo.conf",
    "https://raw.githubusercontent.com/ddgksf2013/Rewrite/master/AdBlock/XiaoHongShu.conf",
    "https://raw.githubusercontent.com/ddgksf2013/Rewrite/master/AdBlock/Ximalaya.conf",
    "https://raw.githubusercontent.com/ddgksf2013/Rewrite/master/AdBlock/YoutubeAds.conf"
]


def get_QX_content(url):
    r = requests.get(url)
    return r.text


def parse_content(content):
    # 重写
    regular_expression_for_rewrite = r".*?\surl\s(302|307|(reject(-\w+)?)).*"
    results = re.finditer(regular_expression_for_rewrite,
                          content, re.MULTILINE)
    return_content = "" + "[Rewrite]\n"
    for match in results:
        match = re.sub("\surl\s", " ", match.group()) + "\n"
        return_content += match

    # 引用
    regular_expression_for_script = r".*?\surl\sscript-(response|request)-body\s.*?\.js"
    results = re.finditer(regular_expression_for_script, content, re.MULTILINE)
    return_content += "\n\n[Script]\n"

    for match in results:
        match = match.group()
        url_pat = re.findall(r"(.*?)\surl\s", match)[0]
        http_type = re.findall(r"(response|request)", match)[0]
        script_url = re.findall(r"-body\s(.*?)\.js", match)[0] + ".js"
        tag = re.findall(r"body\s.*\/(.*?)\.js", match)[0]
        response = f"http-{http_type} {url_pat} script-path={script_url}, requires-body=true, tag={tag}"
        return_content += response

    # MitM
    return_content += "\n\n[Mitm]\n"
    regular_expression_for_hostname = r"hostname\s?=\s?.*"
    results = re.finditer(regular_expression_for_hostname,
                          content, re.MULTILINE)

    for match in results:
        match = match.group()
        return_content += match

    return return_content


def parse_header(content):
    name = re.findall(r"[ScriptName|\应\用\名\称\：]\s+(.*)", content)[0]
    desc = re.findall(r"[Function|\使\用\说\明\：]\s+(.*)", content)[0]
    openUrl = re.findall(r"[ScriptURL|\脚\本\地\址\：]\s+(.*)", content)[0]
    author = re.findall(r"[Author|\脚\本\作\者\：]\s+(.*)", content)[0]
    homepage = re.findall(r"[ScriptURL|\脚\本\地\址\：]\s+(.*)", content)[0]
    icon = ""
    return_content = """#!name = {name}
#!desc = {desc}
#!openUrl = {openUrl}
#!author = {author}
#!homepage = {homepage}
#!icon = {icon}
"""
    return return_content.format(name=name,
                                 desc=desc,
                                 openUrl=openUrl,
                                 author=author,
                                 homepage=homepage,
                                 icon=icon)


def main():
    script_content = get_QX_content(
        url="https://raw.githubusercontent.com/ddgksf2013/Rewrite/master/AdBlock/WeChat.conf")
    plugin_content = ""
    header = parse_header(script_content)
    plugin_content += header
    content = parse_content(script_content)
    plugin_content += content
    print(plugin_content)


if __name__ == "__main__":
    main()
