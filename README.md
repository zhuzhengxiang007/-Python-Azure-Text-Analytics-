适用于Python的Azure Text Analytics客户端库的示例
这些代码示例显示了Azure文本分析客户端库的常见方案操作。样本的异步版本需要Python 3.5或更高版本。
您可以使用Cognitive Services / Text Analytics API密钥或通过Azure Active Directory使用Azure身份的令牌凭证对客户端进行身份验证：

表1
文档名称	描述
sample_detect_language.py和sample_detect_language_async.py	检测文档中的语言
sample_recognize_entities.py和sample_recognize_entities_async.py	识别文档中的命名实体
sample_recognize_linked_entities.py和sample_recognize_linked_entities_async.py	识别文档中的链接实体
sample_recognize_pii_entities.py和sample_recognize_pii_entities_async.py	识别文档中的个人身份信息
sample_extract_key_phrases.py和sample_extract_key_phrases_async.py	从文档中提取关键短语
sample_analyze_sentiment.py和sample_analyze_sentiment_async.py	分析文件的情绪
sample_alternative_document_input.py和sample_alternative_document_input_async.py	使用字典将文档传递到端点
sample_analyze_healthcare.py和sample_analyze_healthcare_async.py	分析医疗机构
sample_analyze.py和sample_analyze_async.py	在单个请求中将多个分析一起批处理

先决条件
使用此软件包需要Python 2.7或3.5或更高版本（如果使用asyncio，则需要3.5或更高版本）
您必须具有Azure订阅和 Azure Text Analytics帐户才能运行这些示例。

安装
Install the Azure Text Analytics client library for Python with pip:
pip install azure-ai-textanalytics --pre
For more information about how the versioning story of the SDK corresponds to the versioning story of the service's API, see here.
pip install azure-identity# -Python-Azure-Text-Analytics-
