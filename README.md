适用于Python的Azure Text Analytics客户端库的示例

这些代码示例显示了Azure文本分析客户端库的常见方案操作。样本的异步版本需要Python 3.5或更高版本。

您可以使用Cognitive Services / Text Analytics API密钥或通过Azure Active Directory使用Azure身份的令牌凭证对客户端进行身份验证：

Azure_Text_Analytics.py

方法名称	          描述

detect_language	检测文档中的语言

recognize_entities	识别文档中的命名实体

recognize_linked_entities	识别文档中的链接实体

recognize_pii_entities	识别文档中的个人身份信息

extract_key_phrases	从文档中提取关键短语

sample_analyze_sentiment_with_opinion_mining analyze_sentiment 	分析文档的情绪

alternative_document_input	使用字典将文档传递到端点

analyze_healthcare	分析医疗机构

analyze	在单个请求中将多个分析一起批处理

先决条件

使用此软件包需要Python 2.7或3.5或更高版本（如果使用asyncio，则需要3.5或更高版本）

您必须具有Azure订阅和 Azure Text Analytics帐户才能运行这些示例。

安装

Install the Azure Text Analytics client library for Python with pip:

pip install azure-ai-textanalytics --pre

For more information about how the versioning story of the SDK corresponds to the versioning story of the service's API, see here.

pip install azure-identity# -Python-Azure-Text-Analytics-
