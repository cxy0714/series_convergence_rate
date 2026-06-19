# CLAUDE.md — 项目工作说明

Overleaf 同步的 LaTeX 项目。论文 *“On computing and the complexity of computing
higher-order U-statistics, exactly”*，目前正在回复 *Statistics and Computing*
的审稿意见（major revision）。

## 主要工作目录

**所有当前工作都在 `Statistics_and_computing_submission/` 里进行。**
仓库根目录下的其他文件（`main.tex`、`jmlr.tex`、`slides*.tex`、
`JCGS submission/` 等）是历史版本/旧投稿/幻灯片，一般不要动。
`Master.bib`（文献库）和 `Figures/` 在项目根目录，编译时工作目录设在
**项目根**（Overleaf 的习惯），这样 `Master.bib` 和跨文档引用才能找到。

## 各文件的角色（`Statistics_and_computing_submission/`）

| 文件 | 角色 | 规则 |
|---|---|---|
| `ustats_Stat_Comput.tex` | 投稿时的原稿 | **永远不要修改**，只作对照基准 |
| `ustats_revision.tex` | 修订稿 | 所有修订都改在这里；**新增/修改的文本一律用 `\rev{...}` 包起来**（显示为红色），**删除的句子用 `\del{...}` 标记**（红色删除线，仅限行内文本，`\sout` 包不住 display 公式）；preamble 里 `\showchangesfalse` 可一键关闭高亮（`\rev` 变正常黑字、`\del` 整句消失） |
| `response.tex` | 给审稿人的回复信 | 每条意见下先写 `\begin{todo}...\end{todo}`（红色，内部计划），定稿回复写在 `\begin{reply}...\end{reply}`（蓝色）；引用修订稿中改动/删除的文字时用 `\rev{...}`/`\del{...}`（与修订稿同名，但在本文件 preamble 里独立定义，新加宏时注意两边同步） |
| `todo_checklist.tex` | 内部修订清单 | 按稿件位置（从前往后）排序；**每天收工时更新**：把已完成项的 `\bx`（`$\square$`）改成 `$\boxtimes$`，统计已做/未做 |
| `ustats_revision_labels.aux` | label 快照 | 供 `response.tex` / `todo_checklist.tex` 通过 `xr-hyper` 解析对修订稿的 `\ref`/`\pageref`；**修订稿编号变动后要刷新**：重新编译 `ustats_revision.tex`，把其 `.aux` 里的 `\newlabel` 行拷进来（`grep '^\\newlabel' ustats_revision.aux`） |
| `response_drafted_by_claude.tex` | 早期 Claude 起草的整封回复草稿 | 仅供参考/摘抄，不直接编译提交 |
| `SC-report.pdf`, `review_stats_computing.pdf` | 审稿报告原件 | 只读 |

## 审稿意见的标记约定

- `[R1.4]` = Referee 1 的第 4 条 major comment；`[R2.2]` = Referee 2 的第 2 条；
  `[R1.8, minor]` = minor comment。
- `(clear)` / `(minor)` = 快速、自包含的小改动；`(substantial)` = 需要新文本、
  新例子或新分析的大改动。
- 回复信中给审稿人看的编号用审稿人自己的编号（如 Definition 9、Proposition 1），
  括号里或正文中可用 `\ref{}` 同步显示修订稿的当前编号。

## 工作流程

1. 在 `ustats_revision.tex` 中做修订，改动用 `\rev{...}` 包裹。
2. 在 `response.tex` 对应条目的 `reply` 环境里写正式回复（todo 环境保留内部计划）。
3. 收工时更新 `todo_checklist.tex` 的勾选状态（done 改 `$\boxtimes$`，部分完成就标
   "partial done"），并在根目录 `CHANGELOG.md` 追加当天改动摘要。
4. 若修订稿的编号/页码变了，刷新 `ustats_revision_labels.aux` 快照。

## 其他注意

- LaTeX 宏：修订稿的自定义命令很多（`\ustat`、`\vstat`、`\tensorcontraction`、
  `\treewidthp` 等），起草文本时务必沿用稿内既有宏，不要手写裸记号。
- `response.tex` 的 preamble 里复制了修订稿的一份宏定义，修订稿加新宏时要同步。
- 例子编号有特殊处理：`subexample` 环境 + `\setcounter{example}{1}` 让
  running example 的延续显示为 Example 1(a)、1(b)……新增 subexample 会使后续
  字母顺延，引用会自动更新，但需刷新 label 快照。
- git：在指定的工作分支上提交并推送；不要往 `main` 直接推。
