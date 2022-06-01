#!/usr/bin/env python

# Artificing made GUI

# Import required packages
import PySimpleGUI as sg
import os.path
import random as rand

sg.theme("DarkTanBlue")

#-------------------------------------------------------------------------------

# Define default values
# A list of the components
materials=[]
known_recipes=[]
terrains={
"Desert":[],
"Forest":[],
"Hill":[],
"Mountain":[],
"Plain":[],
"Swamp":[],
"Coast":[],
"None":[]
}

# A description of the artificed item
description="Submit components to craft an item."
# default list type
list_type="components"

# Modifier tags - these gets skipped when assessing type
# Add requirement tags here as well
modifiers=["Volatile", "Amplifier", "Stabilizer", "Nebulizer", "Weapon", "Armor", "Spell slot"]

# Types that get effects by default
# Add type here if you want a random effect to always be added to that type
types_w_effects=["Potion", "Gas", "Magic weapon", "Poison", "Magic armor"]

# Backfire tags
# Add Modifier tag that you wish to possibly explode as soon its made
backfire_type = ["Volatile", "Nebulizer"]

subclass_types={
"Novice":"Novice:\n\nYou know little but are eager. With your learning you know just enough to be dangerous. To your enemies, to your allies, and to yourself...",
"Potency specialist": "Potency specialist:\n\nAfter years of study, you've found ways get the most 'boom' for the buck.\n\nYou can alter the number of dice to be rolled. Potency assignations can round up and your proficiency score is added to your rolls.",
"Duration specialist": "Duration specialist:\n\nDespite multiple setbacks, you've learned how to sustain and spread effects. \n\nTime and distance rolls for your creations can round up and your proficiency score is added to random time/distance rolls.",
"Holistic crafter": "Holistic crafter:\n\nWhile other's see components as merely the 'means to an end', you understand that every component add its own unique function. \n\nAn additional effect, if possible, is added to every item you craft.",
"Versatile crafter": "Versatile crafter:\n\nAlthough many squander efficiency in the opulance of the university, you've learned to make do with less. \n\nYou do not need requirements to craft contraptions that require certain types.",
"Careful crafter": "Careful crafter:\n\nAfter watching many of your peers succumb to carelessness, you've learned that the only old crafters are careful crafters. \n\nCreations you craft will not backfire.",
"Perfectionist": "Perfectionist:\n\nSome crafters stop working after success but you've learned that practice makes perfect. \n\nYou are able to re-roll stats (for better or worse) when remaking known recipes.",
"Forager": "Forager:\n\nWhile other crafter focus on the products, you have excelled at finding the components. \n\nWhen foraging, you are guaranteed to find at least one component and may even find nonnative components."
}

sub_names=[]
for i in subclass_types:
    sub_names.append(i)

#-------------------------------------------------------------------------------

def roll_desc(first_desc,
read_only=False,
proficiency_boost=0,
damage_boost=False,
damage_boost_number=0,
time_boost=False,
time_boost_number=0,
distance_boost=False,
distance_boost_number=0,
amplify=False):
    mat_boost=int((len(materials)-2)/2)
    new_desc=first_desc
    if amplify==True:
        amp=2
    else:
        amp=1
    if "DAMAGE" in new_desc:
        new_desc=new_desc.split("DAMAGE")
        ticker=1
        desc=""
        for i in new_desc:
            if ticker%2==0:
                spot=i.split("-")
                low_number=int(spot[0])
                high_number=int(spot[1])+mat_boost+1
                theNumber=round(rand.randint(low_number, high_number)+((amp*rand.randint(1, 21))+proficiency_boost+damage_boost_number)/20)
                if damage_boost!=True:
                    theNumber=int(rand.randint(low_number, high_number)+((amp*rand.randint(1, 21))/20))
                if read_only:
                    theNumber=str(low_number)+"-"+str(high_number)
                desc+=str(theNumber)
            else:
                desc+=i
            ticker+=1
        new_desc=desc
    if "TIME" in new_desc:
        new_desc=new_desc.split("TIME")
        ticker=1
        desc=""
        for i in new_desc:
            if ticker%2==0:
                spot=i.split("-")
                low_number=int(spot[0])
                high_number=int(spot[1])+mat_boost+1
                theNumber=round(rand.randint(low_number, high_number)+((amp*rand.randint(1, 21))+proficiency_boost+time_boost_number)/20)
                if time_boost!=True:
                    theNumber=int(rand.randint(low_number, high_number)+(amp*rand.randint(1, 21))/20)
                if read_only:
                    theNumber=str(low_number)+"-"+str(high_number)
                desc+=str(theNumber)
            else:
                desc+=i
            ticker+=1
        new_desc=desc
    if "DISTANCE" in new_desc:
        new_desc=new_desc.split("DISTANCE")
        ticker=1
        desc=""
        for i in new_desc:
            if ticker%2==0:
                spot=i.split("-")
                low_number=int(spot[0])
                high_number=int(spot[1])+mat_boost+1
                theNumber=5*(round(rand.randint(low_number, high_number)+5*(((amp*rand.randint(1, 21))+proficiency_boost+distance_boost_number)/20))//5)
                if distance_boost!=True:
                    theNumber==5*(int(rand.randint(low_number, high_number)+5*(((amp*rand.randint(1, 21)))/20))//5)
                if read_only:
                    theNumber=str(low_number)+"-"+str(high_number)
                desc+=str(theNumber)
            else:
                desc+=i
            ticker+=1
        new_desc=desc
    if "VALUE" in new_desc:
        new_desc=new_desc.split("VALUE")
        desc=""
        for i in new_desc:
            desc+=i
        new_desc=desc
    return new_desc

# Makes the popups
def popup_select(text_choice, the_list,select_multiple=False):
    layout = [[sg.Text(text_choice)],
    [sg.Listbox(the_list,key='_LIST_',size=(45,len(the_list)),select_mode='extended' if select_multiple else 'single',bind_return_key=True),sg.OK()]]
    window3 = sg.Window('Select One',layout=layout)
    event, values = window3.read()
    window3.close()
    del window3
    if len(values['_LIST_']):
        return values['_LIST_'][0]
    else:
        return the_list[0]

def popup_shop(text_choice, the_list,remove_item=False,select_multiple=False):
    layout = [[sg.Text(text_choice)],
    [sg.Listbox(the_list,key='_LIST_',size=(45,20),select_mode='extended' if select_multiple else 'single',bind_return_key=True),
    [sg.Button("Add to player pocket"),
    sg.Listbox(list(pocket.keys()), size=(10,3),key="-shop_name-"),
    sg.OK(key="-OK-")]]]

    window2 = sg.Window('Select One',layout=layout)
    try:
        event2, values2 = window2.read()
        if event2 == "Exit" or event2 == sg.WIN_CLOSED:
            window2.close()
            del window2
        while event2 != "-OK-":
            event2, values2 = window2.read()
            if event2 == "Exit" or event2 == sg.WIN_CLOSED:
                break

            elif event2 == "_LIST_" and len(values2["_LIST_"]):
                selected_name=values2["_LIST_"][0].split(" - ")[0].lower()
                desc_name=components[selected_name].name
                desc_desc=components[selected_name].description
                desc_types=components[selected_name].types
                description=desc_name+"\n\n"+desc_desc
                if len(components[selected_name].effects) > 0:
                    description=description+"\n\nTypes:"
                    for i in desc_types:
                        description+="\n   -"+i+": "+components[selected_name].effects[i]
                description=roll_desc(description, True)
                window["-item_description_2-"].update(description)
                if selected_name+".png" in images_list:
                    window["-item_image-"].update("resources/images/"+selected_name+".png")
                else:
                    window["-item_image-"].update("resources/images/general_component.png")

            elif event2=="Add to player pocket" and len(values2["_LIST_"]):
                if len(values2["-shop_name-"]):
                    if remove_item==True:
                        the_list.remove(values2["_LIST_"][0])
                        window2["_LIST_"].update(the_list)
                    if " - " in values2["_LIST_"][0]:
                        item_name=values2["_LIST_"][0].split(" - ")[0]
                    else:
                        item_name=values2["_LIST_"][0]
                    pocket[values2["-shop_name-"][0]].append(item_name)
                    pocket[values2["-shop_name-"][0]].sort()
                    secret_pocket[values2["-shop_name-"][0]].append(item_name)
                    secret_pocket[values2["-shop_name-"][0]].sort()
                    if pocket_name==values2["-shop_name-"][0] and list_type=="pocket":
                        window["-lb_1-"].update(pocket[pocket_name])

        window2.close()
        del window2
    except:
        pass


#------------------------------------------------------------------------------
# Define the Component class
class Component:
    def __init__(self, name, description, types, effects):
        self.name=name
        self.description=description
        self.types=types
        self.effects=effects

# Define the Recipe class
class Recipe:
    def __init__(self, name, description, components, types):
        self.name=name
        self.description=description
        self.components=components
        self.types=types


# Define the Type class
class Type:
    def __init__(self, name, description, requirements):
        self.name=name
        self.description=description
        self.requirements=requirements

#-------------------------------------------------------------------------------

# First, we generat a list of available components from the component files
# Generate a blank dictionary
components={}
# Make a list of the component files
component_list=os.listdir("resources/components/")
# Iterate through the component files and add them to the dictionary
for i in component_list:
    # Makes sure the file is a .component file
    if i.lower().endswith(".component"):
        try:
            # Opens, loads, and closes the component file
            component_i=open("resources/components/"+i, "r")
            loaded_i=component_i.read()
            component_i.close()
            # Strips and splits the component file based on newlines
            loaded_i=loaded_i.strip().split("\n")
            # Gets the component name
            name_i=loaded_i[0].strip().split("Name:")[1].strip()
            # If the component isn't in the component dictionary, it gets added
            if name_i not in components:
                pre_splice=loaded_i[1].split("Description:")[1].strip()
                if "SPACE" in pre_splice:
                    post_splice=""
                    for exon in pre_splice[0].split("SPACE"):
                        post_splice+=exon+"\n"
                    post_splice=post_splice[0:len(post_splice)-2]
                else:
                    post_splice=pre_splice
                new_comp=Component(
                name_i,
                post_splice,
                loaded_i[2].split("Types:")[1].strip().split(", "),
                {}
                )
                for j in loaded_i[3:len(loaded_i)]:
                    effect_type=j.split(":")[0].rstrip()
                    effect_effect=j.split(":")[1].rstrip()
                    if "SPACE" in effect_effect:
                        spliced=effect_effect.split("SPACE")
                        tick=""
                        for exon in spliced:
                            tick+=exon+"\n"
                        tick=tick[0:len(tick)-2]
                    else:
                        tick = effect_effect
                    new_comp.effects[effect_type]=tick
                components[name_i.lower()]=new_comp
        except:
            print("Unable to parse file: "+i)

#-------------------------------------------------------------------------------
# Now we pull the recipes and load in any components missing from the component dictionary
# Same deal, we make a blank dictionary
recipes={}
# Get a list of all the recipe files
recipe_files=os.listdir("resources/recipes/")
# Iterate through them
for i in recipe_files:
    # Make sure its a recipe file
    if i.lower().endswith(".recipe"):
        try:
            # Open the file, read it, then close it
            possible_recipe=open("resources/recipes/"+i, "r")
            loaded_recipe=possible_recipe.read()
            possible_recipe.close()
            # We split the recipe based on the newlines
            loaded_recipe=loaded_recipe.strip().split("\n")
            # We pull the name of the recipe
            name_i=loaded_recipe[0].strip().split("Name:")[1].strip()
            # If the name isn't in the recipe list, we add it
            if name_i not in recipes:
                # Set the first list value to be the description of the recipe
                new_recipe=Recipe(
                name_i,
                loaded_recipe[3:len(loaded_recipe)],
                loaded_recipe[2].split("Components:")[1].strip().split(", "),
                loaded_recipe[1].split("Types:")[1].strip()
                )
                thingo=""
                for desc_effect in new_recipe.description:
                    if "SPACE" in desc_effect:
                        desc_effect=desc_effect.split("SPACE")
                        for exon in desc_effect:
                            thingo+=exon+"\n"
                    else:
                        thingo+=desc_effect+"\n"
                new_recipe.description=thingo
                recipes[name_i.lower()]=new_recipe
                for j in new_recipe.components:
                    if j.lower() not in components:
                        new_comp=Component(
                        j,
                        "A material of unknown use.",
                        [name_i],
                        {}
                        )
                        modifiers.append(j)
                        components[j.lower()]=new_comp
        except:
            print("Unable to parse file: "+i)

recipe_keys=[]
recipe_values=[]
for i in recipes:
    recipe_keys.append(recipes[i].name)
    hit_value=recipes[i].components
    hit_value.sort()
    recipe_values.append(hit_value)

known_recipes=recipe_keys

component_list=[]
for i in components:
    component_list.append(components[i].name)
component_list.sort()

#-------------------------------------------------------------------------------
# Now we get the list of the possible files
images_list=os.listdir("resources/images/")

#-------------------------------------------------------------------------------
# Okay, now lets load all the type files
# First, lets make a type blank directory
types={}
type_files=os.listdir("resources/types")
# Now we iterate through them
for i in type_files:
    # If the file is a type file...
    if i.lower().endswith(".type"):
        try:
            # It gets opened, loaded, and closed
            type_i=open("resources/types/"+i, "r")
            loaded_i=type_i.read()
            type_i.close()
            # Then it gets stripped and split by the newlines
            loaded_i=loaded_i.strip().split("\n")
            # The name of the type is pulled
            name_i=loaded_i[0].split("Name:")[1].strip()
            # If the type doesn't exist int he type directory, it gets added!
            if name_i.lower() not in types:
                pre_splice=loaded_i[1].split("Description:")[1].strip()
                if "SPACE" in pre_splice[0]:
                    post_splice=""
                    for exon in pre_splice[0].split("SPACE"):
                        post_splice+=exon+"\n"
                    post_splice=post_splice[0:len(post_splice)-2]
                else:
                    post_splice=pre_splice
                new_type=Type(
                name_i,
                post_splice,
                [loaded_i[2].split("Requirements:")[1].strip()],
                )
                types[name_i.lower()]=new_type
        except:
            print("unable to parse file: "+i)

type_list=[]
for i in types:
    type_list.append(types[i].name)

#-------------------------------------------------------------------------------
pocket={}
secret_pocket={}
if ".pockets" in os.listdir():
    pocket_file=open(".pockets", "r")
    pocket_start=pocket_file.read()
    pocket_file.close()
    pocket_start=pocket_start.strip().split("-")
    for i in pocket_start:
        piq=[]
        if len(i) >0:
            pname=i.split("\n")
            if len(pocket)==0:
                pocket_name=pname[1].strip()
            pocket[pname[1].strip()]=[]
            secret_pocket[pname[1].strip()]=[]
            for j in range(2, len(pname)):
                if len(pname[j])>0:
                    piq.append(pname[j])
            pocket[pname[1].strip()]=piq
            pocket[pname[1].strip()].sort()
            secret_pocket[pname[1].strip()]=piq
            secret_pocket[pname[1].strip()].sort()
else:
    pocket_name="None"

#-------------------------------------------------------------------------------
# Now we parse the component files and look for terrain key words so that
# they can get added to the terrain dictionary
for i in components:
    for j in terrains:
        if j != "None":
            if j.lower() in components[i].description.lower():
                terrains[j].append(components[i].name)
            else:
                terrains["None"].append(components[i].name)

#-------------------------------------------------------------------------------
# Generate the columns
# First column is the search box and buttons to toggle between components, recipes, and types
material_entry_column = [
    sg.Button("Search"),
    sg.In(size=(10, 2), key="-search_key-"),
    sg.Push(),
    sg.Button("Components"),
    sg.Button("Types"),
    sg.Button("Known recipes"),
    sg.Button("Subclasses")
]
# Second column has the first listbox, which you can select items to check characteristics,
# and the second listbox, which shows you list items you've selected, as well as the artifice button
all_submitted_column = [
    sg.Listbox(values=component_list, enable_events=True, size = (43,15), key="-lb_1-"),
    [sg.Button("Add component"),
    sg.Push(),
    sg.Push(),
    sg.Button("Remove component"),
    sg.Push(),
    sg.Button("Clear list"),],
    sg.Push(),
    sg.Listbox(values=materials, size = (43,15), key="-lb_2-"),
]
# Third column shows the item image and the procedurally generated description
main_font=("Arial bold", 11)
item_description = [
    sg.Image("resources/images/none.png", key = "-item_image-"),
    sg.Multiline(description, size=(50,15),key = "-item_description_2-", font=main_font),
]

# This new column lets you select a artificing subtype. It may get switched to a checkbox system
# depending on Shepherd's thoughts
subclass_buttons=[
    [sg.Push(),
    sg.Radio("Novice", "subclass", default=True, key = "-subclass_novice-"),
    sg.Radio("Potency specialist", "subclass", default=False, key = "-subclass_damage-"),
    sg.Radio("Duration specialist", "subclass", default=False, key = "-subclass_duration-"),
    sg.Radio("Holistic crafter", "subclass", default=False, key = "-subclass_holistic-"),
    sg.Push()],
    [sg.Push(),
    sg.Radio("Versatile crafter", "subclass", default=False, key = "-subclass_versa-"),
    sg.Radio("Careful crafter", "subclass", default=False, key = "-subclass_care-"),
    sg.Radio("Perfectionist", "subclass", default=False, key = "-subclass_perf-"),
    sg.Radio("Forager", "subclass", default=False, key = "-subclass_for-"),
    sg.Push()]
]

pockets_column=[
    sg.In(pocket_name, size=(10, 2),key="-pocket-"),
    sg.Button("View pocket"),
    sg.Button("Switch pocket"),
    sg.Push(),
    sg.Button("Add new"),
    sg.Button("Delete pocket")
]

# Now all four columns get placed into a singlular layout, which gets called
layout=[
    material_entry_column,
    subclass_buttons,
    all_submitted_column,
    [sg.Button("Add to pocket"),
    sg.Push(),
    sg.Push(),
    sg.Button("Shop"),
    sg.Button("Forage"),
    sg.Push(),
    sg.Text("Proficiency bonus:"),
    sg.In(size=(15,1), key="-prof-"),
    sg.Button("Craft!")],
    item_description,
    pockets_column
]
window=sg.Window("Crafting made easy!", layout)

# This while true loop is where all the magic happens
while True:
    # events and values are read as the first thing
    event, values = window.read()
    # If the exit button is pressed or the window is otherwise closed, the loop breaks
    if event == "Exit" or event == sg.WIN_CLOSED:
        break

    # If the search button is pressed, a search list is generated depending on if
    # you're searching through the components, types, or recipes
    elif event == "Search":
        # First, a blank list is generated
        search_list=[]
        # if the list type is components, components are searched
        if list_type=="components":
            for i in components:
                if values["-search_key-"].lower() in components[i].name.lower():
                    search_list.append(components[i].name)

        # if the list type is types, types are searched
        elif list_type=="types":
            for i in types:
                if values["-search_key-"].lower() in types[i].name.lower():
                    search_list.append(types[i].name)

        # if the list type is reicpes, recipes are searched
        elif list_type=="recipes":
            for i in recipes:
                if values["-search_key-"].lower() in recipes[i].name.lower():
                    search_list.append(recipes[i].name)
        # Finally, listbox 1 is updated with the search list
        search_list.sort()
        window["-lb_1-"].update(search_list)

    #Switches list_type to components and updates listbox 1
    elif event=="Components":
        list_type="components"
        window["-lb_1-"].update(component_list)

    # Switched list_type to types and updates listbox 1
    elif event=="Types":
        list_type="types"
        window["-lb_1-"].update(type_list)

    # Switches list_type to recipes and updats listbox 11
    elif event=="Known recipes":
        list_type="recipes"
        window["-lb_1-"].update(known_recipes)

    # View the contents of current pocket
    elif event=="View pocket":
        if pocket_name != "None":
            list_type="pocket"
            pocket[pocket_name]=list(secret_pocket[pocket_name])
            window["-lb_1-"].update(pocket[pocket_name])
            materials=[]
            window["-lb_2-"].update(materials)

    elif event=="Switch pocket":
        if len(pocket):
            try:
                pocket_name=popup_select("Which pocket you would you like to explore:", list(pocket.keys()))
            except:
                pass
            window["-pocket-"].update(pocket_name)
            if list_type=="pocket":
                window["-lb_1-"].update(pocket[pocket_name])
        else:
            sg.Popup("There are no pockets! Try making one.")

    elif event == "Add new":
        pocket_name=sg.popup_get_text("What is player's name:")
        pocket[pocket_name]=[]
        secret_pocket[pocket_name]=[]
        window["-pocket-"].update(pocket_name)
        if list_type=="pocket":
            window["-lb_1-"].update(pocket[pocket_name])

    # Adds selected components or selected recipes components to listbox 2 for artificing
    elif event=="Add component" and len(values["-lb_1-"]):
        for i in values["-lb_1-"]:
            if i in component_list and list_type=="components":
                materials.append(i)
            elif i in recipe_keys and list_type=="recipes":
                for j in recipes[i.lower()].components:
                    materials.append(j)
            elif i in component_list and list_type=="pocket":
                materials.append(i)
                pocket[pocket_name].remove(i)
                window["-lb_1-"].update(pocket[pocket_name])
        # Updates listbox 2
        window["-lb_2-"].update(materials)

    elif event == "Add to pocket" and len(values["-lb_1-"]) and list_type=="components":
        if pocket_name != "None":
            for i in values["-lb_1-"]:
                pocket[pocket_name].append(i)
                pocket[pocket_name].sort()
                secret_pocket[pocket_name].append(i)
                secret_pocket[pocket_name].sort()

    elif event == "Delete pocket":
        try:
            delet_name=popup_select("Which pocket should be deleted?", list(pocket.keys()))
            actual_delete=sg.popup_yes_no("Are you sure you want to delete "+delet_name+"'s pocket?")
            if actual_delete=="Yes":
                if pocket_name==delet_name:
                    pocket_name="None"
                    window["-lb_1-"].update([""])
                    window["-pocket-"].update(pocket_name)
                pocket.pop(delet_name)
                secret_pocket.pop(delet_name)
        except:
            pass

    # Clears listbox 2 to refresh component selection
    elif event == "Clear list":
        materials=[]
        window["-lb_2-"].update(materials)

    elif event=="Remove component" and len(values["-lb_2-"]):
        materials.remove(values["-lb_2-"][0])
        window["-lb_2-"].update(materials)

    elif event=="Remove component" and list_type=="pocket" and len(values["-lb_1-"]):
        pocket[pocket_name].remove(values["-lb_1-"][0])
        secret_pocket[pocket_name].remove(values["-lb_1-"][0])
        window["-lb_1-"].update(pocket[pocket_name])

    elif event=="Subclasses":
        list_type="subclass"
        window["-lb_1-"].update(sub_names)

# This code will pull the descriptions of compone, item types, or recipes selected in the box
    elif event=="-lb_1-":
        selected_name=values["-lb_1-"][0].lower()

        if selected_name in components and (list_type=="components" or list_type=="pocket"):
            desc_name=components[selected_name].name
            desc_desc=components[selected_name].description
            desc_types=components[selected_name].types
            description=desc_name+"\n\n"+desc_desc
            if len(components[selected_name].effects) > 0:
                description=description+"\n\nTypes:"
                for i in desc_types:
                    description+="\n   -"+i+": "+components[selected_name].effects[i]

            description=roll_desc(description, True)

            window["-item_description_2-"].update(description)
            if selected_name+".png" in images_list:
                window["-item_image-"].update("resources/images/"+selected_name+".png")
            else:
                window["-item_image-"].update("resources/images/general_component.png")

        elif list_type=="subclass" and selected_name.capitalize() in subclass_types:
            description=subclass_types[selected_name.capitalize()]
            window["-item_description_2-"].update(description)
            if selected_name+".png" in images_list:
                window["-item_image-"].update("resources/images/"+selected_name+".png")
            else:
                window["-item_image-"].update("resources/images/general_component.png")

        elif selected_name in types and list_type=="types":
            desc_name=types[selected_name].name
            desc_desc=types[selected_name].description
            desc_requirements=types[selected_name].requirements
            description=desc_name+"\n\n"+desc_desc+"\n\nSpecific requirements:"
            if len(desc_requirements)>0:
                for i in desc_requirements:
                    description+="\n   -"+i
            else:
                description+="\n   -None"

            description=roll_desc(description, True)
            window["-item_description_2-"].update(description)
            if selected_name+".png" in images_list:
                window["-item_image-"].update("resources/images/"+selected_name+".png")
            else:
                window["-item_image-"].update("resources/images/success.png")


        elif selected_name in recipes and list_type=="recipes":
            desc_name=recipes[selected_name].name
            desc_desc=recipes[selected_name].description
            desc_components=recipes[selected_name].components
            desc_types=recipes[selected_name].types

            description=desc_name+"\nType: "+desc_types+"\n\n"+desc_desc+"\n\nRequired components:"
            description=roll_desc(description, True)
            for i in desc_components:
                description+="\n   -"+i
            window["-item_description_2-"].update(description)
            if selected_name+".png" in images_list:
                window["-item_image-"].update("resources/images/"+selected_name+".png")
            elif desc_types.lower()+".png" in images_list:
                window["-item_image-"].update("resources/images/"+desc_types.lower()+".png")
            else:
                window["-item_image-"].update("resources/images/success.png")

    elif event=="Shop":
        total_components=len(components)
        inventory_number=sg.popup_get_text("How many items would you like? ("+str(total_components)+" available, 5-10 as default.)")
        try:
            inventory_number=int(inventory_number)
        except:
            inventory_number=rand.randint(5, 10)
        inventory=[]
        inv_names=[]
        while len(inventory)<inventory_number:
            hit=rand.randint(0,len(components)-1)
            if component_list[hit] not in inv_names:
                inv_names.append(component_list[hit])
                inv_desc=components[component_list[hit].lower()].description
                if "VALUE" in inv_desc:
                    inv_desc=inv_desc.split("VALUE")
                    values=inv_desc[1].split("-")
                    if len(values)<2:
                        values=values[0]
                        try:
                            values=str(int(values))+" GP"
                        except:
                            values=str(values)
                    else:
                        values=rand.randint(int(values[0]), int(values[1]))
                        values=str(values)+" GP"
                else:
                    values=rand.randint(1,20)
                    values=str(values)+" GP"
                inventory.append(component_list[hit]+" - "+values)
        popup_shop("Welcome to the shop! Here's what we have in stock:",inventory)


    elif event=="Forage":
        try:
            terrain_type=popup_select("What terrain will you be foraging in?", list(terrains.keys()))
#            print(terrain_type)
            if len(terrains[terrain_type])>0:
                time_spent=popup_select("How long will you be foraging", ["1 minute", "10 minutes", "1 hour"])
#                print(time_spent)
                try:
                    prof=int(values["-prof-"])
                except:
                    prof=0
                extra_found=0
                if values["-subclass_for-"]==True:
                    prof+=2
                    extra_found+=1
                forage_roll=rand.randint(0,21)+prof
#                print(forage_roll)
                if time_spent=="1 minute":
#                    print("1 min")
                    if forage_roll < 6:
                        forage_found=0+extra_found
                    elif forage_roll > 5 and forage_roll < 11:
                        forage_found=rand.randint(0,2)+extra_found
                    elif forage_roll < 16 and forage_roll > 10:
                        forage_found=rand.randint(0,3)+extra_found
                    elif forage_roll < 20 and forage_roll > 15:
                        forage_found=rand.randint(1,4)+extra_found
                    elif forage_roll > 20:
                        forage_found=rand.randint(2,5)+extra_found
                elif time_spent=="10 minutes":
#                    print("10 min")
                    if forage_roll < 6:
                        forage_found=rand.randint(0,2)+extra_found
                    elif forage_roll > 5 and forage_roll < 11:
                        forage_found=rand.randint(0,3)+extra_found
                    elif forage_roll < 16 and forage_roll > 10:
                        forage_found=rand.randint(1,4)+extra_found
                    elif forage_roll < 20 and forage_roll > 15:
                        forage_found=rand.randint(2,5)+extra_found
                    elif forage_roll > 20:
                        forage_found=rand.randint(3,6)+extra_found
                elif time_spent=="1 hour":
#                    print("1 hour")
                    if forage_roll < 6:
                        forage_found=rand.randint(0,3)+extra_found
                    elif forage_roll > 5 and forage_roll < 11:
                        forage_found=rand.randint(1,4)+extra_found
                    elif forage_roll < 16 and forage_roll > 10:
                        forage_found=rand.randint(2,5)+extra_found
                    elif forage_roll < 20 and forage_roll > 15:
                        forage_found=rand.randint(3,6)+extra_found
                    elif forage_roll > 20:
                        forage_found=rand.randint(4,7)+extra_found

                if forage_found==0:
                    sg.Popup("You found nothing while searching.")
                else:
                    forage_pool=[]
                    trick=0
                    if values["-subclass_for-"]==True:
                        trick+=1
                        nonnative=component_list[rand.randint(0, len(components)-1)]
                        while "-" not in components[nonnative.lower()].description.split("VALUE")[1]:
                            nonnative=component_list[rand.randint(0, len(components)-1)]
                        forage_pool.append(nonnative)
                    while trick < forage_found:
                        forage_pool.append(terrains[terrain_type][rand.randint(0,len(terrains[terrain_type])-1)])
                        trick+=1
                    popup_shop("You found the following components while searching.", forage_pool, True)
            else:
                sg.Popup("No components can be found in "+terrain_type+" terrain. Sorry.")

        except:
            pass

    # Here's where the crafting/procerdual generating starts!
    elif event=="Craft!":

        if len(pocket)>1 and pocket_name != "None":
            secret_pocket[pocket_name]=list(pocket[pocket_name])

        # First, we determine what the user's crafting proficiency is.
        # If left blank, we assume 0
        if isinstance(values["-prof-"], str):
            try:
                prof_bonus=int(values["-prof-"])
            except:
                prof_bonus=0
        else:
            prof_bonus=0

        can_run=True
        # So long as more than one material is entered, artificing begins
        if len(materials)>1:
            # we sort the materials to see if they'll match recipes later
            materials.sort()
            # make an initial and total type pool
#            print(materials)
            type_pool_1=[]
            type_pool_2=[]
            comp_count=0
            for i in materials:
                type_pool_1=components[i.lower()].types
                for j in type_pool_1:
                    type_pool_2.append(j)
                for j in components[i.lower()].types:
                    if j not in modifiers:
                        comp_count+=1
                        break

            min_set=list(set(type_pool_2))
#            print(min_set)
            type_pool=[]
#            print(comp_count)
            for i in min_set:
#                print(i)
                mat_count=0
                for j in type_pool_2:
                    if i == j:
                        mat_count+=1
                if mat_count==comp_count or i in modifiers:
                    type_pool.append(i)
#                print(mat_count)
            # We'll save a redundant list for magic later
            reduntant_type_pool=type_pool_2
            # and we take the unique list of shared types and modifiers
            type_pool=list(set(type_pool))
            small_type_pool=[]
            for i in type_pool:
                if i not in modifiers:
                    small_type_pool.append(i)

            if "Amplifier" in type_pool:
                amp_it=True
            else:
                amp_it=False
#            print(type_pool)
#            print(small_type_pool)

            # If the materials share no common types, and don't make a recipe, failure happens
            if len(type_pool)==0 and materials not in recipe_values:
                description="Nothing was produced..."
                window["-item_description_2-"].update(description)
                window["-item_image-"].update("resources/images/failure.png")

            # If the components can make a recipe and nothing else, the recipe is made
            elif materials in recipe_values and len(small_type_pool) < 2:

                recipe_index=recipe_values.index(materials)
                selected_name=recipe_keys[recipe_index].lower()
                desc_name=recipes[selected_name].name
                desc_desc=recipes[selected_name].description
                desc_components=recipes[selected_name].components
                desc_types=recipes[selected_name].types
                if desc_types == small_type_pool[0]:

                    # If perfectionist is the subclass, user is given the chance to
                    # reroll the description with a bonus 1d4 to proficiency
                    if values["-subclass_perf-"]==True:
                        reroll_desc=sg.popup_yes_no("You are perfectionist, who already knows this recipe. Would you like to attempt to improve the recipe?")
                        if reroll_desc=="Yes":
                            desc_desc=types[desc_types.lower()].description

                            # if the user is a holistic crafter, then a random component effect is added
                            picked_material=""
                            if values["-subclass_holistic-"]==True:
                                random_material=materials[rand.randint(0,len(materials)-1)]
                                picked_material=random_material
                                poss_effects=components[random_material.lower()].effects
                                while desc_name not in poss_effects:
                                    random_material=materials[rand.randint(0,len(materials)-1)]
                                    poss_effects=components[random_material.lower()].effects
                                desc_desc+="\n   -"+poss_effects[desc_types]

                            # If the item is a potion, a random component effect is added

                            if desc_name in types_w_effects:
                                mat_count=0
                                random_material=materials[rand.randint(0,len(materials)-1)]
                                poss_effects=components[random_material.lower()].effects
                                while mat_count<len(materials):
                                    if random_material==picked_material:
                                        random_material=materials[rand.randint(0,len(materials)-1)]
                                    elif len(components[random_material.lower()].types)<2 and components[random_material.lower()].types in modifiers:
                                        random_material=materials[rand.randint(0,len(materials)-1)]
                                    else:
                                        poss_effects=components[random_material.lower()].effects
                                        desc_desc+="\n   -"+poss_effects[desc_types]
                                        break
                                    mat_count+=1

                            desc_desc=roll_desc(types[desc_types.lower()].description, False ,prof_bonus, values["-subclass_damage-"], 0, values["-subclass_duration-"], 0, values["-subclass_duration-"], 0, amp_it)
                            recipes[selected_name].description=desc_desc
                            write_file="Name: "+desc_name+"\nTypes: "+desc_types+"\nComponents: "
                            for i in materials:
                                write_file+=i+", "
                            write_file=write_file[0:len(write_file)-2]
                            write_file+="\nDescription: "+desc_desc
                            file_in=open("resources/recipes/"+selected_name+".recipe", "w")
                            file_in.write(write_file)
                            file_in.close()

                    description=desc_name+"\nType: "+desc_types+"\n\n"+desc_desc+"\n\nRequired components:"
                    for i in desc_components:
                        description+="\n   -"+i
                    window["-item_description_2-"].update(description)
                    if selected_name+".png" in images_list:
                        window["-item_image-"].update("resources/images/"+selected_name+".png")
                    elif "resources/images/"+desc_types.lower()+".png" in images_list:
                        window["-item_image-"].update("resources/images/"+desc_types.lower()+".png")
                    else:
                        window["-item_image-"].update("resources/images/success.png")

                    for bkf in backfire_type:
                        if bkf in reduntant_type_pool:
                            for vol in reduntant_type_pool:
                                if vol=="Stabilizer" and bkf in reduntant_type_pool:
                                    reduntant_type_pool.remove(bkf)
                                    reduntant_type_pool.remove("Stabilizer")
                    for bkf in backfire_type:
                        if bkf in reduntant_type_pool and values["-subclass_care-"] == False:
                            backfire=reduntant_type_pool[rand.randint(0,len(reduntant_type_pool)-1)]
                            if backfire in backfire_type:
                                sg.Popup("Something went wrong! Your contraption activates immediately originating at your position.")
                            else:
                                sg.Popup("Your "+desc_types.lower()+" was successfully created with no issues!")
                            break
                        else:
                            if bkf==backfire_type[len(backfire_type)-1]:
                                sg.Popup("Your "+desc_types.lower()+" was successfully created with no issues!")
                else:
                    description="Nothing was produced..."
                    window["-item_description_2-"].update(description)
                    window["-item_image-"].update("resources/images/failure.png")

            # If the components all share types, they make a random, shared type
            else:
                # First, lets make sure that modiers aren't the only thing in the type pool
                good=False
                for i in small_type_pool:
                    if i not in modifiers:
                        good=True
                # If there's at least one other type then...
                if good == True:
                    # First we'll see if a recipe exists for this combination
                    if materials in recipe_values:
                        matching_recipe_type=[]
                        matching_recipe_names=[]
                        count=0
                        # First, lets pull all the recipes that ARE known
                        for i in recipe_values:
                            if i == materials:
                                matching_recipe_type.append(recipes[recipe_keys[count].lower()].types)
                                matching_recipe_names.append(recipes[recipe_keys[count].lower()].name)
                            count+=1
                        # Then lets see if there are missing, potential recipes
                        for i in small_type_pool:
                            if i not in matching_recipe_type:
                                matching_recipe_names.append("Tinker")

                        matching_recipe_name=list(set(matching_recipe_names))

                        if "Tinker" in matching_recipe_names:
                            choice=popup_select("This combination may generate a known recipe or you could tinker with it and try to make something new. What would you like to do?", matching_recipe_names)
                        elif len(matching_recipe_names) > 1:
                            choice=popup_select("This combination may generates multiple recipes. Which would you like to create?", matching_recipe_names)
                        else:
                            choice=matching_recipe_names[0]
                        if choice != "Tinker":
                            selected_name=choice.lower()
                            desc_name=recipes[selected_name].name
                            desc_desc=recipes[selected_name].description
                            desc_components=recipes[selected_name].components
                            desc_types=recipes[selected_name].types

                            # If perfectionist is the subclass, user is given the chance to
                            # reroll the description with a bonus 1d4 to proficiency
                            if values["-subclass_perf-"]==True:
                                reroll_desc=sg.popup_yes_no("You are perfectionist, who already knows this recipe. Would you like to attempt to improve the recipe?")
                                if reroll_desc=="Yes":
                                    desc_desc=types[desc_types.lower()].description

                                    # if the user is a holistic crafter, then a random component effect is added
                                    picked_material=""
                                    if values["-subclass_holistic-"]==True:
                                        random_material=materials[rand.randint(0,len(materials)-1)]
                                        picked_material=random_material
                                        poss_effects=components[random_material.lower()].effects
                                        while desc_name not in poss_effects:
                                            random_material=materials[rand.randint(0,len(materials)-1)]
                                            poss_effects=components[random_material.lower()].effects
                                        desc_desc+="\n   -"+poss_effects[desc_types]

                                    # If the item is a potion, a random component effect is added
                                    if desc_types in types_w_effects:
                                        mat_count=0
                                        random_material=materials[rand.randint(0,len(materials)-1)]
                                        poss_effects=components[random_material.lower()].effects
                                        while mat_count<len(materials):
                                            random_material=materials[rand.randint(0,len(materials)-1)]
                                            if random_material==picked_material:
                                                random_material=materials[rand.randint(0,len(materials)-1)]
                                            elif len(components[random_material.lower()].types)<2 and components[random_material.lower()].types[0] in modifiers:
                                                random_material=materials[rand.randint(0,len(materials)-1)]
                                            else:
                                                poss_effects=components[random_material.lower()].effects
                                                desc_desc+="\n   -"+poss_effects[desc_types]
                                                break
                                            mat_count+=1


                                    desc_desc=roll_desc(desc_desc, False, prof_bonus, values["-subclass_damage-"], 0, values["-subclass_duration-"], 0, values["-subclass_duration-"], 0, amp_it)
                                    recipes[selected_name].description=desc_desc
                                    write_file="Name: "+desc_name+"\nTypes: "+desc_types+"\nComponents: "
                                    for i in materials:
                                        write_file+=i+", "
                                    write_file=write_file[0:len(write_file)-2]
                                    write_file+="\nDescription: "+desc_desc
                                    file_in=open("resources/recipes/"+selected_name+".recipe", "w")
                                    file_in.write(write_file)
                                    file_in.close()
                                    description=desc_name+"\nType: "+desc_types+"\n\n"+desc_desc+"\n\nRequired components:"
                                    for i in desc_components:
                                        description+="\n   -"+i

                            else:
                                description=desc_name+"\nType: "+desc_types+"\n\n"+desc_desc+"\n\nRequired components:"
                                for i in desc_components:
                                    description+="\n   -"+i

                            window["-item_description_2-"].update(description)
                            if selected_name+".png" in images_list:
                                window["-item_image-"].update("resources/images/"+selected_name+".png")
                            elif "resources/images/"+desc_types.lower()+".png" in images_list:
                                window["-item_image-"].update("resources/images/"+desc_types.lower()+".png")
                            else:
                                window["-item_image-"].update("resources/images/success.png")
                                for bkf in backfire_type:
                                    if bkf in reduntant_type_pool:
                                        for vol in reduntant_type_pool:
                                            if vol=="Stabilizer" and bkf in reduntant_type_pool:
                                                reduntant_type_pool.remove(bkf)
                                                reduntant_type_pool.remove("Stabilizer")
                                for bkf in backfire_type:
#                                   print(reduntant_type_pool)
                                    if bkf in reduntant_type_pool and values["-subclass_care-"] == False:
                                        backfire=reduntant_type_pool[rand.randint(0,len(reduntant_type_pool)-1)]
#                                    print(backfire)
                                    if backfire in backfire_type:
                                        sg.Popup("Something went wrong! Your contraption activates immediately originating at your position.")
                                    else:
                                        sg.Popup("Your "+desc_types.lower()+" was successfully created with no issues!")
                                    break
                                else:
                                    if bkf==backfire_type[len(backfire_type)-1]:
                                        sg.Popup("Your "+desc_types.lower()+" was successfully created with no issues!")

                        # If the user decides to tinker, then a different type is explored
                        elif choice=="Tinker":
                            for known_type in matching_recipe_type:
                                if known_type in small_type_pool:
                                    small_type_pool.remove(known_type)

                            if len(small_type_pool) > 1:
                                selected_name=small_type_pool[rand.randint(1,len(small_type_pool))-1].lower()
                            else:
                                selected_name=small_type_pool[0].lower()
                            desc_name=types[selected_name].name
                            desc_desc=types[selected_name].description
                            desc_requirements=types[selected_name].requirements
                            for rq in desc_requirements:
#                                print("Requirement found for "+desc_name+": "+rq)
                                if rq not in type_pool and rq != "None" and values["-subclass_versa-"]!=True:
                                    description="Despite there being other kinds of objects, nothing was produced..."
                                    window["-item_description_2-"].update(description)
                                    window["-item_image-"].update("resources/images/failure.png")
                                    can_run=False

                            if can_run:
                                # if the user is a holistic crafter, then a random component effect is added
                                picked_material=""
                                if values["-subclass_holistic-"]==True:
                                    random_material=materials[rand.randint(0,len(materials)-1)]
                                    picked_material=random_material
                                    poss_effects=components[random_material.lower()].effects
                                    while desc_name not in poss_effects:
                                        random_material=materials[rand.randint(0,len(materials)-1)]
                                        poss_effects=components[random_material.lower()].effects
                                    desc_desc+="\n   -"+poss_effects[desc_name]

                                # If the item is a potion, a random component effect is added
                                if desc_name in types_w_effects:
                                    mat_count=0
                                    random_material=materials[rand.randint(0,len(materials)-1)]
                                    while mat_count<len(materials):
                                        if random_material==picked_material:
                                            random_material=materials[rand.randint(0,len(materials)-1)]
                                        elif len(components[random_material.lower()].types)<2 and components[random_material.lower()].types[0] in modifiers:
                                            random_material=materials[rand.randint(0,len(materials)-1)]
                                        else:
                                            poss_effects=components[random_material.lower()].effects
                                            desc_desc+="\n   -"+poss_effects[desc_name]
                                            break
                                        mat_count+=1


                                desc_desc=roll_desc(desc_desc, False, prof_bonus, values["-subclass_damage-"], 0, values["-subclass_duration-"], 0, values["-subclass_duration-"], 0, amp_it)

                                description="New "+desc_name.lower()+"\n\n"+desc_desc+"\n\nRequired components:"
                                for i in materials:
                                    description+="\n   -"+i

                                window["-item_description_2-"].update(description)
                                if selected_name+".png" in images_list:
                                    window["-item_image-"].update("resources/images/"+selected_name+".png")
                                elif "resources/images/"+types[selected_name].name.lower()+".png" in images_list:
                                    window["-item_image-"].update("resources/images/"+types[selected_name].name.lower()+".png")
                                else:
                                    window["-item_image-"].update("resources/images/success.png")
                                new_name=sg.popup_get_text("New recipe discovered! What should it be name?")
                                if isinstance(new_name, str):
                                    new_recipe=Recipe(
                                    new_name,
                                    desc_desc,
                                    materials,
                                    types[selected_name].name
                                    )

                                    write_file="Name: "+new_name+"\nTypes: "+types[selected_name].name+"\nComponents: "
                                    for i in materials:
                                        write_file+=i+", "
                                    write_file=write_file[0:len(write_file)-2]
                                    write_file+="\nDescription: "+desc_desc

                                    file_in=open("resources/recipes/"+new_name.lower()+".recipe", "w")
                                    file_in.write(write_file)
                                    file_in.close()

                                    recipes[new_name.lower()]=new_recipe
                                    recipe_keys=[]
                                    recipe_values=[]
                                    for i in recipes:
                                        recipe_.append(recipes[i].name)
                                        hit_value=recipes[i].components
                                        hit_value.sort()
                                        recipe_values.append(hit_value)

                                    known_recipes=recipe_keys

                                    for bkf in backfire_type:
                                        if bkf in reduntant_type_pool:
                                            for vol in reduntant_type_pool:
                                                if vol=="Stabilizer" and bkf in reduntant_type_pool:
                                                    reduntant_type_pool.remove(bkf)
                                                    reduntant_type_pool.remove("Stabilizer")
                                    for bkf in backfire_type:
                                        if bkf in reduntant_type_pool and values["-subclass_care-"] == False:
                                            backfire=reduntant_type_pool[rand.randint(0,len(reduntant_type_pool)-1)]
                                            if backfire in backfire_type:
                                                sg.Popup("Something went wrong! Your contraption activates immediately originating at your position.")
                                            else:
                                                sg.Popup("Your "+types[selected_name].name.lower()+" was successfully created with no issues!")
                                            break
                                        else:
                                            if bkf==backfire_type[len(backfire_type)-1]:
                                                sg.Popup("Your "+types[selected_name].name.lower()+" was successfully created with no issues!")


                    # If the materials are not part of known recipe, then we'll look for new ones!
                    else:
                        if len(small_type_pool) > 1:
                            selected_name=small_type_pool[rand.randint(0,len(small_type_pool))-1].lower()
                        else:
                            selected_name=small_type_pool[0].lower()
                        desc_name=types[selected_name].name
                        desc_desc=types[selected_name].description
                        desc_requirements=types[selected_name].requirements
                        for rq in desc_requirements:
#                            print("Requirement found for "+desc_name+": "+rq)
                            if rq not in type_pool and rq != "None" and values["-subclass_versa-"]!=True:
                                description="Nothing was produced...But it was close"
                                window["-item_description_2-"].update(description)
                                window["-item_image-"].update("resources/images/failure.png")
                                can_run=False
                        if can_run:
                            # if the user is a holistic crafter, then a random component effect is added
                            picked_material=""
                            if values["-subclass_holistic-"]==True:
                                random_material=materials[rand.randint(0,len(materials)-1)]
                                poss_effects=components[random_material.lower()].effects
                                while desc_name not in poss_effects:
                                    random_material=materials[rand.randint(0,len(materials)-1)]
                                    picked_material=random_material
                                    poss_effects=components[random_material.lower()].effects
                                desc_desc+="\n   -"+poss_effects[desc_name]

                            # If the item is a potion, a random component effect is added
                            if desc_name in types_w_effects:
                                mat_count=0
                                random_material=materials[rand.randint(0,len(materials)-1)]
                                poss_effects=components[random_material.lower()].effects
                                while mat_count<len(materials):
                                    if random_material == picked_material:
                                        random_material=materials[rand.randint(0,len(materials)-1)]
                                    elif len(components[random_material.lower()].types)<2 and components[random_material.lower()].types[0] in modifiers:
                                        random_material=materials[rand.randint(0,len(materials)-1)]
                                    else:
                                        poss_effects=components[random_material.lower()].effects
                                        desc_desc+="\n   -"+poss_effects[desc_name]
                                        break
                                    mat_count+=1


                            desc_desc=roll_desc(desc_desc, False, prof_bonus, values["-subclass_damage-"], 0, values["-subclass_duration-"], 0, values["-subclass_duration-"], 0, amp_it)

                            description="New "+desc_name.lower()+"\n\n"+desc_desc+"\n\nSpecific requirements:"
                            desc_requirements=list(set(desc_requirements))
                            if len(desc_requirements)>0:
                                for i in desc_requirements:
                                    description+="\n   -"+i
                            else:
                                description+="\n   -None"
                            window["-item_description_2-"].update(description)
                            if selected_name+".png" in images_list:
                                window["-item_image-"].update("resources/images/"+selected_name+".png")
                            elif "resources/images/"+desc_name.lower()+".png" in images_list:
                                window["-item_image-"].update("resources/images/"+desc_name.lower()+".png")
                            else:
                                window["-item_image-"].update("resources/images/success.png")
                            new_name=sg.popup_get_text("New recipe discovered! What should it be name?")
                            if isinstance(new_name, str):
                                new_recipe=Recipe(
                                new_name,
                                desc_desc,
                                materials,
                                types[selected_name].name
                                )

                                write_file="Name: "+new_name+"\nTypes: "+types[selected_name].name+"\nComponents: "
                                for i in materials:
                                    write_file+=i+", "
                                write_file=write_file[0:len(write_file)-2]
                                write_file+="\nDescription: "+desc_desc
                                file_in=open("resources/recipes/"+new_name.lower()+".recipe", "w")
                                file_in.write(write_file)
                                file_in.close()

                                recipes[new_name.lower()]=new_recipe
                                recipe_keys=[]
                                recipe_values=[]
                                for i in recipes:
                                    recipe_keys.append(recipes[i].name)
                                    hit_value=recipes[i].components
                                    hit_value.sort()
                                    recipe_values.append(hit_value)

                                known_recipes=recipe_keys

                                for bkf in backfire_type:
                                    if bkf in reduntant_type_pool:
                                        for vol in reduntant_type_pool:
                                            if vol=="Stabilizer" and bkf in reduntant_type_pool:
                                                reduntant_type_pool.remove(bkf)
                                                reduntant_type_pool.remove("Stabilizer")
                                for bkf in backfire_type:
                                    if bkf in reduntant_type_pool and values["-subclass_care-"] == False:
                                        backfire=reduntant_type_pool[rand.randint(0,len(reduntant_type_pool)-1)]
                                        if backfire in backfire_type:
                                            sg.Popup("Something went wrong! Your contraption activates immediately originating at your position.")
                                        else:
                                            sg.Popup("Your "+types[selected_name].name.lower()+" was successfully created with no issues!")
                                        break
                                    else:
                                        if bkf==backfire_type[len(backfire_type)-1]:
                                            sg.Popup("Your "+types[selected_name].name.lower()+" was successfully created with no issues!")


                else:
                    description="Nothing was produced..."
                    window["-item_description_2-"].update(description)
                    window["-item_image-"].update("resources/images/failure.png")

            materials=[]
            window["-lb_2-"].update(materials)
        # if less than two materials are used, nothing is produced
        else:
            description="Insufficient materials used"
            window["-item_description_2-"].update(description)
            window["-item_image-"].update("resources/images/none.png")


window.close()
pocket=secret_pocket

all_files=""
file_names=os.listdir("resources/components/")
for i in file_names:
    if i.endswith(".component"):
        compo=open("resources/components/"+i, "r")
        loaded_comp=compo.read()
        compo.close()

        loaded_comp=loaded_comp.split("\n")
        for i in loaded_comp:
            if i == loaded_comp[0]:
                all_files+="**"+i+"**\n"
            elif i == loaded_comp[len(loaded_comp)-1]:
                all_files+=i+"\n\n\n"
            else:
                all_files+=i+"\n"

compo=open("components.txt", "w")
compo.write(all_files)
compo.close()

#all_files=""
#file_names=os.listdir("resources/types/")
#for i in file_names:#
#    if i.endswith(".type"):
#        compo=open("resources/types/"+i, "r")
#        loaded_comp=compo.read()
#        compo.close()
#
#        loaded_comp=loaded_comp.split("\n")
#        for i in loaded_comp:
#            if i == loaded_comp[0]:
#                all_files+="**"+i+"**\n"
#            elif i == loaded_comp[len(loaded_comp)-1]:
#                all_files+=i+"\n\n\n"
#            else:
#                all_files+=i+"\n"

#compo=open("types.txt", "w")
#compo.write(all_files)
#compo.close()

#all_files=""
#file_names=os.listdir("resources/recipes/")
#for i in file_names:
#    if i.endswith(".recipe"):
#        compo=open("resources/recipes/"+i, "r")
#        loaded_comp=compo.read()
#        compo.close()
#
#        loaded_comp=loaded_comp.split("\n")
#        for i in loaded_comp:
#                all_files+="**"+i+"**\n"
#            elif i == loaded_comp[len(loaded_comp)-1]:
#                all_files+=i+"\n\n\n"
#            else:
#                all_files+=i+"\n"

#compo=open("recipes.txt", "w")
#compo.write(all_files)
#compo.close()

if pocket_name=="None" and len(pocket)>=1:
    pocket_name=list(pocket.keys())[0]
if len(pocket)>0:
    pocket_start=""
    pocket_start+="-\n"+pocket_name+"\n"
    for i in pocket[pocket_name]:
        pocket_start+=i+"\n"
    if len(pocket)>1:
        for i in pocket:
            if i != "None":
                pocket_start+="-\n"+i+"\n"
                for j in pocket[i]:
                    pocket_start+=j+"\n"
    pocket_start+="-"
    pocket_file=open(".pockets", "w")
    pocket_file.write(pocket_start)
    pocket_file.close()
else:
    if ".pockets" in os.listdir():
        os.remove(".pockets")
