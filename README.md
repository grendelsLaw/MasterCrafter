# MasterCrafter
Python-gui for generating semi-random crafting recipes for Dungeons and Dragons

  This project is meant to be a (relatively) easy way to develop and deploy a crafting option for your D&D players. The script uses three main types of files to do this: Component files, Recipe files, and Type files. All of these can be edited, removed, or added easily to adapt to the player or campaign - so long as they follow the generic formula.
  
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

4) ___Runic Attunement Slot___ 
	- Runes require a creature to form a bond with them before their magical properties can be invoked. This bond is called attunement, and all runes have a prerequisite number of runic attunement slots which they occupy as part of the attuning process.
	- Attuning to a rune requires a creature to spend a Short Rest focused on only that rune while being in physical contact with it. If the Short Rest is interrupted, or if the creature does not meet the necessary prerequisites for attunement to the rune, the attunement attempt fails. Otherwise, at the end of this short rest, the creature gains an intuitive understanding of how to activate the rune's magical properties, as well as any necessary Command words, and may choose a weapon, piece of armor, or item they are holding or wearing to imbue with the power of the rune. The creature may imbue a new weapon, piece of armor, or item they are holding or wearing with the power of the rune they are attuned to by spending a Short Rest while being in physical contact with the rune and the new item; this process removes the rune's power from the originally-imbued weapon, piece of armor, or item.
	- A rune may be attuned to only one creature at a time, and creatures have a set number of runic attunemtent slots, as outlined in the runic attunement table below. Any attempt to attune to a rune while lacking the required number of unoccupied runic attunement slots fails; the creature must end its attunement to a number of runes which satisfies the new rune's runic attunement slot requirements. Additionally, a creature can't attune to more than one copy of a rune. However, a creature may attune to more than one rune at a time, provided they have the required number of unoccupied runic attunement slots. Any ability score requirements for runic attunement only apply for creatures who did not craft the rune.
>-    Level	-	Runic Attunement Slots
>-	1st		-	1
>-	2nd		-	1
>-	3rd		-	2
>-	4th		-	2
>-	5th		-	3
>-	6th		-	3
>-	7th		-	4
>-	8th		-	4
>-	9th		-	5
>-	10th	-	5
>-	11th	-	6
>-	12th	-	6
>-	13th	-	7
>-	14th	-	7
>-	15th	-	8
>-	16th	-	8
>-	17th	-	9
>-	18th	-	9
>-	19th	-	10
>-	20th	-	10
  
  Yay! Okay, but how do you use it? Great question. I'll get back to you on that....
