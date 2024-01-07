# Problem Statement 
Given the dataset submitted by individuals on their ideas of how companies can implement the circular economy in their businesses, the team developed an algorithmic tool to validate these ideas against certain keyword metrics. 

# Our Solution
Sustainable Scan evaluates each solution to a sustainability problem based on the following rationale metrics: maturity stage, market potential, feasibility, scalability, technological innovation or adherence to circular economy principles.
This code uses a branch of AI (NLP) to analyze the solutions with the NLTK tool and Word2Vec Algorithm.

Sustainable Scan ranks these solutions through three main steps:
1) Processing - orginizes data by the given index, problem, and solution
2) Filtering - removes solutions that are considered "bad" or spam.
3) Scoring - Ranks the correlation of each word to the keywords [Sustainable, Feasible, Innovative, Novelty]
   The higher the accumulative score, the higher the correlation and more strong the solution is.

# Findings/Insight
- Determines which index (solution) is the strongest based on its 4 categories (Sustainability, Feasiblilty, Innovation, Novelty).
- Showcases the distribution of the solution scores based on its categories with a graphical representation
