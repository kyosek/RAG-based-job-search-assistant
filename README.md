# RAG-based Job Search Assistant

This project aims to help your job search with GenAI!

Have you done a job search and ended up with too many jobs look like a good next step and didn't know where to start? This project seeks to assist and be an AI guidance for your job search.

## Use case examples

Here are a few use case ideas how you can leverage this job search assistant but not limited to... Use your creativity to take advantage of this assistant.

- Pick up $n$ jobs that are most relevant to you
- Tailor your CV to the job you want to apply
- Help you to write a statement of purpose

## Architecture Overview

Here is the most simplistic RAG-based Job Search Assistant architecture overview.
You will need to build a vector store with job posts and then you upload your CV then can query a question regarding your job search.
![Overview RAG-based job search assistant architecture](doc/overview.png)

## How to use

There are 3 components in this project so far - It will source the job post data, build a vector storage and start querying questions regarding your job search. The usage of each components can be found below:

### Scrape the job posts

This can be done by running `src/job_scraper.py`. This script will use `linkedin_jobs_scraper` package to scrape the job posts in LinkedIn. You can configure the scraper to suit your job title, location, full/part time, etc in the file. The example is using job title: Data scientist and location: United Kingdom.

### Build a vector storage

This can be done by running `src/store_data.py`. This process takes the csv file that contains job posts and create a vector store in `storage` directory.

### Start querying

This can be done by running `src/main.py`. You can upload your CV in `input_cv` directory and can be consumed in RAG.

Note: The LLM this demo is using is Open AI GPT-3.5 turbo, so it will require to set `OPENAI_API_KEY` environmental variable

## Limitations

- You will get a helpful response only when there are several job posts that are relevant to you, in other words, the quality of the response depends on the data you have in the vector store
- This demo does not have a fancy UI, so you will need to run the script `main.py`
- As mentioned above, the LLMs that employed in this demos are Open AI GPT-3.5 turbo, so it is not fine-tuned
- The architecture of RAG in this demo is very simplistic (Naive RAG + LLM evaluation), so there are so much space to improve the quality of the response
