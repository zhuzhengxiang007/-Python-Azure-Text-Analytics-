from src.Azure_Text_Analytics import Azure_Text_Analytics

documents = [
            """
            Take "children's Classics Reading" as the educational idea
Grasp the core of education from the source
"Reading" is the method, "classics" is the content. The classics are pre-existing, dominant and eternal. In the most appropriate time, children should read the most appropriate method to teach the most appropriate teaching materials, from the source to grasp the core of education, namely, the three principles of education.
Children are willing to recite and repeat
Children's mental characteristics are good at intuition and memory, but not good at speculation and understanding. Therefore, before the age of 13, let children recite more profound cultural materials for a long time. When they grow up, gradually enrich their life experience, and naturally mature their understanding, they can learn by analogy.
            """
        ]
sample = Azure_Text_Analytics()
#detect_language = sample.detect_language(documents)
#print(detect_language)

extract_key_phrases = sample.extract_key_phrases(documents)
print(extract_key_phrases)