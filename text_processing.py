import sqlite3

# text processing


succession_texts = {
  'mg1': """Some of the most frequent zonations involving Arrhenatheretum stands are the often sharp juxtapositions of the various sub-communities and variants with one another or with other vegetation types along road margins. Such patterns are very varied and sometimes reflect long, local traditions of boundary construction and maintenance. Where stands are not maintained by cutting, zonations are generally a reflection of stages in succession to mixed deciduous woodland. This succession is most often mediated by grazing. Arrhenatherum is a ready invader of soils and calcareous talus exposed by landslip, construction work or the abandonment of ploughed land. It can also spread into and increase in certain other grassland types where grazing is absent or withdrawn or where there is injudicious pastoral treatment. Resumption of grazing can once more reduce its cover. Hope-Simpson (1940b) noted that, within four years of the removal of rabbits from a primitive Festuca ovina-Avenula pratensis sward at War Down, Hampshire, Arrhenatherum previously no more than occasional, had become very abundant. Within seven years of the resumption of grazing by sheep and rabbits on an Arrhenatheretum at nearby Coulter’s Dean Wasteland, the vegetation had been converted to a Festuca ovina-Avenula pratensis grassland with no Arrhenatherum (Hope-Simpson 1940b). Thomas (1960, 1963) showed that, after the virtual elimination of rabbits by myxomatosis, the coarser grasses characteristic of the Arrhenatheretum were among those species which spread in grasslands and heaths on chalk. These had previously been present in small amounts and had provided a valuable winter-green bite for the rabbits. They were reduced in cover when rabbit numbers rose again. Arrhenatherum can also spread into seeded verges and some of the floristic variation within the Festuca rubra sub-community (see above) is attributable to this advance. Increase of Arrhenatherum in Centaureo-Cynosuretum grasslands seems to follow careless grazing, perhaps by the use of such grasslands as horse-paddocks, and the Centaurea nigra sub-community of the Arrhenatheretum may originate partly in this way. Ploughing and subsequent abandonment of land after unsuccessful arable cultivation seems to have been a fairly widespread factor in the development of some of the more extensive stands of the community, especially on deeper soils over chalk. The Arrhenatheretum at Coulter’s Dean Wasteland had developed on land ploughed and abandoned some 30 years before (Tansley & Adamson 1925). Brenchley & Adam (1915) had reported a similar occurrence of the community on the abandoned and ungrazed Broadbalk Wilderness at Rothamsted. Several subsequent studies (Lloyd & Pigott 1967 in the Chilterns, Grubb et al. 1969 at Lullington Heath, Sussex and Wells et al. 1976 at Porton Down on the Hampshire/Wiltshire border) have confirmed the view that the Arrhenatheretum is one of the communities dominated by coarse grasses which can, in the absence of grazing, develop naturally on the chalk without the prior development of a Festuca ovina-Avenula pratensis sward. The Arrhenathereta described in these studies are of the kind classified here as the Pastinaca and Centaurea nigra sub-communities but the lists provided are generally insufficiently precise to allocate stands unequivocally to one or the other. The available data suggest that the Pastinaca sub-community develops on the more calcareous and oligotrophic soils where these have been exposed by ploughing or where there has been a relaxation of grazing of calcicolous grassland. This sub-community is most common on the chalk of the south and east where P. sativa has its centre of distribution in Britain and where there has been a history of unsuccessful arable cultivation of marginal chalkland and pastoral neglect (see, for example, Smith 1980). The Centaurea sub-community is more widespread and seems to develop on more mesotrophic soils which are generally less calcareous. It is perhaps the more natural sub-community on deeper soils over chalk, such as those derived from superficial deposits, but it may also develop by the relaxation of grazing of mesotrophic grasslands throughout the lowlands, especially where this has been combined with application of fertilisers. Similar differences in the trophic state of soils may be an important factor in controlling whether it is Arrhenatheretum (of any kind) or grassland dominated by other coarse species such as Avenula pubescens, Festuca rubra, Bromus erectus and Brachypodium pinnatum which develops in any given situation. Wells et al. (1976) showed that, at Porton, the Arrhenatheretum occurred on land ploughed relatively recently where, they suggested, there was still a comparatively small accumulation of organic matter and mineral nutrients. Other coarse grassland types had developed on soils ploughed less recently which were consequently richer. If any kind of Arrhenatheretum remains ungrazed and uncut it eventually develops a pronounced tussock physiognomy and litter accumulation depresses species-richness. Shrubs invade and the frequently close hedgerows and field boundaries provide a seed source. Foremost among the invaders is Crataegus monogyna with Prunus spinosa, Sambucus nigra (especially where there has been disturbance and soil eutrophication), Rubus fruticosus agg., Rosa spp. and, on the more calcareous soils, Cornus sanguinea, Viburnum lantana and Ligustrum vulgare. Clematis vitabla may form a tangle among the developing scrub. Eventually, succession progresses to some form of mixed deciduous woodland but even very coarse and scrubby Arrhenatheretum can be converted to a low sward by grazing. At Aston Rowant NNR, Oxfordshire, four years of sheep-grazing in winter and spring drastically reduced the height of a scrubby Arrhenatheretum and converted A. elatius itself from large tussocks to small scattered shoots in a ground of Festuca ovina (Wells 1969: compare especially Figures 1 and 2).""", 
  'mg2': """Spatial transitions between the Filipendulo-Arrhenatheretum and other vegetation types are partly controlled by the sharpness of local topographic discontinuities. Stands are often small and fragmentary and confined to ledges and embayments, giving way abruptly on less sheltered, sunnier slopes to the local form of calcicolous grassland. Where the vegetation is open to stock, grazing may blur the zonation. There is sometimes a gradation to mixed deciduous woodland of the Fraxinus-Acer-Mercurialis or Fraxinus-Sorbus-Mecurialis types. However, although many sites may formerly have had a more extensive local woodland cover, the broken terrain on which the community is typically found could never have been densely wooded (Pigott 1958). The Filipendulo-Arrhenatheretum should therefore be regarded as a persistent woodland margin community rather than a serai precursor. The occasional association of the community with old mixed hedgerows is interesting in this respect.""",
  'mg3': """Stands of the Anthoxanthum-Geranium community occur most frequently in fields bounded by walls or fences and each subject to a more or less uniform treatment regime. Spatial zonations between the sub-communities are therefore infrequent, although neglected corners and margins of fields with either the Briza or the Bromus sub-community may show a narrow transition to the Arrhenatherum sub-community. The blue-violet flowers of Geranium pratense often mark out this sub-community in summer. On verges which have a less systematic treatment such transitions are more common and irregular. The local appearance of mire species in stands of the Anthoxanthum-Geranium community may form part of a transition to flush vegetation where drainage of soil water is strongly impeded. The types of mire involved in such sequences depend on the calcium status and pH of the ground water and include the Pinguiculo-Caricetum and the Molinia-Crepis fen. Along stream sides where there is seasonal inundation a tall-herb Filipendulion mire may terminate the sequence. The striking floristic similarity between the Anthoxanthum-Geranium community and the field layer of open stands of the Fraxinus-Sorbus-Mercurialis and Alnus-Fraxinus-Lysimachia woodlands strongly suggests that this meadow vegetation has developed by canopy clearance and is maintained by annual mowing which excludes tall dominants (Pigott 1956a, Bradshaw 1962). Zonations between the community and such woodland are rare but occasionally the two vegetation types occur contiguously on identical sites separated only by a boundary wall. In Scandinavia, very similar meadow vegetation is mown in the clearings of such open woodland (Nordhagen 1928, Sjörs 1954; see ‘Affinities’ below). Traditional treatment has maintained the community in all its richness but the vegetation of the Bromus sub-community represents one stage in a process of increasing the productivity and decreasing the floristic diversity of hay-meadows in response to various combinations of fertiliser application, ploughing and re-seeding. This seems eventually to convert the vegetation to the Holcus-Trifolium sub-community of Festuca-Agrostis-Galium grassland or the Anthoxanthum sub-community of the Lolio-Cynosuretum.""",
  'mg4': """Stands of the community frequently show considerable variation in the abundance of particular species. Some of this is related to the distinctive bushy (e.g. S. officinalis and F. ulmaria) or tussock (e.g. larger grasses) habit of certain components but local variations in treatment, such as differences in mowing-time, continued over long periods, may also have an effect (Ratcliffe 1977). Zonations to other communities are most frequently related to differences in soil moisture status. Damp hollows in meadows sometimes show gradations to the Holcus lanatus-Deschampsia cespitosa community or to the Holco-Juncetum, especially the Juncus inflexus sub-community on more base-rich soils. These in turn may give way to Carex acutiformis swamp. Sharper zonations of this kind can sometimes be seen bordering the older drainage ditches which frequently traverse the meadows or in such places there may be an abrupt switch to the Agrostis stolonifera-Alopecurus geniculatus inundation grassland. Modern ditches around the meadows often have linear stands of Salix spp. or Alnus on their banks. Changes in treatment practice can alter the composition of the Alopecurus-Sanguisorba community and may initiate successions to other grassland types. An extension of grazing into the spring reduces the abundance of some of the most distinctive species of the community such as Sanguisorba officinalis, Silaum silaus and Fritillaria meleagris, all of which are highly palatable. This is the major community in Britain for F. meleagris and, if grazing is continued into its flowering period in late April to early May, it cannot set seed. At Marston Meadows in Staffordshire, a change from mowing to late spring grazing over the last 20 years has extensively reduced its cover (Ratcliffe 1977). It can, however, remain dormant in the soil for a number of years and seems able to recolonise fields from margins or ditch edges. If stands are ungrazed over the winter months, coarse grasses such as Arrhenatherum elatius (in drier places) and Deschampsia cespitosa (in wetter areas) may expand and eventually form stands of the Arrhenatheretum or the Holcus lanatus-Deschampsia cespitosa community. Drainage, ploughing, re-seeding or the addition of artificial fertilisers can all have a more drastic effect on the vegetation. Combined with an increase in grazing, such changes probably convert the community to the Lolium perenne-Alopecurus pratensis-Festuca pratensis flood-pasture or to the Lolio-Cynosuretum.""",
  'mg5': """Zonations in the Centaureo-Cynosuretum are usually related to edaphic patterns and, even in enclosed fields subject to a uniform treatment, there may be soil differences which reflect heterogeneities in the parent material. Within the Galium sub-community, an increase in Mesobromion species (such as Koeleria macrantha and Sanguisorba minor) is often related to a rise in calcium content and pH as the soil thins towards limestone exposures. Such patterns are commonly part of a complete transition from the Centaureo-Cynosuretum to calcicolous grassland on the Carboniferous Limestone of the Yorkshire Dales where meadows on till or head abut on to, or surround, rocky outcrops (cf. Ivimey-Cook & Proctor 1966b on comparable zonations in The Burren). In a similar fashion, there may be an increase of species typical of calcifugous grasslands and heaths in the Danthonia sub-community where its characteristic brown earths grade to rankers or podzolised soils over siliceous material. The patchy occurrence of Juncus spp. or F. ulmaria within stands of the Centaureo-Cynosuretum represents truncated zonations to the Holco-Juncetum or Filipendulion mires which are mediated by the soil moisture status. Such patterns are a common feature of meadows on undulating topography and frequently accentuate ridge-and-furrow with fragmentary strips of F. ulmaria or Juncus spp. on the less well-drained soils of the furrows. Alongside streams there may be a more complete gradation to poorfen vegetation. Occasionally, differences in treatment may be evident as zonations within enclosed meadows as, for example, where narrow belts of rich Centaureo-Cynosuretum remain on steeper banks within fields or around margins which have escaped improvement. Generally, however, differences in treatment style have a gradual successional effect upon the community which is evident in a range of intermediates between the Centaureo-Cynosuretum and more improved and productive grassland types. Two changes of practice are of particular importance. The first is an increase of grazing pressure. Growth starts quite early in the regions where the community occurs and stands may provide a valuable supplementary bite towards the end of April. If grazing is continued into the summer, and especially if it is heavy, there is an eventual decrease in the richness of the sward. Early-flowering species such as Orchis morio are then unable to set seed and there is a gradual expansion of rosette hemicryptophytes. The occurrence of the poisonous Colchicum autumnale in stands of the community has sometimes led to their being set aside for hay but some farmers have destroyed this species so as to allow an expansion of grazing. In fact, C. autumnale is more toxic during the early part of the season than in summer (Butcher 1954). Frequent mowing of the community, as occurs in some churchyards and on some verges and lawns, appears to have a similar effect to an increase in grazing. Although such treatment may permit the survival of an impoverished form of the Centaureo-Cynosuretum, the trend is for the sward to be converted eventually to the Lolio-Cynosuretum. This change may be further encouraged by the second, now very widespread, alteration in treatment. This is the replacement of the traditional farmyard manure by artificial mineral fertilisers. These enhance the growth of the grasses to the detriment of the dicotyledons. Lotus corniculatus and Leontodon hispidus are often the first species to be lost from the vegetation but a much greater impoverishment accompanies the rise in productivity in the long term. More drastic treatments of the community involve ploughing or the use of total weedkillers such as paraquat and re-seeding to produce Lolio-Cynosuretum or various kinds of ley. Such artificial successions to pasture depend ultimately on the maintenance of grazing. When the Centaureo-Cynosuretum or its derivatives are ungrazed, there is an expansion of coarser grasses and an eventual invasion of shrubs. The Lathyrus and Galium sub-communities seem to progress to various types of Arrhenatheretum or, on more calcareous soils, to one of the coarser Mesobromion swards. The exact nature of the succession may also be influenced by the fertiliser regime on the original meadow. Ungrazed stands of the Danthonia sub-community may be directly invaded by heath shrubs or Ulex europeaus. The results of careless grazing are sometimes evident as mosaics of Centaureo-Cynosuretum with patches of coarse grassland or heath. Distribution Stands of the community occur throughout the British lowlands but the centre of distribution is on the claylands of the Midlands. Even here, however, agricultural improvement has drastically reduced the extent of the community. The sub-communities are distributed largely in relation to local and regional variations in soil type. The Lathyrus sub-community is the most widespread type with the Galium sub-community showing a more restricted occurrence, largely over calcareous bedrocks. The Danthonia sub-community extends the altitudinal range of the community on to the upland margins of the Welsh borderlands and northern England. In the harsh montane climate of the northern Pennines the community is replaced by the Anthoxanthum-Geranium community. As with this other increasingly restricted meadow type, verge stands provide a valuable reserve.""",
  'mg6': """The application of careful uniform treatment within enclosed pasture stands of the Lolio-Cynosuretum tends to minimise the occurrence of zonations. However, where past improvement has been uneven, transitions may remain. Steeper banks inaccessible to ploughing may still carry patches of Centaureo-Cynosuretum as remnants of previous meadow vegetation. Hollows resistant to drainage may have the Holcus-Deschampsia community or Holco-Juncetum; the Deschampsia and Iris variants of the Typical sub-community can be seen as truncated zonations to such vegetation which occur where drainage is less successful. Where rivers and pools are not embanked, the Alopecurus geniculatus variant represents part of a transition to the vegetation of regularly-inundated water margins. Where pastures have been won from rocky upland topography, there may be zonations to calcifugous grasslands (with the Anthoxanthum sub-community) or calcicolous grasslands (with the Trisetum sub-community) as the soil thins to some type of lithomorphic profile around outcrops. The Lolio-Cynosuretum can be derived from a very wide range of vegetation types (Figure 9) including, in extreme cases, communities of stabilised sand-dunes and blanket mire. Certain kinds of agricultural treatment or neglect may allow some of the more closely related types of original unimproved vegetation to replace the Lolio-Cynosuretum. In older pastures, a return to more traditional organic manuring and the withdrawal of summer grazing may permit the re-establishment of the meadow vegetation of the Centaureo-Cynosuretum. This is perhaps more likely in the Anthoxanthum and Trisetum sub-communities where certain meadow species persist or where there are fragments of meadow-sward on banks or adjacent verges. Similarly, the choking of drains may permit the development of extensive Holco-Juncetum. Generally, however, successions involving the Lolio-Cynosuretum appear to be mediated by grazing. Undergrazing allows coarser species to increase their cover and this is sometimes a prelude to the invasion and spread of Arrhenatherum elatius and the development of an Arrhenatheretum. Abandoned pasture often shows a patchy mosaic of the two communities with scattered saplings of Crataegus monogyna. Where grazing is too severe, the sward may be opened up for invasion by weeds and rabbit infestation may speed the run-down to some weed-dominated vegetation. Trampling may be an attendant problem with over-grazing by cattle but is especially important in recreational and amenity stands of the Lolio-Cynosuretum where heavy use along footpaths, around gateways and in goal-mouths may produce a succession to Lolio-Plantaginion vegetation.""",
  'mg7': """None""",
  'mg8': """Enclosed stands of the community in riverside pastures may be subject to uniform treatment and show no zonations to other vegetation types. In some cases, however, improvement and management have been restricted by difficult topography and an inability to prevent flooding. Here, and around the more fragmentary spring and flush stands, there may be zonations related to soil moisture conditions. A usual pattern is for the Cynosurus-Caltha community to give way to inundation communities on the bare substrates of river banks or pool-sides or to small-sedge mires of the Caricion davallianae in base-rich flushes. On drier ground, there may be a transition to the Lolium-Alopecurus-Festuca flood-pasture or, where there has been extensive improvement, directly to Lolio-Cynosuretum. Such a sequence can be seen on the drained levels of West Sedgemoor in Somerset. Artificial drainage can mediate a successional sequence from the Cynosurus-Caltha community to drier pasture types but neglect permits a fairly rapid invasion of Salix spp. and other shrubs and trees of wet woodland.""",
  'mg9': """The community occurs very frequently as part of zonations related to differences in soil moisture status. The Poa sub-community is common in moist hollows within pastures and on grazed verges where there is gleying and it commonly gives way, with a decrease in the cover of D. cespitosa, to Lolio-Cynosuretum or the Lolium-Alopecurus-Festuca community on better-drained soils. Around permanently wet hollows, pools and lakes, the community regularly forms part of an ecotone to some type of fen or swamp or, where there is a frequent rise and fall of water level, as around reservoirs, to a sequence of inundation communities. In many cases, it is possible to discern a range of intermediates between the Holcus-Deschampsia community and its neighbours and, in zonations to fen-meadows, there is, or has been in the past, the further complication of mowing and grazing effects. Such transitional swards may also figure in serai changes that ensue in badly-managed or abandoned pastures and meadows. Once established, D. cespitosa cannot be totally eradicated by continued grazing and, if drainage deteriorates, it will slowly spread to dominate in the Poa sub-community. Even where drainage is improved, preferential grazing of other species may prevent D. cespitosa being ousted by possible competitors. Where there is a reduction of grazing on better-drained land, the Arrhenatherum sub-community may develop from pasture swards. Although a switch to mowing is probably the best form of control of D. cespitosa (Davy 1980), the silting up of ditches within meadows may precipitate a spread of the community. If grazing continues, the Holcus-Deschampsia grassland is maintained as a plagioclimax and, even when it ceases, the densely-tussocky character of the vegetation often severely hinders any establishment of seedling shrubs and trees. Where succession to woodland does occur, it is usually to the Deschampsia sub-communities of the Alnus-Fraxinus-Lysimachia or Fraxinus-Acer-Mercurialis woodlands. Stands of the Holcus-Deschampsia grassland can often be found in rides and clearings in tracts of these kinds of woodlands or planted replacements of them in forests on heavy, clay soils with considerable continuity among the herb flora. In such situations, the Holcus-Deschampsia grassland can provide an important seed source for the spread of D. cespitosa beneath the trees when felling or coppicing increases the light.""",
  'mg10': """The community very commonly occurs in mosaics related to patterns of soil moisture. The Typical sub-community is very frequent as patches and sometimes as extensive stands in damper hollows in the Lolio-Cynosuretum and Centaureo-Cynosuretum and distinctive patterns often reflect the occurrence of ridge-and-furrow or drains that are too widely spaced, rushy strips picking out the wetter bands of soil. The Juncus inflexus sub-community is encountered in less well-drained areas within more calcareous soils in the Alopecurus-Sanguisorba flood-meadow and the more calcicolous types of Centaureo-Cynosuretum. The Iris sub-community occurs in often very prominent patches in alluvial Lolio-Cynosuretum in western river valleys. Where the water-table rises beside streams and pools, the Holco-Juncetum may form part of a complete or partial transition from grassland to swamp, fen or inundation communities. Here, as with the field mosaics, there may be a range of intermediate types of vegetation based on the abundance of the dominant Junci. The Holco-Juncetum commonly develops by the invasion of J. effusus and J. inflexus into established or newly-seeded grasslands. A number of studies have demonstrated that J. effusus produces formidable quantities of seed (Chippindale & Milton 1934, Milton 1936, 1948, Moore & Burr 1948, Salisbury 1964) and that these are readily dispersed by wind, by animals and farm machinery after the seed-coat becomes mucilaginous, and by water (Richards & Clapham 1941b, Salisbury 1964). However, two conditions must be fulfilled for germination and survival of the seedlings: light and soil-surface humidity (Moore & Burr 1948, Lazenby 1955a, b, Agnew 1961). Successful invasion is therefore most readily achieved in a broken or badly-seeded sward where the soil surface does not dry out, conditions which are often met in over-grazed and poached pasture or on ill-drained land that is being put down to leys. Once established, the Holco-Juncetum is not readily eradicated. Grazing alone will not reduce the cover of J. effusus or J. inflexus and both are relatively tolerant of mowing. Systematic drainage, re-seeding and fertilising probably convert the community to the Lolium-Alopecurus-Festuca flood-pasture or Lolio-Cynosuretum but careful pastoral management is necessary to prevent re-infestation. Ungrazed stands may be invaded by shrubs and trees tolerant of wet soils and eventually be converted to scrub and woodland.""",
  'mg11': """Zonations involving the community most frequently reflect patterns of soil moisture and, on salt-marshes, the frequency of inundation of salt-laden water. Inland stands of the Lolium sub-community are frequently rather uniform but, where this vegetation occurs patchily in less well-managed grasslands, it grades, on drier ground, to some form of pasture, such as the Lolio-Cynosuretum or the Lolium-Alopecurus-Festuca community, and, around open water, to the Agrostis stolonifera-Alopecurus geniculatus grassland or to more open inundation communities. Salt-marsh stands of the Lolium sub-community and the Atriplex sub-community often pass down-marsh to some form of the Juncus maritimus community or Juncetum gerardi (such as the Leontodon sub-community or its derivatives). Secondary successions to the latter can sometimes be seen in turf-cuttings in the upper marsh which may be quickly colonised by P. anserina and have temporary stands of the Festuca-Agrostis-Potentilla community. Up-marsh, zonations are frequently terminated artificially by a sea-wall or bank but the community sometimes grades to a less frequently inundated form of pasture, free of halophytes. Similarly, the Honkenya sub-community may form a transition zone between more unstable and halophytic Strandline or shingle vegetation and essentially inland grassland. Festuca arundinacea is a sometimes conspicuous occasional in the Festuca-Agrostis-Potentilla community and probably increases its cover with a relaxation of grazing. Zonations between this community and the Potentillo-Festucetum arundinaceae may therefore be a reflection of successions between these two vegetation types mediated by changes in pasturing intensity.""",
  'mg12': """The Lolium-Holcus sub-community generally shows abrupt zonations to other vegetation types, sharpened by treatment where stands abut on to agricultural land or by sudden topographic differences where stands lie on steep banks alongside ditches. Occasionally, there are more gradual zonations to the Festuca-Agrostis-Potentilla community with increased grazing pressure or, on the upper salt-marsh, to the Oenanthe sub-community on more saline soils. Although this latter sub-community sometimes occurs as extensive pure stands, it is frequently encountered in a mosaic with some form of Juncus maritimus salt-marsh which replaces it on more frequently submerged ground.""",
  'mg13': """Small stands commonly form part of the often fragmentary sequences of communities which develop around fluctuating open waters in relation to frequency of inundation and the amount of disturbance by sediment movement and trampling. A frequent pattern is for an intact pasture sward (such as the typical variant of the typical sub-community of the Lolio-Cynosuretum) to give way through an intermediate (the A. geniculatus variant of the same vegetation) to the Agrostis-Alopecurus community on puddled soil around a pool or stream that is used by stock for watering. On moister silts which are more frequently inundated, this in turn may pass to more ephemeral inundation vegetation or to the Glycerietum fluitantis or related assemblages in the Glycerio-Sparganion. In washlands, the community occurs in mosaics with the Glycerietum fluitantis, the Festuca rubra-Agrostis stolonifera-Potentilla anserina inundation grassland and, around dykes, the Phalaridetum arundinaceae and Glycerietum maximae. Where the community occurs around areas of freshwater seepage on the upper salt-marsh, it may pass to more halophytic vegetation types in which A. stolonifera remains prominent."""
  }

communities_query = """
SELECT
  communities.community_level_code,
  communities.community_code,
  communities.community_name
FROM
  communities
"""

column_names = ['community', 'code', 'name', 'list', 'succession']

communities = list()

def load_table_from_database(database_name, query_string):
    con = sqlite3.connect(database_name)
    cur = con.cursor()

    for row in cur.execute(query_string):
        # print(row[0], row[1], row[2])
        current_row_list = list(row)
        current_row_list.append(list()) # names list
        current_row_list.append(list()) # succession pathways
        current_row = dict(zip(column_names, current_row_list))

        community_name = current_row['name']
        community_name_list = community_name.lower().split(" ")
        current_row['list'] = community_name_list
        # print(current_row)
        communities.append(current_row)

    con.close()

    # for community in communities:
    #     print(community)
    # #     print(community[0], community[1],community[2])


def mapstrip(s):
    return s.strip(".,:() ")


def find_communities(key, succession_string_list):
  # now we have the community names and codes loaded into the list communities
  # and the succession text for mg1 broken into the list mg1_lower_split
  # so now, iterate over the list mg1_lower_split, using the current word to search the community names
  # for the matching first word - then cycle through the next words for each looking for a match
  # maybe pre-prepare the community names in the same way by splitting them by " "

  recognised_communities = list()

  communities_iterator = communities.__iter__()
  # community_iterator = community.__iter__()
  for community in communities_iterator:
      word_iterator = succession_string_list.__iter__()
      for word in word_iterator:
        subcommander = 0
        while ((subcommander < len(community['list'])) and (community['list'][subcommander] == word)):
            # print("Found", subcommander, community['code'], word)
            if (subcommander > 1):
              # print("Recognised", word, subcommander, community['community'], community['code'], community['name'])
              # print("Record", key, "succeeds to", community['community'])
              if (community['community'] not in recognised_communities):
                 recognised_communities.append(community['community'])

            subcommander = subcommander + 1
            word = word_iterator.__next__()
  
  # print("Recognised succession communities", recognised_communities)
  return(recognised_communities)


# word_list = list(map(mapstrip, succession_text['mg1'].lower().split(" ")))
# for word in word_list:
#     print(word)

load_table_from_database("nvc.db", communities_query)

# found = find_communities('mg1'.upper(), list(map(mapstrip, succession_text['mg1'].lower().split(" "))))
# print("Recognised succession communities", found)

for k, v in succession_texts.items():
  # print(k.upper())
  found = find_communities(k.upper(), list(map(mapstrip, v.lower().split(" "))))
  print("Recognised", k.upper(), "succeeds to", found)
