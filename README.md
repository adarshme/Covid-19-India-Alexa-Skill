# Covid 19 India Alexa Skill
An Alexa Skill for information about Covid-19 in India.

<p align="center">
  <img width="512" height="512" src="https://raw.githubusercontent.com/InfernoCoder11/Covid-19-India-Alexa-Skill/master/Alexa%20Skill/images/en-IN_largeIconUri.png">
</p>

## About this Skill
This skill is to help you know the number of new cases, active cases, 
and recoveries due to Covid-19 in any state/UT of the country. You may 
ask for a brief overview or detailed information. Choose to give phone 
number permissions to receive an SMS containing links to resources on 
Covid-19.

To get started, you can say - "Alexa, run Covid India",
 then try asking - "How many cases are there?" or "What's the current 
status in Maharashtra?" or "What's the current number of cases in Uttar 
Pradesh?". To get more details, you can ask "Give me additional 
information for India" or "Tell me more details about Rajasthan". You 
may also choose to receive an SMS containing links to resources on 
Covid-19 by giving the required permissions to the skill in your Alexa 
app settings and saying "Send me an SMS" or "Send me information about 
coronavirus".

This skill gets all its data from https://api.covid19india.org/ API.

Stay Home! Stay Safe!

## Setup Instructions
The setup instructions are divided into three parts. In the first part we'll deal with setting up our Alexa Skill's interaction model. In the second part we'll set up our AWS Lambda function to send SMS. In the third part we'll set up our skill's Python code and deploy it.
### Interaction Model
1. Head over to https://developer.amazon.com/alexa and login/create an account. If you are creating an account then fill in your details and ensure you answer "NO" for "Do you plan to monetize apps by charging for apps or selling in-app items" and "Do you plan to monetize apps by displaying ads from the Amazon Mobile Ad Network or Mobile Associates?" to avoid entering billing and other information.

2. From the Alexa Skills Kit Developer Console, click "Create Skill".

3. Give a name to the skill. (It doesn't have to be the name you plan to invoke your skill with). **Important: Select the English language version to which your Alexa device is set otherwise the skill will not work.**

4. In "Choose a model to add to your skill", select "Custom". In the "Choose a method to host your skill's backend resources", choose Alexa-Hosted (Python). Then click "Create Skill".

5. Wait for a few seconds while AWS allocates resources for the skill. Then click the "JSON Editor" on the left side of the page. Replace all the contents of the editor with [this file's](https://github.com/InfernoCoder11/Covid-19-India-Alexa-Skill/blob/master/Alexa%20Skill/interactionModel.json) contents. Click on "Save Model".

6. On the left side of the page, scroll down and click on "Permissions". Enable "Customer Phone Number" permission. Then click on "Custom" on the left side of the page.

7. Click on any Intent or the "JSON Editor" then click on "Save Model" and then "Build Model".

### AWS Lambda Function
1. Go to http://aws.amazon.com/. You will need to set-up an AWS account if you don't have one already (the basic one will do fine). 

2. After setting up/logging in to your account search for "lambda" in the search bar. Click on "Create function".

3. Choose "Author from scratch" and give your function a name. In "Runtime" choose the latest version of Python. In "Execution Role" choose "Create a new role from AWS policy templates", give it a name "Basic" and click on "Create Function".

4. Replace all the contents of the inline editor with [this file's](https://github.com/InfernoCoder11/Covid-19-India-Alexa-Skill/blob/master/AWS%20Lambda%20Function/lambda_function.py) contents. Click on "Save".

5. Scroll down and add two environment variables. The first one should be `TWILIO_ACCOUNT_SID` and its value should be set to your Twilio account's SID. The second one should be `TWILIO_AUTH_TOKEN` and its value should be set to your Twilio account's Auth Token. You can find these values in your Twilio dashboard.

6. Scroll up and click on "+ Add Trigger". Select the "API Gateway" Trigger, set API to "Create An API","API Type" to "HTTP API", "Security" to "Open". Click on "Add".

7. Click on "API Gateway" and find your API Endpoint URL. It will be required later.

### Python Code
1. Click on the "Code" button at the top of the Alexa Developer Console page. Replace all the contents of the editor with [this file's](https://github.com/InfernoCoder11/Covid-19-India-Alexa-Skill/blob/master/Alexa%20Skill/lambda_function.py) contents.

2. Somewhere close to the top of the code set the `fromPhoneNumber` variable to the Twilio phone number you own. Set the `lambdaFuncUrl` variable to the URL of the AWS Lambda Endpoint you created.

3. Click on "Save" and then "Build".

Congratulations! If all went well you have successfully built this skill yourself. You can test it on your Alexa device (connected to the same account) or in the Alexa Developer Console. To test the SMS sending feature don't forget to add your phone number and give permission to the skill in your Alexa app or at https://alexa.amazon.com/spa/index.html#cards.

## Supported commands
- What is the current status
- What is the current status in {state}
- How many cases are there
- How many cases are there in {state}
- What is the current number of cases
- What is the current number of cases in {state}
- Send me an SMS
- Send me information about covid nineteen
- Send me information about coronavirus
- Send additional links to me
- Send additional resources to me
- Give me additional data for {state}
- Tell me more details about {state}
- Extra details for {state}
- Give me additional information of {state}
