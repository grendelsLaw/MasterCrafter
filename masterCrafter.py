#!/usr/bin/env python

# Artificing made GUI

# Import required packages
import PySimpleGUI as sg
import os.path
import random as rand

sg.theme("LightGrey1")

#-------------------------------------------------------------------------------

def roll_desc(first_desc,
proficiency_boost=0,
damage_boost=False,
damage_boost_number=0,
time_boost=False,
time_boost_number=0,
distance_boost=False,
distance_boost_number=0):
    new_desc=first_desc
    if "DAMAGE" in new_desc:
        new_desc=new_desc.split("DAMAGE")
        ticker=1
        desc=""
        for i in new_desc:
            if ticker%2==0:
                spot=i.split("-")
                low_number=int(spot[0])
                high_number=int(spot[1])
                theNumber=int(rand.randint(low_number, high_number)*((rand.randint(1, 21)+proficiency_boost+damage_boost_number))/20)
                if damage_boost!=True:
                    theNumber=low_number
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
                high_number=int(spot[1])
                theNumber=int(rand.randint(low_number, high_number)*((rand.randint(1, 21)+proficiency_boost+time_boost_number))/20)
                if time_boost!=True:
                    theNumber=low_number
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
                high_number=int(spot[1])
                theNumber=5*(int(rand.randint(low_number, high_number)*((rand.randint(1, 21)+proficiency_boost+distance_boost_number))/20)//5)
                if distance_boost!=True:
                    theNumber=low_number
                desc+=str(theNumber)
            else:
                desc+=i
            ticker+=1
        new_desc=desc
    return new_desc

# Makes the popups
def popup_select(text_choice, the_list,select_multiple=False):
    layout = [[sg.Text(text_choice)],
    [sg.Listbox(the_list,key='_LIST_',size=(45,len(the_list)),select_mode='extended' if select_multiple else 'single',bind_return_key=True),sg.OK()]]
    window = sg.Window('Select One',layout=layout)
    event, values = window.read()
    window.close()
    del window
    if len(values['_LIST_']):
        return values['_LIST_'][0]
    else:
        return the_list[0]


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
# Define default values
# A list of the components
materials=[]
secret_materials=[]
known_recipes=[]

# A description of the artificed item
description="Submit components to artifice a new item."

# default list type
list_type="components"

# Modifier tags
modifiers=["Volatile", "Amplifier", "Stabillizer"]

# types that get effects by default
types_w_effects=["Potion", "Gas"]

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
                new_comp=Component(
                name_i,
                loaded_i[1].split("Description:")[1].strip(),
                loaded_i[2].split("Types:")[1].strip().split(", "),
                {}
                )
                for j in loaded_i[3:len(loaded_i)]:
                    effect_type=j.split(":")[0].rstrip()
                    effect_effect=j.split(":")[1].rstrip()
                    new_comp.effects[effect_type]=j.split(":")[1]
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
                # Set the first lsit value to be the description of the recipe
                new_recipe=Recipe(
                name_i,
                loaded_recipe[3:len(loaded_recipe)],
                loaded_recipe[2].split("Components:")[1].strip().split(", "),
                loaded_recipe[1].split("Types:")[1].strip()
                )
                thingo=""
                for desc_effect in new_recipe.description:
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
                new_type=Type(
                name_i,
                loaded_i[1].split("Description:")[1].strip(),
                [loaded_i[2].split("Requirements:")[1].strip()],
                )
                types[name_i.lower()]=new_type
        except:
            print("unable to parse file: "+i)

type_list=[]
for i in types:
    type_list.append(types[i].name)

#-------------------------------------------------------------------------------
# Generate the columns
# First column is the search box and buttons to toggle between components, recipes, and types
material_entry_column = [
    sg.Button("Search"),
    sg.In(size=(10, 2), key="-search_key-"),
    sg.Button("Components"),
    sg.Button("Types"),
    sg.Button("Known recipes")
]
# Second column has the first listbox, which you can select items to check characteristics,
# and the second listbox, which shows you list items you've selected, as well as the artifice button
all_submitted_column = [
    sg.Listbox(values=component_list, enable_events=True, size = (40,10), key="-lb_1-"),
    sg.Button("Submit"),
    sg.Button("Clear list"),
    sg.Listbox(values=materials, size = (40,10), key="-lb_2-"),
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
    sg.Radio("Damage specialist", "subclass", default=False, key = "-subclass_damage-"),
    sg.Radio("Duration specialist", "subclass", default=False, key = "-subclass_duration-"),
    sg.Radio("Holistic crafter", "subclass", default=False, key = "-subclass_holistic-"),
    sg.Radio("Versatile crafter", "subclass", default=False, key = "-subclass_versa-"),
    sg.Radio("Careful crafter", "subclass", default=False, key = "-subclass_care-"),
    sg.Radio("Perfectionist", "subclass", default=False, key = "-subclass_perf-")
]

# Now all four columns get placed into a singlular layout, which gets called
layout=[
    material_entry_column,
    subclass_buttons,
    all_submitted_column,
    [sg.Text("Added proficiency score:"),
    sg.In(size=(15,1), key="-prof-"),
    sg.Button("Artifice!"),],
    item_description,
]
window=sg.Window("Artificing made easy!", layout)

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

    # Adds selected components or selected recipes components to listbox 2 for artificing
    elif event=="Submit" and len(values["-lb_1-"]):
        for i in values["-lb_1-"]:
            if i in component_list and list_type=="components":
                materials.append(i)
                secret_materials.append(i)
            elif i in recipe_keys and list_type=="recipes":
                materials=recipes[i.lower()].components
        # Updates listbox 2
        window["-lb_2-"].update(materials)

    # Clears listbox 2 to refresh component selection
    elif event == "Clear list":
        materials=[]
        secret_materials=[]
        window["-lb_2-"].update(materials)

# This code will pull the descriptions of compone, item types, or recipes selected in the box
    elif event=="-lb_1-":
        selected_name=values["-lb_1-"][0].lower()

        if selected_name in components and list_type=="components":
            desc_name=components[selected_name].name
            desc_desc=components[selected_name].description
            desc_types=components[selected_name].types
            description=desc_name+"\n\n"+desc_desc
            if len(components[selected_name].effects) > 0:
                description=description+"\n\nTypes:"
                for i in desc_types:
                    description+="\n   -"+i+": "+components[selected_name].effects[i]

            window["-item_description_2-"].update(description)
            if selected_name+".png" in images_list:
                window["-item_image-"].update("resources/images/"+selected_name+".png")
            else:
                window["-item_image-"].update("resources/images/success.png")

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
            for i in desc_components:
                description+="\n   -"+i
            window["-item_description_2-"].update(description)
            if selected_name+".png" in images_list:
                window["-item_image-"].update("resources/images/"+selected_name+".png")
            else:
                window["-item_image-"].update("resources/images/success.png")

    # Here's where the crafting/procerdual generating starts!
    elif event=="Artifice!":

        # First, we determine what the user's crafting proficiency is.
        # If left blank, we assume 0
        if isinstance(values["-prof-"], str):
            try:
                prof_bonus=int(values["-prof-"])
            except:
                prof_bonus=0
        else:
            prof_bonus=0

        # So long as more than one material is entered, artificing begins
        if len(materials)>1:
            # we sort the materials to see if they'll match recipes later
            materials.sort()
            # make an initial and total type pool
            type_pool_1=[]
            type_pool=[]
            for i in materials:
                if type_pool_1==[]:
                    type_pool_1=components[i.lower()].types
                else:
                    type_pool_2=components[i.lower()].types
                    # if the first component shares types with the iterating component or is a modifying tag, it gets added to the pool
                    for j in type_pool_1:
                        if j.lower() in types:
                            if j in type_pool_2 or j in modifiers:
                                type_pool.append(j)
                    # if the pool has a type that isn't shared by the iterating component or is in the modifiers, it gets removed
                    for j in type_pool:
                        if j not in type_pool_2 and j not in modifiers:
                            type_pool.remove(j)
            # We'll save a redundant list for magic later
            reduntant_type_pool=type_pool
            # and we take the unique list of shared types and modifiers
            type_pool=list(set(type_pool))
            for modifier in modifiers:
                if modifier in type_pool:
                    type_pool.remove(modifier)

            # If the materials share no common types, and don't make a recipe, failure happens
            if len(type_pool)==0 and materials not in recipe_values:
                description="Nothing was produced..."
                window["-item_description_2-"].update(description)
                window["-item_image-"].update("resources/images/failure.png")

            # If the components can make a recipe and nothing else, the recipe is made
            elif materials in recipe_values and len(type_pool) < 2:

                recipe_index=recipe_values.index(materials)
                selected_name=recipe_keys[recipe_index].lower()
                desc_name=recipes[selected_name].name
                desc_desc=recipes[selected_name].description
                desc_components=recipes[selected_name].components
                desc_types=recipes[selected_name].types

                # If perfectionist is the subclass, user is given the chance to
                # reroll the description with a bonus 1d4 to proficiency
                if values["-subclass_perf-"]==True:
                    reroll_desc=sg.popup_yes_no("You are perfectionist, who already knows this recipe. Would you like to attempt to improve the recipe?")
                    if reroll_desc=="Yes":
                        desc_desc=roll_desc(types[desc_types.lower()].description, prof_bonus, values["-subclass_damage-"], 0, values["-subclass_duration-"], 0, values["-subclass_duration-"], 0)
                        recipes[selected_name].description=desc_desc
                        write_file="Name: "+desc_name+"\nDescription: "+desc_desc+"\nTypes: "+desc_types+"\nComponents: "
                        for i in materials:
                            write_file+=i+", "
                        write_file=write_file[0:len(write_file)-2]
                        file_in=open("resources/recipes/"+selected_name+".recipe", "w")
                        file_in.write(write_file)
                        file_in.close()

                description=desc_name+"\nType: "+desc_types+"\n\n"+desc_desc+"\n\nRequired components:"
                for i in desc_components:
                    description+="\n   -"+i
                window["-item_description_2-"].update(description)
                if selected_name+".png" in images_list:
                    window["-item_image-"].update("resources/images/"+selected_name+".png")
                else:
                    window["-item_image-"].update("resources/images/success.png")

            # If the components all share types, they make a random, shared type
            else:
                # First, lets make sure that modiers aren't the only thing in the type pool
                good=False
                for i in type_pool:
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
                        for i in type_pool:
                            if i not in matching_recipe_type and i not in modifiers:
                                matching_recipe_names.append("Tinker")

#------------ Need to check Requirements

#------------Need to add effects

#-----------Need to parse modiers
                        if "Tinker" in matching_recipe_names:
                            choice=popup_select("This combination may generate a known recipe or you could tinker with it and try to make something new. What would you like to do?", matching_recipe_names)
                        else:
                            choice=popup_select("This combination may generates multiple recipes. Which would you like to create?", matching_recipe_names)
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
                                    if values["-subclass_holistic-"]==True:
                                        random_material=materials[rand.randint(0,len(materials)-1)]
                                        desc_desc+="\n   -"+components[random_material.lower()].effects[desc_types]

                                    # If the item is a potion, a random component effect is added
                                    if desc_types in types_w_effects:
                                        random_material=materials[rand.randint(0,len(materials)-1)]
                                        desc_desc+="\n   -"+components[random_material.lower()].effects[desc_types]

                                    desc_desc=roll_desc(desc_desc, prof_bonus, values["-subclass_damage-"], 0, values["-subclass_duration-"], 0, values["-subclass_duration-"], 0)
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
                            else:
                                window["-item_image-"].update("resources/images/success.png")
                        # If the user decides to tinker, then a different type is explored
                        else:
                            for known_type in matching_recipe_type:
                                if known_type in type_pool:
                                    type_pool.remove(known_type)

                            if len(type_pool) > 1:
                                selected_name=type_pool[rand.randint(1,len(type_pool))-1].lower()
                            else:
                                selected_name=type_pool[0].lower()
                            desc_name=types[selected_name].name
                            desc_desc=types[selected_name].description

                            # if the user is a holistic crafter, then a random component effect is added
                            if values["-subclass_holistic-"]==True:
                                random_material=materials[rand.randint(0,len(materials)-1)]
                                desc_desc+="\n   -"+components[random_material.lower()].effects[desc_name]

                            # If the item is a potion, a random component effect is added
                            if desc_name in types_w_effects:
                                random_material=materials[rand.randint(0,len(materials)-1)]
                                desc_desc+="\n   -"+components[random_material.lower()].effects[desc_name]

                            desc_desc=roll_desc(desc_desc, prof_bonus+rand.randint(1,4), values["-subclass_damage-"], 0, values["-subclass_duration-"], 0, values["-subclass_duration-"], 0)

                            desc_requirements=types[selected_name].requirements
                            description=desc_name+"\n\n"+desc_desc+"\n\nSpecific requirements:"
                            if len(desc_requirements)>0:
                                for i in desc_requirements:
                                    description+="\n   -"+i
                                else:
                                    description+="\n   -None"
                                    window["-item_description_2-"].update(description)
                                    if selected_name+".png" in images_list:
                                        window["-item_image-"].update("resources/images/"+selected_name+".png")
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
                    else:
                        if len(type_pool) > 1:
                            selected_name=type_pool[rand.randint(1,len(type_pool))-1].lower()
                        else:
                            selected_name=type_pool[0].lower()
                        desc_name=types[selected_name].name
                        desc_desc=types[selected_name].description

                        # if the user is a holistic crafter, then a random component effect is added
                        if values["-subclass_holistic-"]==True:
                            random_material=materials[rand.randint(0,len(materials)-1)]
                            desc_desc+="\n   -"+components[random_material.lower()].effects[desc_name]

                        # If the item is a potion, a random component effect is added
                        if desc_name in types_w_effects:
                            random_material=materials[rand.randint(0,len(materials)-1)]
                            desc_desc+="\n   -"+components[random_material.lower()].effects[desc_name]

                        desc_desc=roll_desc(desc_desc, prof_bonus)

                        desc_requirements=types[selected_name].requirements
                        description=desc_name+"\n\n"+desc_desc+"\n\nSpecific requirements:"
                        if len(desc_requirements)>0:
                            for i in desc_requirements:
                                description+="\n   -"+i
                            else:
                                description+="\n   -None"
                                window["-item_description_2-"].update(description)
                                if selected_name+".png" in images_list:
                                    window["-item_image-"].update("resources/images/"+selected_name+".png")
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
                else:
                    description="Nothing was produced..."
                    window["-item_description_2-"].update(description)
                    window["-item_image-"].update("resources/images/failure.png")

            materials=[]
            secret_materials=[]
            window["-lb_2-"].update(materials)
        # if less than two materials are used, nothing is produced
        else:
            description="Insufficient materials used"
            window["-item_description_2-"].update(description)
            window["-item_image-"].update("resources/images/none.png")


window.close()
