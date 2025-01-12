# PetScam-baiting(Individual Graduation Project)
An Automated Response System for Disrupting Online Pet Scamming

Note: The code for this project is developed based on the open-source project [scambaiter_back](https://github.com/an19352/scambaiter_back) 

## Project overview
The online pet scam is an increasingly sophisticated threat that can cause emotional and financial distress to victims. To aid the public in identifying and avoiding such pet scams, this project aims to develop an automated response system that wastes scammers' time and resources. Using web scraping, fake profiles, data analysis and visualization technologies, this system will leave contact information on various pet scam websites' contact pages, and engage scammers in prolonged conversations based on different scam-baiting templates. According to the statistical analysis of quantity, conversation, and time metrics as three types of quantitative metrics, we can reveal and optimize the most effective scam-baiting strategies. Ultimately, by reducing scammers' return on investment, the system can mitigate these harmful frauds and protect potential victims.

## Pet scam websites
On https://petscams.com/, which have listed known pet scam and delivery scam websites, is still in real-time updates.

## Four different response strategies (generated by gpt-3.5 and gpt-4 prompt)
1. Newbie 
2. Bargainer
3. Investigator
4. Impatient Consumer

## Project execution process
This experiment was start on 15th March 3.30pm, last for 31 days, which was ended on 15th April. In the experiment, the following procedure were repeated four times, taking the first time as an example:
1. To get petscam websites: run ./crawler/petscams/petscam_crawl.py, then all the scam websites which are listed in recent 30 days will be saved in scam-webs/pet-scams1.json.
2. To get contact form urls: run ./crawler/petscams/contactpage-crawler.py, then most of the vaild contact form urls will be saved success/in form1.json.
3. To automatedly fill in the contact form: run ./crawler/petscams/formfill_crawler.py. then the contact forms information will be saved in crawler/cache.json
4. Waiting for the scam emails from pet scammers...
5. Fetching the received scam emails: run ./crawler/petscams/email_crawler.py, then the email information will be saved in emails/record.json.
6. Automatedly sending bait emails: run ./corn.py, and then the sol_counts will be updated in models/history.json

## Data analysis
1. The runtime of each crawler can be checked in rate_calculate/rate_result.json.

## Essential resources
1. Github Student Developer Pack on https://education.github.com/pack, in order to use tools like name.com and mailgun for free:
  - mailgun by PATHWIRE: APIs that enable you to send, receive and track 20,000 free emails and get 100 free email validations every month for up to 12 months.
  - name.com: Apply a domain name.
2. Three months API access of gpt-3.5-turbo-0125 model, provided by UoB. 

