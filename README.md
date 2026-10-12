# Waffo Payments Skill

一个帮助 AI 编程助手完成 Waffo/Pancake 收款接入的开源 Skill，涵盖注册审核、新增店铺、商品配置、网站后台接入和付款退款验收。

An open-source workflow skill for Waffo/Pancake payment onboarding, store setup, backend integration, and payment/refund verification. Instructions are currently written in Chinese.

> 社区整理的流程，非 Waffo 官方产品。它为 AI 助手提供操作指引，不是支付 SDK，也不保证自动通过审核或无需人工介入。

## 能做什么

- **从零开始**：注册、邮箱验证、商户申请及审核准备，获批后完成接入。
- **已有账号**：为新站新增或核对店铺，配置品牌、域名、商品、订阅、通知及结算账户。
- **网站后台**：对接服务端密钥、Webhook、商品映射、订单、积分/权益与既有支付渠道。
- **验收与售后**：检查付款到账、重复/延迟通知、订阅续费与取消，以及全额/部分退款和账本对账。
- **故障排查**：处理环境混用、配置未保存、未付款订单阻塞重试等问题。

不同站点使用自己的主体资料、商品价格、账号、密钥和审核结果。真实付款、退款、转账及合同签署需要相应授权；验证码、身份认证和付款资料由本人完成。

## 安装到 Codex

需要已安装 Codex；浏览器后台操作还需要受支持的浏览器工具，推荐已配置的 OpenCLI。商品清单校验脚本需要 Python 3；Skill 的文档本身不依赖 Python。网站接入所需语言、SDK 和部署工具按具体项目选择。

### 方式一：让 Codex 安装

将此仓库地址交给 Codex，并说：

> 请将 https://github.com/yi8882025/waffo-payments 安装为我本机的全局 Skill，保留全部 references 和 scripts，不覆盖已有同名技能。

### 方式二：手动安装

将整个仓库克隆到用户技能目录；如同名目录已存在，请先检查，不要覆盖：

```sh
git clone https://github.com/yi8882025/waffo-payments.git ~/.agents/skills/waffo-payments
```

也可以在 GitHub 选择 **Code → Download ZIP**，解压后将文件夹重命名为 `waffo-payments`，放到 `~/.agents/skills/`。Windows 可使用用户目录下的 `.agents/skills/waffo-payments`。

确认 `SKILL.md` 直接位于 `waffo-payments` 文件夹内，避免多套一层目录。Codex 会自动发现技能；若未出现，重启 Codex。参见 [Codex 官方技能说明](https://learn.chatgpt.com/docs/build-skills)。不要在多个技能目录重复安装同名技能。

## 使用示例

在 Codex 打开目标网站项目，然后输入：

**已有审核账号：**

> 使用 $waffo-payments 给这个站接入 Waffo。我已有审核通过的账号，需要新增店铺。请先检查现有支付代码与配置，再完成商品配置、后台接入和验收。

**从注册开始：**

> 使用 $waffo-payments，从注册 Waffo 开始，帮我完成审核准备、店铺与商品配置，再接入网站后台。

**检查支付问题：**

> 使用 $waffo-payments 检查这个站的付款和权益到账流程，排查“无法发起支付”，先查已有订单，避免重复创建支付。

**准备退款：**

> 使用 $waffo-payments 帮我核对指定订单的可退金额和权益影响，整理退款步骤，先不要提交真实退款。

提前准备正式域名、Logo、客服邮箱、真实经营主体资料，以及已经确定的商品价格、订阅周期和权益规则。助手应先读取项目记录，缺少的信息再询问。

## 目录

- `SKILL.md`：入口、分流及执行边界。
- `references/new-account.md`：注册与商户审核。
- `references/existing-account.md`：已有账号新增店铺。
- `references/integration.md`：商品、密钥、Webhook 和网站后台。
- `references/acceptance-refunds.md`：验收、退款与对账。
- `references/troubleshooting.md`：常见问题与恢复。
- `references/sources.md`：官方资料与核实范围。
- `scripts/check-catalog.py`：离线商品清单格式校验，不调用支付接口。

查看清单字段及运行检查：

```sh
python3 scripts/check-catalog.py --help
python3 scripts/check-catalog.py /path/to/catalog.json
python3 -m unittest discover -s tests -v
```

校验通过只表示清单结构符合要求，不证明价格已批准、平台支持相关币种或支付已成功。

## 隐私与维护

仓库只包含通用流程、文档和离线校验工具，不包含原接入项目的账号、密钥、域名、客户、订单或收款账户资料。请勿在 Issue、PR 或日志中上传真实凭据、证件、客户信息及带 token 的支付链接。

Waffo 的界面、API、费率和可用能力可能变化，执行时必须核对当前官方资料和真实后台。欢迎以脱敏步骤和可复现证据改进流程。本仓库未声称所有主体的开户、所有支付方式或退款场景都已实测通过。

## License

[MIT](LICENSE)
