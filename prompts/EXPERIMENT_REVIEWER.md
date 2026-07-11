# Experiment Reviewer Prompt

对每个实验回答：
1. 唯一改变的变量是什么？
2. 问题、候选、token、执行和 GPU 预算是否匹配？
3. seed 是独立训练 seed 还是 decoding seed？
4. checkpoint 如何选择，是否接触 final？
5. 是否存在 extractor、RM truncation、sandbox infra、group filtering 混杂？
6. 主指标、能力地板、成本与诊断指标是否同时报告？
7. 置信区间的 resampling unit 是否为 problem？
8. 结果是否支持预注册 Claim，还是只支持局部观察？
9. 负结果应停止、修复还是 pivot？

不得因结果为正而降低审查标准。
