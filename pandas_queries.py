#pandas queries
# pylint: disable=all

"""
to=='MG6' or to=='CG10' or to=='CG14' or to=='OV40' or to=='W20' or to=='M11' or to=='U16' or to=='W17' or to=='H8'

fwd_count>0 and rev_count==0


(to=='MG1' or to=='MG9' or to=='MG10' or to=='OV10' or to=='OV23') or 
(to=='OV8' or to=='OV33' or to=='OV18') or (to=='OV21' or to=='OV12' or to=='OV20' or to=='OV24' or to=='OV19' or to=='OV25') or
(to=='M28' or to=='MG5' or to=='S23' or to=='OV35' or to=='S18' or to=='OV26' or to=='S27' or to=='M13' or to=='W1' or to=='W10' or to=='W8' or to=='MG6' or to=='SD8' or to=='W22' or to=='MG4')
or (to=='SD16' or to=='SD13' or to=='SD11' or to=='H19' or to=='SD7' or to=='SD14' or to=='SD10' or to=='SD4' or to=='SD19' or to=='SD17' or to=='SD6' or to=='SD5' or to=='H11' or to=='OV4' or to=='SD9' or to=='OV27' or to=='CG8' or to=='W12' or to=='OV37' or to=='OV39' or to=='MG2' or to=='OV38' or to=='CG9' or to=='SD18' or to=='W7' or to=='W25' or to=='W16' or to=='W6' or to=='U20' or to=='W15' or to=='W5' or to=='S23' or to=='OV26' or to=='M13' or to=='S18' or to=='M16' or to=='SD15' or to=='M18' or to=='H5' or to=='M27' or to=='W3' or to=='M23' or to=='MG8' or to=='M22' or to=='M17' or to=='H4' or to=='MG13' or to=='M24' or to=='MG11' or to=='MG3' or to=='U3' or to=='CG10' or to=='M28' or to=='SD3' or to=='OV41' or to=='W21' or to=='W24')
and (grazing==1 or flooding==1)




(to=='OV28' or to=='OV29' or to=='OV31') or (to=='OV19' or to=='OV20' or to=='OV21' or to=='OV24' or to=='OV25')




((to=='MG1' or to=='MG9' or to=='MG10' or to=='OV10' or to=='OV23') or (to=='OV8' or to=='OV33' or to=='OV18') or (to=='OV21' or to=='OV12' or to=='OV20' or to=='OV24' or to=='OV19' or to=='OV25') or (to=='M28' or to=='MG5' or to=='S23' or to=='OV35' or to=='S18' or to=='OV26' or to=='S27' or to=='M13' or to=='W1' or to=='W10' or to=='W8' or to=='MG6' or to=='SD8' or to=='W22' or to=='MG4') or (to=='SD16' or to=='SD13' or to=='SD11' or to=='H19' or to=='SD7' or to=='SD14' or to=='SD10' or to=='SD4' or to=='SD19' or to=='SD17' or to=='SD6' or to=='SD5' or to=='H11' or to=='OV4' or to=='SD9' or to=='OV27' or to=='CG8' or to=='W12' or to=='OV37' or to=='OV39' or to=='MG2' or to=='OV38' or to=='CG9' or to=='SD18' or to=='W7' or to=='W25' or to=='W16' or to=='W6' or to=='U20' or to=='W15' or to=='W5' or to=='S23' or to=='OV26' or to=='M13' or to=='S18' or to=='M16' or to=='SD15' or to=='M18' or to=='H5' or to=='M27' or to=='W3' or to=='M23' or to=='MG8' or to=='M22' or to=='M17' or to=='H4' or to=='MG13' or to=='M24' or to=='MG11' or to=='MG3' or to=='U3' or to=='CG10' or to=='M28' or to=='SD3' or to=='OV41' or to=='W21' or to=='W24')) and (grazing==1 or flooding==1)






(to=='MG1' or to=='MG9' or to=='MG10' or to=='OV10' or to=='OV23') or (to=='OV8' or to=='OV33' or to=='OV18') or (to=='OV21' or to=='OV12' or to=='OV20' or to=='OV24' or to=='OV19' or to=='OV25') or (to=='M28' or to=='MG5' or to=='S23' or to=='OV35' or to=='S18' or to=='OV26' or to=='S27' or to=='M13' or to=='W1' or to=='W10' or to=='W8' or to=='MG6' or to=='SD8' or to=='W22' or to=='MG4') or (to=='SD16' or to=='SD13' or to=='SD11' or to=='H19' or to=='SD7' or to=='SD14' or to=='SD10' or to=='SD4' or to=='SD19' or to=='SD17' or to=='SD6' or to=='SD5' or to=='H11' or to=='OV4' or to=='SD9' or to=='OV27' or to=='CG8' or to=='W12' or to=='OV37' or to=='OV39' or to=='MG2' or to=='OV38' or to=='CG9' or to=='SD18' or to=='W7' or to=='W25' or to=='W16' or to=='W6' or to=='U20' or to=='W15' or to=='W5' or to=='S23' or to=='OV26' or to=='M13' or to=='S18' or to=='M16' or to=='SD15' or to=='M18' or to=='H5' or to=='M27' or to=='W3' or to=='M23' or to=='MG8' or to=='M22' or to=='M17' or to=='H4' or to=='MG13' or to=='M24' or to=='MG11' or to=='MG3' or to=='U3' or to=='CG10' or to=='M28' or to=='SD3' or to=='OV41' or to=='W21' or to=='W24') and (grazing==1 or flooding==1)



#final query
( (to=='MG1' or to=='MG9' or to=='MG10' or to=='OV10' or to=='OV23') or (to=='W1' or to=='OV35' or to=='OV26' or to=='M6' or to=='M5' or to=='MG4') ) and ( grazing==1  or flooding==1  )

or
grazing==1 and to in['MG10', 'MG9', 'W1', 'OV26', 'M6', 'M5', 'MG4']

grazing==1 and to in['MG10', 'MG9', 'W1', 'OV26', 'M6', 'M5', 'MG4', 'OV10', 'OV23', 'MG1']

(grazing==1 or flooding==1) and to in['MG10', 'MG9', 'W1', 'OV26', 'M6', 'M5', 'MG4', 'OV10', 'OV23', 'MG1']

or (to in ['OV8','OV33','OV18'])
or (to in ['OV21', 'OV12', 'OV20', 'OV24', 'OV19', 'OV25'])
or (to in ['M28', 'MG5', 'S23', 'OV35', 'S18', 'OV26', 'S27', 'M13', 'W1', 'W10', 'W8', 'MG6', 'SD8', 'W22', 'MG4'])
or (to in ['SD16', 'SD13', 'SD11', 'H19', 'SD7', 'SD14', 'SD10', 'SD4', 'SD19', 'SD17', 'SD6', 'SD5', 'H11', 'OV4', 'SD9', 'OV27', 'CG8', 'W12','OV37','OV39','MG2','OV38','CG9','SD18','W7','W25','W16','W6','U20','W15','W5','S23','OV26','M13','S18','M16','SD15','M18','H5','M27','W3', 'M23', 'MG8', 'M22', 'M17', 'H4', 'MG13', 'M24', 'MG11', 'MG3', 'U3', 'CG10', 'M28', 'SD3', 'OV41', 'W21', 'W24'])



 ( (to in['MG10', 'MG9', 'W1', 'OV26', 'M6', 'M5', 'MG4', 'OV10', 'OV23', 'MG1']) or (to in ['OV8','OV33','OV18']) or (to in ['OV21', 'OV12', 'OV20', 'OV24', 'OV19', 'OV25']) or (to in ['M28', 'MG5', 'S23', 'OV35', 'S18', 'OV26', 'S27', 'M13', 'W1', 'W10', 'W8', 'MG6', 'SD8', 'W22', 'MG4']) or (to in ['SD16', 'SD13', 'SD11', 'H19', 'SD7', 'SD14', 'SD10', 'SD4', 'SD19', 'SD17', 'SD6', 'SD5', 'H11', 'OV4', 'SD9', 'OV27', 'CG8', 'W12','OV37','OV39','MG2','OV38','CG9','SD18','W7','W25','W16','W6','U20','W15','W5','S23','OV26','M13','S18','M16','SD15','M18','H5','M27','W3', 'M23', 'MG8', 'M22', 'M17', 'H4', 'MG13', 'M24', 'MG11', 'MG3', 'U3', 'CG10', 'M28', 'SD3', 'OV41', 'W21', 'W24']) )  and (grazing==1 or flooding==1)


#grazingabandoned



or (to in ['W1', 'OV26', 'OV35', 'MG4', 'W8'])
or (to in ['M6'])




and (grazing==1 or flooding==1 or abandonment==1 or wetting==1 or drying==1 or myxomatosis==1 or mowing==1 or mowingstopped==1 or ploughingstarted==1 or clearance==1 or fire==1 or improvement==1 or grazingstopped==1)

and (grazing==1 and abandonment==1)


( ( to in['MG10', 'MG9', 'OV10', 'OV23', 'MG1'] )  or (to in ['W1', 'OV26', 'M6', 'M5', 'MG4', 'OV35', 'W8', 'M28']) or (to in ['OV27', 'W10']) or (to in ['W24', 'W14', 'W7', 'W16']) ) and (grazing==1 or flooding==1 or abandonment==1 or wetting==1 or drying==1 or fire==1 or improvement==1 or grazingstopped==1)


or (to in ['W24', 'W14', 'W7', 'W16'])
or (to in ['H9', 'W19'])

( ( to in['MG10', 'MG9', 'OV10', 'OV23', 'MG1'] )  or (to in ['W1', 'OV26', 'M6', 'M5', 'MG4', 'OV35', 'W8', 'M28']) or (to in ['OV27', 'W10']) or (to in ['W24', 'W14', 'W7', 'W16'])  or (to in ['H9', 'W19']) ) and (grazing==1 or flooding==1 or abandonment==1 or wetting==1 or drying==1 or fire==1 or improvement==1 or grazingstopped==1)



# use the below query to explore PER SUCCESSION REASON the potential succession pathways to the MAVIS communities
( ( to in['MG10', 'MG9', 'OV10', 'OV23', 'MG1'] )  or (to in ['W1', 'OV26', 'M6', 'M5', 'MG4', 'OV35', 'W8', 'M28', 'MG6']) or (to in ['OV27', 'W10']) or (to in ['W24', 'W14', 'W7', 'W16'])  or (to in ['H9', 'W19']) ) and (grazing==1 or flooding==1 or abandonment==1 or wetting==1 or drying==1 or fire==1 or improvement==1 or grazingstopped==1)


# just for drying-related conditions
(((wetting==1 or flooding==1) and abandonment==1) or drying==1) and ( (to in ['MG10', 'MG9', 'MG1', 'OV10', 'OV23']) or (to in ['MG6', 'W8', 'W10']) or (to in ['M6', 'W7', 'W14', 'W16']))




--------------------------
start again with networks 28/4/24

start:  ( (to in ['MG1', 'MG9', 'MG10', 'OV10', 'OV23'])

step 1:
  or (to in ['OV8', 'OV33', 'OV18', 'OV21', 'OV25', 'OV19', 'OV20', 'OV12', 'OV24', 'OV35', 'S18', 'OV26', 'W1', 'S27', 'W22', 'W10', 'MG4', 'MG6', 'W8', 'SD8', 'M28', 'S23', 'M13', 'S24'])


step 2:
or (to in ['OV31', 'OV29', 'OV8', 'OV9', 'OV22', 'OV3', 'OV41', 'SD3', 'SD9', 'OV4', 'SD14', 'SD5', 'SD17', 'SD19', 'SD7', 'SD6', 'H11', 'SD4', 'SD13', 'SD16', 'SD12', 'SD10', 'SD11', 'SD18', 'W25', 'W6', 'W15', 'W16', 'U20', 'W7', 'MG2', 'CG8', 'OV39', 'OV38', 'OV37', 'CG9', 'M6', 'W5', 'M23', 'M27', 'M18', 'H5', 'M16', 'SD15', 'M22', 'M24', 'U3', 'CG10', 'M17', 'MG8', 'MG11', 'MG13', 'H4', 'MG3', 'S7', 'S3', 'S17', 'A4', 'S5', 'S13', 'M9', 'W2', 'M26', 'W3', 'S1', 'M5', 'S9', 'S12', 'A13', 'A10'])


step 3:
or (to in ['S2', 'A8', 'A7', 'A22', 'A9', 'A12', 'M12', 'M7', 'M32', 'M3', 'H7', 'M15', 'H17', 'H14', 'M35', 'H13', 'CG14', 'H15', 'U17', 'OV40', 'U15', 'U19', 'H10', 'H9', 'U21', 'OV39', 'OV37', 'CG6', 'W13', 'SD4', 'SD13', 'SD14', 'SD19', 'SD6', 'SD5', 'SD2', 'MC6', 'OV3', 'OV11', 'OV17', 'OV36', 'OV16', 'OV8', 'OV31'])


step 4:
or (to in ['A5', 'A3', 'A11', 'A23', 'A14', 'A24', 'A17', 'M31', 'M34', 'M33', 'U11', 'H16', 'U12', 'U18', 'U9', 'H20', 'U13', 'U14', 'OV40', 'CG13', 'H6', 'OV34', 'CG1', 'CG7', 'OV1', 'SD1', 'S22', 'OV30', 'OV1', 'M31', 'A19', 'CG5', 'CG4', 'CG3'])   )

or (to in [ 'S22', 'OV30', 'OV1', 'M31', 'A19'])

or (to in ['CG5', 'CG4', 'CG3'])


-----------------------
Final query for nodes connecting TO the MAVIS set

( ( to in['MG10', 'MG9', 'OV10', 'OV23', 'MG1'] )  or (to in ['OV8', 'OV33', 'OV18', 'OV19', 'OV21', 'OV25', 'OV20', 'OV12', 'OV24',   'OV35', 'S18', 'OV26', 'W1', 'S27', 'W22', 'W10', 'MG4', 'MG6', 'W8', 'MG5', 'SD8', 'M28', 'S23', 'M13', 'S24'])  or (to in ['OV31', 'OV29', 'OV8', 'OV9', 'OV22', 'OV3', 'OV41', 'SD3', 'SD9', 'OV4', 'SD14', 'SD5', 'SD17', 'SD19', 'SD7', 'SD6', 'H11', 'SD4', 'SD13', 'H19', 'SD16', 'SD12', 'SD10', 'SD11', 'SD18', 'W25', 'W6', 'W15', 'W16', 'U20', 'W7', 'MG2', 'CG8', 'OV39', 'W12', 'OV38', 'OV37', 'CG9', 'M6', 'W5', 'M23', 'M27', 'M18', 'H5', 'M16', 'SD15', 'M22', 'M24', 'U3', 'CG10', 'M17', 'MG8', 'MG11', 'MG13', 'H4', 'MG3', 'S26', 'S7', 'S3', 'S17', 'A4', 'S5', 'S13', 'M9', 'W2', 'W4', 'M26', 'W3', 'S1', 'M5', 'S9', 'S12', 'A13', 'A10']) or (to in ['S2', 'A8', 'A7', 'A22', 'A9', 'A12', 'H3', 'M12', 'M7', 'M8', 'M32', 'M3', 'U10', 'H7', 'M15', 'H17', 'H14', 'M35', 'H22', 'U7', 'H13', 'H18', 'CG12', 'CG14', 'H15', 'U17', 'OV40', 'U15', 'CG11', 'U19', 'W20', 'M38', 'H10', 'H9', 'U21', 'H1', 'OV39', 'OV37', 'H2', 'U1', 'CG6', 'W13', 'SD4', 'SD13', 'SD14', 'SD19', 'SD6', 'SD5', 'SD2', 'MC6', 'OV3', 'OV11', 'OV17', 'OV36', 'OV16', 'OV8', 'OV31'])  or (to in ['A5', 'A3', 'A11', 'A23', 'A14', 'A24', 'A17', 'M31', 'M34', 'M33', 'U11', 'H16', 'U12', 'U18', 'U9', 'H20', 'U13', 'U16', 'U14', 'OV40', 'CG13', 'M37', 'H6', 'OV34', 'CG1', 'CG7', 'OV1', 'SD1'])  or (to in ['CG2', 'S22', 'OV30', 'OV1', 'M31', 'A19'])  or (to in ['CG5', 'CG4', 'CG3'])  )




-------
Fig 14 MC9 succession pathway

grazing==1 and ( (to in ['MC9'])  or (to in ['W21', 'H8', 'H7', 'MC10'])  or (to in ['H2', 'MC8', 'H3', 'W8'])  )


Fig 15 MG1 / CG2 pathway

(grazing==1 or flooding==1 or abandonment==1 or myxomatosis==1 or drying==1 or clearance==1) and ( (to in ['CG2', 'MG1', 'CG4', 'CG3', 'W8', 'CG1', 'CG7', 'U1', 'OV27']) )


Fig 16 MG10 pathways

(grazing==1 ) and ( (to in ['MG10', 'W8', 'OV26', '', 'W1', 'OV35', 'W10', 'S24']) or (to in ['W7', 'OV27', 'W14', 'W16', 'M22', 'W2', 'M6', 'M24', '', 'H8', 'U3', 'MG8', 'MG4']) or (to in ['M23', 'M7', 'M5']) or (to in ['M25', 'U4', 'M28', 'M26']) or (to in ['W17', 'W11', 'U5', 'U19', 'OV37', 'H10', 'M10']) or (to in ['U6', 'H7', 'U16', 'H12', 'M27', 'H22', 'H21', 'M35', 'H2']) or (to in ['U18', 'M20', 'U20', 'M13', 'W5', 'W6', 'S25'   ]) )


Fig 17 MG9 pathways

( (to in ['MG9', 'MG4', 'MG6', 'W10', 'W22', 'W8', 'MG10' ])  ) and (grazing==1 or flooding==1 or wetting==1 or drying==1)

( (to in ['MG9', 'MG4', 'MG6', 'W10', 'W22', 'W8', 'MG10' ])  ) and (grazing==1)


Fig 18
OV10, OV23



Fig 19

( to in['MG10', 'MG9', 'OV10', 'OV23', 'MG1'] )


Fig 20

( ( to in['MG10', 'MG9', 'OV10', 'OV23', 'MG1'] ) or (to in ['']) )





Query for just pathways incoming to MAVIS communities

( (to in ['MG1', 'MG9', 'MG10', 'OV10', 'OV23'])  or (to in ['OV8', 'OV33', 'OV18', 'OV21', 'OV25', 'OV19', 'OV20', 'OV12', 'OV24', 'OV35', 'S18', 'OV26', 'W1', 'S27', 'W22', 'W10', 'MG4', 'MG6', 'W8', 'SD8', 'M28', 'S23', 'M13', 'S24']) or (to in ['OV31', 'OV29', 'OV8', 'OV9', 'OV22', 'OV3', 'OV41', 'SD3', 'SD9', 'OV4', 'SD14', 'SD5', 'SD17', 'SD19', 'SD7', 'SD6', 'H11', 'SD4', 'SD13', 'SD16', 'SD12', 'SD10', 'SD11', 'SD18', 'W25', 'W6', 'W15', 'W16', 'U20', 'W7', 'MG2', 'CG8', 'OV39', 'OV38', 'OV37', 'CG9', 'M6', 'W5', 'M23', 'M27', 'M18', 'H5', 'M16', 'SD15', 'M22', 'M24', 'U3', 'CG10', 'M17', 'MG8', 'MG11', 'MG13', 'H4', 'MG3', 'S7', 'S3', 'S17', 'A4', 'S5', 'S13', 'M9', 'W2', 'M26', 'W3', 'S1', 'M5', 'S9', 'S12', 'A13', 'A10']) or (to in ['S2', 'A8', 'A7', 'A22', 'A9', 'A12', 'M12', 'M7', 'M32', 'M3', 'H7', 'M15', 'H17', 'H14', 'M35', 'H13',  'H15', 'U17', 'OV40', 'U15', 'U19', 'H10', 'H9', 'U21', 'OV39', 'OV37', 'CG6', 'W13', 'SD4', 'SD13', 'SD14', 'SD19', 'SD6', 'SD5', 'SD2', 'MC6', 'OV3', 'OV11', 'OV17', 'OV36', 'OV16', 'OV8', 'OV31']) or (to in ['A5', 'A3', 'A11', 'A23', 'A14', 'A24', 'A17', 'M31', 'M34', 'M33', 'U11', 'H16', 'U12', 'U18', 'U9', 'H20', 'U13', 'U14', 'OV40', 'CG13', 'H6', 'OV34', 'CG1', 'CG7', 'OV1', 'SD1', 'S22', 'OV30', 'OV1', 'M31', 'A19', 'CG5', 'CG4', 'CG3'])   ) and ( grazing==1 or flooding==1  or wetting==1 or drying==1  or grazingstopped==1 or clearance==1 or abandonment==1 or fire==1 or ploughingstopped==1 or myxomatosis==1 or mowing==1 or mowingstopped==1 or improvement==1 )





"""