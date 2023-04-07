
import ask_sdk_core.utils as ask_utils
from ask_sdk_core.skill_builder import SkillBuilder
from ask_sdk_core.dispatch_components import AbstractRequestHandler, AbstractExceptionHandler
from ask_sdk_core.handler_input import HandlerInput
from ask_sdk_model import IntentConfirmationStatus,Response

import requests
import json

mongoUrls = {
    'findUrl': "https://data.mongodb-api.com/app/data-ojsvg/endpoint/data/v1/action/find",
    'deleteUrl': "https://data.mongodb-api.com/app/data-ojsvg/endpoint/data/v1/action/deleteMany",
    'updateUrl': "https://data.mongodb-api.com/app/data-ojsvg/endpoint/data/v1/action/updateOne",
}

mongoHeaders = {
    'Content-Type': 'application/json',
    'Access-Control-Request-Headers': '*',
    'api-key': "",
}


class LaunchRequestHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return ask_utils.is_request_type("LaunchRequest")(handler_input)

    def handle(self, handler_input):
        handler_input.attributes_manager.session_attributes['waiting_for_response'] = True

        speech_text = "Welcome, what do you want to know about your plant?"
        reprompt_text = "What do you want to know about your plant?"

        return handler_input.response_builder.speak(speech_text).ask(reprompt_text).response

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

        try:
            dataResponse = json.loads(requests.request("POST", mongoUrls["findUrl"], headers=mongoHeaders, data=findData).text)

            if dataResponse["documents"]==[]:
                raise Exception("The database is empty.")

            dataTable=dataResponse["documents"][0]      
            speak_output = "On your plant, the latest sensor values measured are: Light: " + str(dataTable["Light"]) + ", Temperature: " + str(dataTable["Temperature"]) + ", Humidity: " + str(dataTable["Humidity"])  + ", Soil Moisture: " + str(dataTable["SoilMoisture"]) 

        except Exception as e:
            speak_output = str(e)

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
        
        try:
            dataResponse = json.loads(requests.request("POST", mongoUrls["findUrl"], headers=mongoHeaders, data=findData).text)
            slot_value = handler_input.request_envelope.request.intent.slots['sensor'].resolutions.resolutions_per_authority[0].values[0].value.name

            if dataResponse["documents"]==[]:
                raise Exception("The database is empty.")

            dataTable=dataResponse["documents"][0]     
            speak_output = "On your plant, the latest "+slot_value+" value measured is: " + str(dataTable[slot_value])

        except Exception as e:
            speak_output = str(e)

        return handler_input.response_builder.speak(speak_output).response

class deleteValuesIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return ask_utils.is_intent_name("deleteValuesIntent")(handler_input)

    def handle(self, handler_input):
        
        dataDelete = json.dumps({
            "collection": "plant1",
            "database": "plants",
            "dataSource": "Cluster0",
            "filter": { "delete": 1 },
              }
        )

        confirmation_status = handler_input.request_envelope.request.intent.confirmation_status

        if confirmation_status == IntentConfirmationStatus.CONFIRMED:
            speak_output = "Great, your data will be erased."
            try:
                requests.request("POST", mongoUrls["deleteUrl"], headers=mongoHeaders, data=dataDelete)
            except Exception:
                speak_output = "Something went wrong while deleting your data,try again later."
        else:
            speak_output = "Okay, I won't do that."
            
        return handler_input.response_builder.speak(speak_output).response

class changeIntervalIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return ask_utils.is_intent_name("changeIntervalIntent")(handler_input)

    def handle(self, handler_input):

        try:
            slot_value = int(handler_input.request_envelope.request.intent.slots['number'].value)

            data = json.dumps({
            "collection": "device1",
            "database": "devices",
            "dataSource": "Cluster0",
            "filter": { "_id": 1 },
              "update": {
                  "$set": {
                      "interval": slot_value,
                      }
                  }
            })
            
            if slot_value<=0:
                raise Exception("You must choose a number between one and five, please try again.")
            if slot_value>5:
                raise Exception("The maximum number of reading is five times a day, please try again.")
            
            try:
                response = requests.request("POST", mongoUrls["updateUrl"], headers=mongoHeaders, data=data)
                speak_output = "Your scanning interval will be changed to "+str(slot_value)+" times a day, after the next scan."
            except:
                speak_output = "Something went wrong while changing the interval."
                
        except Exception as e:
            return handler_input.response_builder.speak(str(e)).response
        
        return handler_input.response_builder.speak(speak_output).response

class changePumpStateIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return ask_utils.is_intent_name("changePumpStateIntent")(handler_input)

    def handle(self, handler_input):

        confirmation_status = handler_input.request_envelope.request.intent.confirmation_status

        if confirmation_status == IntentConfirmationStatus.CONFIRMED:
            try:
                slot_value = int(handler_input.request_envelope.request.intent.slots['state'].resolutions.resolutions_per_authority[0].values[0].value.name)           
                
                data = json.dumps({
                "collection": "device1",
                "database": "devices",
                "dataSource": "Cluster0",
                "filter": { "_id": 1 },
                "update": {
                    "$set": {
                        "pump": int(slot_value),
                        }
                    }
                })

                response = requests.request("POST", mongoUrls["updateUrl"], headers=mongoHeaders, data=data)
                if slot_value==0:
                    speak_output = "You disabled the watering system."
                else:
                    speak_output = "You enabled the watering system. If the soil moisture level is below 30, your plant will be watered."
            except:
                speak_output = "Something went wrong while changing the pump state."
        else:
            speak_output = "Okay, I won't do that."
            
        return handler_input.response_builder.speak(speak_output).response


class HelpIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return ask_utils.is_intent_name("AMAZON.HelpIntent")(handler_input)

    def handle(self, handler_input):
        handler_input.attributes_manager.session_attributes['waiting_for_response'] = True

        speak_output = "You can ask me about your plant or set the measuring interval for the sensors! How can I help?"
        reprompt_text = "What do you want to know about your plant?"

        return handler_input.response_builder.speak(speak_output).ask(reprompt_text).response

class CancelOrStopIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return (ask_utils.is_intent_name("AMAZON.CancelIntent")(handler_input) or
                ask_utils.is_intent_name("AMAZON.StopIntent")(handler_input))

    def handle(self, handler_input):
        speak_output = "Plant analyser closed."

        return handler_input.response_builder.speak(speak_output).set_should_end_session(True).response

class FallbackIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return ask_utils.is_intent_name("AMAZON.FallbackIntent")(handler_input)

    def handle(self, handler_input):
        reprompt = "Hmm, I'm not sure."
        speech = "I didn't catch that. What can I help you with?"

        return handler_input.response_builder.speak(speech).ask(reprompt).response

class SessionEndedRequestHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return ask_utils.is_request_type("SessionEndedRequest")(handler_input)

    def handle(self, handler_input):

        return handler_input.response_builder.response

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
sb.add_request_handler(changePumpStateIntentHandler())

sb.add_request_handler(HelpIntentHandler())
sb.add_request_handler(CancelOrStopIntentHandler())
sb.add_request_handler(FallbackIntentHandler())
sb.add_request_handler(SessionEndedRequestHandler())

sb.add_exception_handler(CatchAllExceptionHandler())

lambda_handler = sb.lambda_handler()