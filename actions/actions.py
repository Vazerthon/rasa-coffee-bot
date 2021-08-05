from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk import events
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet

class ActionSelectRecipe(Action):
    aeropress = {
        "summary": "Cool! You'll need 11g of coffee, ground medium-fine and 200g of water at around 98C.",
        "recipe": [
            "Grab your AeroPress and a filter, place the filter in the cap and fit it to the body of the AeroPress.",
            "Place your AeroPress on top of your cup and throw in your coffee.",
            "Pour 200g of water into the AeroPress and place the lid on.",
            "After two minutes, press down gently until the AeroPress is completely empty.",
            "Enjoy your brew!!",
        ],
    }

    chemex = {
        "summary": "Amazing! You'll need 55g of coffee, ground medium-coarse and 900g of water at around 98C.",
        "recipe": [
            "Grab your Chemex and a filter, place the filter in the Chemex and give it a rinse.",
            "Add your ground coffee.",
            "Pour 100g of water and give the Chemex a swirl.",
            "After 45 seconds, pour another 450g",
            "At around two minutes, pour the remaining 350g of water.",
            "Swirl the Chemex and allow to drain out.",
            "Enjoy your brew!!",
        ],
    }

    methods = {
        "aeropress": aeropress,
        "chemex": chemex,
    }

    def name(self) -> Text:
        return "select_recipe"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        brew_method = tracker.get_slot("brew_method")

        if brew_method is None or brew_method not in self.methods:
            dispatcher.utter_message(text="Sorry, I'm not familiar with that brew method. Please try another one")
            return []

        method = self.methods[brew_method]
        recipe = method["recipe"]

        dispatcher.utter_message(text=method["summary"])
        dispatcher.utter_message(text=f"This recipe has {len(recipe)} steps. When you're ready to brew, say 'next' and we'll get started")            

        return [
            SlotSet("brew_method", None),
            SlotSet("active_recipe", recipe),
            SlotSet("recipe_step", 0),
        ]

class ActionNextRecipeStep(Action):
    def name(self) -> Text:
        return "next_recipe_step"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        active_recipe = tracker.get_slot("active_recipe")
        recipe_step = tracker.get_slot("recipe_step")

        if active_recipe is None or recipe_step >= len(active_recipe):
            dispatcher.utter_message(text="No recipe selected, tell me how you're brewing your coffee and we'll get started")
            return []
        
        current_step = active_recipe[recipe_step]
        dispatcher.utter_message(text=current_step)

        return [SlotSet("recipe_step", recipe_step + 1)]
