from xml.etree.ElementTree import Element
import re


def replace(root: Element) -> Element | None:
    for element in root.iter():
        if element.tag != 'Content':
            continue
        e = element.find('url')
        if e is None:
            continue
        e.text = re.sub(
            r'https?://(?:assetgame\.|assetdelivery\.|www\.)?roblox\.com/+(?:v1/)?asset/?\?id=([\d]{1,17})',
            lambda m: 'rbxassetid://%s' % m.group(1),
            e.text or '',
        )
    return root
