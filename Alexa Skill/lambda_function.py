# -*- coding: utf-8 -*-

# This sample demonstrates handling intents from an Alexa skill using the Alexa Skills Kit SDK for Python.
# Please visit https://alexa.design/cookbook for additional examples on implementing slots, dialog management,
# session persistence, api calls, and more.
# This sample is built using the handler classes approach in skill builder.
import logging
import ask_sdk_core.utils as ask_utils

import requests
import json

from ask_sdk_core.skill_builder import SkillBuilder
from ask_sdk_core.dispatch_components import AbstractRequestHandler
from ask_sdk_core.dispatch_components import AbstractExceptionHandler
from ask_sdk_core.handler_input import HandlerInput

from ask_sdk_model import Response

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

fromPhoneNumber = "YOUR_TWILIO_PHONE_NUMBER"
lambdaFuncUrl = "YOUR_AWS_LAMBDA_SEND_SMS_FUNCTION"

class LaunchRequestHandler(AbstractRequestHandler):
    """Handler for Skill Launch."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool

        return ask_utils.is_request_type("LaunchRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speak_output = "Welcome, you can ask for national or state covid 19 data."

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )


class NationalCasesIntentHandler(AbstractRequestHandler):
    """Handler for National Cases Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("NationalCasesIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        url = "https://api.covid19india.org/data.json";
        response = requests.get(url)
        if response.status_code == 200:
            parsed_json = json.loads(response.text)
            speak_output = "{} new cases have been reported so far. There are {} confirmed cases in India, out of which {} are active. There have been {} recoveries and {} deaths.".format(
                parsed_json["statewise"][0]["deltaconfirmed"], parsed_json["statewise"][0]["confirmed"], parsed_json["statewise"][0]["active"], parsed_json["statewise"][0]["recovered"], parsed_json["statewise"][0]["deaths"])
        else:
            speak_output = "Sorry, covid 19 India API is down"

        return (
            handler_input.response_builder
                .speak(speak_output)
                # .ask("add a reprompt if you want to keep the session open for the user to respond")
                .response
        )


class StateCasesIntentHandler(AbstractRequestHandler):
    """Handler for State Cases Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("StateCasesIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        slots = handler_input.request_envelope.request.intent.slots
        url = "https://api.covid19india.org/data.json"
        response = requests.get(url)
        if response.status_code == 200:
            parsed_json = json.loads(response.text)
            if slots["state"].value.lower() == "india":
                toCheck = "total"
            else:
                toCheck = slots["state"].value.lower()
            index = -1
            for i in range(len(parsed_json["statewise"])):
                if parsed_json["statewise"][i]["state"].lower() == toCheck:
                    index = i
                    break
            if index == -1:
                speak_output = "Sorry, please try another state"
            elif parsed_json["statewise"][index]["confirmed"] == "0":
                speak_output = "There are no cases in {}".format(parsed_json["statewise"][index]["state"])
            else:
                speak_output = "{} new cases have been reported so far. There are {} confirmed cases in {}, out of which {} are active. There have been {} recoveries and {} deaths.".format(
                    parsed_json["statewise"][index]["deltaconfirmed"], parsed_json["statewise"][index]["confirmed"], parsed_json["statewise"][index]["state"], parsed_json["statewise"][index]["active"], parsed_json["statewise"][index]["recovered"], parsed_json["statewise"][index]["deaths"])
        else:
            speak_output = "Sorry, covid 19 India API is down"

        return (
            handler_input.response_builder
                .speak(speak_output)
                # .ask("add a reprompt if you want to keep the session open for the user to respond")
                .response
        )

class SMSIntentHandler(AbstractRequestHandler):
    """Handler for SMS Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("SMSIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        if str(handler_input.request_envelope.request.intent.confirmation_status) == "IntentConfirmationStatus.DENIED":
            speak_output = "All right. Not sending the SMS"
            return (
                handler_input.response_builder
                    .speak(speak_output)
                    # .ask("add a reprompt if you want to keep the session open for the user to respond")
                    .response
            )
        accessToken = handler_input.request_envelope.context.system.api_access_token
        headers = {'Authorization': 'Bearer {}'.format(str(accessToken))}
        phoneUrl = "https://api.eu.amazonalexa.com/v2/accounts/~current/settings/Profile.mobileNumber"
            
        try:
            phoneResponse = requests.get(phoneUrl, headers=headers)
            
            if phoneResponse.status_code == 200:
                parsed_json = json.loads(phoneResponse.text)
                phoneNumber = '+' + parsed_json["countryCode"] + parsed_json["phoneNumber"]
                speak_output = self.sendSMS(phoneNumber)
            elif phoneResponse.status_code == 204:
                speak_output = "Sorry, no phone number was found! Please add your phone number in the alexa app"
            elif phoneResponse.status_code == 403:
                speak_output = "Please provide the required permissions in your alexa app"
            elif phoneResponse.status_code == 401:
                speak_output = "Sorry, a problem occurred while fetching your phone number"
            else:
                speak_output = "Sorry, an error occurred. Error code is " + str(phoneResponse.status_code)
        except Exception as e:
            speak_output = e
        
        return (
            handler_input.response_builder
                .speak(speak_output)
                # .ask("add a reprompt if you want to keep the session open for the user to respond")
                .response
        )
    def sendSMS(self, toPhoneNumber):
        body = "Hi there, thanks for using the Covid 19 India skill.%0a"
        body += "Here are some resources you might find useful:%0a"
        body += "https://www.mygov.in/covid-19/ -> Official Government of India Covid-19 dashboard.%0a"
        body += "https://bit.ly/2S8iAbj -> WHO QnA on coronaviruses%0a"
        body += "https://bit.ly/354AmBk -> WHO Myth Buster%0a"
        body += "https://bit.ly/2xPVVtp -> WHO Public Advice%0a"
        body += "https://www.covid19india.org/ -> A beatiful open-source website with detailed information and graphs about the spread of the pandemic in India.%0a"
        body += "This skill gets all Covid-19 data from https://api.covid19india.org/ API%0a"
        body += "Stay Home! Stay Safe!"
        url = lambdaFuncUrl + "?To={}&From={}&Body={}".format(toPhoneNumber, fromPhoneNumber, body)
        response = requests.get(url)
        if response.status_code == 200:
            return response.text
        else:
            return "Sorry, an error occured. Error is " + response.text

class AddInfoIntentHandler(AbstractRequestHandler):
    """Handler for AddInfo Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("AddInfoIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        slots = handler_input.request_envelope.request.intent.slots
        
        url = "https://api.covid19india.org/state_district_wise.json"
        NatUrl = "https://api.covid19india.org/data.json"
        
        try:
            if slots["state"].value.lower() =="india":
                response = requests.get(NatUrl)
                if response.status_code == 200:
                    parsed_json = json.loads(response.text)
                    data = parsed_json["statewise"]
                    activeData = sorted(data, key=lambda x: int(x['active']), reverse=True)
                    confirmedData = sorted(data, key=lambda x: int(x['confirmed']), reverse=True)
                    if activeData[1]["active"] != 0:
                        speak_output = activeData[1]["state"] + " has the highest number of active cases at " + str(activeData[1]["active"]) + " in " + slots["state"].value
                        if activeData[2]["active"] != 0:
                            speak_output += " followed by " + activeData[2]["state"] + " which has " + str(activeData[2]["active"]) + " active cases"
                        if activeData[1]["state"] != confirmedData[1]["state"]:
                            speak_output += ". " + confirmedData[1]["state"] + " has the highest number of confirmed cases at " + str(confirmedData[1]["active"])
                    else:
                        speak_output = "There are no active cases in " + slots["state"].value
                else:
                    speak_output = "Sorry, covid 19 India API is down"
                    
            else:
                response = requests.get(url)
                if response.status_code == 200:
                    parsed_json = json.loads(response.text)
                    key = 0
                    for k in parsed_json:
                        if k.lower() == slots["state"].value.lower():
                            key = k
                            break
                    if key == 0:
                        speak_output = "Sorry, please try another state"
                    else:
                        data = parsed_json[key]["districtData"]
                        confirmedData = sorted(data, key=lambda x: data[x]['confirmed'], reverse=True)
                        activeData = sorted(data, key=lambda x: data[x]['active'], reverse=True)
                        new = 0
                        if data[activeData[0]]["active"] != 0:
                            '''response = requests.get(NatUrl)
                            if response.status_code == 200:
                                parsed_json = json.loads(response.text)
                                if slots["state"].value.lower() == "india":
                                    toCheck = "total"
                                else:
                                    toCheck = slots["state"].value.lower()
                                index = -1
                                for i in range(len(parsed_json["statewise"])):
                                    if parsed_json["statewise"][i]["state"].lower() == toCheck:
                                        index = i
                                        break
                                if index != -1:
                                    new = parsed_json["statewise"][index]["deltaconfirmed"]
                            else:
                                speak_output = "Sorry, covid 19 India API is down"'''
                                
                            #speak_output =  str(new) + " new cases have been reported so far"
                            speak_output = activeData[0] + " district has the highest number of active cases at " + str(data[activeData[0]]["active"]) + " in " + slots["state"].value
                            if data[activeData[1]]["active"] != 0:
                                speak_output += " followed by " + activeData[1] + " district which has " + str(data[activeData[1]]["active"]) + " active cases"
                            if activeData[0] != confirmedData[0]:
                                speak_output += ". " + confirmedData[0] + " district has the highest number of confirmed cases at " + str(data[confirmedData[0]]["confirmed"])
                        else:
                            speak_output = "There are no active cases in " + slots["state"].value
                else:
                    speak_output = "Sorry, covid 19 India API is down"
        except Exception as e:
            speak_output = str(e)

        return (
            handler_input.response_builder
                .speak(speak_output)
                # .ask("add a reprompt if you want to keep the session open for the user to respond")
                .response
        )

class HelpIntentHandler(AbstractRequestHandler):
    """Handler for Help Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("AMAZON.HelpIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speak_output = "You can ask for state or national data! How can I help?"

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )


class CancelOrStopIntentHandler(AbstractRequestHandler):
    """Single handler for Cancel and Stop Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return (ask_utils.is_intent_name("AMAZON.CancelIntent")(handler_input) or
                ask_utils.is_intent_name("AMAZON.StopIntent")(handler_input))

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speak_output = "Goodbye!"

        return (
            handler_input.response_builder
                .speak(speak_output)
                .response
        )


class SessionEndedRequestHandler(AbstractRequestHandler):
    """Handler for Session End."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_request_type("SessionEndedRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response

        # Any cleanup logic goes here.

        return handler_input.response_builder.response


class IntentReflectorHandler(AbstractRequestHandler):
    """The intent reflector is used for interaction model testing and debugging.
    It will simply repeat the intent the user said. You can create custom handlers
    for your intents by defining them above, then also adding them to the request
    handler chain below.
    """
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_request_type("IntentRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        intent_name = ask_utils.get_intent_name(handler_input)
        speak_output = "You just triggered " + intent_name + "."

        return (
            handler_input.response_builder
                .speak(speak_output)
                # .ask("add a reprompt if you want to keep the session open for the user to respond")
                .response
        )


class CatchAllExceptionHandler(AbstractExceptionHandler):
    """Generic error handling to capture any syntax or routing errors. If you receive an error
    stating the request handler chain is not found, you have not implemented a handler for
    the intent being invoked or included it in the skill builder below.
    """
    def can_handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> bool
        return True

    def handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> Response
        logger.error(exception, exc_info=True)

        speak_output = "Sorry, I had trouble doing what you asked. Please try again."

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )

# The SkillBuilder object acts as the entry point for your skill, routing all request and response
# payloads to the handlers above. Make sure any new handlers or interceptors you've
# defined are included below. The order matters - they're processed top to bottom.


sb = SkillBuilder()

sb.add_request_handler(LaunchRequestHandler())
sb.add_request_handler(NationalCasesIntentHandler())
sb.add_request_handler(AddInfoIntentHandler())
sb.add_request_handler(StateCasesIntentHandler())
sb.add_request_handler(SMSIntentHandler())
sb.add_request_handler(HelpIntentHandler())
sb.add_request_handler(CancelOrStopIntentHandler())
sb.add_request_handler(SessionEndedRequestHandler())
sb.add_request_handler(IntentReflectorHandler()) # make sure IntentReflectorHandler is last so it doesn't override your custom intent handlers

sb.add_exception_handler(CatchAllExceptionHandler())

lambda_handler = sb.lambda_handler()