#!/usr/bin/env python3
"""
多源学术文献搜索工具
整合 Semantic Scholar + OpenAlex + Crossref API
零反爬，全免费，覆盖中英文期刊

用法:
  python academic_search.py "叶片滞尘 植物" --limit 30
  python academic_search.py "leaf dust retention urban trees" --sources openalex,semantic
  python academic_search.py --doi "10.16768/j.issn.1004-874x.2013.24.011"  # 补全元数据
"""

import argparse
import json
import sys
import time
import urllib.request
import urllib.parse
import urllib.error
import ssl
from datetime import datetime
from typing import Optional

# ============================================================
# API 客户端
# ============================================================

_VERBOSE = False

def _fetch(url: str, timeout: int = 15) -> Optional[dict]:
    """通用 HTTP GET，返回 JSON"""
    ctx = ssl.create_default_context()
    try:
        req = urllib.request.Request(url, headers={
            'User-Agent': 'AcademicSearchTool/1.0 (mailto:research@example.com)'
        })
        with urllib.request.urlopen(req, timeout=timeout, context=ctx) as resp:
            raw = resp.read().decode()
            if resp.status != 200:
                print(f"  [HTTP {resp.status}] {url[:120]}", file=sys.stderr)
                return None
            return json.loads(raw)
    except urllib.error.HTTPError as e:
        print(f"  [HTTP {e.code}] {url[:120]}", file=sys.stderr)
        return None
    except Exception as e:
        print(f"  [ERROR] {e} | {url[:120]}", file=sys.stderr)
        return None


# --- Semantic Scholar ---
# API: https://api.semanticscholar.org/api-docs/graph

def search_semantic_scholar(query: str, limit: int = 30) -> list[dict]:
    """搜索 Semantic Scholar（偏英文，2亿+论文）"""
    params = urllib.parse.urlencode({
        'query': query,
        'limit': min(limit, 100),
        'fields': 'title,authors,year,venue,journal,externalIds,abstract,openAccessPdf,publicationTypes'
    })
    url = f'https://api.semanticscholar.org/graph/v1/paper/search?{params}'
    data = _fetch(url)
    if not data or 'data' not in data:
        return []

    results = []
    for p in data['data']:
        authors = [a.get('name', '') for a in p.get('authors', [])]
        ext = p.get('externalIds', {}) or {}

        results.append({
            'title': (p.get('title') or '').strip(),
            'authors': ', '.join(authors[:8]),
            'year': p.get('year'),
            'venue': (p.get('venue') or '') if isinstance(p.get('venue'), str) else '',
            'journal': (p.get('journal', {}) or {}).get('name', '') if p.get('journal') else '',
            'doi': ext.get('DOI', ''),
            'abstract': (p.get('abstract') or '')[:500] if p.get('abstract') else '',
            'pdf_url': (p.get('openAccessPdf') or {}).get('url', '') if p.get('openAccessPdf') else '',
            'source': 'semantic_scholar',
        })
    return results


# --- OpenAlex ---
# API: https://docs.openalex.org/
# 对中文期刊收录极好，很多知网/万方论文有元数据

def search_openalex(query: str, limit: int = 30) -> list[dict]:
    """搜索 OpenAlex（2.5亿+，中英文覆盖广）"""
    params = urllib.parse.urlencode({
        'search': query,
        'per_page': min(limit, 200),
        'filter': 'type:article',
    })
    url = f'https://api.openalex.org/works?{params}'
    data = _fetch(url, timeout=20)
    if not data or 'results' not in data:
        return []

    results = []
    for w in data['results']:
        # Authors
        authors = []
        for a in w.get('authorships', [])[:8]:
            name = (a.get('author', {}) or {}).get('display_name', '')
            if name:
                authors.append(name)

        # Year
        year = w.get('publication_date', '')[:4] if w.get('publication_date') else None
        if year:
            year = int(year)

        # Venue
        venue = ''
        primary_loc = w.get('primary_location', {}) or {}
        source = primary_loc.get('source', {}) or {}
        if source:
            venue = source.get('display_name', '')

        # DOI
        doi = w.get('doi', '')
        if doi and doi.startswith('https://doi.org/'):
            doi = doi[16:]

        # Open access PDF
        oa = w.get('open_access', {}) or {}
        pdf_url = oa.get('oa_url', '') if oa.get('is_oa') else ''

        results.append({
            'title': (w.get('title') or '').strip(),
            'authors': ', '.join(authors),
            'year': year,
            'venue': venue,
            'journal': venue,
            'doi': doi,
            'abstract': '',  # OpenAlex free tier doesn't include abstract
            'pdf_url': pdf_url,
            'source': 'openalex',
            'cited_by': w.get('cited_by_count', 0),
        })

    return results


# --- Crossref ---
# API: https://api.crossref.org/
# DOI 补全元数据 & 搜索

def search_crossref(query: str, limit: int = 30) -> list[dict]:
    """搜索 Crossref（DOI注册中心，1.4亿+记录）"""
    params = urllib.parse.urlencode({
        'query': query,
        'rows': min(limit, 100),
        'sort': 'relevance',
    })
    url = f'https://api.crossref.org/works?{params}'
    data = _fetch(url, timeout=20)
    if not data or 'message' not in data:
        return []

    results = []
    for item in data['message'].get('items', []):
        # Authors
        authors = []
        for a in item.get('author', [])[:8]:
            family = a.get('family', '')
            given = a.get('given', '')
            name = f'{given} {family}'.strip()
            if name:
                authors.append(name)

        # Year
        year = None
        date_parts = item.get('published-print', {}).get('date-parts', [[None]])[0]
        if not date_parts or not date_parts[0]:
            date_parts = item.get('created', {}).get('date-parts', [[None]])[0]
        if date_parts and date_parts[0]:
            year = int(date_parts[0])

        # Venue
        container = item.get('container-title', [''])
        venue = (container[0] if container else '') or ''

        # DOI
        doi = item.get('DOI', '')

        results.append({
            'title': (item.get('title', [''])[0] or '').strip(),
            'authors': ', '.join(authors),
            'year': year,
            'venue': venue,
            'journal': venue,
            'doi': doi,
            'abstract': (item.get('abstract', '') or '')[:500],
            'pdf_url': f'https://doi.org/{doi}' if doi else '',
            'source': 'crossref',
        })

    return results


def lookup_doi(doi: str) -> Optional[dict]:
    """通过 DOI 补全单篇论文元数据"""
    url = f'https://api.crossref.org/works/{urllib.parse.quote(doi)}'
    data = _fetch(url, timeout=15)
    if not data or 'message' not in data:
        return None

    item = data['message']
    authors = []
    for a in item.get('author', [])[:8]:
        family = a.get('family', '')
        given = a.get('given', '')
        name = f'{given} {family}'.strip()
        if name:
            authors.append(name)

    date_parts = item.get('published-print', {}).get('date-parts', [[None]])[0]
    if not date_parts or not date_parts[0]:
        date_parts = item.get('created', {}).get('date-parts', [[None]])[0]
    year = int(date_parts[0]) if date_parts and date_parts[0] else None

    container = item.get('container-title', [''])
    venue = (container[0] if container else '') or ''

    return {
        'title': (item.get('title', [''])[0] or '').strip(),
        'authors': ', '.join(authors),
        'year': year,
        'venue': venue,
        'journal': venue,
        'doi': doi,
        'abstract': (item.get('abstract', '') or '')[:500],
        'pdf_url': f'https://doi.org/{doi}',
        'source': 'crossref_doi',
    }


# ============================================================
# 去重 & 合并
# ============================================================

def _title_key(title: str) -> str:
    """标准化标题用于去重"""
    t = title.lower().strip()
    # 移除常见标点
    for ch in '，。！？、：；""''（）《》【】':
        t = t.replace(ch, '')
    # 移除多余空格
    t = ' '.join(t.split())
    return t


def merge_results(all_results: list[dict]) -> list[dict]:
    """多源合并去重，保留信息最完整的记录"""
    merged = {}
    for r in all_results:
        key = _title_key(r['title'])
        if not key or len(key) < 3:
            continue

        if key in merged:
            existing = merged[key]
            # 补全缺失字段
            for field in ['doi', 'abstract', 'pdf_url', 'year', 'authors', 'journal', 'venue']:
                if not existing.get(field) and r.get(field):
                    existing[field] = r[field]
            # 合并来源标注
            src = existing.get('source', '')
            if r['source'] not in src:
                existing['source'] = f"{src}+{r['source']}"
            # 保留更高的引用数
            if r.get('cited_by', 0) > existing.get('cited_by', 0):
                existing['cited_by'] = r['cited_by']
        else:
            merged[key] = dict(r)

    # 按年份降序排列
    results = list(merged.values())
    results.sort(key=lambda x: (x.get('year') or 0), reverse=True)
    return results


# ============================================================
# 命令行接口
# ============================================================

def main():
    parser = argparse.ArgumentParser(description='多源学术文献搜索')
    parser.add_argument('query', nargs='?', help='搜索关键词')
    parser.add_argument('--limit', '-n', type=int, default=30, help='结果数量上限')
    parser.add_argument('--sources', '-s', default='all',
                        help='搜索源: all / openalex / semantic / crossref (逗号分隔)')
    parser.add_argument('--doi', help='通过 DOI 查询单篇元数据')
    parser.add_argument('--output', '-o', help='输出 JSON 文件路径')
    parser.add_argument('--format', '-f', choices=['json', 'csv', 'table'], default='table',
                        help='输出格式')
    args = parser.parse_args()

    # DOI 查询模式
    if args.doi:
        print(f"查询 DOI: {args.doi}", file=sys.stderr)
        result = lookup_doi(args.doi)
        if result:
            results = [result]
        else:
            print("未找到", file=sys.stderr)
            sys.exit(1)
    elif args.query:
        sources = args.sources.split(',') if args.sources != 'all' else ['all']
        if 'all' in sources:
            sources = ['openalex', 'semantic', 'crossref']

        all_results = []

        if 'semantic' in sources:
            print(f"  [Semantic Scholar] 搜索中...", file=sys.stderr)
            results = search_semantic_scholar(args.query, args.limit)
            print(f"    找到 {len(results)} 条", file=sys.stderr)
            all_results.extend(results)

        if 'openalex' in sources:
            print(f"  [OpenAlex] 搜索中...", file=sys.stderr)
            results = search_openalex(args.query, args.limit)
            print(f"    找到 {len(results)} 条", file=sys.stderr)
            all_results.extend(results)

        if 'crossref' in sources:
            print(f"  [Crossref] 搜索中...", file=sys.stderr)
            results = search_crossref(args.query, args.limit)
            print(f"    找到 {len(results)} 条", file=sys.stderr)
            all_results.extend(results)

        if not all_results:
            print("无搜索结果", file=sys.stderr)
            sys.exit(0)

        results = merge_results(all_results)
        results = results[:args.limit]
        print(f"  合并去重后: {len(results)} 条", file=sys.stderr)

    else:
        parser.print_help()
        sys.exit(1)

    # 输出
    if args.format == 'json':
        output = json.dumps(results, ensure_ascii=False, indent=2)
    elif args.format == 'csv':
        import csv, io
        buf = io.StringIO()
        if results:
            writer = csv.DictWriter(buf, fieldnames=results[0].keys())
            writer.writeheader()
            writer.writerows(results)
        output = buf.getvalue()
    else:  # table
        lines = []
        header = f"{'年份':6} {'标题':50} {'出处':25} {'DOI':30}"
        lines.append(header)
        lines.append('-' * 120)
        for r in results:
            title = (r.get('title') or '')[:48]
            venue = (r.get('journal') or r.get('venue') or '')[:23]
            doi = (r.get('doi') or '')[:28]
            year = str(r.get('year') or '?')
            lines.append(f"{year:6} {title:50} {venue:25} {doi:30}")
        output = '\n'.join(lines)

    if args.output:
        with open(args.output, 'w', encoding='utf-8') as f:
            f.write(output)
        print(f"结果已写入: {args.output}", file=sys.stderr)
    else:
        print(output)


if __name__ == '__main__':
    main()
