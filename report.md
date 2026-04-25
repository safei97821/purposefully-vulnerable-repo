# Semgrep 自写规则源码分析报告

## 学生信息

姓名：周宇坤  
学号：25140924  
GitHub账号：safei97821  

## 一、仓库说明

本次实验使用 GitHub 上的 purposefully-vulnerable-repo 仓库（已 fork 到本人账号）作为分析对象。

本次扫描严格按照要求，仅使用本人自编写的 Semgrep 规则进行分析，未使用官方规则库或 p/owasp-top-ten 等现成规则包。

## 二、人工源码分析

通过对仓库源码的阅读，重点分析了涉及外部输入与系统命令执行的模块 app.py。

发现代码中存在如下模式：

- 使用 subprocess.call / subprocess.check_output 执行系统命令
- 使用 shell=True
- 命令参数通过字符串拼接构造

该模式存在命令注入风险。如果攻击者控制输入参数，可能拼接恶意命令并执行。

## 三、适合用 Semgrep 表达的原因

该问题适合用 Semgrep 规则表达，原因如下：

1. 危险 API 具有固定形式，例如 subprocess / os.system。
2. shell=True 是稳定的危险特征。
3. 动态命令参数可通过变量匹配识别。
4. 可通过 pattern-not 排除固定字符串，减少误报。

## 四、规则触发判据

本次规则设计的触发条件如下：

- 调用 subprocess.run / subprocess.call / subprocess.check_output / subprocess.Popen。
- 参数中包含 shell=True。
- 调用 os.system 且参数为变量或动态字符串。
- 命中点位于危险 API 调用处。

## 五、规则说明

规则文件路径：

```text
rules/command-injection.yaml

rules/command-injection.test.py
