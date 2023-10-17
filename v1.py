from llama_index import VectorStoreIndex, Document, SimpleDirectoryReader
from llama_index.node_parser import SimpleNodeParser
import os

os.environ['OPENAI_API_KEY'] = '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'


text1 = "TechSolutions Inc. is a burgeoning startup in the SaaS industry, specializing in cloud-based project management software. Founded by a team of experienced tech entrepreneurs, the company has successfully entered North American and European markets, securing $2 million in seed funding and currently in the process of raising Series A funding to further accelerate their growth. Their main objectives include enhancing user onboarding, driving feature adoption, and improving customer retention to reduce churn rates. Additionally, they aim to maintain product scalability and actively gather user feedback for continuous product development. As a Customer Success Manager for TechSolutions Inc., my role revolves around collaborating closely with the client to address these challenges, devise tailored success strategies, and consistently monitor their progress and satisfaction to ensure a prosperous, long-term partnership."
text2 = "HealthTech Innovations, a three-year-old startup in the health tech industry, is dedicated to pioneering innovative digital health solutions, with a focus on remote patient monitoring and telehealth services. Founded by a team of healthcare professionals, software engineers, and data scientists, the company has established itself in the U.S. healthcare market and is actively seeking further funding to expand internationally. Their key challenges encompass navigating healthcare regulatory compliance, expanding into new markets, fortifying data security, enhancing patient engagement, and ensuring product scalability. As a Customer Success Manager for HealthTech Innovations, my role revolves around collaboratively addressing these challenges, developing tailored success strategies, and continuously monitoring progress and client satisfaction to foster a prosperous and long-lasting partnership."

text_list = [text1, text2]
documents = [Document(text=t) for t in text_list]
parser = SimpleNodeParser.from_defaults()
nodes = parser.get_nodes_from_documents(documents)
index = VectorStoreIndex.from_documents(documents)

query_engine = index.as_query_engine()
response = query_engine.query("Based off of the given information, create a success plan for TechSolutions")
print(response)