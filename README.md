# PetScam-baiting
An Automated Response System for Disrupting Online Pet Scamming

## Project overview
The online pet scam is an increasingly sophisticated threat that can cause emotional and financial distress to victims. To aid the public in identifying and avoiding such pet scams, this project aims to develop an automated response system that wastes scammers' time and resources. Using web scraping, fake profiles, data analysis and visualization technologies, this system will leave contact information on various pet scam websites' contact pages, and engage scammers in prolonged conversations based on different scam-baiting templates. According to the statistical analysis of quantity, conversation, and time metrics as three types of quantitative metrics, we can reveal and optimize the most effective scam-baiting strategies. Ultimately, by reducing scammers' return on investment, the system can mitigate these harmful frauds and protect potential victims.

## Pet scam websites
On https://petscams.com/, which have listed known pet scam and delivery scam websites, is still in real-time updates.

## Basic process of project
Project will involve creating a new process that acts as a sort of 'crawler', visiting pet scam sites and arranging for them to contact personalities created by the bot. It will probably has to make changes to other parts of the system to make this work smoothly, and for the experiments it'll want to disable the previous crawlers. To accomplish all this will need to get very familiar with the codebase, so getting a version of it running early on will be important.

## How to accomplish
1. Add a new crawler based on the open-source Expandable Scam-baiting Mail Server(https://github.com/an19352/scambaiter_back):
  - leaving contact information on various pet scam websites' contact pages which are already listed on the https://petscams.com/.
2. Make some changes to other parts of the system in order to work the following three steps smoothly:
  - fetching initial scam emails from pet scammers;
  - arranging for them to contact different personalities(different scam-baiting templates) created by the bot;
  - configure own directories and API keys.
3. Write a basic version first, which can be successfully run and tested the email conversations between you and the robot system.

## Essential resources
1. Sign up for Github Student Developer Pack on https://education.github.com/pack, in order to get useful APIs like testmail.app and mailgun for free:
  - testmail.app: Get unlimited email addresses and mailboxes for automating email tests with the APIs
  - mailgun by PATHWIRE: APIs that enable you to send, receive and track 20,000 free emails and get 100 free email validations every month for up to 12 months.
2. Apply one or more domains for the responder emails. For example, emails sent to "user@gmail.com" would be directed to the mail server responsible for the "gmail.com" domain.
