from langchain_google_genai import GoogleGenerativeAI
from langchain.prompts import PromptTemplate
from langchain.output_parsers import ResponseSchema, StructuredOutputParser


class GeminiConnector(self):


    def __init__(self, google_api_key):
        
        self.duration = None
        self.source = None
        self.destination = None
        self.currency = None
        self.budget = None
        self.start_date = None
        self.people = None
        self.diet = None


    def gemini_llm(self, google_api_key):

        llm = GoogleGenerativeAI(model="gemini-pro", google_api_key=google_api_key)

        return llm


    def create_output_parser(self):

        response_schema = [
            ResponseSchema(name="accommodation", description='name of accommodation suggested to user'),
            ResponseSchema(name="accommodation description", description='description of accommodation suggested to user'),
            ResponseSchema(name="accommodation cost per night", description='cost of accommodation per night suggested to user')
        ]
        for i in range(self.duration):
            response_schema.extend([
                ResponseSchema(name="morning itinerary item name day {day}".format(day=i+1), description='name of morning itinerary item for day {day}'.format(day=i+1)),
                ResponseSchema(name="morning itinerary item day {day}".format(day=i+1), description='morning itinerary item for day {day} with cost'.format(day=i+1)),
                ResponseSchema(name="afternoon itinerary item name day {day}".format(day=i+1), description='name of afternoon itinerary item for day {day}'.format(day=i+1)),
                ResponseSchema(name="afternoon itinerary item afternoon day {day}".format(day=i+1), description='afternoon itinerary item for day {day} with cost'.format(day=i+1)),
                ResponseSchema(name="evening itinerary item name day {day}".format(day=i+1), description='name of evening itinerary item for day {day}'.format(day=i+1)),
                ResponseSchema(name="evening itinerary item evening day {day}".format(day=i+1), description='evening itinerary item for day {day} with cost'.format(day=i+1))
            ])
        response_schema.append(
            ResponseSchema(name="suggested packing", description='suggested luggage to pack for travelling to {destination} for {duration} starting {start_date}'.format(destination=self.destination, duration=self.duration, start_date=self.start_date))
        )
        response_schema.extend([
            ResponseSchema(name="suggested mode of transportation", description='suggested mode of transportation within {destination}'.format(destination=self.destination))
        ])
        response_schema.extend([
            ResponseSchema(name="suggested mode of travel", description='suggested mode of travel from {source} to {destination}'.format(source=self.source, destination=self.destination)),
            ResponseSchema(name="travel cost", description='cost of suggested mode of travel')
        ])
        response_schema.extend([
            ResponseSchema(name="suggested tips", description='suggested tips when in {destination}'.format(destination=self.destination))
        ])
        output_parser = StructuredOutputParser.from_response_schemas(response_schema)

        return output_parser

    
    def core_prompt(self, format_instructions):

        prompt = PromptTemplate(
            template='provide itinerary for {destination} for {people} people for a duration of {duration} days for a budget of {currency} {budget} along with accommodation if {destination} and {source} exist. Provide 3 places per day. Give costs associated with each item. Also suggest what needs to be packed if travelling starting {start_date}. Finally suggest the recommended mode of travel from {source} to {destination} with estimated cost.\n{format_instructions}',
            input_variables=['source', 'destination', 'duration', 'budget', 'currency', 'start_date', 'people'],
            partial_variables={'format_instructions': format_instructions}
        )

        return prompt


    def attach_prompt(self):
        # attach extra filters to core prompt whenever required
        pass


    def chain(self, google_api_key, attach_to_prompt=False):

        llm = self.gemini_llm(google_api_key)
        output_parser = self.create_output_parser()
        format_instructions = output_parser.get_format_instructions()

        if not attach_to_prompt:
            prompt = self.core_prompt(format_instructions)

        chain = prompt | llm | output_parser

        output = chain.invoke({"source": self.source, "destination": self.destination, "duration": self.duration, "budget": self.budget, "currency": self.currency, "start_date": self.start_date, "people": self.people})
