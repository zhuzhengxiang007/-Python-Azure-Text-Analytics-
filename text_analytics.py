from src.Azure_Text_Analytics import Azure_Text_Analytics

documents = [
            """
            The concierge Paulette was extremely helpful. Sadly when we arrived the elevator was broken, but with Paulette's help we barely noticed this inconvenience.
            She arranged for our baggage to be brought up to our room with no extra charge and gave us a free meal to refurbish all of the calories we lost from
            walking up the stairs :). Can't say enough good things about my experience!
            """,
            """
            北京文礼经典学校以“开发人性，传承智慧”为办学主旨，把握人性内容的全幅性，顺应人性发展的全程性，围绕传承智慧的教育目的，展开全人格教育实践，注重培养孩子志道、乐学、博文、约礼的人文精神及严谨、耐烦、开朗、友爱的处世之风。
            """
        ]
sample = Azure_Text_Analytics()
#detect_language = sample.detect_language(documents)
#print(detect_language)

extract_key_phrases = sample.extract_key_phrases(documents)
print(extract_key_phrases)