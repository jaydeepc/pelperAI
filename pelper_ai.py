from dotenv import load_dotenv
from langchain_community.chat_models import ChatOpenAI
import os
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser


def load_chat_model(model_name="gpt-4-1106-preview"):
    load_dotenv()
    openai_api_key = os.getenv("OPENAI_API_KEY")
    temperature = 0.9
    max_tokens = 1000
    model_name = model_name

    llm = ChatOpenAI(openai_api_key=openai_api_key, model_name=model_name,
                     temperature=temperature, max_tokens=max_tokens)
    return llm


def ai_suggestion(player_hand, community_cards, current_pot, raise_amount, my_position, blind_size, current_bank_roll):
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are world class poker player and poker odds calculator with ultimate knowledge of poker math."),  
        ("user", "{input}")
    ])

    output_parser = StrOutputParser()
    chain = prompt | load_chat_model() | output_parser
    question = f"""In an online Texas NLH poker with max 6 player with {blind_size} INR For {player_hand} and 
                {community_cards} after flop with pot size of {current_pot} and raise amount of {raise_amount}
                suggest what to do after you do the math of equity, pot odds, EV etc and also tell me why?
                My current position is {my_position}.

                Do not give too lengthy answers, just one short paragraph.
                Imagine that you are playing and you are thinking what to do next. Your bankroll is {current_bank_roll}.
                All values are in Indian Rupees.
                
                Give me the result in this format: \n              

                Final Suggestions: [Raise, Call, Fold] (Chose one of these three only) \n
                Reason: [Reason for your suggestion] (Give a short reason for your suggestion)
                """

    response = chain.invoke({"input": question})
    return response