"""Process NVC succession text to find succession pathways for each"""

# pylint: disable=line-too-long
# pylint: disable=unused-import
# pylint: disable=too-many-locals

import copy
import load_community_data
import read_pdf
import save_succession_data


# empty communities list, to be loaded up with dictionaries of
# zipped up field names with database rows
communities = []
compressed_communities = []

NAME_END_WORDS = ["community", "grassland", "grass-heath", "sedge-heath","rush-heath","heath",
                  "dwarf-herb", "nana heath", "mire", "wet heath", "blanket mire", "blanket and raised mire",
                  "valley mire", "bog pool community", "fen-meadow", "rush-pasture", "soakway", 
                  "spring", "flush", "maritime rock-crevice community", "maritime grassland",
                  "maritime bluebell community", "maritime cliff-ledge community", 
                  "maritime therophyte community", "maritime sea-bird cliff community", 
                  "swamp", "swamp and sedge-beds", "water-margin vegetation", "other water-margin vegetation", "tall-herb fen",
                  "shingle community", "dune community", "dune grassland", "dune-slack community",
                  "dune scrub", "dune annual community", "strandline community", "foredune community",
                  "mobile dune community", "semi-fixed dune community", "salt-marsh community",
                  "drift-line commmunity", "stands", "moss-heath", "snow-bed", "banks",
                  "woodland", "scrub", "underscrub"]


SUCCESSION_TEXTS = {}
SUCCESSION_TEXTS_FILENAME = "txts/all_processed_succession_text.csv"  #"succession_text.csv"


# alternative community names - these need to be added to the communities database in a new column
ALTERNATIVE_NAMES = {
    'mg2':  """Filipendulo-Arrhenatheretum""",
    'mg5':  """Cynosurus-Caltha""",
    'mg6':  """Lolio-Cynosuretum""",
    'mg7':  """Lolio-Plantaginion""",
    'mg10': """Holco-Juncetum""",
    'mg12': """Potentillo-Festucetum""",
    'm18':  """Erico-Sphagnion""",
    'w2':   """Rhamno-franguletum""",
    'w6':   """Betulo-Alnetum""",
    'w7':   """Pellio-Alnetum""",
    'w8':   """Querco-Fraxinetum""",
    'w9':   """Corylo-Fraxinetum""",
    'w10':  """Querco-Betuletum""",
    'w11':  """Lonicero-Quercetum""",
    'w16':  """Querco-Betuletum"""
}

# reasons why succession might take place. To be extended
SUCCESSION_DRIVERS = {'grazing-stopped': ["abandonment of grazing"],
                      'grazing-started': ["grazing", "introduction of grazing"],
                      'ploughing-stopped': ["abandonment of ploughing"],
                      'ploughing-started': ["introduction of ploughing"],
                      'wetting': ["wetting"],
                      'drying': ["drying"],
                      'fire': ["fire"],
                      'mowing-stopped': ["abandonment of mowing"],
                      'abandonment': ["abandonment"],
                      'myxomatosis': ["myxomatosis"],
                      'flooding': ["flooding", "flooded", "flood"],
                      'clearance': ['clearance']
                      }

# MW_COMMUNITY_SUCCESSION_DRIVERS = {'grazing-stopped': ["grazing", "abandonment of grazing"],
#                       'grazing-started': ["introduction of grazing"],
#                       'flooding': ["flooding", "flooded", "flood"]
#                       }


def mapstrip(string_to_strip):
    """strips characters from each entry in a list of words, originally separated by split()"""
    return string_to_strip.strip(".,:() ")


def find_full_community_names(verbose=False):
    """go through community names and find substring ending in words in NAME_END_WORDS"""
    for com in communities:
        # print(com)
        c = com['community']
        sc = com['code']
        n = com['name'].lower()
        if c == sc: # only work on top-level communities, not sub-communities
            found_name_end_words = []
            for i in NAME_END_WORDS:
                if n.find(i) >= 0:
                    # print(c, ":", n, "->", i)
                    found_name_end_words.append(i)
            if len(found_name_end_words) > 0:
                fn = ""
                fnlen = 0
                for f in found_name_end_words:
                    if len(f) > fnlen:
                        fn = f
                        fnlen = len(fn)
                com['found_end'] = fn
                com['actual_name'] = n.partition(fn)[0].strip(" ")

    if verbose:
        print("\n\n")
        for com in communities:
            if com['community'] == com['code']:
                print(com)


def find_actual_names_in_text(c, key, sentence, verbose=False):
    """whizz through communities looking for actual_name in text"""
    recognised_communities = []
    for community in c:
        if community['community'] == community['code']:
            if 'actual_name' in community:
                an = community['actual_name']
                if sentence.find(an) > 0:
                    recognised_communities.append(community['community'])

    if verbose:
        print("For", key, "recognised", recognised_communities)

    return recognised_communities


## delete this function
# def find_succession_with_actual_names(c, t, verbose=False):
#     """whizz through texts to find actual community names"""
#     found = {}
#     for text_key, full_text in t.items():
#         found[text_key] = find_actual_names_in_text(c, text_key, full_text, verbose)
#         if verbose:
#             print(found[text_key])
#     return found


def find_compressed_community_names(name, name_list, verbose=False):
    """process community names to construct 'compressed community names'"""
    compressed_community_name = ""
    ccn = []
    name_list_copy = copy.deepcopy(name_list)
    hyphens = name.count("-")
    if hyphens > 0:
        # print(name)
        ccn.append(name_list_copy.pop(0))
        # print(ccn)
        if name.count("sub-community") > 0:
            hyphens -= 1
        if name.count("salt-marsh") > 0:
            hyphens -= 1
        if name.count("drift-line") > 0:
            hyphens -= 1
        if name.count("snow-bed") > 0:
            hyphens -= 1

        for h in range(0, hyphens):
            if verbose:
                print(h)    # shut up pylint about unused variable h
            split_name = name_list_copy.pop(0)
            if "-" in split_name:
                split_name_list = split_name.split("-")
                # print(split_name_list)
                split_name_list.pop(0)
                ccn.append(split_name_list.pop(0))
            # print(ccn)

        if len(ccn) > 1:
            compressed_community_name = ccn.pop(0)
            for i in ccn:
                compressed_community_name += "-" + i

    # print("compressed community name", compressed_community_name)
    return compressed_community_name


def process_compressed_community_names():
    """search community names and process compressed names
        then add in pre-identified alternative names"""
    found_compressed_communities = []
    for cm in communities:
        found_compressed_community_name = find_compressed_community_names(
            cm['name'], cm['list'])
        # cm['list'].append(found_compressed_community_name)
        # print(cm)
        if found_compressed_community_name != "":
            # append the newly found community name to a list of compressed names
            fccn = {'community': cm['community'], 'code': cm['code'],
                    'name': cm['name'], 'ccn': found_compressed_community_name}
            # print(fccn)
            found_compressed_communities.append(fccn)

    for cmnty_key, cmnty_val in ALTERNATIVE_NAMES.items():
        fccn = {'community': cmnty_key.upper(), 'code': cmnty_key.upper(),
                'name': cmnty_val.lower(), 'ccn': cmnty_val.lower()}
        found_compressed_communities.append(fccn)

    return found_compressed_communities


def find_succession_drivers(text, drivers, verbose=False):
    """scan for succession drivers in text, and return list of drivers found"""
    found_drivers = []
    for driver, driver_texts in drivers.items():
        found_driver = False
        for driver_text in driver_texts:
            x = text.find(driver_text)
            if x != -1:
                found_driver = True
        if found_driver:
            found_drivers.append(driver)
            if verbose:
                print("found driver", driver)

    return found_drivers


def find_communities(c, cc, key, succession_string_list, verbose=False):
    """process each community succession text and each community name to find the communities
        named in each succession text"""
    # now we have the community names and codes loaded into the list communities
    # and the succession text for a community broken into the list succession_string_list
    # so now, iterate over the list succession_string_list,
    # using the current word to search the community names
    # for the matching first word - then cycle through the next words for each
    # looking for a match
    # use pre-prepared community names split into a list by " "

    recognised_communities = []
    # found_drivers = []

    if verbose:
        print(key, 'processing', succession_string_list)

    for community in c:    # communities_iterator:
        word_iterator = iter(succession_string_list)
        word = next(word_iterator, None)
        while word is not None:
            # print("Processing", word, "against", community['list'])
            substring_index = 0
            while ((substring_index < len(community['list']))
                and (community['list'][substring_index] == word)):
                # print("Found", substring_index, community['code'],
                #   word, "in", community['list'][substring_index])
                if substring_index > 1:
                    # print("Recognised", word, substring_index, community['community'],
                    #   community['code'], community['name'])
                    # print("Record", key, "succeeds to", community['community'])
                    if community['community'] not in recognised_communities:
                        recognised_communities.append(community['community'])
                word = next(word_iterator, None)
                substring_index += 1
            word = next(word_iterator, None)

    for word in succession_string_list:
        for community in cc:
            if community['ccn'] == word:
                # print("Found compressed", word, "in", community['community'])
                if community['community'] not in recognised_communities:
                    recognised_communities.append(community['community'])

    #     for driver_code, driver_list in load_community_data.SUCCESSION_DRIVERS.items():
    #         for d in driver_list:
    #             if word == d:
    #                 load_community_data.COMMUNITY_SUCCESSION_DRIVERS[key].append(driver_code)
    #                 if verbose:
    #                     print("found succession driver", d)

    # # load_community_data.COMMUNITY_SUCCESSION_DRIVERS[key].append(found_drivers)
    # if verbose:
    #     print("\nfor key", key, "found drivers", load_community_data.COMMUNITY_SUCCESSION_DRIVERS[key])

    # print("For", key, "recognised succession communities", recognised_communities)
    return recognised_communities


def find_succession_pathways(c, cc, t, succession_driver_definitions, verbose=False):
    """by sentence, find the community names and hence succession pathways
        in each community's succession text"""
    found_dict = {}
    found_succession_drivers_dict = {}
 
    for text_key, full_text in t.items():
        # print("Community", text_key.upper())
        found = []
        found_succession_drivers_dict[text_key] = []
        text = read_pdf.clean_text(load_community_data.remove_carriage_returns(full_text))
        by_sentence_list = text.split(".")
        # print("By sentence list", by_sentence_list)

        for sentence in by_sentence_list:
            # print("Sentence", sentence)
            sentence_list = list(map(mapstrip, sentence.strip(" ").lower().split(" ")))
            # print("Key", text_key, "Sentence list", sentence_list)
            find = find_communities(c, cc, text_key.upper(), sentence_list, False)
            for f in find:
                if f not in found:
                    found.append(f)

            # we're looking for a subset of drivers relevant to the MW site
            succession_drivers = find_succession_drivers(sentence, succession_driver_definitions, False)
            if succession_drivers:
                # found_succession_drivers_dict[text_key] = succession_drivers
                # found_succession_drivers_dict[text_key] = []
                for f in find:
                    found_succession_drivers_dict[text_key].append({f: succession_drivers})
                # if found_succession_drivers_dict[text_key]:
                    # found_succession_drivers_dict[text_key] += succession_drivers
                if verbose:
                    print("\n\nfor", text_key.upper(), "found", succession_drivers, "for", find)
                    print(found_succession_drivers_dict[text_key])

        if verbose:
            if len(found) > 0:
                print("Recognised", text_key.upper(), "successes to", found)
            else:
                print(text_key.upper(), "does not success")

        found_dict.update({text_key: found})
    return found_dict, found_succession_drivers_dict


if __name__ == "__main__":
    ## Text Processing
    ## Load communities from NVC database
    communities = load_community_data.load_communities_table_from_database(
        load_community_data.NVC_DATABASE_NAME, load_community_data.LOAD_COMMUNITIES_QUERY)

    ## Find the commpressed (shortform) community names
    compressed_communities = process_compressed_community_names()
    # for x in compressed_communities:
    #     print(x)

    SUCCESSION_TEXTS = load_community_data.load_succession_text_from_csv(SUCCESSION_TEXTS_FILENAME)

    ## Process the Zonation and succession text to find the communities successed to

    found_pathways = {}
    found_succession_drivers = {}
    found_pathways, found_succession_drivers = find_succession_pathways(communities,
                                                                        compressed_communities,
                                                                        SUCCESSION_TEXTS,
                                                                        SUCCESSION_DRIVERS,
                                                                        True)

    # the found_pathways (dict) contains the succession pathways (list) for each community for which
    # succession text has been captured
    # for community_key, community_succession_values in found_pathways.items():
    #     S = set(community_succession_values)
    #     print(community_key.upper(), community_succession_values, S)


    ## abortive attempt to find community names another way
    # find_full_community_names(verbose=True)
    # found_pathways = find_succession_with_actual_names(communities, load_community_data.SUCCESSION_TEXTS, True)


    ## Add the list of succession communities for each community back into the communities list
    for cmnty in communities:
        # print("checking", cmnty['community'].lower(), "for succession pathway")
        if cmnty['community'].lower() in found_pathways:
            # print(cmnty['community'], "found pathway")
            cmnty['succession'] = found_pathways[cmnty['community'].lower()]
            # print(cmnty['community'], "pathway", cmnty['succession'])
        if cmnty['community'] == cmnty['code'] and cmnty['community'].lower() in found_succession_drivers:
            cmnty['drivers'] = found_succession_drivers[cmnty['community'].lower()]
        else:
            cmnty['drivers'] = []

    # DEBUG print it out
    print("computed succession data")
    for cmnty in communities:
        if cmnty['succession'] != []:
            print(cmnty['community'], cmnty['name'], "successes to", cmnty['succession'], "because of", cmnty['drivers'])

    ## TODO - remove this temporary comment to restore saving community succession data
    # save_succession_data.save_succession_data(communities)
    ##
