#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Copyright (C) 2018  David Arroyo Menéndez

# Author: David Arroyo Menéndez <davidam@gnu.org>
# Maintainer: David Arroyo Menéndez <davidam@gnu.org>

# This file is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3, or (at your option)
# any later version.

# This file is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with Damegender; see the file LICENSE.  If not, write to
# the Free Software Foundation, Inc., 51 Franklin Street, Fifth Floor,
# Boston, MA 02110-1301 USA,

from app.dame_gender import Gender
from app.dame_sexmachine import DameSexmachine
from app.dame_namsor import DameNamsor
from app.dame_genderguesser import DameGenderGuesser
from app.dame_genderapi import DameGenderApi
from app.dame_genderize import DameGenderize
from app.dame_nameapi import DameNameapi
from app.dame_customsearch import DameCustomsearch
import os
import argparse
parser = argparse.ArgumentParser()
parser.add_argument('--csv', type=str, required=True, help="files/names/min.csv")
parser.add_argument('--jsondownloaded', default="", help="files/names/genderapifiles_names_min.csv.json")
parser.add_argument('--api', required=True, choices=['namsor', 'genderize', 'genderapi', 'genderguesser', 'damegender', 'nameapi', 'all'])
parser.add_argument('--ml', default="nltk", choices=['nltk', 'svc', 'sgd', 'gaussianNB', 'multinomialNB', 'bernoulliNB'])
parser.add_argument('--reverse', default=False, action="store_true")
parser.add_argument('--dimensions', default="2x3", choices=['1x1', '1x2', '1x3', '2x1', '2x2', '2x3', '3x1', '3x2', '3x3'])
args = parser.parse_args()

print("A confusion matrix C is such that Ci,j is equal to the number of observations known to be in group i but predicted to be in group j.")
print("If the classifier is nice, the diagonal is high because there are true positives")


if (args.api == "all"):
    dg = Gender()
    if (dg.config['DEFAULT']['namsor'] == 'yes'):
        dn = DameNamsor()
        print("Namsor confusion matrix:\n")
        dn.print_confusion_matrix_gender(path=args.csv, dimensions=args.dimensions)

    if (dg.config['DEFAULT']['genderize'] == 'yes'):
        dg = DameGenderize()
        print("Genderize confusion matrix:\n ")
        dg.print_confusion_matrix_gender(path=args.csv, dimensions=args.dimensions)

    if (dg.config['DEFAULT']['genderapi'] == 'yes'):
        dga = DameGenderApi()
        print("Genderapi confusion matrix:\n")
        dga.print_confusion_matrix_gender(path=args.csv, dimensions=args.dimensions, jsonf=args.jsondownloaded)

    dgg = DameGenderGuesser()
    print("Gender Guesser confusion matrix:\n")
    dgg.print_confusion_matrix_gender(path=args.csv, dimensions=args.dimensions)

    ds = DameSexmachine()
    print("Damegender confusion matrix:\n")
    ds.print_confusion_matrix_gender(path=args.csv, dimensions=args.dimensions, ml='nltk')

    if (dg.config['DEFAULT']['nameapi'] == 'yes'):
        dna = DameNameapi()
        print("Nameapi confusion matrix:\n")
        dna.print_confusion_matrix_gender(path=args.csv, dimensions=args.dimensions)

elif (args.api == "namsor"):
    dn = DameNamsor()
    print("Namsor confusion matrix:\n")
    if (os.path.isfile(args.jsondownloaded)):
        dn.print_confusion_matrix_gender(path=args.csv, dimensions=args.dimensions, jsonf=args.jsondownloaded, reverse=args.reverse)
    elif (args.jsondownloaded == ''):
        dn.print_confusion_matrix_gender(path=args.csv, dimensions=args.dimensions, reverse=args.reverse)
    else:
        print("In the path %s doesn't exist file" % args.jsondownloaded)


elif (args.api == "genderize"):
    dg = DameGenderize()
    print("Genderize confusion matrix:\n")
    if (os.path.isfile(args.jsondownloaded)):
        dg.print_confusion_matrix_gender(path=args.csv, dimensions=args.dimensions, jsonf=args.jsondownloaded, reverse=args.reverse)
    elif (args.jsondownloaded == ''):
        dg.print_confusion_matrix_gender(path=args.csv, dimensions=args.dimensions, reverse=args.reverse)
    else:
        print("In the path %s doesn't exist file" % args.jsondownloaded)

elif (args.api == "genderapi"):
    dga = DameGenderApi()
    if (os.path.isfile(args.jsondownloaded)):
        dga.print_confusion_matrix_gender(path=args.csv, dimensions=args.dimensions, jsonf=args.jsondownloaded, reverse=args.reverse)
    elif (args.jsondownloaded == ''):
        dga.print_confusion_matrix_gender(path=args.csv, dimensions=args.dimensions, reverse=args.reverse)
    else:
        print("In the path %s doesn't exist file" % args.jsondownloaded)

elif (args.api == "genderguesser"):
    dgg = DameGenderGuesser()
    print("Gender Guesser confusion matrix:\n")
    dgg.print_confusion_matrix_gender(path=args.csv, dimensions=args.dimensions, reverse=args.reverse)

elif (args.api == "damegender"):
    ds = DameSexmachine()
    print("Damegender confusion matrix:\n")
    if (os.path.isfile(args.jsondownloaded)):
        ds.print_confusion_matrix_gender(path=args.csv, dimensions=args.dimensions, jsonf=args.jsondownloaded, ml=args.ml, reverse=args.reverse)
    elif (args.jsondownloaded == ''):
        ds.print_confusion_matrix_gender(path=args.csv, dimensions=args.dimensions, ml=args.ml, reverse=args.reverse)
    else:
        print("In the path %s doesn't exist file" % args.jsondownloaded)

elif (args.api == "nameapi"):
    dna = DameNameapi()
    print("Nameapi confusion matrix:\n")
#    dna.print_confusion_matrix_gender(path=args.csv, dimensions=args.dimensions)
    if (os.path.isfile(args.jsondownloaded)):
        dna.print_confusion_matrix_gender(path=args.csv, dimensions=args.dimensions, jsonf=args.jsondownloaded, reverse=args.reverse)
    elif (args.jsondownloaded == ''):
        dna.print_confusion_matrix_gender(path=args.csv, dimensions=args.dimensions, reverse=args.reverse)
    else:
        print("In the path %s doesn't exist file" % args.jsondownloaded)


# elif (args.api == "customsearch"):
#     dc = DameCustomsearch()
#     print("Google Custom Search confusion matrix:\n")
#     dc.print_confusion_matrix_gender(path=args.csv)
