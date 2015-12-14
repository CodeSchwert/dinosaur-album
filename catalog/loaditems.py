#!/usr/bin/python
#
# loaditems.py - Udacity Project 3
#
# Nik Ho, 2015
#
# This code page loads a number of dinosaur categories and dinosaurs into
# the database so it's 'ready' to use.
#
# Licence: MIT
#
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_model import Base, Category, CategoryItem, User

engine = create_engine('sqlite:///itemcatalogue.db')
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until you call
# session.commit(). If you're not happy about the changes, you can
# revert all of them back to the last commit by calling
# session.rollback()
session = DBSession()


# class Dinosaur:
#     """Each dinosaur is a category item"""
#     def __init__(self, name, image_url, caption):
#         self.name = name
#         self.image_url = image_url
#         self.caption = caption


# class DinosaurCategory:
#     """docstring for DinosaurCategory"""
#     def __init__(self, name, description, dinosaurs):
#         self.name = name
#         self.description = description
#         self.dinosaurs = dinosaurs


""" Ceratopsia """

category1 = Category(name="Ceratopsia", description="Greek: 'horned faces'; \
    is a group of herbivorous, beaked dinosaurs that thrived in what are \
    now North America, Europa, and Asia, during the Cretaceous Period.")
session.add(category1)
session.commit()

# Centrosaurus
item1 = CategoryItem(
    name="Centrosaurus",
    description="Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed \
    do eiusmod tempor incididunt ut labore et dolore magna aliqua.",
    image_url="/static/img/centrosaurus.jpg",
    image_caption="Centrosaurus",
    category=category1
    )
session.add(item1)
session.commit()

# Styracosaurus
item2 = CategoryItem(
    name="Styracosaurus",
    description="Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed \
    do eiusmod tempor incididunt ut labore et dolore magna aliqua.",
    image_url="/static/img/styracosaurus.jpg",
    image_caption="Styracosaurus",
    category=category1
    )
session.add(item2)
session.commit()

""" Ornithopoda """

category2 = Category(name="Ornithopoda", description="Ornithopoda means 'bird \
    feet'; this refers to their characteristic three-toed feet, although many \
    early forms retained four toes.")
session.add(category2)
session.commit()

# Parasaurolophus
item3 = CategoryItem(
    name="Parasaurolophus",
    description="Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed \
    do eiusmod tempor incididunt ut labore et dolore magna aliqua.",
    image_url="/static/img/parasaurolophus.jpg",
    image_caption="Parasaurolophus",
    category=category2
    )
session.add(item3)
session.commit()

""" Pachycephalosauria """

category3 = Category(name="Pachycephalosauria", description="From Greek for \
    'thich headed lizards'; They were all bipedal, herbivorous/omnivorous \
    animals with thick skulls. In some fossils, the skull roof is domed and \
    several centimeters thick.")
session.add(category3)
session.commit()

# Pachycephalosaurus
item4 = CategoryItem(
    name="Pachycephalosaurus",
    description="Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed \
    do eiusmod tempor incididunt ut labore et dolore magna aliqua.",
    image_url="/static/img/pachycephalosaurus.jpg",
    image_caption="Pachycephalosaurus",
    category=category3
    )
session.add(item4)
session.commit()

""" Stegosauria  """

category4 = Category(name="Stegosauria", description="The Stegosauria is a \
    group of herbivorous ornithischian dinosaurs that lived during the \
    Jurassic and early Cretaceous periods. Stegosaurians were armored \
    dinosaurs.")
session.add(category4)
session.commit()

# Stegosaurus
item5 = CategoryItem(
    name="Stegosaurus",
    description="Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed \
    do eiusmod tempor incididunt ut labore et dolore magna aliqua.",
    image_url="/static/img/Stegosaurus.jpg",
    image_caption="Stegosaurus",
    category=category4
    )
session.add(item5)
session.commit()

""" Ankylosauria """

category5 = Category(name="Ankylosauria", description="Ankylosauria, Ancient \
    Greek for 'crooked lizard', is a group of herbivorous dinosaurs. It \
    includes the great majority of dinosaurs with armor in the form of bony \
    osteoderms. Ankylosaurs were bulky quadrupeds, with short, powerful \
    limbs.")
session.add(category5)
session.commit()

# Ankylosaurus
item6 = CategoryItem(
    name="Ankylosaurus",
    description="Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed \
    do eiusmod tempor incididunt ut labore et dolore magna aliqua.",
    image_url="/static/img/ankylosaurus.jpg",
    image_caption="Ankylosaurus",
    category=category5
    )
session.add(item6)
session.commit()

""" Sauropoda """

category6 = Category(name="Sauropoda", description="Sauropoda, or the \
    sauropds 'lizard-footed', had very long necks, long tails, small heads \
    (relative to the rest of their body), and four thick, pillar-like legs. \
    They are notable for the enormous sizes attained by some species, and the \
    group includes the largest animals to have ever lived on land.")
session.add(category6)
session.commit()

# Brachiosaurus
item7 = CategoryItem(
    name="Brachiosaurus",
    description="Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed \
    do eiusmod tempor incididunt ut labore et dolore magna aliqua.",
    image_url="/static/img/brachiosaurus.jpg",
    image_caption="Brachiosaurus",
    category=category6
    )
session.add(item7)
session.commit()

# Apatosaurus
item8 = CategoryItem(
    name="Apatosaurus",
    description="Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed \
    do eiusmod tempor incididunt ut labore et dolore magna aliqua.",
    image_url="/static/img/apatosaurus.jpg",
    image_caption="Apatosaurus",
    category=category6
    )
session.add(item8)
session.commit()

""" Therapoda """

category7 = Category(name="Theropoda", description="Theropoda, from Greek \
    meaning 'beast feet'. Theropods were ancestrally carnivorous, although a \
    number of theropod groups evolved herbivory, omnivory, piscivory, and \
    insectivory.")
session.add(category7)
session.commit()

# Allosaurus
item9 = CategoryItem(
    name="Allosaurus",
    description="Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed \
    do eiusmod tempor incididunt ut labore et dolore magna aliqua.",
    image_url="/static/img/allosaurus.jpg",
    image_caption="Allosaurus", category=category7
    )
session.add(item9)
session.commit()

# Deinonychus
item10 = CategoryItem(
    name="Deinonychus",
    description="Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed \
    do eiusmod tempor incididunt ut labore et dolore magna aliqua.",
    image_url="/static/img/deinonychus_antirrhopus.jpg",
    image_caption="Deinonychus",
    category=category7
    )
session.add(item10)
session.commit()

# Tyrannosaurus
item11 = CategoryItem(
    name="Tyrannosaurus",
    description="Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed \
    do eiusmod tempor incididunt ut labore et dolore magna aliqua.",
    image_url="/static/img/tyrannosaurus.jpg",
    image_caption="Tyrannosaurus Rex",
    category=category7
    )
session.add(item11)
session.commit()
