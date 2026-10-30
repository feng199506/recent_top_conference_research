# 近五年顶会主会文献库：下载、解压与离线阅读说明

本 Release 是 `recent_top_conference_research` 文献库的完整发布包，快照日期为 2026-10-30。内容如下：

- 7 个方向共 649 条目录记录，对应 642 个全文 PDF（有 7 个 PDF 各被两条记录共用）。
- 297 个论文配套代码仓库的快照，只做了 `git clone --depth 1`，没有运行过。
- 目录、代码可用性、进度与失败记录（CSV 格式）。
- 各方向的中文说明、检索日志和续跑脚本。

## 1. 下载哪些文件

所有 tar 包都**不压缩**，可以各自独立解压。解压到同一个目录后，就能还原完整的目录树。

| 包 | 内容 | 是否需要 |
|---|---|---|
| `…_batch001_cn_en.tar` | 离线首页、目录 CSV、说明、脚本、约一半论文 PDF | **必需** |
| `…_batch002_cn_en.tar` | 其余论文 PDF，以及第一批代码快照 | 读全文必需 |
| `…_batch003` ～ `…_batch009_cn_en.tar` | 有开源许可证的代码快照（MIT、Apache、BSD、GPL、CC 等，共 198 个仓库，从 batch002 末尾开始） | 按需 |
| `…_batch010` ～ `…_batch013_code_nolicense_cn_en.tar` | **未声明许可证**的代码快照（99 个仓库） | 按需，见第 5 节 |

每个文件在哪个包里，可以在 `archive_index_cn.csv` 中查（用 Excel 打开，按“相对路径”列搜索）。

## 2. Windows 下解压（重要：请解压到短路径）

部分代码仓库的目录很深，包内最长的相对路径有 203 个字符。Windows 资源管理器默认只能处理 260 个字符以内的完整路径，因此**请解压到短目录**，例如 `D:\rtcr\`，不要解压到“下载”文件夹下，也不要解压到以包名命名的子文件夹里。

**方法 A：PowerShell（Windows 10 1803 及以上自带 `tar`）**

把所有 tar 包放进同一个文件夹，在该文件夹中打开 PowerShell，执行：

```powershell
mkdir D:\rtcr -Force
Get-ChildItem *.tar | ForEach-Object { tar -xf $_.FullName -C D:\rtcr }
```

**方法 B：7-Zip**

1. 全选所有 tar 包，右键选择“7-Zip → 提取文件…”。
2. 目标填 `D:\rtcr\`。
3. 取消勾选“按压缩包名创建子文件夹”（如果有这个选项）。

如果系统已开启长路径支持（组策略“启用 Win32 长路径”，或注册表 `LongPathsEnabled=1`），可以解压到更深的目录，但部分旧软件仍可能打不开深层文件。

**Linux / macOS**

```bash
mkdir -p ~/rtcr && for f in *.tar; do tar -xf "$f" -C ~/rtcr; done
```

## 3. 离线阅读

用浏览器（Edge、Chrome 或 Firefox）打开 `D:\rtcr\index_cn.html`，不需要联网。

- 首页按方向列出全部 649 条论文。“全文 PDF”打开本地 PDF；“本地代码”打开本地代码目录，浏览器会显示文件列表，源码可以直接点开。
- “论文页”“代码仓库”是原始在线地址，需要联网。
- `README_cn.html`、`domains/*/README_cn.html`、`guides/resume_cn.html`、`search_log_cn.html` 是对应 Markdown 文档的 HTML 版本。文中的路径可以点击；优先阅读清单里的论文标题后面附有本地“全文 PDF / 本地代码”链接。
- 发布前做过静态检查：这些页面里的 1,251 个本地链接全部能解析到包内文件，没有失效链接。没有在 Windows 真机上做浏览器渲染测试。
- CSV 文件带 BOM，用 Excel 直接打开，中文不会乱码。
- 代码快照里的 HTML 文档是上游项目原样保留的，它们引用的在线资源（CDN、图片等）离线时可能显示不全。这不影响阅读源码。

## 4. 发布包相对本机原件的改动

只改了发布副本，本机原件没有改动。

- **Windows 兼容改名，共 7,015 个文件，都在代码快照内。** 完整路径超过 200 个字符的，把其中较长的目录名或文件名截短为“前 8 个字符 + 原名的 6 位哈希”。同一仓库内同名的目录统一改名，24 个文本文件里对这些名字的引用已同步改写。没有含 Windows 非法字符的文件名，也没有只差大小写的重名文件。原路径和新路径的对照见 `windows_rename_map_cn.csv`。
  - **注意**：被截短的名字如果是 Python 包名或脚本中写死的路径，直接运行代码会找不到文件。这些快照主要用于对照论文阅读；需要运行时，请按 `code_availability_cn.csv` 中的“URL”和“提交”两列重新 `git clone` 并 `git checkout <提交>`。
- **离线化新增（不改动原有文档的正文）：**
  - `index_cn.html`，以及 10 个 Markdown 文档的 HTML 版本。
  - `README_cn.md` 和 `guides/resume_cn.md` 中的 16 处路径改为相对链接。原文中 `/root/recent_top_conference_research/...` 形式的本机绝对路径，已映射为包内的相对路径。
- **未打包的内容：**
  - 各代码快照内的 `.git/` 目录（约 4.6 GB），阅读用不到。仓库地址和提交号见 `code_availability_cn.csv`。
  - 1,225 个指向不存在文件的符号链接（多为没有下载的 LFS 数据或数据集）。
  - 19 个指向目录的符号链接。
  - 另有 41 个指向文件的符号链接，已替换为文件副本。
- **未发布的仓库：** `D05-037` NTT chaos-eater 的许可证（Software License Agreement for Evaluation）明确禁止向第三方分发，因此没有打包，见 `release_excluded_cn.csv`。首页对应条目标为“未随发布包提供”，并给出在线地址。

## 5. 版权与许可

- **论文 PDF**：版权归作者或出版方所有。它们来自 PMLR、NeurIPS、CVF、ACL Anthology、USENIX、IJCAI、arXiv 等公开渠道，仅供个人学习研究。
- **有许可证的代码（batch002–009 中的 198 个仓库）**：按各仓库自带的 LICENSE 使用。其中包括 CC BY-NC、CC BY-NC-SA 等非商业许可，以及 GPL、AGPL 等 copyleft 许可，请逐个查看。
- **无许可证的代码（`code_nolicense` 包中的 99 个仓库）**：作者没有声明任何开源许可证，按默认规则作者保留全部权利。每个仓库目录中都放了 `_NO_LICENSE_NOTICE_cn.txt`。这些快照仅供个人对照论文阅读，请勿再分发、修改后发布或商用；如需使用，请联系作者。首页对这些仓库标有“无许可证”。

## 6. 校验

- `archive_index_cn.csv`：每个文件所在的包、发布路径和字节数。
- `checksums`：原库没有整库的 SHA256 文件。论文 PDF 的 SHA256 记录在 `catalog_cn.csv` 的“SHA256”列，可以用 PowerShell 的 `Get-FileHash` 核对。
- 上传结果见 Release 附件 `upload_report_cn.md`。
