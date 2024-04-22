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
( ( to in['MG10', 'MG9', 'OV10', 'OV23', 'MG1'] )  or (to in ['W1', 'OV26', 'M6', 'M5', 'MG4', 'OV35', 'W8', 'M28']) or (to in ['OV27', 'W10']) or (to in ['W24', 'W14', 'W7', 'W16'])  or (to in ['H9', 'W19']) ) and (grazing==1 or flooding==1 or abandonment==1 or wetting==1 or drying==1 or fire==1 or improvement==1 or grazingstopped==1)



"""