import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import AIMessage
from utils import parse_bullet_points, TreeNode, print_tree

#import the OpenAI API key from the .env file
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
# LLMs
llm = ChatOpenAI(model="gpt-4o-mini", api_key=OPENAI_API_KEY)

scamper_gen_ideas_prompt = ChatPromptTemplate.from_template("""You are a clever work assistant that helps people generate ideas for their project, reasearch, paper or any other creative work. You'll be having a query from the user and you need to generate 5 (five) diverse, detailed, developed, precise and significant ideas related to the context of the query. The ideas should not be redundant and repetitive, be creative and unique. The ideas must be formatted in the form of bullet points without titles and without bold text.
Query:{query}
List of 5 bullet points ideas:""")

scamper_ideas_prompt = ChatPromptTemplate.from_template("""
You are a clever idea generator assistant that helps people brainstorm and generate new ideas using the SCAMPER method. SCAMPER is an activity-based thinking process that assists in developing an idea through a structured approach. Here’s how each step in SCAMPER works:

- Substitute (analogy): Come up with another topic or element that could replace or be equivalent to the present topic.
- Combine (convergence): Add relevant information or ideas to enhance the original topic.
- Adjust: Identify ways to construct or adapt the topic to make it more flexible or better suited to various situations.
- Modify, magnify, minify: Change aspects of the topic creatively or adjust a feature to make it bigger or smaller.
- Put to other uses (generate/divergence/connect): Think of scenarios or situations where this topic could be applied.
- Eliminate: Remove elements of the topic that don’t add value or might be unnecessary.
- Reverse, rearrange: Evolve a new concept from the original by changing its structure or reversing key elements.

For each SCAMPER step, generate one creative and distinct idea based on the topic provided. Link ideas to relevant creativity methods and present the resulting list in bullet points without titles and bold text.

Topic to brainstorm: {idea}
List of 7 SCAMPER ideas bullet points:
""")

scamper_gen_ideas_chain = scamper_gen_ideas_prompt | llm | parse_bullet_points
scamper_ideas_chain = scamper_ideas_prompt | llm | parse_bullet_points

user_query = "I am searching for ideas to automate hard tasks in any company using AI agents powered by LLMs"
root_sc = TreeNode(user_query)

initial_ideas = scamper_gen_ideas_chain.invoke({"query": user_query})

for idea in initial_ideas:
    child_node = TreeNode(idea)
    root_sc.add_child(child_node)

    scamper_ideas = scamper_ideas_chain.invoke({"idea": idea})

    for scamper_idea in scamper_ideas:
        grandchild_node = TreeNode(scamper_idea)
        child_node.add_child(grandchild_node)

print_tree(root_sc)

