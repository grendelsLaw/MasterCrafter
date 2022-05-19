#!/usr/bin/env python

# Artificing made GUI

# Import required packages
import PySimpleGUI as sg
import os.path
import random as rand

sg.theme("LightGrey1")

# Define default values
# A list of the components
materials=[]

# A description of the artificed item
description="Submit components to artifice a new item."

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
        # Opens, loads, and closes the component file
        component_i=open("resources/components/"+i, "r")
        loaded_i=component_i.read()
        component_i.close()
        # Strips and splits the component file based on newlines
        loaded_i=loaded_i.strip().split("\n")
        # Gets the component name
        name_i=loaded_i[0].strip()
        # If the component isn't in the component dictionary, it gets added
        if name_i not in components:
            components[name_i]=loaded_i[1:len(loaded_i)]

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
        # Open the file, read it, then close it
        possible_recipe=open("resources/recipes/"+i, "r")
        loaded_recipe=possible_recipe.read()
        possible_recipe.close()
        # We split the recipe based on the newlines
        loaded_recipe=loaded_recipe.strip().split("\n")
        # We pull the name of the recipe
        name_i=loaded_recipe[0].strip()
        # If the name isn't in the recipe list, we add it
        if name_i not in recipes:
            # Set the first lsit value to be the description of the recipe
            tick=[loaded_recipe[1]]
            # Then we add the recipe components as the second item of the value list
            recipe_comps=loaded_recipe[2].split(", ")
            recipe_comps.sort()
            recipes[name_i]=tick
            recipes[name_i].append(recipe_comps)
            for j in recipe_comps:
                if j not in components:
                    components[j]=[["No description found for this object"],[]]

recipe_keys=list(recipes.keys())
recipe_values=list(recipes.values())

component_list=list(components.keys())
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
        # It gets opened, loaded, and closed
        type_i=open("resources/types/"+i, "r")
        loaded_i=type_i.read()
        type_i.close()
        # Then it gets stripped and split by the newlines
        loaded_i=loaded_i.strip().split("\n")
        # The name of the type is pulled
        name_i=loaded_i[0]
        # If the type doesn't exist int he type directory, it gets added!
        if name_i not in types:
            types[name_i]=loaded_i[1].strip()

#-------------------------------------------------------------------------------
# Here's where we'll load the classes when we.... get there

#-------------------------------------------------------------------------------
# Generate the columns
# First column where you add the components
material_entry_column = [
    sg.Text("Component type:"),
    sg.Combo(component_list, default_value=component_list[0], size = (20,1), enable_events= True, key="-Comp1-"),
    sg.Button("Submit"),
    sg.Button("Types"),
    sg.Button("Known recipes"),
    sg.In(size=(10, 1), key="-search_key-"),
    sg.Button("Search")
]
#
all_submitted_column = [
    sg.Listbox(values=component_list, size = (40,10), key="-lb_1-"),
    sg.Text("Added proficiency score:"),
    sg.In(size=(3,1), key="-prof-"),
    sg.Button("Artifice!"),
    sg.Button("Clear list")
]

main_font=("Arial bold", 11)
item_description = [
    sg.Image("resources/images/None.png", key = "-item_image-"),
    sg.Multiline(description, size=(50,10),key = "-item_description_2-", font=main_font),
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
        for i in component_list:
            if values["-search_key-"] in i:
                search_list.append(i)
        window["-lb_1-"].update(search_list)
#    elif event == "Clear list":
#        materials=[]
#        secret_materials=[]
#        window["-materials_list-"].update(materials)
#        window["-item_image-"].update("images/None.png")
#        description="Submit components to artifice a new item."
#        window["-item_description_2-"].update(description)
#    elif event == "Submit":
#        material_1 = values["-Comp1-"]
#            secret_materials.append(material_1)
#            material_1=material_1+" of "+values["-quality-"]+" quality"
#            materials.append(material_1)
#            window["-materials_list-"].update(materials)
#            window["-Comp1-"].update("")
#            window["-number-"].update("1")
#            quality_tally+=quality_converter[values["-quality-"]]
#    elif event == "Artifice!":
#        secret_materials.sort()
#        if secret_materials in recipe_values:
#            hit=recipe_values.index(secret_materials)
#            hit_name=recipe_keys[hit]
#            item_name=hit_name.split("SPLIT")[0]
#            description=hit_name.split("SPLIT")[1]
#            item_image=item_name+".png"

#            quality_tally=round(quality_tally/len(secret_materials),0)
#            if len(description.split("MAXIMUM")):
#                if values["-prof-"]=="":
#                    prof_add=0
#                else:
#                    prof_add=int(values["-prof-"])
#                new_desc=""
#                for i in description.split("MAXIMUM"):
#                    if "DICE" in i:
#                        max_dice=int(round(int(i.split("DICE")[0])*(quality_tally/4)*((rand.randrange(1,21)+prof_add)/20)))
#                        new_desc+=str(max_dice)+i.split("DICE")[1]
#                    else:
#                        new_desc+=i
#                description=new_desc

#            window["-item_description_2-"].update(item_name+"\n"+description)
#            if item_image in images_list:
#                window["-item_image-"].update("images/"+item_image)
#            else:
#                window["-item_image-"].update("images/Success.png")
#        else:
#            description="Nothing new was generated..."
#            window["-materials_list-"].update(materials)
#            window["-item_description_2-"].update(description)
#            window["-item_image-"].update("images/Failure.png")
#        materials=[]
#        secret_materials=[]
#        window["-materials_list-"].update(materials)
#        quality_tally=0
    elif event=="-lb_1-":
        window["-item_image-"].update("images/Success.png")
        window["-item_description_2-"].update(value["-lb_1-"])

window.close()
