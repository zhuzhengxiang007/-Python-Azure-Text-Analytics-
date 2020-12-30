# coding: utf-8
import os
import logging

from azure.core.credentials import AzureKeyCredential
from azure.ai.textanalytics import TextAnalyticsClient, \
    EntitiesRecognitionTask, \
    PiiEntitiesRecognitionTask, \
    KeyPhraseExtractionTask

_LOGGER = logging.getLogger(__name__)
#初始化配置访问Azure Text Analytics API ENDPOINT AND KEY
os.environ.setdefault('AZURE_TEXT_ANALYTICS_ENDPOINT', "")
os.environ.setdefault('AZURE_TEXT_ANALYTICS_KEY', "")

class Azure_Text_Analytics(object):

    def __init__(self):
        self.endpoint = os.environ["AZURE_TEXT_ANALYTICS_ENDPOINT"]
        self.key = os.environ["AZURE_TEXT_ANALYTICS_KEY"]
        self.text_analytics_client = TextAnalyticsClient(endpoint=self.endpoint, credential=AzureKeyCredential(self.key))

    def detect_language(self,documents):
        print('检测语言\n')
        result = self.text_analytics_client.detect_language(documents)

        review_to_language = {}
        reviewed_docs = [doc for doc in result if not doc.is_error]
        for idx, doc in enumerate(reviewed_docs):
            lang = []
            lang.append(doc.primary_language.name)
            lang.append(doc.primary_language.iso6391_name)
            review_to_language[idx] = lang
            if doc.is_error:
                review_to_language[doc.id] = doc.error
        # [END detect_language]
        return review_to_language
    
    def extract_key_phrases(self,documents):
        print('从文档中提取关键短语\n')
        result = self.text_analytics_client.extract_key_phrases(documents)
        print(result)
        review_to_language = {}
        for idx, doc in enumerate(result):
            if not doc.is_error:
                review_to_language[idx] = doc.key_phrases
        # [END extract_key_phrases]
        return review_to_language

    def alternative_document_input(self,documents):
        print('使用字典将文档传递到端点\n')
        result = self.text_analytics_client.detect_language(documents)
        review_to_language = {}
        for idx, doc in enumerate(result):
            if not doc.is_error:
                lang = []
                lang.append(doc.primary_language.name)
                lang.append(doc.primary_language.iso6391_name)
                lang.append(doc.primary_language.confidence_score)
                review_to_language[idx] = lang
            if doc.is_error:
                review_to_language[idx] = doc.error
        return review_to_language

    def analyze_healthcare(self,documents):
        print('分析医疗机构\n')
        #需要api version v3.1-preview.3
        text_analytics_client = TextAnalyticsClient(
            endpoint=self.endpoint, 
            credential=AzureKeyCredential(self.key),
            api_version="v3.1-preview.3")
        poller = text_analytics_client.begin_analyze_healthcare(documents, show_stats=True)
        result = poller.result()
        docs = [doc for doc in result if not doc.is_error]
        review_to_language = {}
        for idx, doc in enumerate(docs):
            entitys = {}
            for entity in doc.entities:
                entitys['entity'] = entity.text
                entitys['Category'] = entity.category
                entitys['Subcategory'] = entity.subcategory
                entitys['Offset'] = entity.offset
                entitys['Confidence_score'] = entity.confidence_score
                if entity.links is not None:
                    for link in entity.links:
                        entitys['ID'] = link.id
                        entitys['Data_source'] = link.data_source
            for relation in doc.relations:
                entitys['Source'] = relation.source.text
                entitys['Target'] = relation.target.text
                entitys['Type'] = relation.relation_type
                entitys['Bidirectional'] = relation.is_bidirectional
            review_to_language[idx] = entitys
        return review_to_language
    
    def sample_analyze_sentiment_with_opinion_mining(self,documents):
        print('通过仔细分析文档中的情绪，分析出句子中存在的个人意见。仅适用于API版本v3.1-preview和更高版本\n')
        result = self.text_analytics_client.analyze_sentiment(documents, show_opinion_mining=True)
        doc_result = [doc for doc in result if not doc.is_error]
        review_to_language = {}
        review_to_language['positive_reviews'] = [doc for doc in doc_result if doc.sentiment == "positive"]
        review_to_language['mixed_reviews'] = [doc for doc in doc_result if doc.sentiment == "mixed"]
        review_to_language['negative_reviews'] = [doc for doc in doc_result if doc.sentiment == "negative"]

        aspect_to_complaints = {}
        for document in doc_result:
            for sentence in document.sentences:
                for mined_opinion in sentence.mined_opinions:
                    aspect = mined_opinion.aspect
                    if aspect.sentiment == 'negative':
                        aspect_to_complaints.setdefault(aspect.text, [])
                        aspect_to_complaints[aspect.text].append(mined_opinion)
        review_to_language['aspect_to_complaints'] = aspect_to_complaints
        
        return review_to_language
        
    def analyze_sentiment(self,documents):
        print('分析文档中的情绪,返回一个整体和每句话的情绪\n')
        result = self.text_analytics_client.analyze_sentiment(documents)
        docs = [doc for doc in result if not doc.is_error]
        review_to_language = {}
        review_to_language_doc = []
        for idx, doc in enumerate(docs):
            lang = {}
            lang['Document_text'] = documents[idx]
            lang['Overall_sentiment'] = doc.sentiment
            review_to_language_doc.append(lang)
        review_to_language['review_to_language_doc'] = review_to_language_doc
        
        positive_reviews = [doc for doc in docs if doc.sentiment == 'positive']
        positive_reviews = [
            review for review in positive_reviews
            if review.confidence_scores.positive >= 0.9
        ]
        review_to_language['positive_reviews'] = positive_reviews

        positive_reviews_final = []
        for idx, review in enumerate(positive_reviews):
            print("Looking at positive review #{}".format(idx + 1))
            any_sentence_not_positive = False
            for sentence in review.sentences:
                print("...Sentence '{}' has sentiment '{}' with confidence scores '{}'".format(
                    sentence.text,
                    sentence.sentiment,
                    sentence.confidence_scores
                    )
                )
                if sentence.sentiment != 'positive':
                    any_sentence_not_positive = True
            if not any_sentence_not_positive:
                positive_reviews_final.append(review)
        review_to_language['positive_reviews_final'] = positive_reviews_final

        return review_to_language

    def analyze(self,documents,display_name):
        print('在单个请求中将多个分析一起批处理\n')

        text_analytics_client = TextAnalyticsClient(
            endpoint=self.endpoint, 
            credential=AzureKeyCredential(self.key),
            api_version="v3.1-preview.3"
        )

        poller = text_analytics_client.begin_analyze(
            documents,
            display_name=display_name,
            entities_recognition_tasks=[EntitiesRecognitionTask()],
            pii_entities_recognition_tasks=[PiiEntitiesRecognitionTask()],
            key_phrase_extraction_tasks=[KeyPhraseExtractionTask()]
        )

        result = poller.result()
        review_to_language = {}
        for i,page in result:
            lang = []
            for task in page.entities_recognition_results:
                docs = [doc for doc in task.results if not doc.is_error]
                for idx, doc in enumerate(docs):
                    for entity in doc.entities:
                        entitys = {}
                        entitys['Entity'] = entity.text
                        entitys['Category'] = entity.category
                        entitys['Confidence_Score'] = entity.confidence_score
                        entitys['Offset'] = entity.offset
                        lang.append(entitys)

            for task in page.pii_entities_recognition_results:
                docs = [doc for doc in task.results if not doc.is_error]
                for idx, doc in enumerate(docs):
                    for entity in doc.entities:
                        entitys = {}
                        entitys['piiEntity'] = entity.text
                        entitys['piiCategory'] = entity.category
                        entitys['piiConfidence_Score'] = entity.confidence_scores
                        lang.append(entitys)

            for task in page.key_phrase_extraction_results:
                docs = [doc for doc in task.results if not doc.is_error]
                for idx, doc in enumerate(docs):
                    entitys = {}
                    entitys['Document_text'] = documents[idx]
                    entitys['Key_Phrases'] = doc.Key_Phrases
                    lang.append(entitys)
            review_to_language[i] = lang
        
        return review_to_language

    def authentication_with_api_key_credential(self,documents):
        print('使用api密钥凭据进行身份验证\n')
        result = self.text_analytics_client.detect_language(documents)

        docs = [doc for doc in result if not doc.is_error]
        review_to_language = {}
        for idx, doc in enumerate(docs):
            lang = {}
            lang['Language_detected'] = doc.primary_language.name
            lang['Confidence_score'] = doc.primary_language.confidence_score
            review_to_language[idx] = lang
        
        return review_to_language

    def authentication_with_azure_active_directory(self,documents):
        print('使用目录进行身份验证\n')
        from azure.identity import DefaultAzureCredential

        text_analytics_client = TextAnalyticsClient(self.endpoint, credential=DefaultAzureCredential())
        result = text_analytics_client.detect_language(documents)

        docs = [doc for doc in result if not doc.is_error]
        review_to_language = {}
        for idx, doc in enumerate(docs):
            lang = {}
            lang['Language_detected'] = doc.primary_language.name
            lang['Confidence_score'] = doc.primary_language.confidence_score
            review_to_language[idx] = lang
        
        return review_to_language

    def recognize_entities(self,documents):
        print('识别文档中的命名实体\n')
        result = self.text_analytics_client.recognize_entities(documents)
        result = [review for review in result if not review.is_error]
        organization_to_reviews = {}
        for idx, review in enumerate(result):
            for entity in review.entities:
                if entity.category == 'Organization':
                    organization_to_reviews.setdefault(entity.text, [])
                    organization_to_reviews[entity.text].append(documents[idx])

        return organization_to_reviews
    
    def recognize_linked_entities(self,documents):
        print('识别文档中的链接实体\n')
        result = self.text_analytics_client.recognize_linked_entities(documents)
        docs = [doc for doc in result if not doc.is_error]
        entity_to_url = {}
        for doc in docs:
            for entity in doc.entities:
                print("Entity '{}' has been mentioned '{}' time(s)".format(
                    entity.name, len(entity.matches)
                ))
                if entity.data_source == "Wikipedia":
                    entity_to_url[entity.name] = entity.url
        # [END recognize_linked_entities]

        print("\nNow let's see all of the Wikipedia articles we've extracted from our research documents")
        for entity, url in entity_to_url.items():
            print("Link to Wikipedia article for '{}': {}".format(
                    entity, url
            ))
        return entity_to_url

    def recognize_pii_entities(self,documents):
        print('识别文档中的个人身份信息\n')
        result = self.text_analytics_client.recognize_pii_entities(documents)
        docs = [doc for doc in result if not doc.is_error]
        for idx, doc in enumerate(docs):
            print("Document text: {}".format(documents[idx]))
            print("Redacted document text: {}".format(doc.redacted_text))
            for entity in doc.entities:
                print("...Entity '{}' with category '{}' got redacted".format(
                    entity.text, entity.category
                ))

        # [END recognize_pii_entities]
        print("All of the information that I expect to be redacted is!")

        print(
            "Now I want to explicitly extract SSN information to add to my user SSN database. "
            "I also want to be fairly confident that what I'm storing is an SSN, so let's also "
            "ensure that we're > 60% positive the entity is a SSN"
        )
        ssns = []
        for doc in docs:
            for entity in doc.entities:
                if entity.category == 'U.S. Social Security Number (SSN)' and entity.confidence_score >= 0.6:
                    ssns.append(entity.text)

        return ssns