
import ask_sdk_core.utils as ask_utils

from ask_sdk_core.skill_builder import SkillBuilder
from ask_sdk_core.dispatch_components import AbstractRequestHandler
from ask_sdk_core.dispatch_components import AbstractExceptionHandler
from ask_sdk_core.handler_input import HandlerInput

from ask_sdk_model import IntentConfirmationStatus
from ask_sdk_model import Response

import requests
import json


findOneUrl = "https://data.mongodb-api.com/app/data-ojsvg/endpoint/data/v1/action/findOne"
findUrl = "https://data.mongodb-api.com/app/data-ojsvg/endpoint/data/v1/action/find"
deleteUrl = "https://data.mongodb-api.com/app/data-ojsvg/endpoint/data/v1/action/deleteMany"
updateUrl = "https://data.mongodb-api.com/app/data-ojsvg/endpoint/data/v1/action/updateOne"

api=""
headers = {
  'Content-Type': 'application/json',
  'Access-Control-Request-Headers': '*',
  'api-key': api, 
}


class LaunchRequestHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return ask_utils.is_request_type("LaunchRequest")(handler_input)

    def handle(self, handler_input):
        return handler_input.response_builder.speak("Welcome, what do you want to know about your plants?").response



class getSensorDataIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return ask_utils.is_intent_name("getSensorDataIntent")(handler_input)

    def handle(self, handler_input):

        findData = json.dumps({
            "collection": "plant1",
            "database": "plants",
            "dataSource": "Cluster0",
            "projection": {
                "_id": 0,
                "Light": 1,
                "Temperature": 1,
                "Humidity": 1,
                "SoilMoisture": 1,
                "Timestamp": 1
            },
            "sort": { "Timestamp": -1 },
            "limit": 1
        })

        dataResponse = json.loads(requests.request("POST", findUrl, headers=headers, data=findData).text)

        try:
            speak_output = "On your plant, the latest sensor values measured are: Light: " + str(dataResponse["documents"][0]["Light"]) + ", Temperature: " + str(dataResponse["documents"][0]["Temperature"]) + ", Humidity: " + str(dataResponse["documents"][0]["Humidity"])  + ", SoilMoisture: " + str(dataResponse["documents"][0]["SoilMoisture"]) 
        except:
            speak_output = "The database is probably empty."

        return handler_input.response_builder.speak(speak_output).response


class getOneSensorValueIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return ask_utils.is_intent_name("getOneSensorValueIntent")(handler_input)

    def handle(self, handler_input):
        
        findData = json.dumps({
            "collection": "plant1",
            "database": "plants",
            "dataSource": "Cluster0",
            "projection": {
                "_id": 0,
                "Light": 1,
                "Temperature": 1,
                "Humidity": 1,
                "SoilMoisture": 1,
                "Timestamp": 1
            },
            "sort": { "Timestamp": -1 },
            "limit": 1
        })
        
        dataResponse = json.loads(requests.request("POST", findUrl, headers=headers, data=findData).text)
        
        slot_value = handler_input.request_envelope.request.intent.slots['sensor'].resolutions.resolutions_per_authority[0].values[0].value.name

        try:
            speak_output = "On your plant, the latest "+slot_value+" value measured is: " + str(dataResponse["documents"][0][slot_value])
        except:
            speak_output = "The database is probably empty. ("+slot_value+")"

        return handler_input.response_builder.speak(speak_output).response


class deleteValuesIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return ask_utils.is_intent_name("deleteValuesIntent")(handler_input)

    def handle(self, handler_input):
        
        confirmation_status = handler_input.request_envelope.request.intent.confirmation_status

        if confirmation_status == IntentConfirmationStatus.DENIED:
            speak_output = 'Okay, I won\'t do that.'
        elif confirmation_status == IntentConfirmationStatus.CONFIRMED:
            speak_output = 'Great, your data will be erased.'
            
        dataDelete = json.dumps({
            "collection": "plant1",
            "database": "plants",
            "dataSource": "Cluster0",
            "filter": { "delete": 1 },
              }
        )
        
        requests.request("POST", deleteUrl, headers=headers, data=dataDelete)
            
        return handler_input.response_builder.speak(speak_output).response



class changeIntervalIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return ask_utils.is_intent_name("changeIntervalIntent")(handler_input)

    def handle(self, handler_input):

        try:
            slot_value = int(handler_input.request_envelope.request.intent.slots['number'].value)
            if slot_value<=0:
                raise Exception("negative") 
        except:
            return handler_input.response_builder.speak("You must choose a non-negative whole number, please try again.").response
        
        data = json.dumps({
            "collection": "device1",
            "database": "devices",
            "dataSource": "Cluster0",
            "filter": { "_id": 1 },
              "update": {
                  "$set": {
                      "interval": int(slot_value),
                      }
                  }
              }
        )

        try:
            response = requests.request("POST", updateUrl, headers=headers, data=data)
            speak_output = "Your scanning interval will be changed to "+str(slot_value)+" times a day, after the next scan."
        except:
            speak_output = "Something went wrong while changing the interval."
        
        return handler_input.response_builder.speak(speak_output).response


class HelpIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return ask_utils.is_intent_name("AMAZON.HelpIntent")(handler_input)

    def handle(self, handler_input):
        speak_output = "You can ask me about your plants data values or set the measuring interval for the sensors! How can I help?"

        return handler_input.response_builder.speak(speak_output).response


class CancelOrStopIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return (ask_utils.is_intent_name("AMAZON.CancelIntent")(handler_input) or
                ask_utils.is_intent_name("AMAZON.StopIntent")(handler_input))

    def handle(self, handler_input):
        speak_output = "Goodbye!"

        return handler_input.response_builder.speak(speak_output).response


class FallbackIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return ask_utils.is_intent_name("AMAZON.FallbackIntent")(handler_input)

    def handle(self, handler_input):
        speech = "Hmm, I'm not sure."
        reprompt = "I didn't catch that. What can I help you with?"

        return handler_input.response_builder.speak(speech).ask(reprompt).response

class SessionEndedRequestHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return ask_utils.is_request_type("SessionEndedRequest")(handler_input)

    def handle(self, handler_input):

        return handler_input.response_builder.response

class IntentReflectorHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return ask_utils.is_request_type("IntentRequest")(handler_input)

    def handle(self, handler_input):
        intent_name = ask_utils.get_intent_name(handler_input)
        speak_output = "You just triggered " + intent_name + "."

        return handler_input.response_builder.speak(speak_output).response


class CatchAllExceptionHandler(AbstractExceptionHandler):
    def can_handle(self, handler_input, exception):
        return True

    def handle(self, handler_input, exception):

        speak_output = "Sorry, I had trouble doing what you asked. Please try again."

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )


sb = SkillBuilder()

sb.add_request_handler(LaunchRequestHandler())

sb.add_request_handler(getSensorDataIntentHandler())
sb.add_request_handler(getOneSensorValueIntentHandler())
sb.add_request_handler(deleteValuesIntentHandler())
sb.add_request_handler(changeIntervalIntentHandler())

sb.add_request_handler(HelpIntentHandler())
sb.add_request_handler(CancelOrStopIntentHandler())
sb.add_request_handler(FallbackIntentHandler())
sb.add_request_handler(SessionEndedRequestHandler())
sb.add_request_handler(IntentReflectorHandler())

sb.add_exception_handler(CatchAllExceptionHandler())

lambda_handler = sb.lambda_handler()