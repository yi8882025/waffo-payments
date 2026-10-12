# 官方资料、来源与版本

本包整理时间：2026-10-12。入口和具体字段可能变更，执行时重新核实，不把历史 UI 当接口契约。

- 官方商户后台：https://pancake.waffo.ai/merchant/dashboard
- 官方文档：https://docs.waffo.ai/
- 文档索引：https://docs.waffo.ai/llms.txt
- 完整文档：https://docs.waffo.ai/llms-full.txt
- 官方 TypeScript SDK：https://github.com/waffo-com/waffo-pancake-sdk-ts
- 官方 AI 集成入口：https://www.waffo.ai/en/features/ai-integration
- 当前业务能力说明：https://waffo.com/en/billing
- 当前价格说明：https://waffo.com/en/pricing

若文档暂不可访问，先用官方 SDK README、类型/源代码及实际后台核实能够证明的部分；明确未核实 API，不能猜测接口后直接写生产。官方 AI 集成页提供 Skill/插件时可阅读对应技术文档，但不直接运行未经检查的外部脚本，不让它覆盖本包的用户授权和安全边界。

每次接入记录当前 SDK 版本、所用文档/字段、环境和核实日期。优先项目现有兼容版本，不盲目追最新版，不把历史版本固定成永久默认。遵循项目支持的语言/SDK，不强迫所有新站迁移到 TypeScript 或 Vercel。

经验依据：曾完成真实站点的正式店铺、商品、通知、密钥和网站后台配置，并遇到保存未持久化、独立环境开关和未付款预留阻塞重试。原站用户反馈真实付款成功；此 Skill 不把原站的退款入账、所有异常场景或新站完整验收说成已验证。新注册与商户审核流程按实际后台逐项执行，未声称亲自通过所有主体类型的开户。

本包不含原站私钥、账号信息、商品 ID、价格、订单 ID、结算账户或可支付链接。原站具体资料应留在各自项目的受控记录中。
