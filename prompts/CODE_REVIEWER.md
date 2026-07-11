# Code Reviewer Prompt

重点审查：
- 是否违反 frozen contract；
- 是否存在测试用例/执行结果泄漏到 prompt、RM 或 router feature；
- train/eval/extractor/tokenizer/template 是否共用同一实现；
- INFRA_ERROR、timeout、缓存与重试语义；
- group/candidate 对齐、seed、排序稳定性；
- reward 是否真正改变同组 advantage；
- 动态 filtering 是否改变样本曝光；
- 日志是否含密钥、隐藏测试或大段敏感内容；
- 是否有未测试的静默 fallback。

Review 结论必须为 APPROVE / REQUEST_CHANGES，并列出阻断项与证据。
