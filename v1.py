from llama_index import VectorStoreIndex, Document, SimpleDirectoryReader
from llama_index.node_parser import SimpleNodeParser
import os

os.environ['OPENAI_API_KEY'] = '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'


text1 = "TechSolutions Inc. is a burgeoning startup in the SaaS industry, specializing in cloud-based project management software. Founded by a team of experienced tech entrepreneurs, the company has successfully entered North American and European markets, securing $2 million in seed funding and currently in the process of raising Series A funding to further accelerate their growth. Their main objectives include enhancing user onboarding, driving feature adoption, and improving customer retention to reduce churn rates. Additionally, they aim to maintain product scalability and actively gather user feedback for continuous product development. As a Customer Success Manager for TechSolutions Inc., my role revolves around collaborating closely with the client to address these challenges, devise tailored success strategies, and consistently monitor their progress and satisfaction to ensure a prosperous, long-term partnership."
text2 = "User Onboarding Optimization: Review the current onboarding process to identify potential bottlenecks or areas for improvement. Collaborate with the product team to implement any necessary changes to streamline onboarding.Develop and update onboarding materials, such as guides and tutorials, for new users.Feature Adoption Promotion:Identify which features are underutilized by customers through data analysis.Reach out to customers who aren't using key features to provide personalized training or guidance.Develop a feature adoption campaign to educate users about the benefits of using specific features.Customer Retention Analysis:Analyze customer churn rates and identify the reasons for customer attrition.Work with the marketing team to develop targeted retention campaigns or offers.Contact at-risk customers to understand their concerns and offer solutions.Product Scalability Monitoring:Coordinate with the tech team to ensure the software's scalability and performance as TechSolutions grows. Establish regular performance monitoring and reporting mechanisms. Develop a contingency plan for addressing potential scalability issues.Gathering User Feedback:Schedule and conduct interviews or surveys with a sample of active users.Analyze feedback data to identify trends and actionable insights.Share feedback findings with the product team for continuous improvement.Customer Check-ins:Schedule regular check-in calls with key accounts to assess their satisfaction and needs.Address any concerns or issues raised by customers and document them for follow-up.Share positive feedback and testimonials with the marketing team for promotion."

text_list = [text1, text2]
documents = [Document(text=t) for t in text_list]
parser = SimpleNodeParser.from_defaults()
nodes = parser.get_nodes_from_documents(documents)
#index = VectorStoreIndex.from_documents(documents)
index = VectorStoreIndex(nodes)

query_engine = index.as_query_engine()
response = query_engine.query("I want you to be a Customer Success manageer. Based off of the given information about the client TechSolutions, and the tasks that you have, prioritize the tasks in an ordered list. Make sure that the most important tasks are at the top of the list.")
print(response)