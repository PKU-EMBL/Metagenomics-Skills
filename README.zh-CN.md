# Metagenomics Skills（中文说明）

[English](README.md)

面向 shotgun metagenomics（宏基因组鸟枪法测序）的可移植 Agent Skills：

**研究设计 → 质控 → 组装 → 比对 → 分箱 → 分类 → 功能注释 → 微生物挖掘 → 统计与科研交付**

仓库目前包含 **226 个** Skills，采用开放的
[`SKILL.md` 规范](https://agentskills.io)，同一套内容可供 Claude Code、
Codex、Cursor、Kimi Code、ZCode、Qwen Code 等 coding agent 使用。Skills
负责给 Agent 提供领域流程、命令模式、质量门控和解释边界；它们不会代替
Conda/容器环境、数据库或计算资源。

当前版本为 **v1.25.0**：对 101 个既有 Skills 统一补强了发布级执行、验证、
恢复、provenance 与证据边界契约。

## 快速安装

### Claude Code

```text
/plugin marketplace add PKU-EMBL/Metagenomics-Skills
/plugin install metagenomics@metagenomics-skills
```

### Codex 插件

```bash
codex plugin marketplace add PKU-EMBL/Metagenomics-Skills
codex plugin add metagenomics@metagenomics-skills
```

### Kimi Code / ZCode / Qwen Code / 目录安装

```bash
git clone https://github.com/PKU-EMBL/Metagenomics-Skills.git
cd Metagenomics-Skills

# 推荐：54 个高频 Skills，启动上下文更小
./scripts/install-platforms.sh --user --profile core kimi zcode qwen

# ~/.agents/skills 同时供 Codex、Kimi Code、ZCode 使用；Qwen 走原生目录
./scripts/install-platforms.sh --user --profile core agents qwen

# 全量 226 个 Skills
./scripts/install-platforms.sh --user --profile full all
```

常用选项：

```bash
# 查看支持的平台和任务包
./scripts/install-platforms.sh --list-platforms
./scripts/install-platforms.sh --list-profiles

# 安装到指定项目
./scripts/install-platforms.sh --project --project-root /path/to/project \
  --profile genome-resolved agents qwen

# 不指定 profile 时，--skill 可只安装指定 Skills
./scripts/install-platforms.sh --user --skill fastp --skill multiqc kimi

# 不支持软链接时复制；先预览，不写文件
./scripts/install-platforms.sh --target ~/.new-agent/skills \
  --profile routing --mode copy --dry-run

# 将已有目标切换为更小的 profile，并安全清理此前由本工具管理的其余 Skills
./scripts/install-platforms.sh --user --profile routing --prune kimi
```

Kimi Code 也可以直接加载当前仓库，无需安装：

```bash
kimi --skills-dir "$PWD/skills"
```

完整路径、ZCode marketplace、Qwen extension、Windows copy 模式和冲突处理：
[docs/multi-platform.md](docs/multi-platform.md)。

## Profiles

| Profile | 用途 |
|---------|------|
| `routing` | 仅安装规划和工具路由 Hub，基础上下文最小 |
| `core` | 常用 read profiling、MAG、挖掘、统计和路由 |
| `read-profiling` | reads 质控、宿主去除、物种与功能 profiling |
| `genome-resolved` | 组装、比对、分箱、MAG QC、分类和注释 |
| `mining` | BGC、AMR、病毒、质粒/MGE、代谢和防御系统 |
| `statistics` | MultiQC、多样性、差异分析、网络和工作流 |
| `ai-search` | 同源/结构搜索、系统发育、DNA/蛋白语言模型 |
| `contamination` | 对照设计、污染识别和宿主 reads 去除 |
| `long-read` | ONT / PacBio 质控、过滤、比对、组装和 profiling |
| `virome` | 病毒发现、质量评估、vOTU、宿主和分类 |
| `strain-resolved` | 菌株系统发育、群体 SNV、微多样性和传播证据 |
| `resistome-mobilome` | ARG、MGE、宿主关联和 HGT 分层证据 |
| `transmission` | 菌株共享、来源混合、重组和传播模型 |
| `eukaryotic` | 微生物真核 contig、基因、分箱和质量评估 |
| `pangenome` | 原核泛基因组、注释、去冗余和系统发育 |
| `metatranscriptomics` | 微生物 RNA 质控、rRNA 去除、定量和功能分析 |
| `metabolic-modeling` | 基因组尺度和群落代谢模型 |
| `workflows` | Nextflow、Snakemake 和固定版本的 nf-core 工作流 |
| `full` | 全部 226 个 Skills |

多个 profile 可以叠加：

```bash
./scripts/install-platforms.sh --user \
  --profile genome-resolved --profile mining kimi zcode qwen
```

## 建议的 Agent 使用方式

先明确让 Agent 处于哪种模式：

- **advise**：只解释，不改文件、不运行；
- **plan**：读取元数据后给出分阶段方案；
- **prepare**：生成 manifest、脚本、工作流和 dry-run；
- **execute**：经确认后执行，并逐阶段检查结果；
- **review**：审计既有结果，不擅自重跑。

推荐提示词：

```text
请使用 metagenomics-workflow 和 tool-selection，以 plan 模式设计流程，
暂时不要执行。先检查样本表、read 类型、对照/批次、统计单元、计算资源和
数据库。输出每个阶段的输入、输出、资源、质量门控、失败/恢复策略和
provenance 文件；所有未知信息请显式标记，不要猜测。
```

Agent 必须区分“已观察”“假设”“已生成但未执行”“已执行并验证”“失败或未
检查”。不能仅凭退出码宣称数据已 clean，也不能把 BGC、AMR、病毒、通路或
网络预测写成已实验验证的结论。

详见：[coding-agent playbook](docs/agent-playbook.md) ·
[getting started](docs/getting-started.md) ·
[standard pipeline](docs/standard-pipeline.md) ·
[ARG–MGE–宿主–菌株证据指南](docs/arg-mge-host-strain.md) ·
[skills catalog](docs/skills.md)。

## 典型路线

- 群落组成：`fastp` → `kneaddata` → `metaphlan` / `singlem` /
  `kraken2`+`bracken` → `research-analysis`
- Genome-resolved：QC → `megahit` / long-read assembler → mapping →
  `basalt` / ensemble binning → `checkm2` + `gunc` → `gtdbtk`
- 病毒/MGE：`virome-analysis` → `genomad` / `virsorter2` → `checkv` → `vcontact` / `spacepharer`
- ARG/MGE/宿主/HGT：`resistome-analysis` → `mobilome-analysis` → `arg-mge-host-linkage` / `horizontal-gene-transfer`
- 菌株共享/传播：`strain-resolved-analysis` → `strain-transmission`；分层网络用 `transfer-network-analysis`
- BGC/元素循环：`microbial-mining` → 对应专用 Skill
- 统计与作图：`research-analysis` → `microeco` / `maaslin2` /
  `ancombc` / network skills

## 开发与校验

```bash
python3 -m pip install -r requirements-dev.txt
python3 scripts/validate-skills.py
```

贡献规范见 [CONTRIBUTING.md](CONTRIBUTING.md)。许可证：MIT。
