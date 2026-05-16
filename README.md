# Citation Export Skill (v2.1)

## 简介

本 Skill 用于根据学术论文标题、DOI、PMID 或其他标识符生成引文文件，支持以下格式：

- **EndNote (.enw)** - EndNote 标签格式（符合 EndNote X6 官方标签规范）
- **RIS (.ris)** - Research Information Systems 格式（符合 RIS 2011 官方规范）
- **RIS+ (.ris)** - 扩展 RIS 格式（社区约定，包含 PMID/PMCID 等额外字段）

### v2.1 更新内容

- **格式规范修正**：ENW 中 DOI 改用 `%R` 标签（官方标准），不再错误使用 `%U`/`%6`
- **格式规范修正**：RIS 中 `UR` 改为 URL 字段，`DO` 为 DOI 字段（符合官方规范）
- **格式规范修正**：RIS 文档类型 `PREPRINT` 改为 `ELEC`（RIS 标准中不存在 PREPRINT）
- **DOI 提取修复**：自动从 `doi.org` URL 中提取裸 DOI 值，解决"有 URL 无 DOI"的问题
- **新增 6 个数据库**：arXiv、medRxiv、DBLP、ERIC、AMiner、Unpaywall（总计 47 个）
- **新增文档类型支持**：CPAPER、EJOUR、MGZN、NEWS、BLOG、MANSCPT、GEN 等

## 文件结构

```
citation-export-skill/
├── SKILL.md                    # Skill 主文档（含完整数据库参考）
├── scripts/
│   ├── citation_export.py      # 引文生成脚本
│   └── example_metadata.json   # 示例元数据文件
└── README.md                   # 本文件
```

## 支持的数据库/平台（47个）

### Tier 1: 核心 API（免费开放，无需认证）
| 数据库 | 覆盖范围 | 适用领域 |
|--------|----------|----------|
| CrossRef | 所有 DOI 注册作品 | 通用 |
| PubMed | 3600万+ 生物医学文献 | 生物医学 |
| PubMed Central (PMC) | 900万+ 开放获取生物医学 | 生物医学 |
| Semantic Scholar | 2亿+ 跨学科论文 | 通用 |
| OpenAlex | 2.5亿+ 开放元数据 | 通用 |
| DataCite | 2000万+ 数据集/软件/预印本 | 数据/软件 |
| Dimensions | 1亿+ 出版物/资助/专利 | 通用 |
| Unpaywall | 2亿+ OA 论文定位 | 开放获取 |

### Tier 2: 出版商平台（可能需要认证）
| 数据库 | 覆盖范围 | 适用领域 |
|--------|----------|----------|
| IEEE Xplore | 500万+ 文档 | 电气工程/CS |
| Elsevier ScienceDirect | 1800万+ 出版物 | 综合 |
| Scopus | 9000万+ 记录 | 综合 |
| Wiley Online Library | 400万+ 文章 | 综合 |
| SpringerLink | 1300万+ 文档 | 理工农医 |
| ACM Digital Library | 300万+ 计算机文献 | 计算机 |
| JSTOR | 1200万+ 学术文章 | 人文社科 |
| DBLP | 600万+ CS 出版物 | 计算机/会议 |
| ERIC | 160万+ 教育文献 | 教育学 |

### Tier 3: 中文学术数据库
| 数据库 | 覆盖范围 | 适用领域 |
|--------|----------|----------|
| 中国知网 (CNKI) | 最大中文学术库 | 中文期刊/博硕/会议 |
| 万方数据 | 期刊/博硕/会议/专利 | 中文综合 |
| 维普中文科技期刊 | 中文科技期刊 | 中文理工科 |
| 国家哲学社会科学文献中心 | 中文社科期刊（OA） | 中文社科 |
| 读秀学术搜索 | 图书/章节/学位论文 | 中文图书 |
| CALIS 高校学位论文库 | 高校学位论文 | 中文博硕 |
| 国家科技图书文献中心 (NSTL) | 科技文献 | 中文科技 |
| PubScholar | 中文开放获取资源 | 中文 OA |
| AMiner | 2.6亿+ 论文，AI 学术平台 | CS/AI/中文 |

### Tier 4: 预印本服务器
| 数据库 | 适用领域 |
|--------|----------|
| arXiv | 物理/数学/CS/EE/统计 |
| bioRxiv | 生物学/健康 |
| medRxiv | 医学/健康 |
| ChemRxiv | 化学 |
| EarthArXiv | 地球科学 |
| SSRN | 社科/商科/法学 |
| PSSXiv | 政治学 |

### Tier 5: 开放获取仓储
| 数据库 | 适用领域 |
|--------|----------|
| DOAJ | 开放获取期刊 |
| DOAB | 开放获取图书 |
| CORE | 2.5亿+ OA 论文 |
| Figshare | 研究数据/图表 |
| Zenodo | 数据/软件/预印本 |
| OpenGrey | 欧洲灰色文献 |

### Tier 6: 引文索引（通常需要机构订阅）
| 数据库 | 适用领域 |
|--------|----------|
| Web of Science (WOS) | 高质量引文索引 |
| Scopus | 最大摘要引文库 |
| CPCI | 会议论文引文索引 |

### Tier 7: 专利数据库
| 数据库 | 适用领域 |
|--------|----------|
| USPTO | 美国专利 |
| EPO / Espacenet | 欧洲专利（1.3亿+） |
| Derwent Innovations Index | 增强专利数据 |

### Tier 8: 标准
| 数据库 | 适用领域 |
|--------|----------|
| ISO | 国际标准 |

### Tier 9: 学位论文
| 数据库 | 适用领域 |
|--------|----------|
| ProQuest | 500万+ 全球学位论文 |

### Tier 10: 通用兜底
| 数据库 | 适用领域 |
|--------|----------|
| Google Scholar | 最广泛覆盖 |

## 使用方法

### 1. 准备元数据文件

创建 JSON 格式的元数据文件，包含论文信息：

```json
[
  {
    "title": "论文标题",
    "authors": ["作者1", "作者2"],
    "journal": "期刊名称",
    "year": "2024",
    "volume": "21",
    "issue": "1",
    "pages": "142",
    "issn": "1743-0003",
    "publisher": "出版社",
    "abstract": "摘要",
    "keywords": "关键词",
    "pmid": "39135110",
    "pmcid": "PMC11320866",
    "doi": "10.1186/s12984-024-01420-y",
    "language": "English"
  }
]
```

### 2. 运行脚本生成引文文件

```bash
# 生成 EndNote 格式
python citation_export.py --input metadata.json --format enw --output references.enw

# 生成 RIS 格式
python citation_export.py --input metadata.json --format ris --output references.ris

# 生成 RIS+ 格式（扩展）
python citation_export.py --input metadata.json --format ris+ --output references.ris
```

### 3. 导入到文献管理软件

- **EndNote**: File → Import → Import File → 选择 .enw 文件
- **Zotero**: File → Import → 选择 .ris 文件
- **Mendeley**: File → Import → RIS → 选择 .ris 文件
- **JabRef**: File → Import into new library → 选择文件
- **NoteExpress**: 文件 → 导入题录 → 选择 .ris 或 .enw 文件

## 元数据字段说明

| 字段 | 必填 | 说明 |
|------|------|------|
| title | 是 | 论文标题 |
| authors | 是 | 作者列表（数组） |
| journal | 是 | 期刊/来源名称 |
| year | 是 | 出版年份 |
| volume | 否 | 卷号 |
| issue | 否 | 期号 |
| pages | 否 | 页码（支持 "1-10" 格式） |
| issn | 否 | ISSN |
| publisher | 否 | 出版社 |
| abstract | 否 | 摘要 |
| keywords | 否 | 关键词（分号分隔） |
| pmid | 否 | PubMed ID |
| pmcid | 否 | PubMed Central ID |
| doi | 否 | DOI |
| language | 否 | 语言 |
| notes | 否 | 附加说明（专利号、标准号等） |

## 输出格式对比

| 特性 | EndNote (.enw) | RIS (.ris) | RIS+ (.ris) |
|------|----------------|------------|-------------|
| 基本字段 | ✓ | ✓ | ✓ |
| 摘要 | ✓ | ✓ | ✓ |
| 关键词 | ✓ | ✓ | ✓ |
| PMID | ✓ | ✗ | ✓ |
| PMCID | ✓ | ✗ | ✓ |
| 文档类型 | ✓ | ✓ | ✓ |
| 兼容性 | EndNote | 通用 | Zotero/Mendeley |

## 支持的文献类型

| 类型 | RIS TY 值 | 说明 |
|------|-----------|------|
| 期刊论文 | JOUR | 默认类型 |
| 会议论文 | CONF | 会议录 |
| 图书 | BOOK | 专著 |
| 图书章节 | CHAP | 书籍章节 |
| 学位论文 | THES | 博硕士论文 |
| 专利 | PAT | 发明专利 |
| 标准 | STAND | 国际/国家标准 |
| 预印本 | ELEC | 电子资源（RIS 无 PREPRINT） |
| 技术报告 | RPRT | 技术报告 |
| 数据集 | DATA | 研究数据 |
| 软件 | COMP | 软件包 |

## 智能搜索策略

本 Skill 根据论文特征自动选择最优搜索路径：

```
输入论文信息
├── 有 DOI → CrossRef API → 出版商平台
├── 有 PMID → PubMed → PMC
├── 有专利号 → USPTO / EPO
├── 有标准号 → ISO
├── 仅有标题
│   ├── 中文标题 → CNKI → 万方 → 维普 → PubScholar → NSTL → Google Scholar
│   ├── 生物医学 → PubMed → PMC → Cochrane → CrossRef → Semantic Scholar
│   ├── 工程/CS → IEEE Xplore → ACM DL → SpringerLink → ScienceDirect
│   ├── 社科 → SSRN → JSTOR → 国家哲学社科文献中心 → Google Scholar
│   ├── 会议论文 → IEEE Xplore → CPCI → ACM DL
│   ├── 预印本 → 对应预印本服务器 → CrossRef（查正式版）
│   └── 未知领域 → CrossRef → Semantic Scholar → OpenAlex → Google Scholar
```

## 注意事项

1. 作者格式支持 "Last, First" 或 "First Last" 两种形式
2. 页码支持 "起始页-结束页" 格式，会自动拆分
3. 多篇论文会合并到同一个文件中，用空行分隔
4. 对于中文期刊论文，优先使用中文数据库获取元数据
5. 预印本建议检查是否已有正式发表版本
6. 专利和标准使用特殊的 RIS 文档类型
7. 搜索时请遵守各数据库的 API 速率限制和使用条款
