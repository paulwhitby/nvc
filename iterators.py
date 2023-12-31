# play with iterators

s = """Some of the most frequent zonations involving Arrhenatheretum stands are the often sharp juxtapositions of the various sub-communities and variants with one another or with other vegetation types along road margins. Such patterns are very varied and sometimes reflect long, local traditions of boundary construction and maintenance. Where stands are not maintained by cutting, zonations are generally a reflection of stages in succession to mixed deciduous woodland. This succession is most often mediated by grazing. Arrhenatherum is a ready invader of soils and calcareous talus exposed by landslip, construction work or the abandonment of ploughed land. It can also spread into and increase in certain other grassland types where grazing is absent or withdrawn or where there is injudicious pastoral treatment. Resumption of grazing can once more reduce its cover. Hope-Simpson (1940b) noted that, within four years of the removal of rabbits from a primitive Festuca ovina-Avenula pratensis sward at War Down, Hampshire, Arrhenatherum previously no more than occasional, had become very abundant. Within seven years of the resumption of grazing by sheep and rabbits on an Arrhenatheretum at nearby Coulter’s Dean Wasteland, the vegetation had been converted to a Festuca ovina-Avenula pratensis grassland with no Arrhenatherum (Hope-Simpson 1940b). Thomas (1960, 1963) showed that, after the virtual elimination of rabbits by myxomatosis, the coarser grasses characteristic of the Arrhenatheretum were among those species which spread in grasslands and heaths on chalk. These had previously been present in small amounts and had provided a valuable winter-green bite for the rabbits. They were reduced in cover when rabbit numbers rose again. Arrhenatherum can also spread into seeded verges and some of the floristic variation within the Festuca rubra sub-community (see above) is attributable to this advance. Increase of Arrhenatherum in Centaureo-Cynosuretum grasslands seems to follow careless grazing, perhaps by the use of such grasslands as horse-paddocks, and the Centaurea nigra sub-community of the Arrhenatheretum may originate partly in this way. Ploughing and subsequent abandonment of land after unsuccessful arable cultivation seems to have been a fairly widespread factor in the development of some of the more extensive stands of the community, especially on deeper soils over chalk. The Arrhenatheretum at Coulter’s Dean Wasteland had developed on land ploughed and abandoned some 30 years before (Tansley & Adamson 1925). Brenchley & Adam (1915) had reported a similar occurrence of the community on the abandoned and ungrazed Broadbalk Wilderness at Rothamsted. Several subsequent studies (Lloyd & Pigott 1967 in the Chilterns, Grubb et al. 1969 at Lullington Heath, Sussex and Wells et al. 1976 at Porton Down on the Hampshire/Wiltshire border) have confirmed the view that the Arrhenatheretum is one of the communities dominated by coarse grasses which can, in the absence of grazing, develop naturally on the chalk without the prior development of a Festuca ovina-Avenula pratensis sward. The Arrhenathereta described in these studies are of the kind classified here as the Pastinaca and Centaurea nigra sub-communities but the lists provided are generally insufficiently precise to allocate stands unequivocally to one or the other. The available data suggest that the Pastinaca sub-community develops on the more calcareous and oligotrophic soils where these have been exposed by ploughing or where there has been a relaxation of grazing of calcicolous grassland. This sub-community is most common on the chalk of the south and east where P. sativa has its centre of distribution in Britain and where there has been a history of unsuccessful arable cultivation of marginal chalkland and pastoral neglect (see, for example, Smith 1980). The Centaurea sub-community is more widespread and seems to develop on more mesotrophic soils which are generally less calcareous. It is perhaps the more natural sub-community on deeper soils over chalk, such as those derived from superficial deposits, but it may also develop by the relaxation of grazing of mesotrophic grasslands throughout the lowlands, especially where this has been combined with application of fertilisers. Similar differences in the trophic state of soils may be an important factor in controlling whether it is Arrhenatheretum (of any kind) or grassland dominated by other coarse species such as Avenula pubescens, Festuca rubra, Bromus erectus and Brachypodium pinnatum which develops in any given situation. Wells et al. (1976) showed that, at Porton, the Arrhenatheretum occurred on land ploughed relatively recently where, they suggested, there was still a comparatively small accumulation of organic matter and mineral nutrients. Other coarse grassland types had developed on soils ploughed less recently which were consequently richer. If any kind of Arrhenatheretum remains ungrazed and uncut it eventually develops a pronounced tussock physiognomy and litter accumulation depresses species-richness. Shrubs invade and the frequently close hedgerows and field boundaries provide a seed source. Foremost among the invaders is Crataegus monogyna with Prunus spinosa, Sambucus nigra (especially where there has been disturbance and soil eutrophication), Rubus fruticosus agg., Rosa spp. and, on the more calcareous soils, Cornus sanguinea, Viburnum lantana and Ligustrum vulgare. Clematis vitabla may form a tangle among the developing scrub. Eventually, succession progresses to some form of mixed deciduous woodland but even very coarse and scrubby Arrhenatheretum can be converted to a low sward by grazing. At Aston Rowant NNR, Oxfordshire, four years of sheep-grazing in winter and spring drastically reduced the height of a scrubby Arrhenatheretum and converted A. elatius itself from large tussocks to small scattered shoots in a ground of Festuca ovina (Wells 1969: compare especially Figures 1 and 2)."""

s_sentences = list()
s_sentence_words = list()

s_sentences = s.split(".")
print("Split into sentences:", s_sentences)

sentences_iterator = s_sentences.__iter__()
for sentence in sentences_iterator:
    print("A sentence:", sentence)
    s_sentence_words = sentence.split(" ")
    print("Split into words:", s_sentence_words)

    # sentence_words_iterator = s_sentence_words.__iter__()
    # for word in sentence_words_iterator:
    #     print("Word:", word)
    #     try:
    #         word = sentence_words_iterator.__next__()
    #     finally:
    #         print("StopIter")
    #         pass

    # sentence_words_iterator = iter(s_sentence_words)
    # for word in s_sentence_words:
    #     print("Word:", word)
    #     word = next(sentence_words_iterator, None)
    #     if word == None:
    #         print("reached the end of the line")
    #         break
    #     else:
    #         word = next(sentence_words_iterator, None)
    #         if word == None:
    #             break
    #         else:
    #             continue
    
    sentence_words_iterator = iter(s_sentence_words)
    word = next(sentence_words_iterator)
    print("1st word: ", word)
    while word != None:
        print("Word:", word)
        word = next(sentence_words_iterator, None)
        if word == None:
            print("reached the end of the line")
            break
        else:
            word = next(sentence_words_iterator, None)
            if word == None:
                break
            else:
                continue
    
   

    # for word in s_sentence_words:
    #     print("Word:", word)
    #     continue
