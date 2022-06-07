# MasterCrafter
Python-gui for generating semi-random crafting recipes for Dungeons and Dragons

![Image of the UI of masterCrafter](https://github.com/grendelsLaw/MasterCrafter/blob/main/resources/images/mastercrafter.png)

  This project is meant to be a (relatively) easy way to develop and deploy a crafting option for your D&D players. The script uses three main types of files to do this: Component files, Recipe files, and Type files. All of these can be edited, removed, or added easily to adapt to the player or campaign - so long as they follow the generic formula.
  
![Image of the UI of masterCrafter for various base feature](https://github.com/grendelsLaw/MasterCrafter/blob/main/resources/images/base_1.png)

1) ___Component files___ represent the array of components that can be combined to generate objects. Components that are submitted are compared to see if they share common possible types (see below). Any combination of components can **only** generate objects of a shared type. Components may also possess modifier types, which may alter the likelihood of certain object types being crafted. These files have 4 parts:
    - Name: The name of the Component
    - Description: A flavorful description of the component
    - Types: a list of the types of objects that this component can be used to craft
    - Type effects: a brief description of what effect the component may add to the component

2) ___Type files___ are the basic types of objects that can be created from components. While different combinations of components may all generate the same object type, these types must be defined as a file before that type of object is crafted. Although components may alter the exact effect of its object type, the basic characteristics and use of an object is inherited from its type. Type files have the 3 aspects:
    - Name: Name of the type
    - Description: A basic description of how the object type is used by a player. If this type has an effect (damage amount, damage type, duration, distance, etc) that you wish to be variable (based on the number of components used or the players proficiency), this description should be formatted accordingly.
    - Requirments: Certain types may require very specific type of component to be made. Example - an explosive device may require a *volatile* component to be one of the components used to generate it, while a potion does not require anything special (other than the alchemist's and/or brewing equipment, of course. But it is assumed you're enforcing this requirement on your own...)

3) ___Recipe files___ are templates for what may be crafted. You may develop your own but the files also auto-generate every time you stumble-on a combination of components that make an object. For this reason, each player may like to have their own set of MasterCrafter folders so that known recipes aren't shared between players. Recipe files have the 4 parts as well:
    - Name: The Name of the recipe. When a new recipe is discovered, you will be asked to name the combination. This name is then used to write a new recipe file that can be pulled back up from the GUI.
    - Description: A basic description of the object generated by this recipe. Unique recipes may have specific descriptions, but procedurally generated recipes inherit their descriptions from the object type.
    - Requirements: The specific components required to make this recipe. Unique recipes may have components that are *not* found in the component files but generated recipes will list the exact components used during the initial crafting.
    - Type: The type of object this recipe generates. Since a combination of components may generate more than one type of object, this is used to track which types of a component combination have already been discovered.

## Types of crafting objects
  First and foremost - all crafted objects require at least two components and all components must share a common "type". If all the objects share a "Potion-type", they can craft a potion. If the components share __multiple__ types, a type will be randomly selected from the list of shared types. All created objects will generate a recipe file which can be used to re-craft the object exactly as it was originally made. If a list of components can make multiple types, but not all types have been explored, you have the option to either create a known recipe or __tinker__ and try to craft __other types__. Therefore, the greater number of components used in a craft, the smaller the odds they will share a common type. However, the potential potency of a crafted object will increase with the number of components used. Some types require specific kinds of components to be crafted, which are listed in the recipe files. An example are bombs that require at least one `volatile` component. Certain subtypes have the ability to ___backfire___ and detonate immediately upon crafting. Currently, the only two types that will backfire are `volatile` and `nebulizer` but this can be changed in the python file. Additionally, some types will pull a random component effect. These are currently the `poison`s, `potion`s, and `magic armor/weapon`s but this too can be tweaked in the python script. Finally, there are other component subtypes that do not effect the type of final product, but will change the variables of crafting. Currently there are:
    - Volatile: As mentioned previously, these are required to make bombs. Furthermore, they may cause the product to explode upon completion.
    - Nebulizer: These are required to make gases. Furthermore, they may cause the product to explode upon completion.
    - Amplifiers: boost the damage, duration, and area-of-effect rolls during crafting.
    - Dampeners: conversely, these decrease the damage, duration, and area-of-effect rolls during crafting.
    - Stabilizers: decrease the odds of backfire depending on the ratio of volatile to stabilizers. For each stabilizer in the components, one volatile/nebulizer component's chance of backfiring is removed. Types that require volatile/nebulizer components can still be crafted with the addition of a stabilizer - they just have a decreased chance of backfiring.
    - Infusers: mimic the holistic crafter's ability and add an extra component effect to the crafted object.

1) ___Potions___ Crafting a potion will pull one random component effect, which will last for a duration specified on the generated recipe file.

2) ___Bombs___ By default, bombs deal force damage over a certain area. They require at least one `volatile` component.

3) ___Poisons___ Like potions, poisons will pull one random component effect. Unlike potions, which must be ingested, poisons can be used to coat weapons or be ingested. The poison effects then last for the specified number of attacks or duration, respectively.

4) ___Gases___ Gases require `nebulizer`s and disperse in a given area for a certain amount of time. Similar to potions and poisons, gases will also pull at least one component effect.

5) ___Magic weapons and armor___ Combining certain items with generic weapons or armor can add component effects and require `weapon` and `armor`, respectively.

6) ___Rations___ Crafting a ration will sate anyone who eats its (up to the GM's discretion as to *how many* characters can be fed from a crafting and also, at a basic state, grants a number fo temporary HP. Additionally, many of the components possess the infuser tag, which applies a component effect. These effects can have an immediate effect or last for a duration specified on the generated recipe file per the discretion of the GM.

7) ___Runesmithing___ Runes are a special type known as a `progression` type, which - upon crafting - become a new type of component that can be used in additional craftings. Runes have specific abilities which increase and change with their progression, helping to tell the story of the unique runes crafted by players and characters.
	- Runes require both a blank `Rune` and a `Rune Schemata` to craft an initial Basic Rune. Progressing a rune beyond the Basic tier requires both the crafted rune as well as another Rune Schemata. There are eight total runic *Paths* (i.e. **Aett**, **Bifra**, **Fenr**, **Kao**, **Lokir**, **Ragnr**, **Saeg**, and **Wuldr** Paths), each with four tiers of features and associated abilities (i.e. **Basic Rune**, **Lesser Rune**, **Greater Rune**, and **Epic Rune** tiers). DMs are encouraged to provide Rune Schematas as loot and/or from magical shops, to assist with crafting immersion, and may offer their players either a complete Path schemata (e.g. *Path of Ragnr Schemata*) or a specific tier schemata (e.g. *Lesser Ragnr Rune Schemata* or simply *Lesser Rune Schemata* (for random Path)). 

	- When crafting a rune, DMs/players will have the option to craft a rune following a specific Path or to craft a rune at random, allowing fate (or RNG) to determine the Path of the next tier. When crafting following a specific Path, DMs and players will find that there are hidden bonuses for remaining loyal to the Path, which upgrade existing abilities of the crafted rune that are from the same Path. However, some Runesmiths may prefer to experiment with progressing their unique rune through multiple Paths to reveal previously-undiscovered power (there are 4096 possible combinations of abilities, most of which are as-yet unexplored).

	- Runes are a very powerful addition to any game and, as such, have specific requirements which must be met to wield the magic. Runic requirements, which are described in the first line of each tier's feature description, are specifically designed to be challenging and are related to the abilities granted by the feature, which the player must overcome to wield their power effectively in combat. DMs are encouraged to uphold these requirements, or alter them to suit their unique game and setting, as the achievement of runic attunement can add tremendous flavor to the storied accomplishments of your brave adventurers (while also helping to balance the runes mechanically). 

	- ___Runic Attunement Slot___ Runes require a creature to form a bond with them before their magical properties can be invoked. This bond is called attunement, and all runes have a prerequisite number of runic attunement slots which they occupy as part of the attuning process.
		- Attuning to a rune requires a creature to spend a Short Rest focused on only that rune while being in physical contact with it. If the Short Rest is interrupted, or if the creature does not meet the necessary prerequisites for attunement to the rune, the attunement attempt fails. Otherwise, at the end of this short rest, the creature gains an intuitive understanding of how to activate the rune's magical properties, as well as any necessary Command words, and may choose a weapon, piece of armor, or item they are holding or wearing to imbue with the power of the rune. The creature may imbue a new weapon, piece of armor, or item they are holding or wearing with the power of the rune they are attuned to by spending a Short Rest while being in physical contact with the rune and the new item; this process removes the rune's power from the originally-imbued weapon, piece of armor, or item.

		- A rune may be attuned to only one creature at a time, and creatures have a set number of runic attunemtent slots, as outlined in the runic attunement table below. Any attempt to attune to a rune while lacking the required number of unoccupied runic attunement slots fails; the creature must end its attunement to a number of runes which satisfies the new rune's runic attunement slot requirements. Additionally, a creature can't attune to more than one copy of a rune. However, a creature may attune to more than one rune at a time, provided they have the required number of unoccupied runic attunement slots.

		- If a player's character no longer meets the requirements to attune to a rune as a result of a runic upgrade, their attunement to that rune immediately ends until they meet the requirements and complete a Short Rest to re-establish their attunement.

  Level: Runic Attunement Slots

  1-10 | 11-20
--- | ---
1st:		1   | 11th:  5
2nd:		1   | 12th: 	5
3rd:		2   | 13th: 	5
4th:		2   | 14th: 	6
5th:		3   | 15th: 	6
6th:		3   | 16th: 	6
7th:		3   | 17th: 	7
8th:		4   | 18th: 	7
9th:		4   | 19th: 	8
10th: 	4   | 20th: 	8

## Other goodies

![Image of the UI of masterCrafter for various goodies](https://github.com/grendelsLaw/MasterCrafter/blob/main/resources/images/base_2.png)

1) ___Pockets___ If you're playing with multiple players using this system, it can be hard to keep track of what components each player has and wants to use. Therefore, you can create a *pocket* for each player. Each pocket gets saved between sessions and can be altered independently. Pockets can be added or deleted as you require.

2) ___Shop___ Hitting the `shop` button allows you to simulate a shop for your players. You will be prompted for a number of components you would like the shop to have, after which the specified number of components will be selected randomly from the list of components along with a random price within a set range, based on item utility and rarity, determined from the component file. Some components are listed at `market price` and should be up to the discretion of the GM given that these items are rare and/or extremely useful. Component descriptions can be viewed in the main window by double-clicking them in the shop inventory, and can also be loaded into specific pockets.

3) ___Forage___ Since most of these components are natural products, the players should have the opportunity to find them in the wild. By hitting the `forage` button, you will be prompted to choose the type of terrain your players are in as well as an amount of time the player is spending to look for items. Based on the location and time spent, a random number of items native to that terrain will be presented. Similar to the shop mechanic, component descriptions can be viewed in the main window by double-clicking them, and can also be loaded into specific pockets.

4) ___Subclasses___ Several subclasses have also been written into the program. It is up the GM how they would like these subclasses to be pursued/achieved by players, but a list of the subclasses and description of their associated specializations can be found by selecting the `subclasses` button.

## Conclusion
  We hope that you enjoy the MasterCrafter system and encourage you to experiment with it as well as modify the files to meet your own needs and desires. Simply add or remove files in the `resources` directories and verify they've loaded correctly in the program. Constructive criticism (and shiny new components) welcome!
