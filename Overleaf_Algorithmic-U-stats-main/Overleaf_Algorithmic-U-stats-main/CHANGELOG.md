# CHANGELOG — Statistics and Computing 修订工作日志

每天收工时在最上方追加一条（配合 `Statistics_and_computing_submission/todo_checklist.tex`）。

---

## 2026-06-18

### 修订稿 `ustats_revision.tex` — index-wise vs tensor-wise（[R1.4]、部分 [R2.2]）

- **正文 3.2（Prop 1 之后）**：新增两段 `\rev` + 一个 `\rev` 例子。
  - 第一段点明 index-wise 方案的**时间与空间**复杂度一起说明：时间
    $\less(|\calA| n^{\mathsf{tw}+1})$、峰值工作内存 $\less(n^{\mathsf{tw}})$
    （每个中间张量至多 tw 个指标）。正文统一只讲 index-wise。
  - 第二段说明实际库（numpy/torch.einsum）走 **tensor-wise（=pairwise）**，
    两法异同：都按消去/收缩顺序、都达最优时间，但中间张量不同、空间可能不同；
    细节转到新附录。
  - 例子 `eg:index_tensor`：$\calA_\diamond=((1,2),(2,3),(3,4),(4,1),(1,3))$
    （所有张量同一个 $T$，分解图 = $K_4$ 去掉边 $\{2,4\}$，$\mathsf{tw}=2$），
    按 index-wise 算出时间 $n^3$、空间 $n^2$。
- **新增附录 D `Index-wise versus Tensor-wise…`（`app:index_tensor`）**：
  - 定义 tensor-wise 两个基本操作（`def:tw_primitives`：(P1) 二元收缩、
    (P2) 一元约化）与 schedule / induced ordering（`def:tw_schedule`）。
  - 证明 tensor-wise 与 index-wise **同样的时间复杂度上界**
    （`lem:tw_upper` 模拟构造给上界，`lem:set_elim`+`lem:tw_coresidence`+
    `lem:tw_lower` 给匹配下界，合成 `pro:tw_time`：
    $C^\ast=\appequal(n^{\mathsf{tw}+1})$）。
  - 空间复杂度按用户要求**轻量讨论**：index-wise $\less(n^{\mathsf{tw}})$；
    tensor-wise 上界 $\less(n^{\mathsf{tw}+1})$（最坏紧，精确参数=carving width，
    脚注引 markov2008/gray2021，不展开），并用 `eg_diamond` 同一例子说明
    tensor-wise 也能达 $n^{\mathsf{tw}}$；外加 dcov 例子说明一元操作 (P2) 不可省。
- 术语统一：第一法称 **index-wise**，第二法称 **tensor-wise**（注明亦称 pairwise）。
- 纯新增，未删改正文原句，故只用 `\rev`，未用 `\del`。
- 容器内 pdflatex 编译至收敛（0 错误、0 未定义引用、65 页），附录自动变为 D
  （其后附录顺延一个字母），`ustats_revision_labels.aux` 快照已刷新；
  response/checklist 重新编译 0 未定义引用。
- checklist：[R1.4]、[R2.2] 均标 partial done（greedy-vs-exhaustive、Zhang 对比、
  实验内存列仍未做）。进度 5 done / 4 partial / 8 open。

#### 当日补充（库归属修正 + 为何 tensor-wise）

- **修正库归属**：tensor-wise 只归给 `torch.einsum` / `opt_einsum`（不再笼统说
  `numpy.einsum` 也走 tensor-wise）。正文、附录 intro、primitives 引言三处均改。
- **dcov remark 重写**：按我们自己的实验（稿内被注释的 dcov 表 + `\Chen` 批注证实
  torch 默认 $O(n^2)$）说明两库差别——`torch.einsum` 走真正的一元约化 (P2)，dcov
  达 $O(n^2)$；`numpy.einsum` 的多算子路径由 `tensordot`（只缩共享指标）拼成、无一元
  约化，被迫做外积 $O(n^4)$。即"numpy 没有 P1（高效收缩/一元）路径，torch 有"。
- **新增 `rem:why_tensorwise`（Remark 9）**：解释 einsum 社区为何用 tensor-wise
  ——(1) 每步二元收缩=矩阵乘法（BLAS/GPU 最优原语，接上 HOIF 的 GPU 加速）；
  (2) regime 差异：量子/张量网络是"张量多、$m$ 大、$n$ 小（常 =2）且 closed-binary,
  瓶颈在 NP-hard 找序"，我们是"$K$ 小、$m$ 固定、$n$ 统一大且 $n\to\infty$、富超边/
  不连通",故指数即一切、序可预计算复用。引 markov2008 + gray2021。
- 重新编译收敛（0 错误、0 未定义引用），快照再刷新（153 labels）。

#### 当日补充（例子双算法展示 + 消元图 + 术语修正）

- **正文例子改为同时展示两种算法**：`eg:index_tensor` 不再只讲 index-wise，新增
  `tab:index_tensor`（单张表、两栏并排：Index-wise / Tensor-wise，各 4 步 +
  cost）。指出尾部差异——消掉 2、4 后剩三个 $(1,3)$ 张量，tensor-wise 用一次
  contraction（步 4）同时消掉 1 和 3，index-wise 要分两步（步 3 消 1、步 4 消 3）；
  两者总复杂度同为 $\Theta(n^3)$，差别只在低阶尾部（如实说明，不夸大为渐近加速）。
- **新增消元过程图** `fig:elim_diamond`：一行画出 $G_{\calA_\diamond}$ 的逐步
  vertex elimination（$K_4{-}\{2,4\}$ → 三角形 → 边 → 单点 → $\varnothing$），
  箭头标注每步被消顶点的度数（2,2,1,0），风格沿用 `fig:graphs_examples`
  （黑色圆圈节点）。最大度 2 = treewidth，无 fill-in。
- 附录空间一节里重复的 tensor-wise 例子删去，改为一句引用主文表格。
- **术语修正（matrix multiplication → tensor contraction）**：P1 是 tensor
  contraction（einsum 操作、可一次消多个指标），matrix multiplication 只是其特例
  （两矩阵共享一个指标，= 稿内 `eg:matrix multiplication`）；库快是因为 contraction
  reshape 后落到 BLAS 矩阵乘。正文、附录 intro、`rem:why_tensorwise` 四处改正。
- 编译收敛（0 错误、0 未定义引用，67 页），快照刷新（155 labels）。

#### 当日补充（表格再调整：合并 + 显式常数 + 并排）

- **tensor-wise 尾部两步合并成一步**：去掉广播中间量 $W$，step 3 直接写成
  $V=\sum_{i_1,i_3}U_1\,U_2\,T(i_1,i_3)$（一次 \Einsum{} 同时消 $i_1,i_3$）。于是
  tensor-wise 3 步、index-wise 4 步，并排表里 tensor 第 4 行留空，直观显示
  index-wise 多一步（差别只在低阶尾部，复杂度同 $\Theta(n^3)$）。
- **cost 写明常数**：系数 = 每个求和项的乘法次数——两因子乘积 $n^3$（系数 1）、
  三因子乘积 $2n^2$（系数 2）；index-wise 最后一步是 $n$ 个标量相加。caption 解释。
- **改回并排**（用户觉得并排好看）：办法是 RHS 引用中间张量时省略指标（step 3 写
  $s_2\,s_4$ / $U_1\,U_2$ 不带括号指标），LHS 定义仍写全指标；这样列宽够、\small 并排
  不溢出。$T(\cdot,\cdot)$ 始终带指标。
- 附录空间一节同步：去掉 $W$ 的措辞，改说"step 3 是三张量的一次 \Einsum{}，用 binary
  原语实现即广播 $U_1\odot U_2$ 再与 $T$ 收缩，均不超过 $n\times n$，故空间 $n^{tw}$"。
- 编译收敛（0 错误、0 未定义引用），快照 155 labels。

#### 当日补充（表格定稿：两个表 + remaining 列 + 4 步 tensor-wise）

- 用户更正：strict tensor-wise 是 pairwise，step 3、4 不能合并（必须先广播 $W$ 再
  收缩）。故 **tensor-wise 改回 4 步**（含 $W=U_1\odot U_2$），表头恢复
  "two tensors at a time"。两法都是 4 步、同 $\Theta(n^3)$。
- **改回两个堆叠表**（上 index-wise、下 tensor-wise，同一 Table float 一个 caption）。
- **新增中间列 "remaining sum for $V$"**：每步算完一个中间张量后，$V$ 还剩下的那个
  求和式（逐步缩小），让消元/收缩过程一目了然。
- 既然分成两个表、不再窄，**所有指标写全**（含 RHS 引用的中间张量）。\footnotesize 排版，
  无溢出。
- cost 显式常数：index-wise $n^3,n^3,2n^2,n$（step 3 三因子积=2 次乘法）；
  tensor-wise $n^3,n^3,n^2,n^2$（每步两因子积=1 次乘法）。
- 正文 prose 去掉"tensor-wise 少一步"的说法，改为"两法都 4 步、复杂度相同，只是尾部
  组织方式不同"；附录空间例子同步用回 $W$ 版本。

#### 当日补充（附录新增两个空间复杂度对照例子）

- 在附录 tensor-wise 一节（空间小节）新增两个 worked example，把"index-wise 空间总是
  $n^{\mathsf{tw}}$、tensor-wise 可能更大"的二分讲具体。两例分解图都是 $K_4$（$\mathsf{tw}=3$）：
  - **`eg:space_K4`**：$\calA_1=((1,2),(1,3),(1,4),(2,3),(2,4),(3,4))$（$K_4$ 六条边）。
    index-wise 峰值 $n^3$；tensor-wise 也能 $n^3$——给了一个 pairwise schedule
    （`tab:space_K4`，Table 5），先并两条含 1 的边成 $n^3$ 的 $W_1$，再与第三条
    fused 收缩消 $i_1$，**始终不形成 $n^4$ 的四阶张量**。两法都 $n^3=n^{\mathsf{tw}}$。
  - **`eg:space_triples`**：$\calA_2=((1,2,3),(1,2,4),(1,3,4),(2,3,4))$（$[4]$ 的四个
    三元子集）。index-wise 峰值 $n^3$；但每个指标都在 3 个张量里，第一步无法求和、
    只能广播两个三元组，而任两个的并集都是 $\{1,2,3,4\}$，**被迫物化 $n^4$**。
    故 tensor-wise 峰值 $n^4=n^{\mathsf{tw}+1}>$ index-wise 的 $n^3$。
  - 结论句：同一张图、同样的 index-wise 空间，但 tensor-wise $n^3$ vs $n^4$——差距由
    指标的 multiplicity（超边结构）决定，而非分解图，正是脚注里 carving-width 的现象。
- 编译收敛（0 错误、0 未定义引用），快照刷新（158 labels）。

#### 当日补充（空间例子补 index-wise 表 + 所有表加 start 行）

- 两个空间例子（`eg:space_K4`、`eg:space_triples`）的表格**改成双栏对照**（上 index-wise、
  下 tensor-wise），把 index-wise 算法也列出来，列 = step | operation | size：
  - $\calA_1$（$K_4$ 边，Table 5）：index-wise $n^3,n^2,n,1$；tensor-wise $n^3,n^3,n^3,n^2,1$。两者峰值都 $n^3=n^{\mathsf{tw}}$。
  - $\calA_2$（四个三元组，Table 6）：index-wise $n^3,n^2,n,1$；tensor-wise 第一步即 $n^4$。
    index-wise $n^3$ < tensor-wise $n^4$。tensor-wise 栏只有 1 行，对比鲜明。
- **所有 schedule 表（Table 1、5、6）加一个 start 行**：第一行只在公式列写出完整的
  \Einsum{} 式（要计算的整个量），step 列与 cost/size 列留空，表示起点；用 midrule 与
  后续步骤分隔。diamond 表放在 "remaining sum for $V$" 列（该列本就追踪 $V$）；空间表放在
  operation 列。
- 编译收敛（0 错误、0 未定义引用、无新 overfull），快照刷新（159 labels）。

#### 当日补充（表格补空间列，时间/空间并重）

- **Table 1（diamond，正文）新增 space 列**，与 time 列并列（原 cost 列改名 time）。
  space = 每步之后仍需存储的中间张量总大小（带常数）：index-wise $n^2, 2n^2, n, 1$；
  tensor-wise $n^2, 2n^2, n^2, 1$。两者**第 2 步都是 $2n^2$**（此时 $s_2,s_4$ 或
  $U_1,U_2$ 两个 $n\times n$ 张量同时驻留），峰值 $2n^2=\appequal(n^{\mathsf{tw}})$。
  正文要时间/空间并重，这样一行就同时给出 time 和 space。caption 解释两列含义。
  5 列略宽，用 `\tabcolsep=4pt` + \footnotesize 容下，无溢出。
- 附录空间例子表（Table 5/6）"size" 列改名 **"space"**（线性 schedule 下 = 该步持有
  张量大小，常数为 1），caption 补注"两法时间都是 $\appequal(n^4)=\appequal(n^{\mathsf{tw}+1})$"。
- 编译收敛（0 错误、0 未定义引用、无新 overfull），快照 159 labels。

---

## 2026-06-10

### 修订稿 `ustats_revision.tex`（作者手动修改，main 提交 `58e9687`）

- **[R1.1] done** — 两处：
  - `def:tensors`（Definition 3）中删去 "there is no time complexity to access an
    entry" 的措辞，改在定义后新增 `\rev` 段落说明约定：复杂度按浮点运算
    （加法/乘法）计数，显式存储的张量取条目视为直接数据访问，不计入浮点运算量。
  - 补完 Algorithm 1（tensorization）后那个未写完的 remark，成为新的
    `rem:complexity_tensorization`：tensorization 总代价
    `O(Σ_k n^{|A_k|}) = O(K n^{m_max})`；并由"每个因子在分解图中构成 clique，
    故 `m_max ≤ tw(G)+1`"论证该步不会主导 U/V-statistic 的总复杂度。
- **[R1.2a] done** — Definition 5 与 Example 1 之间新增 `\rev` 段落：Example 1
  演示 `B = ∅`（输出标量，正文主用情形）；并解释一般情形 `B ≠ ∅` 为何不可或缺
  （Prop. 1 证明逐 index 求和，每个中间步骤都是带非空输出的 Einsum）；指向附录 A
  的两个 `B ≠ ∅` 例子。
- **[R1.3 / R1 总评] partial done** — Prop. 1 之后新增两段 `\rev` 证明思路概述
  （对单个 index 部分求和的时间 `O(|A| n^{deg+1})` / 存储 `n^{deg}` 核算，及其与
  顶点消元的精确对应），并新增整幅示意图 `fig:elimination_sketch`：在
  `A = ((1,2),(2,1),(1,3))` 上对比两种消元顺序（先消中心点 → `O(n³)` 且产生
  fill-in 边；顺序 `(2,1,3)` → `O(n²)` = 最优 `n^{tw+1}`）。
  **未完**：tw 的 worked example（链图 / K₄ / dcov 三例，已起草未入稿）。
- **[R1.9] done** — `[m]^{**}` 记号不再解释而是整体移除：Definition 9 改写为
  `A_k ∈ [m]^*`（与 Definition 4 记号统一；这是全文唯一一处用到双星号的地方）。
- **[R1.2b] done** — `\appendix` 后加 `\numberwithin{example}{section}`：附录例子
  重编号为 A.1、A.2（附录 A）和 C.1（附录 C），不再与正文 Example 2 冲突。
- 其他：`\rev` 实现由 `\textcolor{red}{…}` 改为 `{\color{red} …}`（可以包住
  display 公式和图）；附录矩阵乘法例子的公式改为 display 并标红；清理若干
  注释掉的旧块。

### 回复信 `response.tex`

- 写好正式 reply：R1.1（两个小问各成段）、R1.2a、R1.2b、R1.8（typo 已改
  "running example"）、R1.9（说明记号已整体移除）。
- R1 总评 reply 标 `[PARTIAL]`（proof sketch + 图已完成，其余待办以注释保留）；
  R1.3 reply 标 `Partial done`（worked example 部分待入稿）。
- 已完成条目的 todo 块删除或注释掉。

### 其他

- 新增 `exploration/indexwise_vs_tensorwise.tex`（约 700 行，自包含证明：最优
  pairwise/tensor-wise Einsum 调度在时间与空间上都能达到 treewidth 界；为 R1.4
  做准备，内审后再并入修订稿）。
- `todo_checklist.tex` 勾选更新：**5 done / 2 partial / 10 open**。
- 维护：新增 `CLAUDE.md`（工作区说明）与本 `CHANGELOG.md`

### 补记（当日稍晚）

- 从 Overleaf 拉取作者改动：`rem:ordering` 中删去 "dynamic programming is also
  used in Zhang et al. (2025)" 一句；附录矩阵乘法例子的 `\rev` 移到 `align*`
  外侧。
- **新增删除标记命令** `\del{...}`：红色删除线，`\showchangesfalse` 时整句消失
  （仅限行内文本；内部的 `\citet` 等引用命令需用 `\mbox{}` 包住，否则 ulem 报
  错）。两边 preamble 均加载 `\usepackage[normalem]{ulem}`。被删的 Zhang et
  al. 一句已用 `\del` 标回，审稿人可见删除痕迹。
- 回复信的 `\Rev` 统一更名为小写 `\rev`（与修订稿同名；新增的删除标记在两个
  文件里也都叫 `\del`），不再用大小写区分文件。
- 工作分支已合并进 `main`（fast-forward 至 `a7d7df2`）。
- 容器内装好 TeX Live 并完整编译修订稿（pdflatex ×4 + bibtex/bibunits，
  0 错误，59 页），**`ustats_revision_labels.aux` 快照已刷新**：新增
  `rem:complexity_tensorization`（Remark 3，原 Remark 3–5 顺延为 4–6）、
  `fig:elimination_sketch`（Figure 2，后续图号顺延）、附录例子改为
  A.1/A.2/C.1。response/checklist 的 `\ref` 现在显示新编号。

#### 当日补充（space 计入输入 T；附录例子补 time+space+完整 schedule）

- 修正 space 计算：之前漏了输入张量 T 的占用。现在 space = 该步之后内存中所有张量
  总大小（含输入 T，直到其最后一次被用到）。diamond（Table 1）peak 改为 $3n^2$
  （T + 两个 n×n 中间张量并存于 step 2），start 行 space = $n^2$（初始 T）。
- 附录两个空间例子（Table 5/6）补上 time 列和 start 行，space 同样计入 T，并补全
  schedule（A_2 tensor-wise 现为完整 3 步）。结构 = operation | time | space（与正文
  Table 1 一致，唯一差别是因 3 阶张量太宽、省去了 remaining 列，否则并排放不下）。
- 编译 0 错误、0 未定义引用、无新 overfull；快照 159。

#### 当日补充（附录 Table 5/6 改横排整页，恢复 remaining 列）

- 把附录两个空间例子表（`tab:space_K4`、`tab:space_triples`）从竖排 4 列改为
  **横排（landscape）整页** 的 5 列，结构与正文 Table 1 **完全一致**：
  `# | operation | remaining sum for $V$ | time | space`，含 start 行、完整
  index-wise + tensor-wise schedule。横排宽度充裕，3 阶张量的全指标公式不再放不下，
  之前为省宽度删掉的 "remaining" 列得以恢复，caption 的 "in the format of
  Table~\ref{tab:index_tensor}" 现已名副其实。
- 实现：用 `sn-jnl.cls` 在载入 `rotating` 时 `\let` 出来的 `\sidewaystableorg`
  原始环境（类自身把 `sidewaystable` 重定义成带 threeparttable 的版本，会冲突）。
  曾试 `\resizebox{\textwidth}{!}{...}` 包 tabular 失败（与 `\color`/booktabs 冲突，
  报 Missing \endgroup），改横排后无需缩放。
- 数值复核无误：A_1 两法 peak 均 $n^3$；A_2 index-wise peak $n^3$、tensor-wise
  第 1 步即形成 $n^4+n^3$（任两个三元组并集 = $\{1,2,3,4\}$，carving width 点）。
- 编译 0 错误、0 未定义引用、69 页（含参考文献）；两张横排表各自独占一页、无 overfull；
  快照已刷新（page 号随参考文献回归而更新）；response/checklist 0 未定义引用。
