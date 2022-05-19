#!/usr/bin/env python

# Artificing made GUI

# Import required packages
import PySimpleGUI as sg
import os.path
import random as rand

sg.theme("LightGrey1")

#-------------------------------------------------------------------------------
# Define the Component class
class Component:
    def __init__(self, name, description, types, effects):
        self.name=name
        self.description=description
        self.types=types
        self.effects=effects

    def roll_desc(self):
        return

# Define the Recipe class
class Recipe:
    def __init__(self, name, description, components):
        self.name=name
        self.description=description
        self.components=components

    def roll_desc(self):
        return

# Define the Type class
class Type:
    def __init__(self, name, description, requirements):
        self.name=name
        self.description=description
        self.requirements=requirements

    def roll_desc(self):
        return

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
                loaded_i[3:len(loaded_i)]
                )
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
                loaded_recipe[1].split("Description:")[1].strip(),
                loaded_recipe[2].split("Components:")[1].strip().split(", ")
                )
                recipes[name_i.lower()]=new_recipe
                for j in new_recipe.components:
                    if j.lower() not in components:
                        new_comp=Component(
                        j,
                        "A material of unknown use.",
                        [name_i],
                        []
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
                [loaded_i[2].split("Requirements:")[1].strip()]
                )
                types[name_i.lower()]=new_type
        except:
            print("unable to parse file: "+i)

type_list=[]
for i in types:
    type_list.append(types[i].name)

#-------------------------------------------------------------------------------
# Here's where we'll load the subclasses when we.... get there

#-------------------------------------------------------------------------------
# Generate the columns
# First column where you add the components
material_entry_column = [
    sg.Button("Search"),
    sg.In(size=(10, 2), key="-search_key-"),
    sg.Button("Components"),
    sg.Button("Types"),
    sg.Button("Known recipes")
]
#
all_submitted_column = [
#    sg.Text(list_type+":", key="-lb_type-"),
    sg.Listbox(values=component_list, enable_events=True, size = (40,10), key="-lb_1-"),
    sg.Button("Submit"),
    sg.Button("Clear list"),
    sg.Listbox(values=materials, size = (40,10), key="-lb_2-"),
    sg.Text("Added proficiency score:"),
    sg.In(size=(15,1), key="-prof-"),
    sg.Button("Artifice!"),
]

main_font=("Arial bold", 11)
item_description = [
    sg.Image("resources/images/none.png", key = "-item_image-"),
    sg.Multiline(description, size=(50,15),key = "-item_description_2-", font=main_font),
]

layout=[
    material_entry_column,
    all_submitted_column,
    item_description
]

window=sg.Window("Artificing made easy!", layout)

while True:
    event, values = window.read()
    if event == "Exit" or event == sg.WIN_CLOSED:
        break

    elif event == "Search":
        search_list=[]

        if list_type=="components":
            for i in components:
                if values["-search_key-"].lower() in components[i].name.lower():
                    search_list.append(components[i].name)

        elif list_type=="types":
            for i in types:
                if values["-search_key-"].lower() in types[i].name.lower():
                    search_list.append(types[i].name)

        elif list_type=="recipes":
            for i in recipes:
                print(i)
                if values["-search_key-"].lower() in recipes[i].name.lower():
                    search_list.append(recipes[i].name)
        window["-lb_1-"].update(search_list)

    elif event=="Components":
        list_type="components"
        window["-lb_1-"].update(component_list)
#        window["-lb_type-"].update(list_type)

    elif event=="Types":
        list_type="types"
        window["-lb_1-"].update(type_list)
#        window["-lb_type-"].update(list_type)

    elif event=="Known recipes":
        list_type="recipes"
        window["-lb_1-"].update(known_recipes)
#        window["-lb_type-"].update(list_type)

    elif event=="Submit" and len(values["-lb_1-"]):
        for i in values["-lb_1-"]:
            if i in component_list and list_type=="components":
                materials.append(i)
                secret_materials.append(i)
            elif i in recipe_keys and list_type=="recipes":
                materials=recipes[i.lower()].components
        window["-lb_2-"].update(materials)

    elif event == "Clear list":
        materials=[]
        secret_materials=[]
        window["-lb_2-"].update(materials)

# This code will pull the descriptions of compone, item types, or recipes selected in the box
    elif event=="-lb_1-":
        selected_name=values["-lb_1-"][0].lower()

        if selected_name in components:
            desc_name=components[selected_name].name
            desc_desc=components[selected_name].description
            desc_types=components[selected_name].types
            description=desc_name+"\n\n"+desc_desc+"\n\nTypes:"
            for i in desc_types:
                description+="\n   -"+i
            window["-item_description_2-"].update(description)
            if selected_name+".png" in images_list:
                window["-item_image-"].update("resources/images/"+selected_name+".png")
            else:
                window["-item_image-"].update("resources/images/success.png")

        elif selected_name in types:
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


        elif selected_name in recipes:
            desc_name=recipes[selected_name].name
            desc_desc=recipes[selected_name].description
            desc_components=recipes[selected_name].components
            description=desc_name+"\n\n"+desc_desc+"\n\nRequired components:"
            for i in desc_components:
                description+="\n   -"+i
            window["-item_description_2-"].update(description)
            if selected_name+".png" in images_list:
                window["-item_image-"].update("resources/images/"+selected_name+".png")
            else:
                window["-item_image-"].update("resources/images/success.png")

    elif event=="Artifice!":
        if len(materials)>1:
            window["-item_description_2-"].update(materials)
            materials.sort()
            if materials in recipe_values and len(materials) > 0:
                recipe_index=recipe_values.index(materials)
                selected_name=recipe_keys[recipe_index].lower()
                desc_name=recipes[selected_name].name
                desc_desc=recipes[selected_name].description
                desc_components=recipes[selected_name].components
                description=desc_name+"\n\n"+desc_desc+"\n\nRequired components:"
                for i in desc_components:
                    description+="\n   -"+i
                window["-item_description_2-"].update(description)
                if selected_name+".png" in images_list:
                    window["-item_image-"].update("resources/images/"+selected_name+".png")
                else:
                    window["-item_image-"].update("resources/images/success.png")
            else:
                type_pool=[]
                for i in materials:
                    if type_pool==[]:
                        type_pool=components[i.lower()].types
                    else:
                        for j in type_pool:
                            if j.lower() in types:
                                if j not in components[i.lower()].types and j != "Volatile":
                                    type_pool.remove(j)
                                if "Volatile" in components[i.lower()].types:
                                    type_pool.append("Volatile")
                            else:
                                type_pool.remove(j)
                if len(type_pool)==0:
                    description="Nothing was produced..."
                    window["-item_description_2-"].update(description)
                    window["-item_image-"].update("resources/images/failure.png")
                else:
                    if len(type_pool) > 1:
                        selected_name=type_pool[rand.randint(1,len(type_pool))-1].lower()
                    else:
                        selected_name=type_pool[0].lower()
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

            materials=[]
            secret_materials=[]
            window["-lb_2-"].update(materials)
        else:
            description="Insufficient materials used"
            window["-item_description_2-"].update(description)
            window["-item_image-"].update("resources/images/none.png")


window.close()
