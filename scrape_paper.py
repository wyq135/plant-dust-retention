"""
学术论文元数据抓取工具 — 支持中英文期刊
通过 DOI 或直接 URL 获取论文标题、作者、摘要、期刊信息
"""
import sys, io, re, json, os, subprocess, time
from urllib.parse import urlparse, quote

# --- 编码处理 ---
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"

def fetch_html(url, timeout=20):
    """用 curl 下载页面，自动跟随重定向，返回 (final_url, raw_bytes)"""
    cmd = [
        "curl", "-sL", "--max-time", str(timeout),
        "-H", f"User-Agent: {USER_AGENT}",
        "-o", "-", "-w", "\n>>>FINAL_URL:%{url_effective}\n>>>HTTP_CODE:%{http_code}",
        url
    ]
    result = subprocess.run(cmd, capture_output=True, timeout=timeout+5)
    output = result.stdout
    # Split off the -w output
    if b"\n>>>FINAL_URL:" in output:
        body, meta = output.split(b"\n>>>FINAL_URL:", 1)
    else:
        body, meta = output, b""
    # Parse final URL from meta
    final_url = url
    if b"FINAL_URL:" in meta:
        m = re.search(rb'FINAL_URL:(\S+)', meta)
        if m:
            final_url = m.group(1).decode('utf-8', errors='replace')
    return final_url, body


def decode_html(raw_bytes):
    """自动检测编码并解码 HTML"""
    # 先看 meta charset
    head = raw_bytes[:4000]
    meta_enc = None
    m = re.search(rb'charset[=\"\s]+([a-zA-Z0-9_-]+)', head)
    if m:
        meta_enc = m.group(1).decode('ascii', errors='replace').lower()

    # 尝试顺序：meta 指定的 → utf-8 → gb18030 → gbk → gb2312
    candidates = []
    if meta_enc and meta_enc not in ('utf-8', 'utf8'):
        candidates.append(meta_enc)
    candidates.extend(['utf-8', 'gb18030', 'gbk', 'gb2312'])

    for enc in candidates:
        try:
            text = raw_bytes.decode(enc)
            # 检查是否包含有意义的中文
            if any(kw in text for kw in ['摘要', '标题', '作者', '期刊', 'DOI', 'Abstract']):
                return enc, text
        except:
            continue

    # Fallback
    return 'utf-8', raw_bytes.decode('utf-8', errors='replace')


def clean_html(html):
    """移除 script/style 标签和 HTML 实体"""
    html = re.sub(r'<script[^>]*>.*?</script>', '', html, flags=re.DOTALL | re.IGNORECASE)
    html = re.sub(r'<style[^>]*>.*?</style>', '', html, flags=re.DOTALL | re.IGNORECASE)
    html = re.sub(r'<noscript[^>]*>.*?</noscript>', '', html, flags=re.DOTALL | re.IGNORECASE)
    html = re.sub(r'<!--.*?-->', '', html, flags=re.DOTALL)
    # Remove HTML tags but keep content
    text = re.sub(r'<br\s*/?>', '\n', html, flags=re.IGNORECASE)
    text = re.sub(r'</?p[^>]*>', '\n', text, flags=re.IGNORECASE)
    text = re.sub(r'</?div[^>]*>', '\n', text, flags=re.IGNORECASE)
    text = re.sub(r'<[^>]+>', ' ', text)
    # Decode entities
    text = text.replace('&nbsp;', ' ').replace('&lt;', '<').replace('&gt;', '>')
    text = text.replace('&amp;', '&').replace('&quot;', '"').replace('&#215;', '×')
    text = re.sub(r'&#(\d+);', lambda m: chr(int(m.group(1))), text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text


def extract_metadata(text, url):
    """从清洗后的纯文本中提取论文元数据"""
    meta = {
        "url": url,
        "title_cn": None,
        "title_en": None,
        "authors_cn": None,
        "authors_en": None,
        "abstract_cn": None,
        "abstract_en": None,
        "journal": None,
        "doi": None,
        "funding": None,
        "keywords_cn": None,
        "year": None,
        "volume": None,
        "issue": None,
        "pages": None,
    }

    # --- DOI ---
    doi_match = re.search(r'DOI[:\s]*([0-9]+\.[0-9]+/[^\s"\']+)', text, re.IGNORECASE)
    if doi_match:
        meta["doi"] = doi_match.group(1).rstrip('.')
    else:
        # Try to extract from URL
        doi_in_url = re.search(r'(10\.[0-9]+/[^/\s]+)$', url)
        if doi_in_url:
            meta["doi"] = doi_in_url.group(1)

    # --- chndoi.org "多重解析地址选择页面" 特殊处理 ---
    # 这些页面格式: 题名：XXX 作者：XXX 来源：XXX 年份：XXX
    is_chndoi = '多重解析' in text or 'chndoi' in url.lower() or 'chndoi' in text.lower()
    if is_chndoi:
        chndoi_patterns = {
            'title_cn': r'题名[：:]\s*(.+?)(?=\s+(?:作者|来源|年份)[：:]|\s*$)',
            'authors_cn': r'作者[：:]\s*(.+?)(?=\s+(?:来源|年份|摘要)[：:]|\s*$)',
            'journal': r'来源[：:]\s*(.+?)(?=\s+(?:年份|卷|期)[：:]|\s*$)',
            'year': r'年份[：:]\s*(\d{4})',
        }
        for field, pat in chndoi_patterns.items():
            m = re.search(pat, text)
            if m:
                val = m.group(1).strip().rstrip(';；')
                # Skip chndoi "来源" if it's just CNKI publisher info
                if field == 'journal' and ('同方知网' in val or 'CNKI' in val.upper()):
                    continue
                if field == 'journal' and val:
                    # 来源可能是 "林业科学研究, 2021, 34(4): 84-94" 格式
                    j_match = re.match(r'([^,]+)', val)
                    if j_match and '出版' not in j_match.group(1):
                        meta['journal'] = j_match.group(1).strip()
                    # 从来源提取卷期
                    vol_match = re.search(r'(\d{4})\s*,?\s*(\d+)\s*\((\d+)\)\s*[,:]\s*(\d+)\s*[~～\-]?\s*(\d+)', val)
                    if vol_match:
                        meta['year'] = vol_match.group(1)
                        meta['volume'] = vol_match.group(2)
                        meta['issue'] = vol_match.group(3)
                        meta['pages'] = f"{vol_match.group(4)}-{vol_match.group(5)}"
                elif val and field != 'journal':
                    meta[field] = val

    # --- 标题 ---
    # 清理页面 UI 噪音词
    UI_NOISE = [
        'PDF', 'HTML阅读', 'XML下载', '导出引用', '引用提醒', '优先出版',
        '首页', '过刊浏览', '学报首页', '关于本刊', '投稿须知',
        '--请选择--', '中文标题', '英文标题', '+高级检索',
    ]
    def strip_ui_prefix(t):
        for noise in UI_NOISE:
            t = t.replace(noise, '')
        return re.sub(r'\s+', ' ', t).strip()

    # 策略1: DOI 前的长句
    title_patterns = [
        r'引用提醒\s*(.{10,200}?)\s*DOI',
        r'优先出版\s*(.{10,200}?)\s*DOI',
        r'(\S.{10,200}?)\s+DOI\s*[:：]',
        r'>\s*(\S.{10,200}?)\s*</h[1-4]',
    ]
    for pat in title_patterns:
        m = re.search(pat, text)
        if m:
            t = m.group(1).strip()
            t = strip_ui_prefix(t)
            if len(t) > 10 and not re.search(r'^[a-z]{8,}$', t):
                meta["title_cn"] = t
                break

    # 策略2: 从页面开头找第一个长中文句子
    if not meta["title_cn"]:
        for line in text.split('\n')[:30]:
            line = line.strip()
            if len(line) > 15 and any('一' <= c <= '鿿' for c in line):
                if not any(noise in line for noise in UI_NOISE[:3]):
                    meta["title_cn"] = strip_ui_prefix(line)
                    break

    # --- 英文标题 ---
    en_title_match = re.search(r'英文标题[：:\s]*([A-Z].{10,300}?)(?=\s+(?:作者|Author|Abstract|摘要))', text)
    if en_title_match:
        meta["title_en"] = en_title_match.group(1).strip()
    # Alternative: look for the pattern around "Author:"
    if not meta["title_en"]:
        # Often English title is right before "Author:" or "Affiliation:"
        m = re.search(r'(\w[\w\s\-,:;()]{20,200})\s+Author\s*:', text)
        if m:
            meta["title_en"] = m.group(1).strip()

    # --- 作者 ---
    # 策略1: 标准"作者:"字段
    author_match = re.search(r'作者[：:\s]*([^\s].{5,200}?)(?=\s+(?:作者单位|单位|Author|基金|摘要|中图))', text)
    if author_match:
        authors = author_match.group(1).strip()
        # 过滤掉表单标签
        if not any(lbl in authors for lbl in ['中文名', '英文名', '关键字']):
            meta["authors_cn"] = authors

    # 策略2: 从引用格式提取 (如 "王琴,冯晶红,黄奕,...")
    if not meta["authors_cn"]:
        cite_authors = re.search(
            r'(?:引用本文|引用格式|引用\s*|本文\s*)\S{0,10}([一-鿿]{2,4}(?:[,，、\s]+[一-鿿]{2,4}){2,20})',
            text
        )
        if cite_authors:
            authors = cite_authors.group(1)
            # Strip UI noise words
            for noise in ['本文', '引用本文', '引用']:
                if authors.startswith(noise):
                    authors = authors[len(noise):].strip()
            meta["authors_cn"] = authors

    # English authors
    en_author_match = re.search(r'Author\s*[：:]\s*([A-Z][^\s].{5,300}?)(?=\s+(?:Affiliation|Fund|Abstract))', text)
    if en_author_match:
        meta["authors_en"] = en_author_match.group(1).strip()

    # --- 摘要 ---
    for prefix in ['摘要:', '摘要：', '摘要 ']:
        if prefix in text:
            idx = text.index(prefix)
            chunk = text[idx+len(prefix):idx+2000]
            # 截取到下一个标记
            for end_marker in ['Abstract:', 'Abstract：', '关键词', '参考文献', '图/表', '-->', '"/>']:
                if end_marker in chunk:
                    chunk = chunk[:chunk.index(end_marker)]
            meta["abstract_cn"] = chunk.strip()
            break

    # --- 英文摘要 ---
    for prefix in ['Abstract:', 'Abstract：', 'Abstract ']:
        if prefix in text:
            idx = text.index(prefix)
            chunk = text[idx+len(prefix):idx+3000]
            for end_marker in ['关键词', 'Key words', 'References', '-->']:
                if end_marker in chunk:
                    chunk = chunk[:chunk.index(end_marker)]
            meta["abstract_en"] = chunk.strip()[:1500]
            break

    # --- 期刊 ---
    # 策略1: 从引用格式提取 "期刊名, 年份, 卷(期): 页"
    cite_match = re.search(
        r'([^\s,]{2,30})\s*,\s*(\d{4})\s*,?\s*(\d+)\s*\((\d+)\)\s*[,:]\s*(\d+)\s*[~～\-]\s*(\d+)',
        text
    )
    if cite_match:
        journal_name = cite_match.group(1).strip()
        # 清理可能残留的标题片段
        if '.' in journal_name:
            parts = journal_name.split('.')
            journal_name = parts[-1] if len(parts[-1]) > 2 else parts[-2] if len(parts) > 1 else journal_name
        meta["journal"] = journal_name
        meta["year"] = cite_match.group(2)
        meta["volume"] = cite_match.group(3)
        meta["issue"] = cite_match.group(4)
        meta["pages"] = f"{cite_match.group(5)}-{cite_match.group(6)}"

    # 策略2: 其他模式
    if not meta["journal"]:
        journal_patterns = [
            r'([^\s]{3,20}(?:学报|科学|研究|园艺|园林|环境)[^\s]{0,20})\s*,?\s*(?:20\d{2})',
            r'([^\s]{3,20}(?:Journal|Research|Science|Ecology)[^\s]{0,40})\s*,?\s*(?:20\d{2}|\d{4})',
        ]
        for pat in journal_patterns:
            m = re.search(pat, text)
            if m:
                meta["journal"] = m.group(1).strip()
                break

    # --- 基金 ---
    fund_match = re.search(r'基金项目[：:\s]*([^\s].{10,300}?)(?=\s+(?:Dust|摘要|关键词|图/表))', text)
    if fund_match:
        meta["funding"] = fund_match.group(1).strip()

    # --- 关键词 ---
    kw_match = re.search(r'关键词[：:\s]*([^\s].{5,200}?)(?=\s+(?:Abstract|摘要|Key))', text)
    if kw_match:
        meta["keywords_cn"] = kw_match.group(1).strip()

    return meta


def scrape(doi_or_url, timeout=20):
    """主入口：输入 DOI 或 URL，返回元数据字典"""
    # 判断是 DOI 还是 URL
    if doi_or_url.startswith('http'):
        url = doi_or_url
    elif doi_or_url.startswith('10.'):
        url = f"https://doi.org/{doi_or_url}"
    else:
        raise ValueError(f"无法识别的输入: {doi_or_url}")

    print(f"[抓取] {url}", file=sys.stderr)
    final_url, raw = fetch_html(url, timeout)

    if not raw or len(raw) < 100:
        return {"error": "页面内容为空", "url": final_url}

    enc, html = decode_html(raw)
    print(f"[编码] {enc} | 大小: {len(raw)} bytes → {len(html)} chars", file=sys.stderr)

    text = clean_html(html)
    print(f"[清洗] {len(text)} chars", file=sys.stderr)

    meta = extract_metadata(text, final_url)
    meta["encoding_detected"] = enc
    meta["final_url"] = final_url

    return meta


# ============================================================
# 批处理
# ============================================================
if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="学术论文元数据抓取")
    parser.add_argument("input", help="DOI 或 URL")
    parser.add_argument("--json", help="直接输出 JSON", action="store_true")
    parser.add_argument("-o", "--output", help="保存到文件")
    args = parser.parse_args()

    result = scrape(args.input)
    json_str = json.dumps(result, ensure_ascii=False, indent=2)

    if args.output:
        with open(args.output, 'w', encoding='utf-8') as f:
            f.write(json_str)
        print(f"已保存: {args.output}")
    elif args.json:
        print(json_str)
    else:
        # Print summary
        print("\n" + "=" * 60)
        print(f"标题: {result.get('title_cn', 'N/A')}")
        print(f"英文标题: {result.get('title_en', 'N/A')}")
        print(f"作者: {result.get('authors_cn', 'N/A')}")
        print(f"期刊: {result.get('journal', 'N/A')} | {result.get('year', '')} {result.get('volume', '')}({result.get('issue', '')}): {result.get('pages', '')}")
        print(f"DOI: {result.get('doi', 'N/A')}")
        print(f"基金: {result.get('funding', 'N/A')}")
        cn = result.get('abstract_cn', '')
        print(f"摘要({len(cn)}字): {cn[:200]}...")
