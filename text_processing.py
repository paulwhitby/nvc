"""Process NVC succession text to find succession pathways for each"""
import copy
import load_community_data
import save_succession_data


# empty communities list, to be loaded up with dictionaries of
# zipped up field names with database rows
communities = []
compressed_communities = []


def find_compressed_community_names(name, name_list):
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
    for cmnty in communities:
        found_compressed_community_name = find_compressed_community_names(
            cmnty['name'], cmnty['list'])
        # cmnty['list'].append(found_compressed_community_name)
        # print(cmnty)
        if found_compressed_community_name != "":
            # append the newly found community name to a list of compressed names
            fccn = {'community': cmnty['community'], 'code': cmnty['code'],
                    'name': cmnty['name'], 'ccn': found_compressed_community_name}
            # print(fccn)
            found_compressed_communities.append(fccn)

    for cmnty_key, cmnty in load_community_data.ALTERNATIVE_NAMES.items():
        fccn = {'community': cmnty_key.upper(), 'code': cmnty_key.upper(),
                'name': cmnty.lower(), 'ccn': cmnty.lower()}
        found_compressed_communities.append(fccn)
    
    return found_compressed_communities


def mapstrip(string_to_strip):
    """strips characters from each entry in a list of words, originally separated by split()"""
    return string_to_strip.strip(".,:() ")


def find_communities(c, cc, key, succession_string_list):
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

    # print('processing', succession_string_list)

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

    # print("For", key, "recognised succession communities", recognised_communities)
    return recognised_communities


def find_succession_pathways(c, cc, t):
    """by sentence, find the community names and hence succession pathways
        in each community's succession text"""
    found_dict = {}
    for text_key, full_text in t.items():
        # print("Community", k.upper())
        found = []
        text = load_community_data.remove_carriage_returns(full_text)
        by_sentence_list = text.split(".")
        # print("By sentence list", by_sentence_list)

        for sentence in by_sentence_list:
            # print("Sentence", sentence)
            sentence_list = list(map(mapstrip, sentence.strip(" ").lower().split(" ")))
            # print("Key", k, "Sentence list", sentence_list)
            find = find_communities(c, cc, text_key.upper(), sentence_list)
            for f in find:
                if f not in found:
                    found.append(f)  # s.split(" ") --> v.lower().split(" ")

        # if len(found) > 0:
        #     print("Recognised", k.upper(), "successes to", found)
        # else:
        #     print(k.upper(), "does not success")

        found_dict.update({text_key: found})
    return found_dict


## Text Processing

## Load communities from NVC database
communities = load_community_data.load_communities_table_from_database(
    load_community_data.NVC_DATABASE_NAME, load_community_data.LOAD_COMMUNITIES_QUERY)

## Find the commpressed (shortform) community names
compressed_communities = process_compressed_community_names()
# for x in compressed_communities:
#     print(x)

load_community_data.SUCCESSION_TEXTS = load_community_data.load_succession_text_from_csv(load_community_data.SUCCESSION_TEXTS_FILENAME)

## Process the Zonation and succession text to find the communities successed to
found_pathways = find_succession_pathways(
    communities, compressed_communities, load_community_data.SUCCESSION_TEXTS)
# the found_pathways (dict) contains the succession pathways (list) for each community for which
# succession text has been captured
# for community_key, community_succession_values in found_pathways.items():
#     S = set(community_succession_values)
#     print(community_key.upper(), community_succession_values, S)

## Add the list of succession communities for each community back into the communities list
for cmnty in communities:
    # print("checking", cmnty['community'].lower(), "for succession pathway")
    if cmnty['community'].lower() in found_pathways:
        # print(cmnty['community'], "found pathway")
        cmnty['succession'] = found_pathways[cmnty['community'].lower()]
        # print(cmnty['community'], "pathway", cmnty['succession'])

## DEBUG print it out
print("computed succession data")
for cmnty in communities:
    if cmnty['succession'] != []:
        # print(cmnty['community'], cmnty['name'], cmnty['succession'])
        print(cmnty)

print("write computed succession data to nvc database")
save_succession_data.save_succession_data(communities)
