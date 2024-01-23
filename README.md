# PetScam-baiting
An Automated Response System for Disrupting Online Pet Scamming

## Project overview
The online pet scam is an increasingly sophisticated threat that can cause emotional and financial distress to victims. To aid the public in identifying and avoiding such pet scams, this project aims to develop an automated response system that wastes scammers' time and resources. Using web scraping, fake profiles, data analysis and visualization technologies, this system will leave contact information on various pet scam websites' contact pages, and engage scammers in prolonged conversations based on different scam-baiting templates. According to the statistical analysis of quantity, conversation, and time metrics as three types of quantitative metrics, we can reveal and optimize the most effective scam-baiting strategies. Ultimately, by reducing scammers' return on investment, the system can mitigate these harmful frauds and protect potential victims.

## Pet scam websites
On https://petscams.com/, which have listed known pet scam and delivery scam websites, is still in real-time updates.

## Basic process of project
Project will involve creating a new process that acts as a sort of 'crawler', visiting pet scam sites and arranging for them to contact personalities created by the bot. It will probably has to make changes to other parts of the system to make this work smoothly, and for the experiments it'll want to disable the previous crawlers. To accomplish all this will need to get very familiar with the codebase, so getting a version of it running early on will be important.

## How to accomplish
Use the new crawlers based on the open-source Expandable Scam-baiting Mail Server(https://github.com/an19352/scambaiter_back):
  - leaving contact information on various pet scam websites' contact pages;
  - fetching initial scam emails from pet scammers;
  - arranging for them to contact different personalities(different scam-baiting templates) created by the bot;
  - configure own directories and API keys.
