import re
import sys
import zipfile

BOLD = "<w:b /><w:bCs />"
RPR = re.compile(r"(<w:rPr>(?:<w:rStyle [^>]*/>)?(?:<w:rFonts [^>]*/>)?)(.*?)</w:rPr>", re.S)


def bold(row):
    def add(match):
        if re.search(r"<w:b[ />]", match.group(2)):
            return match.group(0)
        return match.group(1) + BOLD + match.group(2) + "</w:rPr>"

    row = RPR.sub(add, row)
    return re.sub(r"<w:r>(?!<w:rPr>)", "<w:r><w:rPr>" + BOLD + "</w:rPr>", row)


def fix(xml):
    xml = xml.replace('<w:tblW w:type="auto" w:w="0" />', '<w:tblW w:type="pct" w:w="5000" />')
    return re.sub(
        r"<w:tr>.*?</w:tr>",
        lambda m: bold(m.group(0)) if "<w:tblHeader" in m.group(0) else m.group(0),
        xml,
        flags=re.S,
    )


def main():
    source, target = sys.argv[1], sys.argv[2]
    with zipfile.ZipFile(source) as src, zipfile.ZipFile(target, "w", zipfile.ZIP_DEFLATED) as out:
        for item in src.infolist():
            data = src.read(item.filename)
            if item.filename == "word/document.xml":
                data = fix(data.decode()).encode()
            out.writestr(item, data)


if __name__ == "__main__":
    main()
