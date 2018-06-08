AMR_HEADERS = ['ORF_ID', 'Start', 'Stop', 'Orientation', 'Best_Identities', 'Best_Hit_ARO']

ARGS_DICT={'disable_serotype':False,'disable_vf':False,'pi':90, 'options':{'vf': True, 'amr': True, 'serotype': True}}

set_spfyids_o157 = set([u'https://www.github.com/superphy#spfy3418', u'https://www.github.com/superphy#spfy3419', u'https://www.github.com/superphy#spfy3412', u'https://www.github.com/superphy#spfy3413', u'https://www.github.com/superphy#spfy3414', u'https://www.github.com/superphy#spfy3415', u'https://www.github.com/superphy#spfy3416', u'https://www.github.com/superphy#spfy3417', u'https://www.github.com/superphy#spfy597', u'https://www.github.com/superphy#spfy596', u'https://www.github.com/superphy#spfy595', u'https://www.github.com/superphy#spfy594', u'https://www.github.com/superphy#spfy593', u'https://www.github.com/superphy#spfy592', u'https://www.github.com/superphy#spfy591', u'https://www.github.com/superphy#spfy590', u'https://www.github.com/superphy#spfy599', u'https://www.github.com/superphy#spfy598', u'https://www.github.com/superphy#spfy93', u'https://www.github.com/superphy#spfy92', u'https://www.github.com/superphy#spfy91', u'https://www.github.com/superphy#spfy90', u'https://www.github.com/superphy#spfy94', u'https://www.github.com/superphy#spfy4709', u'https://www.github.com/superphy#spfy1825', u'https://www.github.com/superphy#spfy1822', u'https://www.github.com/superphy#spfy1820', u'https://www.github.com/superphy#spfy1829', u'https://www.github.com/superphy#spfy5254', u'https://www.github.com/superphy#spfy1458', u'https://www.github.com/superphy#spfy1459', u'https://www.github.com/superphy#spfy2290', u'https://www.github.com/superphy#spfy1452', u'https://www.github.com/superphy#spfy1453', u'https://www.github.com/superphy#spfy1450', u'https://www.github.com/superphy#spfy1451', u'https://www.github.com/superphy#spfy1456', u'https://www.github.com/superphy#spfy1457', u'https://www.github.com/superphy#spfy1454', u'https://www.github.com/superphy#spfy1455', u'https://www.github.com/superphy#spfy1751', u'https://www.github.com/superphy#spfy1753', u'https://www.github.com/superphy#spfy1752', u'https://www.github.com/superphy#spfy1755', u'https://www.github.com/superphy#spfy1754', u'https://www.github.com/superphy#spfy1757', u'https://www.github.com/superphy#spfy1756', u'https://www.github.com/superphy#spfy1697', u'https://www.github.com/superphy#spfy2324', u'https://www.github.com/superphy#spfy4439', u'https://www.github.com/superphy#spfy4438', u'https://www.github.com/superphy#spfy4598', u'https://www.github.com/superphy#spfy3959', u'https://www.github.com/superphy#spfy4599', u'https://www.github.com/superphy#spfy3814', u'https://www.github.com/superphy#spfy1443', u'https://www.github.com/superphy#spfy5248', u'https://www.github.com/superphy#spfy2958', u'https://www.github.com/superphy#spfy4644', u'https://www.github.com/superphy#spfy4645', u'https://www.github.com/superphy#spfy4646', u'https://www.github.com/superphy#spfy4647', u'https://www.github.com/superphy#spfy4640', u'https://www.github.com/superphy#spfy4641', u'https://www.github.com/superphy#spfy4642', u'https://www.github.com/superphy#spfy4643', u'https://www.github.com/superphy#spfy244', u'https://www.github.com/superphy#spfy4648', u'https://www.github.com/superphy#spfy4649', u'https://www.github.com/superphy#spfy2355', u'https://www.github.com/superphy#spfy5253', u'https://www.github.com/superphy#spfy148', u'https://www.github.com/superphy#spfy149', u'https://www.github.com/superphy#spfy1133', u'https://www.github.com/superphy#spfy4310', u'https://www.github.com/superphy#spfy4851', u'https://www.github.com/superphy#spfy4850', u'https://www.github.com/superphy#spfy4853', u'https://www.github.com/superphy#spfy4852', u'https://www.github.com/superphy#spfy1783', u'https://www.github.com/superphy#spfy1780', u'https://www.github.com/superphy#spfy1785', u'https://www.github.com/superphy#spfy2776', u'https://www.github.com/superphy#spfy3622', u'https://www.github.com/superphy#spfy3621', u'https://www.github.com/superphy#spfy3620', u'https://www.github.com/superphy#spfy1719', u'https://www.github.com/superphy#spfy1715', u'https://www.github.com/superphy#spfy1714', u'https://www.github.com/superphy#spfy1716', u'https://www.github.com/superphy#spfy1711', u'https://www.github.com/superphy#spfy1712', u'https://www.github.com/superphy#spfy1917', u'https://www.github.com/superphy#spfy1913', u'https://www.github.com/superphy#spfy1858', u'https://www.github.com/superphy#spfy1859', u'https://www.github.com/superphy#spfy1856', u'https://www.github.com/superphy#spfy1857', u'https://www.github.com/superphy#spfy1854', u'https://www.github.com/superphy#spfy1855', u'https://www.github.com/superphy#spfy1852', u'https://www.github.com/superphy#spfy1853', u'https://www.github.com/superphy#spfy1851', u'https://www.github.com/superphy#spfy2913', u'https://www.github.com/superphy#spfy2916', u'https://www.github.com/superphy#spfy2918', u'https://www.github.com/superphy#spfy1769', u'https://www.github.com/superphy#spfy1767', u'https://www.github.com/superphy#spfy2253', u'https://www.github.com/superphy#spfy4446', u'https://www.github.com/superphy#spfy365', u'https://www.github.com/superphy#spfy366', u'https://www.github.com/superphy#spfy4445', u'https://www.github.com/superphy#spfy360', u'https://www.github.com/superphy#spfy361', u'https://www.github.com/superphy#spfy362', u'https://www.github.com/superphy#spfy363', u'https://www.github.com/superphy#spfy4708', u'https://www.github.com/superphy#spfy218', u'https://www.github.com/superphy#spfy2863', u'https://www.github.com/superphy#spfy4688', u'https://www.github.com/superphy#spfy4689', u'https://www.github.com/superphy#spfy5273', u'https://www.github.com/superphy#spfy5280', u'https://www.github.com/superphy#spfy108', u'https://www.github.com/superphy#spfy109', u'https://www.github.com/superphy#spfy103', u'https://www.github.com/superphy#spfy4616', u'https://www.github.com/superphy#spfy106', u'https://www.github.com/superphy#spfy107', u'https://www.github.com/superphy#spfy2225', u'https://www.github.com/superphy#spfy3409', u'https://www.github.com/superphy#spfy1060', u'https://www.github.com/superphy#spfy587', u'https://www.github.com/superphy#spfy588', u'https://www.github.com/superphy#spfy426', u'https://www.github.com/superphy#spfy4868', u'https://www.github.com/superphy#spfy3035', u'https://www.github.com/superphy#spfy4865', u'https://www.github.com/superphy#spfy4867', u'https://www.github.com/superphy#spfy4862', u'https://www.github.com/superphy#spfy4863', u'https://www.github.com/superphy#spfy3668', u'https://www.github.com/superphy#spfy3663', u'https://www.github.com/superphy#spfy3662', u'https://www.github.com/superphy#spfy3661', u'https://www.github.com/superphy#spfy3660', u'https://www.github.com/superphy#spfy5245', u'https://www.github.com/superphy#spfy1449', u'https://www.github.com/superphy#spfy1448', u'https://www.github.com/superphy#spfy1445', u'https://www.github.com/superphy#spfy1444', u'https://www.github.com/superphy#spfy1447', u'https://www.github.com/superphy#spfy1446', u'https://www.github.com/superphy#spfy1441', u'https://www.github.com/superphy#spfy4088', u'https://www.github.com/superphy#spfy1442', u'https://www.github.com/superphy#spfy1725', u'https://www.github.com/superphy#spfy1727', u'https://www.github.com/superphy#spfy1720', u'https://www.github.com/superphy#spfy4653', u'https://www.github.com/superphy#spfy1728', u'https://www.github.com/superphy#spfy1684', u'https://www.github.com/superphy#spfy4718', u'https://www.github.com/superphy#spfy4719', u'https://www.github.com/superphy#spfy1968', u'https://www.github.com/superphy#spfy4717', u'https://www.github.com/superphy#spfy1967', u'https://www.github.com/superphy#spfy2949', u'https://www.github.com/superphy#spfy43', u'https://www.github.com/superphy#spfy2940', u'https://www.github.com/superphy#spfy4713', u'https://www.github.com/superphy#spfy1438', u'https://www.github.com/superphy#spfy1439', u'https://www.github.com/superphy#spfy1430', u'https://www.github.com/superphy#spfy1431', u'https://www.github.com/superphy#spfy1432', u'https://www.github.com/superphy#spfy1433', u'https://www.github.com/superphy#spfy1434', u'https://www.github.com/superphy#spfy1435', u'https://www.github.com/superphy#spfy1436', u'https://www.github.com/superphy#spfy1437', u'https://www.github.com/superphy#spfy4657', u'https://www.github.com/superphy#spfy4656', u'https://www.github.com/superphy#spfy4655', u'https://www.github.com/superphy#spfy4654', u'https://www.github.com/superphy#spfy258', u'https://www.github.com/superphy#spfy259', u'https://www.github.com/superphy#spfy4651', u'https://www.github.com/superphy#spfy4650', u'https://www.github.com/superphy#spfy4716', u'https://www.github.com/superphy#spfy255', u'https://www.github.com/superphy#spfy4714', u'https://www.github.com/superphy#spfy257', u'https://www.github.com/superphy#spfy4712', u'https://www.github.com/superphy#spfy2261', u'https://www.github.com/superphy#spfy4710', u'https://www.github.com/superphy#spfy4711', u'https://www.github.com/superphy#spfy5308', u'https://www.github.com/superphy#spfy5258', u'https://www.github.com/superphy#spfy5259', u'https://www.github.com/superphy#spfy1698', u'https://www.github.com/superphy#spfy4652', u'https://www.github.com/superphy#spfy4447', u'https://www.github.com/superphy#spfy4444', u'https://www.github.com/superphy#spfy4442', u'https://www.github.com/superphy#spfy1097', u'https://www.github.com/superphy#spfy4443', u'https://www.github.com/superphy#spfy4440', u'https://www.github.com/superphy#spfy4441', u'https://www.github.com/superphy#spfy476', u'https://www.github.com/superphy#spfy478', u'https://www.github.com/superphy#spfy3612', u'https://www.github.com/superphy#spfy2710', u'https://www.github.com/superphy#spfy3619', u'https://www.github.com/superphy#spfy4285', u'https://www.github.com/superphy#spfy1841', u'https://www.github.com/superphy#spfy1840', u'https://www.github.com/superphy#spfy1843', u'https://www.github.com/superphy#spfy1842', u'https://www.github.com/superphy#spfy1845', u'https://www.github.com/superphy#spfy1844', u'https://www.github.com/superphy#spfy1847', u'https://www.github.com/superphy#spfy600', u'https://www.github.com/superphy#spfy1849', u'https://www.github.com/superphy#spfy1848', u'https://www.github.com/superphy#spfy609', u'https://www.github.com/superphy#spfy608', u'https://www.github.com/superphy#spfy2900', u'https://www.github.com/superphy#spfy5234', u'https://www.github.com/superphy#spfy1576', u'https://www.github.com/superphy#spfy5231', u'https://www.github.com/superphy#spfy1779', u'https://www.github.com/superphy#spfy1778', u'https://www.github.com/superphy#spfy1470', u'https://www.github.com/superphy#spfy1471', u'https://www.github.com/superphy#spfy1773', u'https://www.github.com/superphy#spfy1772', u'https://www.github.com/superphy#spfy1771', u'https://www.github.com/superphy#spfy1770', u'https://www.github.com/superphy#spfy1776', u'https://www.github.com/superphy#spfy1775', u'https://www.github.com/superphy#spfy1774', u'https://www.github.com/superphy#spfy359', u'https://www.github.com/superphy#spfy358', u'https://www.github.com/superphy#spfy357', u'https://www.github.com/superphy#spfy170', u'https://www.github.com/superphy#spfy2872', u'https://www.github.com/superphy#spfy2972', u'https://www.github.com/superphy#spfy4690', u'https://www.github.com/superphy#spfy4020', u'https://www.github.com/superphy#spfy2884', u'https://www.github.com/superphy#spfy2886', u'https://www.github.com/superphy#spfy500', u'https://www.github.com/superphy#spfy4623', u'https://www.github.com/superphy#spfy502', u'https://www.github.com/superphy#spfy503', u'https://www.github.com/superphy#spfy3481', u'https://www.github.com/superphy#spfy2988', u'https://www.github.com/superphy#spfy2289', u'https://www.github.com/superphy#spfy2286', u'https://www.github.com/superphy#spfy2283', u'https://www.github.com/superphy#spfy1058', u'https://www.github.com/superphy#spfy137', u'https://www.github.com/superphy#spfy4715', u'https://www.github.com/superphy#spfy4236', u'https://www.github.com/superphy#spfy2053', u'https://www.github.com/superphy#spfy5265', u'https://www.github.com/superphy#spfy1891', u'https://www.github.com/superphy#spfy1896', u'https://www.github.com/superphy#spfy1895', u'https://www.github.com/superphy#spfy1898', u'https://www.github.com/superphy#spfy1899', u'https://www.github.com/superphy#spfy5266', u'https://www.github.com/superphy#spfy1808', u'https://www.github.com/superphy#spfy3022', u'https://www.github.com/superphy#spfy5261', u'https://www.github.com/superphy#spfy3656', u'https://www.github.com/superphy#spfy3657', u'https://www.github.com/superphy#spfy3015', u'https://www.github.com/superphy#spfy3658', u'https://www.github.com/superphy#spfy3659', u'https://www.github.com/superphy#spfy3016', u'https://www.github.com/superphy#spfy336', u'https://www.github.com/superphy#spfy3727', u'https://www.github.com/superphy#spfy3728', u'https://www.github.com/superphy#spfy3729', u'https://www.github.com/superphy#spfy1730', u'https://www.github.com/superphy#spfy1879', u'https://www.github.com/superphy#spfy5278', u'https://www.github.com/superphy#spfy5279', u'https://www.github.com/superphy#spfy1870', u'https://www.github.com/superphy#spfy610', u'https://www.github.com/superphy#spfy1872', u'https://www.github.com/superphy#spfy1873', u'https://www.github.com/superphy#spfy1874', u'https://www.github.com/superphy#spfy1875', u'https://www.github.com/superphy#spfy1877', u'https://www.github.com/superphy#spfy1429', u'https://www.github.com/superphy#spfy1428', u'https://www.github.com/superphy#spfy1423', u'https://www.github.com/superphy#spfy1427', u'https://www.github.com/superphy#spfy1426', u'https://www.github.com/superphy#spfy1425', u'https://www.github.com/superphy#spfy1424', u'https://www.github.com/superphy#spfy4705', u'https://www.github.com/superphy#spfy4704', u'https://www.github.com/superphy#spfy4707', u'https://www.github.com/superphy#spfy261', u'https://www.github.com/superphy#spfy618', u'https://www.github.com/superphy#spfy263', u'https://www.github.com/superphy#spfy262', u'https://www.github.com/superphy#spfy265', u'https://www.github.com/superphy#spfy264', u'https://www.github.com/superphy#spfy267', u'https://www.github.com/superphy#spfy266', u'https://www.github.com/superphy#spfy260', u'https://www.github.com/superphy#spfy4720', u'https://www.github.com/superphy#spfy540', u'https://www.github.com/superphy#spfy2842', u'https://www.github.com/superphy#spfy168', u'https://www.github.com/superphy#spfy169', u'https://www.github.com/superphy#spfy167', u'https://www.github.com/superphy#spfy4972', u'https://www.github.com/superphy#spfy2158', u'https://www.github.com/superphy#spfy4107', u'https://www.github.com/superphy#spfy1647', u'https://www.github.com/superphy#spfy1748', u'https://www.github.com/superphy#spfy1749', u'https://www.github.com/superphy#spfy88', u'https://www.github.com/superphy#spfy89', u'https://www.github.com/superphy#spfy85', u'https://www.github.com/superphy#spfy86', u'https://www.github.com/superphy#spfy87', u'https://www.github.com/superphy#spfy1834', u'https://www.github.com/superphy#spfy1835', u'https://www.github.com/superphy#spfy1830', u'https://www.github.com/superphy#spfy1831', u'https://www.github.com/superphy#spfy1832', u'https://www.github.com/superphy#spfy1838', u'https://www.github.com/superphy#spfy3606', u'https://www.github.com/superphy#spfy2640', u'https://www.github.com/superphy#spfy1467', u'https://www.github.com/superphy#spfy1466', u'https://www.github.com/superphy#spfy1465', u'https://www.github.com/superphy#spfy1464', u'https://www.github.com/superphy#spfy1463', u'https://www.github.com/superphy#spfy1462', u'https://www.github.com/superphy#spfy1461', u'https://www.github.com/superphy#spfy1460', u'https://www.github.com/superphy#spfy1746', u'https://www.github.com/superphy#spfy1469', u'https://www.github.com/superphy#spfy1468', u'https://www.github.com/superphy#spfy4583', u'https://www.github.com/superphy#spfy4581', u'https://www.github.com/superphy#spfy15', u'https://www.github.com/superphy#spfy18', u'https://www.github.com/superphy#spfy340', u'https://www.github.com/superphy#spfy2964', u'https://www.github.com/superphy#spfy1513', u'https://www.github.com/superphy#spfy1512', u'https://www.github.com/superphy#spfy2969', u'https://www.github.com/superphy#spfy1516', u'https://www.github.com/superphy#spfy4639', u'https://www.github.com/superphy#spfy3421', u'https://www.github.com/superphy#spfy3420', u'https://www.github.com/superphy#spfy3423', u'https://www.github.com/superphy#spfy3422', u'https://www.github.com/superphy#spfy3425', u'https://www.github.com/superphy#spfy3424', u'https://www.github.com/superphy#spfy3427', u'https://www.github.com/superphy#spfy3426', u'https://www.github.com/superphy#spfy3428', u'https://www.github.com/superphy#spfy120', u'https://www.github.com/superphy#spfy121', u'https://www.github.com/superphy#spfy401', u'https://www.github.com/superphy#spfy150', u'https://www.github.com/superphy#spfy427', u'https://www.github.com/superphy#spfy589', u'https://www.github.com/superphy#spfy1123', u'https://www.github.com/superphy#spfy2747', u'https://www.github.com/superphy#spfy1887', u'https://www.github.com/superphy#spfy1886', u'https://www.github.com/superphy#spfy5033', u'https://www.github.com/superphy#spfy4846', u'https://www.github.com/superphy#spfy4847', u'https://www.github.com/superphy#spfy4845', u'https://www.github.com/superphy#spfy4848', u'https://www.github.com/superphy#spfy4849', u'https://www.github.com/superphy#spfy3649', u'https://www.github.com/superphy#spfy1709', u'https://www.github.com/superphy#spfy971', u'https://www.github.com/superphy#spfy1703', u'https://www.github.com/superphy#spfy4998', u'https://www.github.com/superphy#spfy974', u'https://www.github.com/superphy#spfy1871', u'https://www.github.com/superphy#spfy5271', u'https://www.github.com/superphy#spfy1869', u'https://www.github.com/superphy#spfy1868', u'https://www.github.com/superphy#spfy1900', u'https://www.github.com/superphy#spfy1863', u'https://www.github.com/superphy#spfy1862', u'https://www.github.com/superphy#spfy1861', u'https://www.github.com/superphy#spfy1860', u'https://www.github.com/superphy#spfy1867', u'https://www.github.com/superphy#spfy5260', u'https://www.github.com/superphy#spfy1864', u'https://www.github.com/superphy#spfy4788', u'https://www.github.com/superphy#spfy4758', u'https://www.github.com/superphy#spfy2928', u'https://www.github.com/superphy#spfy4785', u'https://www.github.com/superphy#spfy2690', u'https://www.github.com/superphy#spfy4787', u'https://www.github.com/superphy#spfy2692', u'https://www.github.com/superphy#spfy607', u'https://www.github.com/superphy#spfy606', u'https://www.github.com/superphy#spfy605', u'https://www.github.com/superphy#spfy5264', u'https://www.github.com/superphy#spfy604', u'https://www.github.com/superphy#spfy603', u'https://www.github.com/superphy#spfy602', u'https://www.github.com/superphy#spfy601', u'https://www.github.com/superphy#spfy2853', u'https://www.github.com/superphy#spfy2851', u'https://www.github.com/superphy#spfy2856', u'https://www.github.com/superphy#spfy2855', u'https://www.github.com/superphy#spfy575', u'https://www.github.com/superphy#spfy4674', u'https://www.github.com/superphy#spfy278', u'https://www.github.com/superphy#spfy279', u'https://www.github.com/superphy#spfy119', u'https://www.github.com/superphy#spfy4600', u'https://www.github.com/superphy#spfy111', u'https://www.github.com/superphy#spfy110', u'https://www.github.com/superphy#spfy282', u'https://www.github.com/superphy#spfy281', u'https://www.github.com/superphy#spfy280'])

BEAUTIFY_VF_SEROTYPE = [
  {
    "analysis": "Serotype",
    "contigid": "n/a",
    "filename": "GCA_000005845.2_ASM584v2_genomic.fna",
    "hitcutoff": "n/a",
    "hitname": "O16:H48",
    "hitorientation": "n/a",
    "hitstart": "n/a",
    "hitstop": "n/a"
  },
  {
    "analysis": "Virulence Factors",
    "contigid": "U00096.3",
    "filename": "GCA_000005845.2_ASM584v2_genomic.fna",
    "hitcutoff": 90,
    "hitname": "EC958",
    "hitorientation": "+",
    "hitstart": 2073473,
    "hitstop": 2074658
  },
  {
    "analysis": "Virulence Factors",
    "contigid": "U00096.3",
    "filename": "GCA_000005845.2_ASM584v2_genomic.fna",
    "hitcutoff": 90,
    "hitname": "ECP",
    "hitorientation": "-",
    "hitstart": 306807,
    "hitstop": 309332
  },
  {
    "analysis": "Virulence Factors",
    "contigid": "U00096.3",
    "filename": "GCA_000005845.2_ASM584v2_genomic.fna",
    "hitcutoff": 90,
    "hitname": "ECP",
    "hitorientation": "-",
    "hitstart": 309358,
    "hitstop": 310075
  },
  {
    "analysis": "Virulence Factors",
    "contigid": "U00096.3",
    "filename": "GCA_000005845.2_ASM584v2_genomic.fna",
    "hitcutoff": 90,
    "hitname": "ECP",
    "hitorientation": "-",
    "hitstart": 310084,
    "hitstop": 310700
  },
  {
    "analysis": "Virulence Factors",
    "contigid": "U00096.3",
    "filename": "GCA_000005845.2_ASM584v2_genomic.fna",
    "hitcutoff": 90,
    "hitname": "ECP",
    "hitorientation": "-",
    "hitstart": 310746,
    "hitstop": 311336
  },
  {
    "analysis": "Virulence Factors",
    "contigid": "U00096.3",
    "filename": "GCA_000005845.2_ASM584v2_genomic.fna",
    "hitcutoff": 90,
    "hitname": "ECS88",
    "hitorientation": "-",
    "hitstart": 3308040,
    "hitstop": 3308924
  },
  {
    "analysis": "Virulence Factors",
    "contigid": "U00096.3",
    "filename": "GCA_000005845.2_ASM584v2_genomic.fna",
    "hitcutoff": 90,
    "hitname": "Z1307",
    "hitorientation": "-",
    "hitstart": 1019013,
    "hitstop": 1020053
  },
  {
    "analysis": "Virulence Factors",
    "contigid": "U00096.3",
    "filename": "GCA_000005845.2_ASM584v2_genomic.fna",
    "hitcutoff": 90,
    "hitname": "Z2203",
    "hitorientation": "-",
    "hitstart": 1588853,
    "hitstop": 1590079
  },
  {
    "analysis": "Virulence Factors",
    "contigid": "U00096.3",
    "filename": "GCA_000005845.2_ASM584v2_genomic.fna",
    "hitcutoff": 90,
    "hitname": "Z2204",
    "hitorientation": "-",
    "hitstart": 1588309,
    "hitstop": 1588839
  },
  {
    "analysis": "Virulence Factors",
    "contigid": "U00096.3",
    "filename": "GCA_000005845.2_ASM584v2_genomic.fna",
    "hitcutoff": 90,
    "hitname": "Z2205",
    "hitorientation": "-",
    "hitstart": 1587793,
    "hitstop": 1588296
  },
  {
    "analysis": "Virulence Factors",
    "contigid": "U00096.3",
    "filename": "GCA_000005845.2_ASM584v2_genomic.fna",
    "hitcutoff": 90,
    "hitname": "Z2206",
    "hitorientation": "-",
    "hitstart": 1586820,
    "hitstop": 1587734
  },
  {
    "analysis": "Virulence Factors",
    "contigid": "U00096.3",
    "filename": "GCA_000005845.2_ASM584v2_genomic.fna",
    "hitcutoff": 90,
    "hitname": "agn43",
    "hitorientation": "+",
    "hitstart": 2071539,
    "hitstop": 2074658
  },
  {
    "analysis": "Virulence Factors",
    "contigid": "U00096.3",
    "filename": "GCA_000005845.2_ASM584v2_genomic.fna",
    "hitcutoff": 90,
    "hitname": "artj",
    "hitorientation": "-",
    "hitstart": 899844,
    "hitstop": 900575
  },
  {
    "analysis": "Virulence Factors",
    "contigid": "U00096.3",
    "filename": "GCA_000005845.2_ASM584v2_genomic.fna",
    "hitcutoff": 90,
    "hitname": "aslA",
    "hitorientation": "-",
    "hitstart": 3984579,
    "hitstop": 3986007
  },
  {
    "analysis": "Virulence Factors",
    "contigid": "U00096.3",
    "filename": "GCA_000005845.2_ASM584v2_genomic.fna",
    "hitcutoff": 90,
    "hitname": "b2972",
    "hitorientation": "-",
    "hitstart": 3113543,
    "hitstop": 3114352
  },
  {
    "analysis": "Virulence Factors",
    "contigid": "U00096.3",
    "filename": "GCA_000005845.2_ASM584v2_genomic.fna",
    "hitcutoff": 90,
    "hitname": "cadA",
    "hitorientation": "-",
    "hitstart": 4356481,
    "hitstop": 4358656
  },
  {
    "analysis": "Virulence Factors",
    "contigid": "U00096.3",
    "filename": "GCA_000005845.2_ASM584v2_genomic.fna",
    "hitcutoff": 90,
    "hitname": "cah",
    "hitorientation": "+",
    "hitstart": 2073486,
    "hitstop": 2074658
  },
  {
    "analysis": "Virulence Factors",
    "contigid": "U00096.3",
    "filename": "GCA_000005845.2_ASM584v2_genomic.fna",
    "hitcutoff": 90,
    "hitname": "cheA",
    "hitorientation": "-",
    "hitstart": 1973360,
    "hitstop": 1975324
  },
  {
    "analysis": "Virulence Factors",
    "contigid": "U00096.3",
    "filename": "GCA_000005845.2_ASM584v2_genomic.fna",
    "hitcutoff": 90,
    "hitname": "cheB",
    "hitorientation": "-",
    "hitstart": 1967452,
    "hitstop": 1968501
  },
  {
    "analysis": "Virulence Factors",
    "contigid": "U00096.3",
    "filename": "GCA_000005845.2_ASM584v2_genomic.fna",
    "hitcutoff": 90,
    "hitname": "cheR",
    "hitorientation": "-",
    "hitstart": 1968504,
    "hitstop": 1969364
  },
  {
    "analysis": "Virulence Factors",
    "contigid": "U00096.3",
    "filename": "GCA_000005845.2_ASM584v2_genomic.fna",
    "hitcutoff": 90,
    "hitname": "cheW",
    "hitorientation": "-",
    "hitstart": 1972836,
    "hitstop": 1973339
  },
  {
    "analysis": "Virulence Factors",
    "contigid": "U00096.3",
    "filename": "GCA_000005845.2_ASM584v2_genomic.fna",
    "hitcutoff": 90,
    "hitname": "cheZ",
    "hitorientation": "-",
    "hitstart": 1966393,
    "hitstop": 1967037
  },
  {
    "analysis": "Virulence Factors",
    "contigid": "U00096.3",
    "filename": "GCA_000005845.2_ASM584v2_genomic.fna",
    "hitcutoff": 90,
    "hitname": "cs3",
    "hitorientation": "-",
    "hitstart": 2994460,
    "hitstop": 2995092
  },
  {
    "analysis": "Virulence Factors",
    "contigid": "U00096.3",
    "filename": "GCA_000005845.2_ASM584v2_genomic.fna",
    "hitcutoff": 90,
    "hitname": "csgD",
    "hitorientation": "-",
    "hitstart": 1102546,
    "hitstop": 1103196
  },
  {
    "analysis": "Virulence Factors",
    "contigid": "U00096.3",
    "filename": "GCA_000005845.2_ASM584v2_genomic.fna",
    "hitcutoff": 90,
    "hitname": "csgG",
    "hitorientation": "-",
    "hitstart": 1100851,
    "hitstop": 1101684
  },
  {
    "analysis": "Virulence Factors",
    "contigid": "U00096.3",
    "filename": "GCA_000005845.2_ASM584v2_genomic.fna",
    "hitcutoff": 90,
    "hitname": "eae",
    "hitorientation": "+",
    "hitstart": 314420,
    "hitstop": 315232
  },
  {
    "analysis": "Virulence Factors",
    "contigid": "U00096.3",
    "filename": "GCA_000005845.2_ASM584v2_genomic.fna",
    "hitcutoff": 90,
    "hitname": "ecpA",
    "hitorientation": "-",
    "hitstart": 310084,
    "hitstop": 310671
  },
  {
    "analysis": "Virulence Factors",
    "contigid": "U00096.3",
    "filename": "GCA_000005845.2_ASM584v2_genomic.fna",
    "hitcutoff": 90,
    "hitname": "ecpB",
    "hitorientation": "-",
    "hitstart": 309358,
    "hitstop": 310026
  },
  {
    "analysis": "Virulence Factors",
    "contigid": "U00096.3",
    "filename": "GCA_000005845.2_ASM584v2_genomic.fna",
    "hitcutoff": 90,
    "hitname": "ecpC",
    "hitorientation": "-",
    "hitstart": 306807,
    "hitstop": 309332
  },
  {
    "analysis": "Virulence Factors",
    "contigid": "U00096.3",
    "filename": "GCA_000005845.2_ASM584v2_genomic.fna",
    "hitcutoff": 90,
    "hitname": "ecpD",
    "hitorientation": "-",
    "hitstart": 305174,
    "hitstop": 306817
  },
  {
    "analysis": "Virulence Factors",
    "contigid": "U00096.3",
    "filename": "GCA_000005845.2_ASM584v2_genomic.fna",
    "hitcutoff": 90,
    "hitname": "ecpE",
    "hitorientation": "-",
    "hitstart": 304497,
    "hitstop": 305250
  },
  {
    "analysis": "Virulence Factors",
    "contigid": "U00096.3",
    "filename": "GCA_000005845.2_ASM584v2_genomic.fna",
    "hitcutoff": 90,
    "hitname": "ecpR",
    "hitorientation": "-",
    "hitstart": 310746,
    "hitstop": 311336
  },
  {
    "analysis": "Virulence Factors",
    "contigid": "U00096.3",
    "filename": "GCA_000005845.2_ASM584v2_genomic.fna",
    "hitcutoff": 90,
    "hitname": "ehaB",
    "hitorientation": "+",
    "hitstart": 392973,
    "hitstop": 394418
  },
  {
    "analysis": "Virulence Factors",
    "contigid": "U00096.3",
    "filename": "GCA_000005845.2_ASM584v2_genomic.fna",
    "hitcutoff": 90,
    "hitname": "entA",
    "hitorientation": "+",
    "hitstart": 628551,
    "hitstop": 629297
  },
  {
    "analysis": "Virulence Factors",
    "contigid": "U00096.3",
    "filename": "GCA_000005845.2_ASM584v2_genomic.fna",
    "hitcutoff": 90,
    "hitname": "entB",
    "hitorientation": "+",
    "hitstart": 627694,
    "hitstop": 628551
  },
  {
    "analysis": "Virulence Factors",
    "contigid": "U00096.3",
    "filename": "GCA_000005845.2_ASM584v2_genomic.fna",
    "hitcutoff": 90,
    "hitname": "entC",
    "hitorientation": "+",
    "hitstart": 624873,
    "hitstop": 626060
  },
  {
    "analysis": "Virulence Factors",
    "contigid": "U00096.3",
    "filename": "GCA_000005845.2_ASM584v2_genomic.fna",
    "hitcutoff": 90,
    "hitname": "entD",
    "hitorientation": "-",
    "hitstart": 609459,
    "hitstop": 610229
  },
  {
    "analysis": "Virulence Factors",
    "contigid": "U00096.3",
    "filename": "GCA_000005845.2_ASM584v2_genomic.fna",
    "hitcutoff": 90,
    "hitname": "entE",
    "hitorientation": "+",
    "hitstart": 626070,
    "hitstop": 627680
  },
  {
    "analysis": "Virulence Factors",
    "contigid": "U00096.3",
    "filename": "GCA_000005845.2_ASM584v2_genomic.fna",
    "hitcutoff": 90,
    "hitname": "entF",
    "hitorientation": "+",
    "hitstart": 614157,
    "hitstop": 617980
  },
  {
    "analysis": "Virulence Factors",
    "contigid": "U00096.3",
    "filename": "GCA_000005845.2_ASM584v2_genomic.fna",
    "hitcutoff": 90,
    "hitname": "entS",
    "hitorientation": "+",
    "hitstart": 622300,
    "hitstop": 623550
  },
  {
    "analysis": "Virulence Factors",
    "contigid": "U00096.3",
    "filename": "GCA_000005845.2_ASM584v2_genomic.fna",
    "hitcutoff": 90,
    "hitname": "espL1",
    "hitorientation": "+",
    "hitstart": 1803439,
    "hitstop": 1804993
  },
  {
    "analysis": "Virulence Factors",
    "contigid": "U00096.3",
    "filename": "GCA_000005845.2_ASM584v2_genomic.fna",
    "hitcutoff": 90,
    "hitname": "espL3",
    "hitorientation": "-",
    "hitstart": 3861987,
    "hitstop": 3863864
  },
  {
    "analysis": "Virulence Factors",
    "contigid": "U00096.3",
    "filename": "GCA_000005845.2_ASM584v2_genomic.fna",
    "hitcutoff": 90,
    "hitname": "espL4",
    "hitorientation": "-",
    "hitstart": 4221348,
    "hitstop": 4222487
  },
  {
    "analysis": "Virulence Factors",
    "contigid": "U00096.3",
    "filename": "GCA_000005845.2_ASM584v2_genomic.fna",
    "hitcutoff": 90,
    "hitname": "espR1",
    "hitorientation": "-",
    "hitstart": 1544385,
    "hitstop": 1545447
  },
  {
    "analysis": "Virulence Factors",
    "contigid": "U00096.3",
    "filename": "GCA_000005845.2_ASM584v2_genomic.fna",
    "hitcutoff": 90,
    "hitname": "espX4",
    "hitorientation": "+",
    "hitstart": 4250703,
    "hitstop": 4252283
  },
  {
    "analysis": "Virulence Factors",
    "contigid": "U00096.3",
    "filename": "GCA_000005845.2_ASM584v2_genomic.fna",
    "hitcutoff": 90,
    "hitname": "espX5",
    "hitorientation": "-",
    "hitstart": 4281783,
    "hitstop": 4283075
  },
  {
    "analysis": "Virulence Factors",
    "contigid": "U00096.3",
    "filename": "GCA_000005845.2_ASM584v2_genomic.fna",
    "hitcutoff": 90,
    "hitname": "espY1",
    "hitorientation": "+",
    "hitstart": 58474,
    "hitstop": 59103
  },
  {
    "analysis": "Virulence Factors",
    "contigid": "U00096.3",
    "filename": "GCA_000005845.2_ASM584v2_genomic.fna",
    "hitcutoff": 90,
    "hitname": "fdeC",
    "hitorientation": "+",
    "hitstart": 314357,
    "hitstop": 315232
  },
  {
    "analysis": "Virulence Factors",
    "contigid": "U00096.3",
    "filename": "GCA_000005845.2_ASM584v2_genomic.fna",
    "hitcutoff": 90,
    "hitname": "fepA",
    "hitorientation": "-",
    "hitstart": 610254,
    "hitstop": 612494
  },
  {
    "analysis": "Virulence Factors",
    "contigid": "U00096.3",
    "filename": "GCA_000005845.2_ASM584v2_genomic.fna",
    "hitcutoff": 90,
    "hitname": "fepB",
    "hitorientation": "-",
    "hitstart": 623554,
    "hitstop": 624510
  },
  {
    "analysis": "Virulence Factors",
    "contigid": "U00096.3",
    "filename": "GCA_000005845.2_ASM584v2_genomic.fna",
    "hitcutoff": 90,
    "hitname": "fepC",
    "hitorientation": "-",
    "hitstart": 619384,
    "hitstop": 620199
  },
  {
    "analysis": "Virulence Factors",
    "contigid": "U00096.3",
    "filename": "GCA_000005845.2_ASM584v2_genomic.fna",
    "hitcutoff": 90,
    "hitname": "fepD",
    "hitorientation": "-",
    "hitstart": 621185,
    "hitstop": 622201
  },
  {
    "analysis": "Virulence Factors",
    "contigid": "U00096.3",
    "filename": "GCA_000005845.2_ASM584v2_genomic.fna",
    "hitcutoff": 90,
    "hitname": "fepE",
    "hitorientation": "+",
    "hitstart": 618254,
    "hitstop": 619387
  },
  {
    "analysis": "Virulence Factors",
    "contigid": "U00096.3",
    "filename": "GCA_000005845.2_ASM584v2_genomic.fna",
    "hitcutoff": 90,
    "hitname": "fepG",
    "hitorientation": "-",
    "hitstart": 620196,
    "hitstop": 621188
  },
  {
    "analysis": "Virulence Factors",
    "contigid": "U00096.3",
    "filename": "GCA_000005845.2_ASM584v2_genomic.fna",
    "hitcutoff": 90,
    "hitname": "fes",
    "hitorientation": "+",
    "hitstart": 612737,
    "hitstop": 613939
  },
  {
    "analysis": "Virulence Factors",
    "contigid": "U00096.3",
    "filename": "GCA_000005845.2_ASM584v2_genomic.fna",
    "hitcutoff": 90,
    "hitname": "fimA",
    "hitorientation": "+",
    "hitstart": 4543115,
    "hitstop": 4543663
  },
  {
    "analysis": "Virulence Factors",
    "contigid": "U00096.3",
    "filename": "GCA_000005845.2_ASM584v2_genomic.fna",
    "hitcutoff": 90,
    "hitname": "fimB",
    "hitorientation": "+",
    "hitstart": 4540957,
    "hitstop": 4541559
  },
  {
    "analysis": "Virulence Factors",
    "contigid": "U00096.3",
    "filename": "GCA_000005845.2_ASM584v2_genomic.fna",
    "hitcutoff": 90,
    "hitname": "fimC",
    "hitorientation": "+",
    "hitstart": 4544355,
    "hitstop": 4545029
  },
  {
    "analysis": "Virulence Factors",
    "contigid": "U00096.3",
    "filename": "GCA_000005845.2_ASM584v2_genomic.fna",
    "hitcutoff": 90,
    "hitname": "fimD",
    "hitorientation": "-",
    "hitstart": 1588853,
    "hitstop": 1590079
  },
  {
    "analysis": "Virulence Factors",
    "contigid": "U00096.3",
    "filename": "GCA_000005845.2_ASM584v2_genomic.fna",
    "hitcutoff": 90,
    "hitname": "fimD",
    "hitorientation": "+",
    "hitstart": 4545096,
    "hitstop": 4547732
  },
  {
    "analysis": "Virulence Factors",
    "contigid": "U00096.3",
    "filename": "GCA_000005845.2_ASM584v2_genomic.fna",
    "hitcutoff": 90,
    "hitname": "fimE",
    "hitorientation": "+",
    "hitstart": 4542037,
    "hitstop": 4542633
  },
  {
    "analysis": "Virulence Factors",
    "contigid": "U00096.3",
    "filename": "GCA_000005845.2_ASM584v2_genomic.fna",
    "hitcutoff": 90,
    "hitname": "fimF",
    "hitorientation": "-",
    "hitstart": 1588309,
    "hitstop": 1588839
  },
  {
    "analysis": "Virulence Factors",
    "contigid": "U00096.3",
    "filename": "GCA_000005845.2_ASM584v2_genomic.fna",
    "hitcutoff": 90,
    "hitname": "fimF",
    "hitorientation": "+",
    "hitstart": 4547742,
    "hitstop": 4548272
  },
  {
    "analysis": "Virulence Factors",
    "contigid": "U00096.3",
    "filename": "GCA_000005845.2_ASM584v2_genomic.fna",
    "hitcutoff": 90,
    "hitname": "fimG",
    "hitorientation": "-",
    "hitstart": 1587793,
    "hitstop": 1588296
  },
  {
    "analysis": "Virulence Factors",
    "contigid": "U00096.3",
    "filename": "GCA_000005845.2_ASM584v2_genomic.fna",
    "hitcutoff": 90,
    "hitname": "fimG",
    "hitorientation": "+",
    "hitstart": 4548285,
    "hitstop": 4548788
  },
  {
    "analysis": "Virulence Factors",
    "contigid": "U00096.3",
    "filename": "GCA_000005845.2_ASM584v2_genomic.fna",
    "hitcutoff": 90,
    "hitname": "fimH",
    "hitorientation": "+",
    "hitstart": 4548808,
    "hitstop": 4549710
  },
  {
    "analysis": "Virulence Factors",
    "contigid": "U00096.3",
    "filename": "GCA_000005845.2_ASM584v2_genomic.fna",
    "hitcutoff": 90,
    "hitname": "fimI",
    "hitorientation": "+",
    "hitstart": 4543620,
    "hitstop": 4544267
  },
  {
    "analysis": "Virulence Factors",
    "contigid": "U00096.3",
    "filename": "GCA_000005845.2_ASM584v2_genomic.fna",
    "hitcutoff": 90,
    "hitname": "flgA",
    "hitorientation": "-",
    "hitstart": 1130204,
    "hitstop": 1130863
  },
  {
    "analysis": "Virulence Factors",
    "contigid": "U00096.3",
    "filename": "GCA_000005845.2_ASM584v2_genomic.fna",
    "hitcutoff": 90,
    "hitname": "flgD",
    "hitorientation": "+",
    "hitstart": 1131854,
    "hitstop": 1132549
  },
  {
    "analysis": "Virulence Factors",
    "contigid": "U00096.3",
    "filename": "GCA_000005845.2_ASM584v2_genomic.fna",
    "hitcutoff": 90,
    "hitname": "flgE",
    "hitorientation": "+",
    "hitstart": 1132574,
    "hitstop": 1133782
  },
  {
    "analysis": "Virulence Factors",
    "contigid": "U00096.3",
    "filename": "GCA_000005845.2_ASM584v2_genomic.fna",
    "hitcutoff": 90,
    "hitname": "flgF",
    "hitorientation": "+",
    "hitstart": 1133802,
    "hitstop": 1134557
  },
  {
    "analysis": "Virulence Factors",
    "contigid": "U00096.3",
    "filename": "GCA_000005845.2_ASM584v2_genomic.fna",
    "hitcutoff": 90,
    "hitname": "flgG",
    "hitorientation": "+",
    "hitstart": 1134729,
    "hitstop": 1135511
  },
  {
    "analysis": "Virulence Factors",
    "contigid": "U00096.3",
    "filename": "GCA_000005845.2_ASM584v2_genomic.fna",
    "hitcutoff": 90,
    "hitname": "flgH",
    "hitorientation": "+",
    "hitstart": 1135564,
    "hitstop": 1136262
  },
  {
    "analysis": "Virulence Factors",
    "contigid": "U00096.3",
    "filename": "GCA_000005845.2_ASM584v2_genomic.fna",
    "hitcutoff": 90,
    "hitname": "flgI",
    "hitorientation": "+",
    "hitstart": 1136274,
    "hitstop": 1137371
  },
  {
    "analysis": "Virulence Factors",
    "contigid": "U00096.3",
    "filename": "GCA_000005845.2_ASM584v2_genomic.fna",
    "hitcutoff": 90,
    "hitname": "flgJ",
    "hitorientation": "+",
    "hitstart": 1137371,
    "hitstop": 1138312
  },
  {
    "analysis": "Virulence Factors",
    "contigid": "U00096.3",
    "filename": "GCA_000005845.2_ASM584v2_genomic.fna",
    "hitcutoff": 90,
    "hitname": "flgK",
    "hitorientation": "+",
    "hitstart": 1138378,
    "hitstop": 1140021
  },
  {
    "analysis": "Virulence Factors",
    "contigid": "U00096.3",
    "filename": "GCA_000005845.2_ASM584v2_genomic.fna",
    "hitcutoff": 90,
    "hitname": "flgL",
    "hitorientation": "+",
    "hitstart": 1140033,
    "hitstop": 1140986
  },
  {
    "analysis": "Virulence Factors",
    "contigid": "U00096.3",
    "filename": "GCA_000005845.2_ASM584v2_genomic.fna",
    "hitcutoff": 90,
    "hitname": "flhA",
    "hitorientation": "-",
    "hitstart": 1962974,
    "hitstop": 1965050
  },
  {
    "analysis": "Virulence Factors",
    "contigid": "U00096.3",
    "filename": "GCA_000005845.2_ASM584v2_genomic.fna",
    "hitcutoff": 90,
    "hitname": "flhB",
    "hitorientation": "-",
    "hitstart": 1965043,
    "hitstop": 1966191
  },
  {
    "analysis": "Virulence Factors",
    "contigid": "U00096.3",
    "filename": "GCA_000005845.2_ASM584v2_genomic.fna",
    "hitcutoff": 90,
    "hitname": "flhC",
    "hitorientation": "-",
    "hitstart": 1977266,
    "hitstop": 1977844
  },
  {
    "analysis": "Virulence Factors",
    "contigid": "U00096.3",
    "filename": "GCA_000005845.2_ASM584v2_genomic.fna",
    "hitcutoff": 90,
    "hitname": "fliA",
    "hitorientation": "-",
    "hitstart": 2001070,
    "hitstop": 2001789
  },
  {
    "analysis": "Virulence Factors",
    "contigid": "U00096.3",
    "filename": "GCA_000005845.2_ASM584v2_genomic.fna",
    "hitcutoff": 90,
    "hitname": "fliD",
    "hitorientation": "+",
    "hitstart": 2003872,
    "hitstop": 2005278
  },
  {
    "analysis": "Virulence Factors",
    "contigid": "U00096.3",
    "filename": "GCA_000005845.2_ASM584v2_genomic.fna",
    "hitcutoff": 90,
    "hitname": "fliF",
    "hitorientation": "+",
    "hitstart": 2013229,
    "hitstop": 2014887
  },
  {
    "analysis": "Virulence Factors",
    "contigid": "U00096.3",
    "filename": "GCA_000005845.2_ASM584v2_genomic.fna",
    "hitcutoff": 90,
    "hitname": "fliG",
    "hitorientation": "+",
    "hitstart": 2014880,
    "hitstop": 2015875
  },
  {
    "analysis": "Virulence Factors",
    "contigid": "U00096.3",
    "filename": "GCA_000005845.2_ASM584v2_genomic.fna",
    "hitcutoff": 90,
    "hitname": "fliH",
    "hitorientation": "+",
    "hitstart": 2015868,
    "hitstop": 2016554
  },
  {
    "analysis": "Virulence Factors",
    "contigid": "U00096.3",
    "filename": "GCA_000005845.2_ASM584v2_genomic.fna",
    "hitcutoff": 90,
    "hitname": "fliI",
    "hitorientation": "+",
    "hitstart": 2016554,
    "hitstop": 2017927
  },
  {
    "analysis": "Virulence Factors",
    "contigid": "U00096.3",
    "filename": "GCA_000005845.2_ASM584v2_genomic.fna",
    "hitcutoff": 90,
    "hitname": "fliK",
    "hitorientation": "+",
    "hitstart": 2018386,
    "hitstop": 2019513
  },
  {
    "analysis": "Virulence Factors",
    "contigid": "U00096.3",
    "filename": "GCA_000005845.2_ASM584v2_genomic.fna",
    "hitcutoff": 90,
    "hitname": "fliM",
    "hitorientation": "+",
    "hitstart": 2020087,
    "hitstop": 2021091
  },
  {
    "analysis": "Virulence Factors",
    "contigid": "U00096.3",
    "filename": "GCA_000005845.2_ASM584v2_genomic.fna",
    "hitcutoff": 90,
    "hitname": "fliP",
    "hitorientation": "+",
    "hitstart": 2021869,
    "hitstop": 2022606
  },
  {
    "analysis": "Virulence Factors",
    "contigid": "U00096.3",
    "filename": "GCA_000005845.2_ASM584v2_genomic.fna",
    "hitcutoff": 90,
    "hitname": "fliR",
    "hitorientation": "+",
    "hitstart": 2022893,
    "hitstop": 2023678
  },
  {
    "analysis": "Virulence Factors",
    "contigid": "U00096.3",
    "filename": "GCA_000005845.2_ASM584v2_genomic.fna",
    "hitcutoff": 90,
    "hitname": "fliY",
    "hitorientation": "-",
    "hitstart": 1999585,
    "hitstop": 2000385
  },
  {
    "analysis": "Virulence Factors",
    "contigid": "U00096.3",
    "filename": "GCA_000005845.2_ASM584v2_genomic.fna",
    "hitcutoff": 90,
    "hitname": "fliZ",
    "hitorientation": "-",
    "hitstart": 2000473,
    "hitstop": 2001060
  },
  {
    "analysis": "Virulence Factors",
    "contigid": "U00096.3",
    "filename": "GCA_000005845.2_ASM584v2_genomic.fna",
    "hitcutoff": 90,
    "hitname": "flk",
    "hitorientation": "+",
    "hitstart": 2437950,
    "hitstop": 2438945
  },
  {
    "analysis": "Virulence Factors",
    "contigid": "U00096.3",
    "filename": "GCA_000005845.2_ASM584v2_genomic.fna",
    "hitcutoff": 90,
    "hitname": "gadX",
    "hitorientation": "-",
    "hitstart": 3664986,
    "hitstop": 3665618
  },
  {
    "analysis": "Virulence Factors",
    "contigid": "U00096.3",
    "filename": "GCA_000005845.2_ASM584v2_genomic.fna",
    "hitcutoff": 90,
    "hitname": "gspC",
    "hitorientation": "-",
    "hitstart": 3112091,
    "hitstop": 3113049
  },
  {
    "analysis": "Virulence Factors",
    "contigid": "U00096.3",
    "filename": "GCA_000005845.2_ASM584v2_genomic.fna",
    "hitcutoff": 90,
    "hitname": "gspL",
    "hitorientation": "-",
    "hitstart": 3111128,
    "hitstop": 3112092
  },
  {
    "analysis": "Virulence Factors",
    "contigid": "U00096.3",
    "filename": "GCA_000005845.2_ASM584v2_genomic.fna",
    "hitcutoff": 90,
    "hitname": "gspo",
    "hitorientation": "+",
    "hitstart": 3465543,
    "hitstop": 3466220
  },
  {
    "analysis": "Virulence Factors",
    "contigid": "U00096.3",
    "filename": "GCA_000005845.2_ASM584v2_genomic.fna",
    "hitcutoff": 90,
    "hitname": "hcp",
    "hitorientation": "-",
    "hitstart": 115714,
    "hitstop": 117099
  },
  {
    "analysis": "Virulence Factors",
    "contigid": "U00096.3",
    "filename": "GCA_000005845.2_ASM584v2_genomic.fna",
    "hitcutoff": 90,
    "hitname": "hlye",
    "hitorientation": "-",
    "hitstart": 1229483,
    "hitstop": 1230538
  },
  {
    "analysis": "Virulence Factors",
    "contigid": "U00096.3",
    "filename": "GCA_000005845.2_ASM584v2_genomic.fna",
    "hitcutoff": 90,
    "hitname": "hofq",
    "hitorientation": "-",
    "hitstart": 3519465,
    "hitstop": 3520703
  },
  {
    "analysis": "Virulence Factors",
    "contigid": "U00096.3",
    "filename": "GCA_000005845.2_ASM584v2_genomic.fna",
    "hitcutoff": 90,
    "hitname": "ibeB",
    "hitorientation": "+",
    "hitstart": 595600,
    "hitstop": 596981
  },
  {
    "analysis": "Virulence Factors",
    "contigid": "U00096.3",
    "filename": "GCA_000005845.2_ASM584v2_genomic.fna",
    "hitcutoff": 90,
    "hitname": "ibeC",
    "hitorientation": "-",
    "hitstart": 4148532,
    "hitstop": 4150309
  },
  {
    "analysis": "Virulence Factors",
    "contigid": "U00096.3",
    "filename": "GCA_000005845.2_ASM584v2_genomic.fna",
    "hitcutoff": 90,
    "hitname": "motA",
    "hitorientation": "-",
    "hitstart": 1976252,
    "hitstop": 1977139
  },
  {
    "analysis": "Virulence Factors",
    "contigid": "U00096.3",
    "filename": "GCA_000005845.2_ASM584v2_genomic.fna",
    "hitcutoff": 90,
    "hitname": "motB",
    "hitorientation": "-",
    "hitstart": 1975329,
    "hitstop": 1976255
  },
  {
    "analysis": "Virulence Factors",
    "contigid": "U00096.3",
    "filename": "GCA_000005845.2_ASM584v2_genomic.fna",
    "hitcutoff": 90,
    "hitname": "nada",
    "hitorientation": "+",
    "hitstart": 782085,
    "hitstop": 783128
  },
  {
    "analysis": "Virulence Factors",
    "contigid": "U00096.3",
    "filename": "GCA_000005845.2_ASM584v2_genomic.fna",
    "hitcutoff": 90,
    "hitname": "nadb",
    "hitorientation": "+",
    "hitstart": 2710420,
    "hitstop": 2712042
  },
  {
    "analysis": "Virulence Factors",
    "contigid": "U00096.3",
    "filename": "GCA_000005845.2_ASM584v2_genomic.fna",
    "hitcutoff": 90,
    "hitname": "ompA",
    "hitorientation": "-",
    "hitstart": 1019013,
    "hitstop": 1020053
  },
  {
    "analysis": "Virulence Factors",
    "contigid": "U00096.3",
    "filename": "GCA_000005845.2_ASM584v2_genomic.fna",
    "hitcutoff": 90,
    "hitname": "ompt",
    "hitorientation": "-",
    "hitstart": 584680,
    "hitstop": 585633
  },
  {
    "analysis": "Virulence Factors",
    "contigid": "U00096.3",
    "filename": "GCA_000005845.2_ASM584v2_genomic.fna",
    "hitcutoff": 90,
    "hitname": "ppdb",
    "hitorientation": "-",
    "hitstart": 2963153,
    "hitstop": 2963716
  },
  {
    "analysis": "Virulence Factors",
    "contigid": "U00096.3",
    "filename": "GCA_000005845.2_ASM584v2_genomic.fna",
    "hitcutoff": 90,
    "hitname": "tar/cheM",
    "hitorientation": "-",
    "hitstart": 1971030,
    "hitstop": 1972691
  },
  {
    "analysis": "Virulence Factors",
    "contigid": "U00096.3",
    "filename": "GCA_000005845.2_ASM584v2_genomic.fna",
    "hitcutoff": 90,
    "hitname": "upaC",
    "hitorientation": "+",
    "hitstart": 392973,
    "hitstop": 394418
  },
  {
    "analysis": "Virulence Factors",
    "contigid": "U00096.3",
    "filename": "GCA_000005845.2_ASM584v2_genomic.fna",
    "hitcutoff": 90,
    "hitname": "ycbF",
    "hitorientation": "+",
    "hitstart": 1003920,
    "hitstop": 1004657
  },
  {
    "analysis": "Virulence Factors",
    "contigid": "U00096.3",
    "filename": "GCA_000005845.2_ASM584v2_genomic.fna",
    "hitcutoff": 90,
    "hitname": "ycbQ",
    "hitorientation": "+",
    "hitstart": 997859,
    "hitstop": 998407
  },
  {
    "analysis": "Virulence Factors",
    "contigid": "U00096.3",
    "filename": "GCA_000005845.2_ASM584v2_genomic.fna",
    "hitcutoff": 90,
    "hitname": "ycbR",
    "hitorientation": "+",
    "hitstart": 998490,
    "hitstop": 999191
  },
  {
    "analysis": "Virulence Factors",
    "contigid": "U00096.3",
    "filename": "GCA_000005845.2_ASM584v2_genomic.fna",
    "hitcutoff": 90,
    "hitname": "ycbS",
    "hitorientation": "+",
    "hitstart": 999216,
    "hitstop": 1001816
  },
  {
    "analysis": "Virulence Factors",
    "contigid": "U00096.3",
    "filename": "GCA_000005845.2_ASM584v2_genomic.fna",
    "hitcutoff": 90,
    "hitname": "ycbT",
    "hitorientation": "+",
    "hitstart": 1001807,
    "hitstop": 1002784
  },
  {
    "analysis": "Virulence Factors",
    "contigid": "U00096.3",
    "filename": "GCA_000005845.2_ASM584v2_genomic.fna",
    "hitcutoff": 90,
    "hitname": "ycbV",
    "hitorientation": "+",
    "hitstart": 1003391,
    "hitstop": 1003954
  },
  {
    "analysis": "Virulence Factors",
    "contigid": "U00096.3",
    "filename": "GCA_000005845.2_ASM584v2_genomic.fna",
    "hitcutoff": 90,
    "hitname": "ycfz",
    "hitorientation": "-",
    "hitstart": 1180479,
    "hitstop": 1181267
  },
  {
    "analysis": "Virulence Factors",
    "contigid": "U00096.3",
    "filename": "GCA_000005845.2_ASM584v2_genomic.fna",
    "hitcutoff": 90,
    "hitname": "ygeH",
    "hitorientation": "+",
    "hitstart": 2992094,
    "hitstop": 2993470
  },
  {
    "analysis": "Virulence Factors",
    "contigid": "U00096.3",
    "filename": "GCA_000005845.2_ASM584v2_genomic.fna",
    "hitcutoff": 90,
    "hitname": "yggr",
    "hitorientation": "-",
    "hitstart": 3094100,
    "hitstop": 3095080
  }
]

BEAUTIFY_SEROTYPE = [
  {
    "analysis": "Serotype",
    "contigid": "n/a",
    "filename": "GCA_000005845.2_ASM584v2_genomic.fna",
    "hitcutoff": "n/a",
    "hitname": "O16:H48",
    "hitorientation": "n/a",
    "hitstart": "n/a",
    "hitstop": "n/a"
  }
]

BEAUTIFY_VF = [
    {
      "analysis": "Virulence Factors",
      "contigid": "U00096.3",
      "filename": "GCA_000005845.2_ASM584v2_genomic.fna",
      "hitcutoff": 90,
      "hitname": "EC958",
      "hitorientation": "+",
      "hitstart": 2073473,
      "hitstop": 2074658
    },
    {
      "analysis": "Virulence Factors",
      "contigid": "U00096.3",
      "filename": "GCA_000005845.2_ASM584v2_genomic.fna",
      "hitcutoff": 90,
      "hitname": "ECP",
      "hitorientation": "-",
      "hitstart": 306807,
      "hitstop": 309332
    },
    {
      "analysis": "Virulence Factors",
      "contigid": "U00096.3",
      "filename": "GCA_000005845.2_ASM584v2_genomic.fna",
      "hitcutoff": 90,
      "hitname": "ECP",
      "hitorientation": "-",
      "hitstart": 309358,
      "hitstop": 310075
    },
    {
      "analysis": "Virulence Factors",
      "contigid": "U00096.3",
      "filename": "GCA_000005845.2_ASM584v2_genomic.fna",
      "hitcutoff": 90,
      "hitname": "ECP",
      "hitorientation": "-",
      "hitstart": 310084,
      "hitstop": 310700
    },
    {
      "analysis": "Virulence Factors",
      "contigid": "U00096.3",
      "filename": "GCA_000005845.2_ASM584v2_genomic.fna",
      "hitcutoff": 90,
      "hitname": "ECP",
      "hitorientation": "-",
      "hitstart": 310746,
      "hitstop": 311336
    },
    {
      "analysis": "Virulence Factors",
      "contigid": "U00096.3",
      "filename": "GCA_000005845.2_ASM584v2_genomic.fna",
      "hitcutoff": 90,
      "hitname": "ECS88",
      "hitorientation": "-",
      "hitstart": 3308040,
      "hitstop": 3308924
    },
    {
      "analysis": "Virulence Factors",
      "contigid": "U00096.3",
      "filename": "GCA_000005845.2_ASM584v2_genomic.fna",
      "hitcutoff": 90,
      "hitname": "Z1307",
      "hitorientation": "-",
      "hitstart": 1019013,
      "hitstop": 1020053
    },
    {
      "analysis": "Virulence Factors",
      "contigid": "U00096.3",
      "filename": "GCA_000005845.2_ASM584v2_genomic.fna",
      "hitcutoff": 90,
      "hitname": "Z2203",
      "hitorientation": "-",
      "hitstart": 1588853,
      "hitstop": 1590079
    },
    {
      "analysis": "Virulence Factors",
      "contigid": "U00096.3",
      "filename": "GCA_000005845.2_ASM584v2_genomic.fna",
      "hitcutoff": 90,
      "hitname": "Z2204",
      "hitorientation": "-",
      "hitstart": 1588309,
      "hitstop": 1588839
    },
    {
      "analysis": "Virulence Factors",
      "contigid": "U00096.3",
      "filename": "GCA_000005845.2_ASM584v2_genomic.fna",
      "hitcutoff": 90,
      "hitname": "Z2205",
      "hitorientation": "-",
      "hitstart": 1587793,
      "hitstop": 1588296
    },
    {
      "analysis": "Virulence Factors",
      "contigid": "U00096.3",
      "filename": "GCA_000005845.2_ASM584v2_genomic.fna",
      "hitcutoff": 90,
      "hitname": "Z2206",
      "hitorientation": "-",
      "hitstart": 1586820,
      "hitstop": 1587734
    },
    {
      "analysis": "Virulence Factors",
      "contigid": "U00096.3",
      "filename": "GCA_000005845.2_ASM584v2_genomic.fna",
      "hitcutoff": 90,
      "hitname": "agn43",
      "hitorientation": "+",
      "hitstart": 2071539,
      "hitstop": 2074658
    },
    {
      "analysis": "Virulence Factors",
      "contigid": "U00096.3",
      "filename": "GCA_000005845.2_ASM584v2_genomic.fna",
      "hitcutoff": 90,
      "hitname": "artj",
      "hitorientation": "-",
      "hitstart": 899844,
      "hitstop": 900575
    },
    {
      "analysis": "Virulence Factors",
      "contigid": "U00096.3",
      "filename": "GCA_000005845.2_ASM584v2_genomic.fna",
      "hitcutoff": 90,
      "hitname": "aslA",
      "hitorientation": "-",
      "hitstart": 3984579,
      "hitstop": 3986007
    },
    {
      "analysis": "Virulence Factors",
      "contigid": "U00096.3",
      "filename": "GCA_000005845.2_ASM584v2_genomic.fna",
      "hitcutoff": 90,
      "hitname": "b2972",
      "hitorientation": "-",
      "hitstart": 3113543,
      "hitstop": 3114352
    },
    {
      "analysis": "Virulence Factors",
      "contigid": "U00096.3",
      "filename": "GCA_000005845.2_ASM584v2_genomic.fna",
      "hitcutoff": 90,
      "hitname": "cadA",
      "hitorientation": "-",
      "hitstart": 4356481,
      "hitstop": 4358656
    },
    {
      "analysis": "Virulence Factors",
      "contigid": "U00096.3",
      "filename": "GCA_000005845.2_ASM584v2_genomic.fna",
      "hitcutoff": 90,
      "hitname": "cah",
      "hitorientation": "+",
      "hitstart": 2073486,
      "hitstop": 2074658
    },
    {
      "analysis": "Virulence Factors",
      "contigid": "U00096.3",
      "filename": "GCA_000005845.2_ASM584v2_genomic.fna",
      "hitcutoff": 90,
      "hitname": "cheA",
      "hitorientation": "-",
      "hitstart": 1973360,
      "hitstop": 1975324
    },
    {
      "analysis": "Virulence Factors",
      "contigid": "U00096.3",
      "filename": "GCA_000005845.2_ASM584v2_genomic.fna",
      "hitcutoff": 90,
      "hitname": "cheB",
      "hitorientation": "-",
      "hitstart": 1967452,
      "hitstop": 1968501
    },
    {
      "analysis": "Virulence Factors",
      "contigid": "U00096.3",
      "filename": "GCA_000005845.2_ASM584v2_genomic.fna",
      "hitcutoff": 90,
      "hitname": "cheR",
      "hitorientation": "-",
      "hitstart": 1968504,
      "hitstop": 1969364
    },
    {
      "analysis": "Virulence Factors",
      "contigid": "U00096.3",
      "filename": "GCA_000005845.2_ASM584v2_genomic.fna",
      "hitcutoff": 90,
      "hitname": "cheW",
      "hitorientation": "-",
      "hitstart": 1972836,
      "hitstop": 1973339
    },
    {
      "analysis": "Virulence Factors",
      "contigid": "U00096.3",
      "filename": "GCA_000005845.2_ASM584v2_genomic.fna",
      "hitcutoff": 90,
      "hitname": "cheZ",
      "hitorientation": "-",
      "hitstart": 1966393,
      "hitstop": 1967037
    },
    {
      "analysis": "Virulence Factors",
      "contigid": "U00096.3",
      "filename": "GCA_000005845.2_ASM584v2_genomic.fna",
      "hitcutoff": 90,
      "hitname": "cs3",
      "hitorientation": "-",
      "hitstart": 2994460,
      "hitstop": 2995092
    },
    {
      "analysis": "Virulence Factors",
      "contigid": "U00096.3",
      "filename": "GCA_000005845.2_ASM584v2_genomic.fna",
      "hitcutoff": 90,
      "hitname": "csgD",
      "hitorientation": "-",
      "hitstart": 1102546,
      "hitstop": 1103196
    },
    {
      "analysis": "Virulence Factors",
      "contigid": "U00096.3",
      "filename": "GCA_000005845.2_ASM584v2_genomic.fna",
      "hitcutoff": 90,
      "hitname": "csgG",
      "hitorientation": "-",
      "hitstart": 1100851,
      "hitstop": 1101684
    },
    {
      "analysis": "Virulence Factors",
      "contigid": "U00096.3",
      "filename": "GCA_000005845.2_ASM584v2_genomic.fna",
      "hitcutoff": 90,
      "hitname": "eae",
      "hitorientation": "+",
      "hitstart": 314420,
      "hitstop": 315232
    },
    {
      "analysis": "Virulence Factors",
      "contigid": "U00096.3",
      "filename": "GCA_000005845.2_ASM584v2_genomic.fna",
      "hitcutoff": 90,
      "hitname": "ecpA",
      "hitorientation": "-",
      "hitstart": 310084,
      "hitstop": 310671
    },
    {
      "analysis": "Virulence Factors",
      "contigid": "U00096.3",
      "filename": "GCA_000005845.2_ASM584v2_genomic.fna",
      "hitcutoff": 90,
      "hitname": "ecpB",
      "hitorientation": "-",
      "hitstart": 309358,
      "hitstop": 310026
    },
    {
      "analysis": "Virulence Factors",
      "contigid": "U00096.3",
      "filename": "GCA_000005845.2_ASM584v2_genomic.fna",
      "hitcutoff": 90,
      "hitname": "ecpC",
      "hitorientation": "-",
      "hitstart": 306807,
      "hitstop": 309332
    },
    {
      "analysis": "Virulence Factors",
      "contigid": "U00096.3",
      "filename": "GCA_000005845.2_ASM584v2_genomic.fna",
      "hitcutoff": 90,
      "hitname": "ecpD",
      "hitorientation": "-",
      "hitstart": 305174,
      "hitstop": 306817
    },
    {
      "analysis": "Virulence Factors",
      "contigid": "U00096.3",
      "filename": "GCA_000005845.2_ASM584v2_genomic.fna",
      "hitcutoff": 90,
      "hitname": "ecpE",
      "hitorientation": "-",
      "hitstart": 304497,
      "hitstop": 305250
    },
    {
      "analysis": "Virulence Factors",
      "contigid": "U00096.3",
      "filename": "GCA_000005845.2_ASM584v2_genomic.fna",
      "hitcutoff": 90,
      "hitname": "ecpR",
      "hitorientation": "-",
      "hitstart": 310746,
      "hitstop": 311336
    },
    {
      "analysis": "Virulence Factors",
      "contigid": "U00096.3",
      "filename": "GCA_000005845.2_ASM584v2_genomic.fna",
      "hitcutoff": 90,
      "hitname": "ehaB",
      "hitorientation": "+",
      "hitstart": 392973,
      "hitstop": 394418
    },
    {
      "analysis": "Virulence Factors",
      "contigid": "U00096.3",
      "filename": "GCA_000005845.2_ASM584v2_genomic.fna",
      "hitcutoff": 90,
      "hitname": "entA",
      "hitorientation": "+",
      "hitstart": 628551,
      "hitstop": 629297
    },
    {
      "analysis": "Virulence Factors",
      "contigid": "U00096.3",
      "filename": "GCA_000005845.2_ASM584v2_genomic.fna",
      "hitcutoff": 90,
      "hitname": "entB",
      "hitorientation": "+",
      "hitstart": 627694,
      "hitstop": 628551
    },
    {
      "analysis": "Virulence Factors",
      "contigid": "U00096.3",
      "filename": "GCA_000005845.2_ASM584v2_genomic.fna",
      "hitcutoff": 90,
      "hitname": "entC",
      "hitorientation": "+",
      "hitstart": 624873,
      "hitstop": 626060
    },
    {
      "analysis": "Virulence Factors",
      "contigid": "U00096.3",
      "filename": "GCA_000005845.2_ASM584v2_genomic.fna",
      "hitcutoff": 90,
      "hitname": "entD",
      "hitorientation": "-",
      "hitstart": 609459,
      "hitstop": 610229
    },
    {
      "analysis": "Virulence Factors",
      "contigid": "U00096.3",
      "filename": "GCA_000005845.2_ASM584v2_genomic.fna",
      "hitcutoff": 90,
      "hitname": "entE",
      "hitorientation": "+",
      "hitstart": 626070,
      "hitstop": 627680
    },
    {
      "analysis": "Virulence Factors",
      "contigid": "U00096.3",
      "filename": "GCA_000005845.2_ASM584v2_genomic.fna",
      "hitcutoff": 90,
      "hitname": "entF",
      "hitorientation": "+",
      "hitstart": 614157,
      "hitstop": 617980
    },
    {
      "analysis": "Virulence Factors",
      "contigid": "U00096.3",
      "filename": "GCA_000005845.2_ASM584v2_genomic.fna",
      "hitcutoff": 90,
      "hitname": "entS",
      "hitorientation": "+",
      "hitstart": 622300,
      "hitstop": 623550
    },
    {
      "analysis": "Virulence Factors",
      "contigid": "U00096.3",
      "filename": "GCA_000005845.2_ASM584v2_genomic.fna",
      "hitcutoff": 90,
      "hitname": "espL1",
      "hitorientation": "+",
      "hitstart": 1803439,
      "hitstop": 1804993
    },
    {
      "analysis": "Virulence Factors",
      "contigid": "U00096.3",
      "filename": "GCA_000005845.2_ASM584v2_genomic.fna",
      "hitcutoff": 90,
      "hitname": "espL3",
      "hitorientation": "-",
      "hitstart": 3861987,
      "hitstop": 3863864
    },
    {
      "analysis": "Virulence Factors",
      "contigid": "U00096.3",
      "filename": "GCA_000005845.2_ASM584v2_genomic.fna",
      "hitcutoff": 90,
      "hitname": "espL4",
      "hitorientation": "-",
      "hitstart": 4221348,
      "hitstop": 4222487
    },
    {
      "analysis": "Virulence Factors",
      "contigid": "U00096.3",
      "filename": "GCA_000005845.2_ASM584v2_genomic.fna",
      "hitcutoff": 90,
      "hitname": "espR1",
      "hitorientation": "-",
      "hitstart": 1544385,
      "hitstop": 1545447
    },
    {
      "analysis": "Virulence Factors",
      "contigid": "U00096.3",
      "filename": "GCA_000005845.2_ASM584v2_genomic.fna",
      "hitcutoff": 90,
      "hitname": "espX4",
      "hitorientation": "+",
      "hitstart": 4250703,
      "hitstop": 4252283
    },
    {
      "analysis": "Virulence Factors",
      "contigid": "U00096.3",
      "filename": "GCA_000005845.2_ASM584v2_genomic.fna",
      "hitcutoff": 90,
      "hitname": "espX5",
      "hitorientation": "-",
      "hitstart": 4281783,
      "hitstop": 4283075
    },
    {
      "analysis": "Virulence Factors",
      "contigid": "U00096.3",
      "filename": "GCA_000005845.2_ASM584v2_genomic.fna",
      "hitcutoff": 90,
      "hitname": "espY1",
      "hitorientation": "+",
      "hitstart": 58474,
      "hitstop": 59103
    },
    {
      "analysis": "Virulence Factors",
      "contigid": "U00096.3",
      "filename": "GCA_000005845.2_ASM584v2_genomic.fna",
      "hitcutoff": 90,
      "hitname": "fdeC",
      "hitorientation": "+",
      "hitstart": 314357,
      "hitstop": 315232
    },
    {
      "analysis": "Virulence Factors",
      "contigid": "U00096.3",
      "filename": "GCA_000005845.2_ASM584v2_genomic.fna",
      "hitcutoff": 90,
      "hitname": "fepA",
      "hitorientation": "-",
      "hitstart": 610254,
      "hitstop": 612494
    },
    {
      "analysis": "Virulence Factors",
      "contigid": "U00096.3",
      "filename": "GCA_000005845.2_ASM584v2_genomic.fna",
      "hitcutoff": 90,
      "hitname": "fepB",
      "hitorientation": "-",
      "hitstart": 623554,
      "hitstop": 624510
    },
    {
      "analysis": "Virulence Factors",
      "contigid": "U00096.3",
      "filename": "GCA_000005845.2_ASM584v2_genomic.fna",
      "hitcutoff": 90,
      "hitname": "fepC",
      "hitorientation": "-",
      "hitstart": 619384,
      "hitstop": 620199
    },
    {
      "analysis": "Virulence Factors",
      "contigid": "U00096.3",
      "filename": "GCA_000005845.2_ASM584v2_genomic.fna",
      "hitcutoff": 90,
      "hitname": "fepD",
      "hitorientation": "-",
      "hitstart": 621185,
      "hitstop": 622201
    },
    {
      "analysis": "Virulence Factors",
      "contigid": "U00096.3",
      "filename": "GCA_000005845.2_ASM584v2_genomic.fna",
      "hitcutoff": 90,
      "hitname": "fepE",
      "hitorientation": "+",
      "hitstart": 618254,
      "hitstop": 619387
    },
    {
      "analysis": "Virulence Factors",
      "contigid": "U00096.3",
      "filename": "GCA_000005845.2_ASM584v2_genomic.fna",
      "hitcutoff": 90,
      "hitname": "fepG",
      "hitorientation": "-",
      "hitstart": 620196,
      "hitstop": 621188
    },
    {
      "analysis": "Virulence Factors",
      "contigid": "U00096.3",
      "filename": "GCA_000005845.2_ASM584v2_genomic.fna",
      "hitcutoff": 90,
      "hitname": "fes",
      "hitorientation": "+",
      "hitstart": 612737,
      "hitstop": 613939
    },
    {
      "analysis": "Virulence Factors",
      "contigid": "U00096.3",
      "filename": "GCA_000005845.2_ASM584v2_genomic.fna",
      "hitcutoff": 90,
      "hitname": "fimA",
      "hitorientation": "+",
      "hitstart": 4543115,
      "hitstop": 4543663
    },
    {
      "analysis": "Virulence Factors",
      "contigid": "U00096.3",
      "filename": "GCA_000005845.2_ASM584v2_genomic.fna",
      "hitcutoff": 90,
      "hitname": "fimB",
      "hitorientation": "+",
      "hitstart": 4540957,
      "hitstop": 4541559
    },
    {
      "analysis": "Virulence Factors",
      "contigid": "U00096.3",
      "filename": "GCA_000005845.2_ASM584v2_genomic.fna",
      "hitcutoff": 90,
      "hitname": "fimC",
      "hitorientation": "+",
      "hitstart": 4544355,
      "hitstop": 4545029
    },
    {
      "analysis": "Virulence Factors",
      "contigid": "U00096.3",
      "filename": "GCA_000005845.2_ASM584v2_genomic.fna",
      "hitcutoff": 90,
      "hitname": "fimD",
      "hitorientation": "-",
      "hitstart": 1588853,
      "hitstop": 1590079
    },
    {
      "analysis": "Virulence Factors",
      "contigid": "U00096.3",
      "filename": "GCA_000005845.2_ASM584v2_genomic.fna",
      "hitcutoff": 90,
      "hitname": "fimD",
      "hitorientation": "+",
      "hitstart": 4545096,
      "hitstop": 4547732
    },
    {
      "analysis": "Virulence Factors",
      "contigid": "U00096.3",
      "filename": "GCA_000005845.2_ASM584v2_genomic.fna",
      "hitcutoff": 90,
      "hitname": "fimE",
      "hitorientation": "+",
      "hitstart": 4542037,
      "hitstop": 4542633
    },
    {
      "analysis": "Virulence Factors",
      "contigid": "U00096.3",
      "filename": "GCA_000005845.2_ASM584v2_genomic.fna",
      "hitcutoff": 90,
      "hitname": "fimF",
      "hitorientation": "-",
      "hitstart": 1588309,
      "hitstop": 1588839
    },
    {
      "analysis": "Virulence Factors",
      "contigid": "U00096.3",
      "filename": "GCA_000005845.2_ASM584v2_genomic.fna",
      "hitcutoff": 90,
      "hitname": "fimF",
      "hitorientation": "+",
      "hitstart": 4547742,
      "hitstop": 4548272
    },
    {
      "analysis": "Virulence Factors",
      "contigid": "U00096.3",
      "filename": "GCA_000005845.2_ASM584v2_genomic.fna",
      "hitcutoff": 90,
      "hitname": "fimG",
      "hitorientation": "-",
      "hitstart": 1587793,
      "hitstop": 1588296
    },
    {
      "analysis": "Virulence Factors",
      "contigid": "U00096.3",
      "filename": "GCA_000005845.2_ASM584v2_genomic.fna",
      "hitcutoff": 90,
      "hitname": "fimG",
      "hitorientation": "+",
      "hitstart": 4548285,
      "hitstop": 4548788
    },
    {
      "analysis": "Virulence Factors",
      "contigid": "U00096.3",
      "filename": "GCA_000005845.2_ASM584v2_genomic.fna",
      "hitcutoff": 90,
      "hitname": "fimH",
      "hitorientation": "+",
      "hitstart": 4548808,
      "hitstop": 4549710
    },
    {
      "analysis": "Virulence Factors",
      "contigid": "U00096.3",
      "filename": "GCA_000005845.2_ASM584v2_genomic.fna",
      "hitcutoff": 90,
      "hitname": "fimI",
      "hitorientation": "+",
      "hitstart": 4543620,
      "hitstop": 4544267
    },
    {
      "analysis": "Virulence Factors",
      "contigid": "U00096.3",
      "filename": "GCA_000005845.2_ASM584v2_genomic.fna",
      "hitcutoff": 90,
      "hitname": "flgA",
      "hitorientation": "-",
      "hitstart": 1130204,
      "hitstop": 1130863
    },
    {
      "analysis": "Virulence Factors",
      "contigid": "U00096.3",
      "filename": "GCA_000005845.2_ASM584v2_genomic.fna",
      "hitcutoff": 90,
      "hitname": "flgD",
      "hitorientation": "+",
      "hitstart": 1131854,
      "hitstop": 1132549
    },
    {
      "analysis": "Virulence Factors",
      "contigid": "U00096.3",
      "filename": "GCA_000005845.2_ASM584v2_genomic.fna",
      "hitcutoff": 90,
      "hitname": "flgE",
      "hitorientation": "+",
      "hitstart": 1132574,
      "hitstop": 1133782
    },
    {
      "analysis": "Virulence Factors",
      "contigid": "U00096.3",
      "filename": "GCA_000005845.2_ASM584v2_genomic.fna",
      "hitcutoff": 90,
      "hitname": "flgF",
      "hitorientation": "+",
      "hitstart": 1133802,
      "hitstop": 1134557
    },
    {
      "analysis": "Virulence Factors",
      "contigid": "U00096.3",
      "filename": "GCA_000005845.2_ASM584v2_genomic.fna",
      "hitcutoff": 90,
      "hitname": "flgG",
      "hitorientation": "+",
      "hitstart": 1134729,
      "hitstop": 1135511
    },
    {
      "analysis": "Virulence Factors",
      "contigid": "U00096.3",
      "filename": "GCA_000005845.2_ASM584v2_genomic.fna",
      "hitcutoff": 90,
      "hitname": "flgH",
      "hitorientation": "+",
      "hitstart": 1135564,
      "hitstop": 1136262
    },
    {
      "analysis": "Virulence Factors",
      "contigid": "U00096.3",
      "filename": "GCA_000005845.2_ASM584v2_genomic.fna",
      "hitcutoff": 90,
      "hitname": "flgI",
      "hitorientation": "+",
      "hitstart": 1136274,
      "hitstop": 1137371
    },
    {
      "analysis": "Virulence Factors",
      "contigid": "U00096.3",
      "filename": "GCA_000005845.2_ASM584v2_genomic.fna",
      "hitcutoff": 90,
      "hitname": "flgJ",
      "hitorientation": "+",
      "hitstart": 1137371,
      "hitstop": 1138312
    },
    {
      "analysis": "Virulence Factors",
      "contigid": "U00096.3",
      "filename": "GCA_000005845.2_ASM584v2_genomic.fna",
      "hitcutoff": 90,
      "hitname": "flgK",
      "hitorientation": "+",
      "hitstart": 1138378,
      "hitstop": 1140021
    },
    {
      "analysis": "Virulence Factors",
      "contigid": "U00096.3",
      "filename": "GCA_000005845.2_ASM584v2_genomic.fna",
      "hitcutoff": 90,
      "hitname": "flgL",
      "hitorientation": "+",
      "hitstart": 1140033,
      "hitstop": 1140986
    },
    {
      "analysis": "Virulence Factors",
      "contigid": "U00096.3",
      "filename": "GCA_000005845.2_ASM584v2_genomic.fna",
      "hitcutoff": 90,
      "hitname": "flhA",
      "hitorientation": "-",
      "hitstart": 1962974,
      "hitstop": 1965050
    },
    {
      "analysis": "Virulence Factors",
      "contigid": "U00096.3",
      "filename": "GCA_000005845.2_ASM584v2_genomic.fna",
      "hitcutoff": 90,
      "hitname": "flhB",
      "hitorientation": "-",
      "hitstart": 1965043,
      "hitstop": 1966191
    },
    {
      "analysis": "Virulence Factors",
      "contigid": "U00096.3",
      "filename": "GCA_000005845.2_ASM584v2_genomic.fna",
      "hitcutoff": 90,
      "hitname": "flhC",
      "hitorientation": "-",
      "hitstart": 1977266,
      "hitstop": 1977844
    },
    {
      "analysis": "Virulence Factors",
      "contigid": "U00096.3",
      "filename": "GCA_000005845.2_ASM584v2_genomic.fna",
      "hitcutoff": 90,
      "hitname": "fliA",
      "hitorientation": "-",
      "hitstart": 2001070,
      "hitstop": 2001789
    },
    {
      "analysis": "Virulence Factors",
      "contigid": "U00096.3",
      "filename": "GCA_000005845.2_ASM584v2_genomic.fna",
      "hitcutoff": 90,
      "hitname": "fliD",
      "hitorientation": "+",
      "hitstart": 2003872,
      "hitstop": 2005278
    },
    {
      "analysis": "Virulence Factors",
      "contigid": "U00096.3",
      "filename": "GCA_000005845.2_ASM584v2_genomic.fna",
      "hitcutoff": 90,
      "hitname": "fliF",
      "hitorientation": "+",
      "hitstart": 2013229,
      "hitstop": 2014887
    },
    {
      "analysis": "Virulence Factors",
      "contigid": "U00096.3",
      "filename": "GCA_000005845.2_ASM584v2_genomic.fna",
      "hitcutoff": 90,
      "hitname": "fliG",
      "hitorientation": "+",
      "hitstart": 2014880,
      "hitstop": 2015875
    },
    {
      "analysis": "Virulence Factors",
      "contigid": "U00096.3",
      "filename": "GCA_000005845.2_ASM584v2_genomic.fna",
      "hitcutoff": 90,
      "hitname": "fliH",
      "hitorientation": "+",
      "hitstart": 2015868,
      "hitstop": 2016554
    },
    {
      "analysis": "Virulence Factors",
      "contigid": "U00096.3",
      "filename": "GCA_000005845.2_ASM584v2_genomic.fna",
      "hitcutoff": 90,
      "hitname": "fliI",
      "hitorientation": "+",
      "hitstart": 2016554,
      "hitstop": 2017927
    },
    {
      "analysis": "Virulence Factors",
      "contigid": "U00096.3",
      "filename": "GCA_000005845.2_ASM584v2_genomic.fna",
      "hitcutoff": 90,
      "hitname": "fliK",
      "hitorientation": "+",
      "hitstart": 2018386,
      "hitstop": 2019513
    },
    {
      "analysis": "Virulence Factors",
      "contigid": "U00096.3",
      "filename": "GCA_000005845.2_ASM584v2_genomic.fna",
      "hitcutoff": 90,
      "hitname": "fliM",
      "hitorientation": "+",
      "hitstart": 2020087,
      "hitstop": 2021091
    },
    {
      "analysis": "Virulence Factors",
      "contigid": "U00096.3",
      "filename": "GCA_000005845.2_ASM584v2_genomic.fna",
      "hitcutoff": 90,
      "hitname": "fliP",
      "hitorientation": "+",
      "hitstart": 2021869,
      "hitstop": 2022606
    },
    {
      "analysis": "Virulence Factors",
      "contigid": "U00096.3",
      "filename": "GCA_000005845.2_ASM584v2_genomic.fna",
      "hitcutoff": 90,
      "hitname": "fliR",
      "hitorientation": "+",
      "hitstart": 2022893,
      "hitstop": 2023678
    },
    {
      "analysis": "Virulence Factors",
      "contigid": "U00096.3",
      "filename": "GCA_000005845.2_ASM584v2_genomic.fna",
      "hitcutoff": 90,
      "hitname": "fliY",
      "hitorientation": "-",
      "hitstart": 1999585,
      "hitstop": 2000385
    },
    {
      "analysis": "Virulence Factors",
      "contigid": "U00096.3",
      "filename": "GCA_000005845.2_ASM584v2_genomic.fna",
      "hitcutoff": 90,
      "hitname": "fliZ",
      "hitorientation": "-",
      "hitstart": 2000473,
      "hitstop": 2001060
    },
    {
      "analysis": "Virulence Factors",
      "contigid": "U00096.3",
      "filename": "GCA_000005845.2_ASM584v2_genomic.fna",
      "hitcutoff": 90,
      "hitname": "flk",
      "hitorientation": "+",
      "hitstart": 2437950,
      "hitstop": 2438945
    },
    {
      "analysis": "Virulence Factors",
      "contigid": "U00096.3",
      "filename": "GCA_000005845.2_ASM584v2_genomic.fna",
      "hitcutoff": 90,
      "hitname": "gadX",
      "hitorientation": "-",
      "hitstart": 3664986,
      "hitstop": 3665618
    },
    {
      "analysis": "Virulence Factors",
      "contigid": "U00096.3",
      "filename": "GCA_000005845.2_ASM584v2_genomic.fna",
      "hitcutoff": 90,
      "hitname": "gspC",
      "hitorientation": "-",
      "hitstart": 3112091,
      "hitstop": 3113049
    },
    {
      "analysis": "Virulence Factors",
      "contigid": "U00096.3",
      "filename": "GCA_000005845.2_ASM584v2_genomic.fna",
      "hitcutoff": 90,
      "hitname": "gspL",
      "hitorientation": "-",
      "hitstart": 3111128,
      "hitstop": 3112092
    },
    {
      "analysis": "Virulence Factors",
      "contigid": "U00096.3",
      "filename": "GCA_000005845.2_ASM584v2_genomic.fna",
      "hitcutoff": 90,
      "hitname": "gspo",
      "hitorientation": "+",
      "hitstart": 3465543,
      "hitstop": 3466220
    },
    {
      "analysis": "Virulence Factors",
      "contigid": "U00096.3",
      "filename": "GCA_000005845.2_ASM584v2_genomic.fna",
      "hitcutoff": 90,
      "hitname": "hcp",
      "hitorientation": "-",
      "hitstart": 115714,
      "hitstop": 117099
    },
    {
      "analysis": "Virulence Factors",
      "contigid": "U00096.3",
      "filename": "GCA_000005845.2_ASM584v2_genomic.fna",
      "hitcutoff": 90,
      "hitname": "hlye",
      "hitorientation": "-",
      "hitstart": 1229483,
      "hitstop": 1230538
    },
    {
      "analysis": "Virulence Factors",
      "contigid": "U00096.3",
      "filename": "GCA_000005845.2_ASM584v2_genomic.fna",
      "hitcutoff": 90,
      "hitname": "hofq",
      "hitorientation": "-",
      "hitstart": 3519465,
      "hitstop": 3520703
    },
    {
      "analysis": "Virulence Factors",
      "contigid": "U00096.3",
      "filename": "GCA_000005845.2_ASM584v2_genomic.fna",
      "hitcutoff": 90,
      "hitname": "ibeB",
      "hitorientation": "+",
      "hitstart": 595600,
      "hitstop": 596981
    },
    {
      "analysis": "Virulence Factors",
      "contigid": "U00096.3",
      "filename": "GCA_000005845.2_ASM584v2_genomic.fna",
      "hitcutoff": 90,
      "hitname": "ibeC",
      "hitorientation": "-",
      "hitstart": 4148532,
      "hitstop": 4150309
    },
    {
      "analysis": "Virulence Factors",
      "contigid": "U00096.3",
      "filename": "GCA_000005845.2_ASM584v2_genomic.fna",
      "hitcutoff": 90,
      "hitname": "motA",
      "hitorientation": "-",
      "hitstart": 1976252,
      "hitstop": 1977139
    },
    {
      "analysis": "Virulence Factors",
      "contigid": "U00096.3",
      "filename": "GCA_000005845.2_ASM584v2_genomic.fna",
      "hitcutoff": 90,
      "hitname": "motB",
      "hitorientation": "-",
      "hitstart": 1975329,
      "hitstop": 1976255
    },
    {
      "analysis": "Virulence Factors",
      "contigid": "U00096.3",
      "filename": "GCA_000005845.2_ASM584v2_genomic.fna",
      "hitcutoff": 90,
      "hitname": "nada",
      "hitorientation": "+",
      "hitstart": 782085,
      "hitstop": 783128
    },
    {
      "analysis": "Virulence Factors",
      "contigid": "U00096.3",
      "filename": "GCA_000005845.2_ASM584v2_genomic.fna",
      "hitcutoff": 90,
      "hitname": "nadb",
      "hitorientation": "+",
      "hitstart": 2710420,
      "hitstop": 2712042
    },
    {
      "analysis": "Virulence Factors",
      "contigid": "U00096.3",
      "filename": "GCA_000005845.2_ASM584v2_genomic.fna",
      "hitcutoff": 90,
      "hitname": "ompA",
      "hitorientation": "-",
      "hitstart": 1019013,
      "hitstop": 1020053
    },
    {
      "analysis": "Virulence Factors",
      "contigid": "U00096.3",
      "filename": "GCA_000005845.2_ASM584v2_genomic.fna",
      "hitcutoff": 90,
      "hitname": "ompt",
      "hitorientation": "-",
      "hitstart": 584680,
      "hitstop": 585633
    },
    {
      "analysis": "Virulence Factors",
      "contigid": "U00096.3",
      "filename": "GCA_000005845.2_ASM584v2_genomic.fna",
      "hitcutoff": 90,
      "hitname": "ppdb",
      "hitorientation": "-",
      "hitstart": 2963153,
      "hitstop": 2963716
    },
    {
      "analysis": "Virulence Factors",
      "contigid": "U00096.3",
      "filename": "GCA_000005845.2_ASM584v2_genomic.fna",
      "hitcutoff": 90,
      "hitname": "tar/cheM",
      "hitorientation": "-",
      "hitstart": 1971030,
      "hitstop": 1972691
    },
    {
      "analysis": "Virulence Factors",
      "contigid": "U00096.3",
      "filename": "GCA_000005845.2_ASM584v2_genomic.fna",
      "hitcutoff": 90,
      "hitname": "upaC",
      "hitorientation": "+",
      "hitstart": 392973,
      "hitstop": 394418
    },
    {
      "analysis": "Virulence Factors",
      "contigid": "U00096.3",
      "filename": "GCA_000005845.2_ASM584v2_genomic.fna",
      "hitcutoff": 90,
      "hitname": "ycbF",
      "hitorientation": "+",
      "hitstart": 1003920,
      "hitstop": 1004657
    },
    {
      "analysis": "Virulence Factors",
      "contigid": "U00096.3",
      "filename": "GCA_000005845.2_ASM584v2_genomic.fna",
      "hitcutoff": 90,
      "hitname": "ycbQ",
      "hitorientation": "+",
      "hitstart": 997859,
      "hitstop": 998407
    },
    {
      "analysis": "Virulence Factors",
      "contigid": "U00096.3",
      "filename": "GCA_000005845.2_ASM584v2_genomic.fna",
      "hitcutoff": 90,
      "hitname": "ycbR",
      "hitorientation": "+",
      "hitstart": 998490,
      "hitstop": 999191
    },
    {
      "analysis": "Virulence Factors",
      "contigid": "U00096.3",
      "filename": "GCA_000005845.2_ASM584v2_genomic.fna",
      "hitcutoff": 90,
      "hitname": "ycbS",
      "hitorientation": "+",
      "hitstart": 999216,
      "hitstop": 1001816
    },
    {
      "analysis": "Virulence Factors",
      "contigid": "U00096.3",
      "filename": "GCA_000005845.2_ASM584v2_genomic.fna",
      "hitcutoff": 90,
      "hitname": "ycbT",
      "hitorientation": "+",
      "hitstart": 1001807,
      "hitstop": 1002784
    },
    {
      "analysis": "Virulence Factors",
      "contigid": "U00096.3",
      "filename": "GCA_000005845.2_ASM584v2_genomic.fna",
      "hitcutoff": 90,
      "hitname": "ycbV",
      "hitorientation": "+",
      "hitstart": 1003391,
      "hitstop": 1003954
    },
    {
      "analysis": "Virulence Factors",
      "contigid": "U00096.3",
      "filename": "GCA_000005845.2_ASM584v2_genomic.fna",
      "hitcutoff": 90,
      "hitname": "ycfz",
      "hitorientation": "-",
      "hitstart": 1180479,
      "hitstop": 1181267
    },
    {
      "analysis": "Virulence Factors",
      "contigid": "U00096.3",
      "filename": "GCA_000005845.2_ASM584v2_genomic.fna",
      "hitcutoff": 90,
      "hitname": "ygeH",
      "hitorientation": "+",
      "hitstart": 2992094,
      "hitstop": 2993470
    },
    {
      "analysis": "Virulence Factors",
      "contigid": "U00096.3",
      "filename": "GCA_000005845.2_ASM584v2_genomic.fna",
      "hitcutoff": 90,
      "hitname": "yggr",
      "hitorientation": "-",
      "hitstart": 3094100,
      "hitstop": 3095080
    }
]

BEAUTIFY_AMR = [
  {
    "analysis": "Antimicrobial Resistance",
    "contigid": "MOHB01000001.1",
    "filename": "GCA_001891995.1_ASM189199v1_genomic.fna",
    "hitcutoff": "Strict",
    "hitname": "Escherichia coli gyrA conferring resistance to fluoroquinolones",
    "hitorientation": "+",
    "hitstart": 159252,
    "hitstop": 161879
  },
  {
    "analysis": "Antimicrobial Resistance",
    "contigid": "MOHB01000001.1",
    "filename": "GCA_001891995.1_ASM189199v1_genomic.fna",
    "hitcutoff": "Strict",
    "hitname": "PmrE",
    "hitorientation": "+",
    "hitstart": 388190,
    "hitstop": 389356
  },
  {
    "analysis": "Antimicrobial Resistance",
    "contigid": "MOHB01000001.1",
    "filename": "GCA_001891995.1_ASM189199v1_genomic.fna",
    "hitcutoff": "Perfect",
    "hitname": "PmrF",
    "hitorientation": "-",
    "hitstart": 134984,
    "hitstop": 135952
  },
  {
    "analysis": "Antimicrobial Resistance",
    "contigid": "MOHB01000001.1",
    "filename": "GCA_001891995.1_ASM189199v1_genomic.fna",
    "hitcutoff": "Strict",
    "hitname": "arnA",
    "hitorientation": "-",
    "hitstart": 133002,
    "hitstop": 134984
  },
  {
    "analysis": "Antimicrobial Resistance",
    "contigid": "MOHB01000001.1",
    "filename": "GCA_001891995.1_ASM189199v1_genomic.fna",
    "hitcutoff": "Perfect",
    "hitname": "baeR",
    "hitorientation": "-",
    "hitstart": 323408,
    "hitstop": 324130
  },
  {
    "analysis": "Antimicrobial Resistance",
    "contigid": "MOHB01000001.1",
    "filename": "GCA_001891995.1_ASM189199v1_genomic.fna",
    "hitcutoff": "Perfect",
    "hitname": "baeS",
    "hitorientation": "-",
    "hitstart": 324127,
    "hitstop": 325530
  },
  {
    "analysis": "Antimicrobial Resistance",
    "contigid": "MOHB01000001.1",
    "filename": "GCA_001891995.1_ASM189199v1_genomic.fna",
    "hitcutoff": "Perfect",
    "hitname": "mdtB",
    "hitorientation": "-",
    "hitstart": 330021,
    "hitstop": 333143
  },
  {
    "analysis": "Antimicrobial Resistance",
    "contigid": "MOHB01000001.1",
    "filename": "GCA_001891995.1_ASM189199v1_genomic.fna",
    "hitcutoff": "Strict",
    "hitname": "mdtD",
    "hitorientation": "-",
    "hitstart": 325527,
    "hitstop": 326942
  },
  {
    "analysis": "Antimicrobial Resistance",
    "contigid": "MOHB01000001.1",
    "filename": "GCA_001891995.1_ASM189199v1_genomic.fna",
    "hitcutoff": "Strict",
    "hitname": "mexN",
    "hitorientation": "-",
    "hitstart": 326943,
    "hitstop": 330020
  },
  {
    "analysis": "Antimicrobial Resistance",
    "contigid": "MOHB01000003.1",
    "filename": "GCA_001891995.1_ASM189199v1_genomic.fna",
    "hitcutoff": "Strict",
    "hitname": "PmrA",
    "hitorientation": "+",
    "hitstart": 28893,
    "hitstop": 29561
  },
  {
    "analysis": "Antimicrobial Resistance",
    "contigid": "MOHB01000003.1",
    "filename": "GCA_001891995.1_ASM189199v1_genomic.fna",
    "hitcutoff": "Strict",
    "hitname": "PmrB",
    "hitorientation": "+",
    "hitstart": 29562,
    "hitstop": 30662
  },
  {
    "analysis": "Antimicrobial Resistance",
    "contigid": "MOHB01000003.1",
    "filename": "GCA_001891995.1_ASM189199v1_genomic.fna",
    "hitcutoff": "Strict",
    "hitname": "PmrC",
    "hitorientation": "+",
    "hitstart": 27253,
    "hitstop": 28896
  },
  {
    "analysis": "Antimicrobial Resistance",
    "contigid": "MOHB01000003.1",
    "filename": "GCA_001891995.1_ASM189199v1_genomic.fna",
    "hitcutoff": "Strict",
    "hitname": "mdtN",
    "hitorientation": "+",
    "hitstart": 58230,
    "hitstop": 59261
  },
  {
    "analysis": "Antimicrobial Resistance",
    "contigid": "MOHB01000003.1",
    "filename": "GCA_001891995.1_ASM189199v1_genomic.fna",
    "hitcutoff": "Strict",
    "hitname": "mdtO",
    "hitorientation": "+",
    "hitstart": 59261,
    "hitstop": 61312
  },
  {
    "analysis": "Antimicrobial Resistance",
    "contigid": "MOHB01000003.1",
    "filename": "GCA_001891995.1_ASM189199v1_genomic.fna",
    "hitcutoff": "Strict",
    "hitname": "mdtP",
    "hitorientation": "+",
    "hitstart": 61309,
    "hitstop": 62775
  },
  {
    "analysis": "Antimicrobial Resistance",
    "contigid": "MOHB01000004.1",
    "filename": "GCA_001891995.1_ASM189199v1_genomic.fna",
    "hitcutoff": "Strict",
    "hitname": "mdtK",
    "hitorientation": "+",
    "hitstart": 126030,
    "hitstop": 127403
  },
  {
    "analysis": "Antimicrobial Resistance",
    "contigid": "MOHB01000005.1",
    "filename": "GCA_001891995.1_ASM189199v1_genomic.fna",
    "hitcutoff": "Strict",
    "hitname": "ACT-7",
    "hitorientation": "-",
    "hitstart": 4604,
    "hitstop": 5737
  },
  {
    "analysis": "Antimicrobial Resistance",
    "contigid": "MOHB01000005.1",
    "filename": "GCA_001891995.1_ASM189199v1_genomic.fna",
    "hitcutoff": "Strict",
    "hitname": "mdtM",
    "hitorientation": "-",
    "hitstart": 187550,
    "hitstop": 188782
  },
  {
    "analysis": "Antimicrobial Resistance",
    "contigid": "MOHB01000005.1",
    "filename": "GCA_001891995.1_ASM189199v1_genomic.fna",
    "hitcutoff": "Strict",
    "hitname": "robA",
    "hitorientation": "-",
    "hitstart": 251658,
    "hitstop": 252527
  },
  {
    "analysis": "Antimicrobial Resistance",
    "contigid": "MOHB01000006.1",
    "filename": "GCA_001891995.1_ASM189199v1_genomic.fna",
    "hitcutoff": "Strict",
    "hitname": "CRP",
    "hitorientation": "-",
    "hitstart": 176803,
    "hitstop": 177435
  },
  {
    "analysis": "Antimicrobial Resistance",
    "contigid": "MOHB01000006.1",
    "filename": "GCA_001891995.1_ASM189199v1_genomic.fna",
    "hitcutoff": "Strict",
    "hitname": "gadX",
    "hitorientation": "+",
    "hitstart": 397,
    "hitstop": 1221
  },
  {
    "analysis": "Antimicrobial Resistance",
    "contigid": "MOHB01000006.1",
    "filename": "GCA_001891995.1_ASM189199v1_genomic.fna",
    "hitcutoff": "Strict",
    "hitname": "mdtE",
    "hitorientation": "-",
    "hitstart": 5818,
    "hitstop": 6975
  },
  {
    "analysis": "Antimicrobial Resistance",
    "contigid": "MOHB01000006.1",
    "filename": "GCA_001891995.1_ASM189199v1_genomic.fna",
    "hitcutoff": "Strict",
    "hitname": "mexD",
    "hitorientation": "-",
    "hitstart": 2680,
    "hitstop": 5793
  },
  {
    "analysis": "Antimicrobial Resistance",
    "contigid": "MOHB01000007.1",
    "filename": "GCA_001891995.1_ASM189199v1_genomic.fna",
    "hitcutoff": "Perfect",
    "hitname": "H-NS",
    "hitorientation": "-",
    "hitstart": 187722,
    "hitstop": 188135
  },
  {
    "analysis": "Antimicrobial Resistance",
    "contigid": "MOHB01000007.1",
    "filename": "GCA_001891995.1_ASM189199v1_genomic.fna",
    "hitcutoff": "Perfect",
    "hitname": "mdtG",
    "hitorientation": "-",
    "hitstart": 25571,
    "hitstop": 26797
  },
  {
    "analysis": "Antimicrobial Resistance",
    "contigid": "MOHB01000007.1",
    "filename": "GCA_001891995.1_ASM189199v1_genomic.fna",
    "hitcutoff": "Strict",
    "hitname": "mdtH",
    "hitorientation": "-",
    "hitstart": 35428,
    "hitstop": 36636
  },
  {
    "analysis": "Antimicrobial Resistance",
    "contigid": "MOHB01000007.1",
    "filename": "GCA_001891995.1_ASM189199v1_genomic.fna",
    "hitcutoff": "Strict",
    "hitname": "phoP",
    "hitorientation": "-",
    "hitstart": 101156,
    "hitstop": 101827
  },
  {
    "analysis": "Antimicrobial Resistance",
    "contigid": "MOHB01000007.1",
    "filename": "GCA_001891995.1_ASM189199v1_genomic.fna",
    "hitcutoff": "Perfect",
    "hitname": "phoQ",
    "hitorientation": "-",
    "hitstart": 99696,
    "hitstop": 101156
  },
  {
    "analysis": "Antimicrobial Resistance",
    "contigid": "MOHB01000008.1",
    "filename": "GCA_001891995.1_ASM189199v1_genomic.fna",
    "hitcutoff": "Strict",
    "hitname": "emrK",
    "hitorientation": "-",
    "hitstart": 9140,
    "hitstop": 10303
  },
  {
    "analysis": "Antimicrobial Resistance",
    "contigid": "MOHB01000008.1",
    "filename": "GCA_001891995.1_ASM189199v1_genomic.fna",
    "hitcutoff": "Strict",
    "hitname": "emrY",
    "hitorientation": "-",
    "hitstart": 7602,
    "hitstop": 9140
  },
  {
    "analysis": "Antimicrobial Resistance",
    "contigid": "MOHB01000008.1",
    "filename": "GCA_001891995.1_ASM189199v1_genomic.fna",
    "hitcutoff": "Perfect",
    "hitname": "evgA",
    "hitorientation": "+",
    "hitstart": 10719,
    "hitstop": 11333
  },
  {
    "analysis": "Antimicrobial Resistance",
    "contigid": "MOHB01000008.1",
    "filename": "GCA_001891995.1_ASM189199v1_genomic.fna",
    "hitcutoff": "Strict",
    "hitname": "evgS",
    "hitorientation": "+",
    "hitstart": 11338,
    "hitstop": 14931
  },
  {
    "analysis": "Antimicrobial Resistance",
    "contigid": "MOHB01000008.1",
    "filename": "GCA_001891995.1_ASM189199v1_genomic.fna",
    "hitcutoff": "Strict",
    "hitname": "mexD",
    "hitorientation": "+",
    "hitstart": 104776,
    "hitstop": 107889
  },
  {
    "analysis": "Antimicrobial Resistance",
    "contigid": "MOHB01000009.1",
    "filename": "GCA_001891995.1_ASM189199v1_genomic.fna",
    "hitcutoff": "Perfect",
    "hitname": "cpxA",
    "hitorientation": "+",
    "hitstart": 22429,
    "hitstop": 23802
  },
  {
    "analysis": "Antimicrobial Resistance",
    "contigid": "MOHB01000009.1",
    "filename": "GCA_001891995.1_ASM189199v1_genomic.fna",
    "hitcutoff": "Perfect",
    "hitname": "cpxR",
    "hitorientation": "+",
    "hitstart": 21734,
    "hitstop": 22432
  },
  {
    "analysis": "Antimicrobial Resistance",
    "contigid": "MOHB01000011.1",
    "filename": "GCA_001891995.1_ASM189199v1_genomic.fna",
    "hitcutoff": "Strict",
    "hitname": "Escherichia coli marR mutant resulting in antibiotic resistance",
    "hitorientation": "+",
    "hitstart": 51100,
    "hitstop": 51534
  },
  {
    "analysis": "Antimicrobial Resistance",
    "contigid": "MOHB01000011.1",
    "filename": "GCA_001891995.1_ASM189199v1_genomic.fna",
    "hitcutoff": "Perfect",
    "hitname": "marA",
    "hitorientation": "+",
    "hitstart": 51554,
    "hitstop": 51937
  },
  {
    "analysis": "Antimicrobial Resistance",
    "contigid": "MOHB01000012.1",
    "filename": "GCA_001891995.1_ASM189199v1_genomic.fna",
    "hitcutoff": "Strict",
    "hitname": "emrA",
    "hitorientation": "-",
    "hitstart": 312493,
    "hitstop": 313665
  },
  {
    "analysis": "Antimicrobial Resistance",
    "contigid": "MOHB01000012.1",
    "filename": "GCA_001891995.1_ASM189199v1_genomic.fna",
    "hitcutoff": "Perfect",
    "hitname": "emrB",
    "hitorientation": "-",
    "hitstart": 310938,
    "hitstop": 312476
  },
  {
    "analysis": "Antimicrobial Resistance",
    "contigid": "MOHB01000012.1",
    "filename": "GCA_001891995.1_ASM189199v1_genomic.fna",
    "hitcutoff": "Strict",
    "hitname": "emrR",
    "hitorientation": "-",
    "hitstart": 313792,
    "hitstop": 314322
  },
  {
    "analysis": "Antimicrobial Resistance",
    "contigid": "MOHB01000013.1",
    "filename": "GCA_001891995.1_ASM189199v1_genomic.fna",
    "hitcutoff": "Strict",
    "hitname": "Staphylococcus aureus gyrB conferring resistance to aminocoumarin",
    "hitorientation": "-",
    "hitstart": 131568,
    "hitstop": 133982
  },
  {
    "analysis": "Antimicrobial Resistance",
    "contigid": "MOHB01000013.1",
    "filename": "GCA_001891995.1_ASM189199v1_genomic.fna",
    "hitcutoff": "Strict",
    "hitname": "emrD",
    "hitorientation": "+",
    "hitstart": 107782,
    "hitstop": 108966
  },
  {
    "analysis": "Antimicrobial Resistance",
    "contigid": "MOHB01000013.1",
    "filename": "GCA_001891995.1_ASM189199v1_genomic.fna",
    "hitcutoff": "Perfect",
    "hitname": "mdtL",
    "hitorientation": "+",
    "hitstart": 145479,
    "hitstop": 146654
  },
  {
    "analysis": "Antimicrobial Resistance",
    "contigid": "MOHB01000015.1",
    "filename": "GCA_001891995.1_ASM189199v1_genomic.fna",
    "hitcutoff": "Strict",
    "hitname": "Escherichia coli parC conferring resistance to fluoroquinolone",
    "hitorientation": "-",
    "hitstart": 68709,
    "hitstop": 70967
  },
  {
    "analysis": "Antimicrobial Resistance",
    "contigid": "MOHB01000015.1",
    "filename": "GCA_001891995.1_ASM189199v1_genomic.fna",
    "hitcutoff": "Strict",
    "hitname": "bacA",
    "hitorientation": "-",
    "hitstart": 104717,
    "hitstop": 105538
  },
  {
    "analysis": "Antimicrobial Resistance",
    "contigid": "MOHB01000015.1",
    "filename": "GCA_001891995.1_ASM189199v1_genomic.fna",
    "hitcutoff": "Strict",
    "hitname": "tolC",
    "hitorientation": "+",
    "hitstart": 80879,
    "hitstop": 82360
  },
  {
    "analysis": "Antimicrobial Resistance",
    "contigid": "MOHB01000016.1",
    "filename": "GCA_001891995.1_ASM189199v1_genomic.fna",
    "hitcutoff": "Strict",
    "hitname": "ACT-7",
    "hitorientation": "+",
    "hitstart": 286,
    "hitstop": 1431
  },
  {
    "analysis": "Antimicrobial Resistance",
    "contigid": "MOHB01000022.1",
    "filename": "GCA_001891995.1_ASM189199v1_genomic.fna",
    "hitcutoff": "Strict",
    "hitname": "Mycobacterium tuberculosis rpoB mutants conferring resistance to rifampicin",
    "hitorientation": "-",
    "hitstart": 22720,
    "hitstop": 26748
  },
  {
    "analysis": "Antimicrobial Resistance",
    "contigid": "MOHB01000023.1",
    "filename": "GCA_001891995.1_ASM189199v1_genomic.fna",
    "hitcutoff": "Strict",
    "hitname": "macA",
    "hitorientation": "-",
    "hitstart": 5642,
    "hitstop": 6757
  },
  {
    "analysis": "Antimicrobial Resistance",
    "contigid": "MOHB01000023.1",
    "filename": "GCA_001891995.1_ASM189199v1_genomic.fna",
    "hitcutoff": "Strict",
    "hitname": "macB",
    "hitorientation": "-",
    "hitstart": 3699,
    "hitstop": 5645
  },
  {
    "analysis": "Antimicrobial Resistance",
    "contigid": "MOHB01000023.1",
    "filename": "GCA_001891995.1_ASM189199v1_genomic.fna",
    "hitcutoff": "Strict",
    "hitname": "mdfA",
    "hitorientation": "-",
    "hitstart": 39796,
    "hitstop": 41028
  },
  {
    "analysis": "Antimicrobial Resistance",
    "contigid": "MOHB01000024.1",
    "filename": "GCA_001891995.1_ASM189199v1_genomic.fna",
    "hitcutoff": "Perfect",
    "hitname": "CTX-M-55",
    "hitorientation": "-",
    "hitstart": 37702,
    "hitstop": 38577
  },
  {
    "analysis": "Antimicrobial Resistance",
    "contigid": "MOHB01000026.1",
    "filename": "GCA_001891995.1_ASM189199v1_genomic.fna",
    "hitcutoff": "Strict",
    "hitname": "Mycobacterium tuberculosis katG mutations conferring resistance to isoniazid",
    "hitorientation": "+",
    "hitstart": 8536,
    "hitstop": 10716
  },
  {
    "analysis": "Antimicrobial Resistance",
    "contigid": "MOHB01000027.1",
    "filename": "GCA_001891995.1_ASM189199v1_genomic.fna",
    "hitcutoff": "Strict",
    "hitname": "APH(3'')",
    "hitorientation": "-",
    "hitstart": 10215,
    "hitstop": 11018
  },
  {
    "analysis": "Antimicrobial Resistance",
    "contigid": "MOHB01000027.1",
    "filename": "GCA_001891995.1_ASM189199v1_genomic.fna",
    "hitcutoff": "Perfect",
    "hitname": "APH(6)",
    "hitorientation": "-",
    "hitstart": 9379,
    "hitstop": 10215
  },
  {
    "analysis": "Antimicrobial Resistance",
    "contigid": "MOHB01000027.1",
    "filename": "GCA_001891995.1_ASM189199v1_genomic.fna",
    "hitcutoff": "Strict",
    "hitname": "floR",
    "hitorientation": "+",
    "hitstart": 5030,
    "hitstop": 6244
  },
  {
    "analysis": "Antimicrobial Resistance",
    "contigid": "MOHB01000027.1",
    "filename": "GCA_001891995.1_ASM189199v1_genomic.fna",
    "hitcutoff": "Perfect",
    "hitname": "sul2",
    "hitorientation": "-",
    "hitstart": 11079,
    "hitstop": 11894
  },
  {
    "analysis": "Antimicrobial Resistance",
    "contigid": "MOHB01000027.1",
    "filename": "GCA_001891995.1_ASM189199v1_genomic.fna",
    "hitcutoff": "Strict",
    "hitname": "tetG",
    "hitorientation": "-",
    "hitstart": 6844,
    "hitstop": 8043
  },
  {
    "analysis": "Antimicrobial Resistance",
    "contigid": "MOHB01000028.1",
    "filename": "GCA_001891995.1_ASM189199v1_genomic.fna",
    "hitcutoff": "Strict",
    "hitname": "emrE",
    "hitorientation": "+",
    "hitstart": 30648,
    "hitstop": 30980
  },
  {
    "analysis": "Antimicrobial Resistance",
    "contigid": "MOHB01000032.1",
    "filename": "GCA_001891995.1_ASM189199v1_genomic.fna",
    "hitcutoff": "Perfect",
    "hitname": "acrE",
    "hitorientation": "+",
    "hitstart": 32702,
    "hitstop": 33859
  },
  {
    "analysis": "Antimicrobial Resistance",
    "contigid": "MOHB01000032.1",
    "filename": "GCA_001891995.1_ASM189199v1_genomic.fna",
    "hitcutoff": "Strict",
    "hitname": "acrS",
    "hitorientation": "-",
    "hitstart": 31641,
    "hitstop": 32303
  },
  {
    "analysis": "Antimicrobial Resistance",
    "contigid": "MOHB01000032.1",
    "filename": "GCA_001891995.1_ASM189199v1_genomic.fna",
    "hitcutoff": "Strict",
    "hitname": "mexD",
    "hitorientation": "+",
    "hitstart": 33871,
    "hitstop": 36975
  },
  {
    "analysis": "Antimicrobial Resistance",
    "contigid": "MOHB01000036.1",
    "filename": "GCA_001891995.1_ASM189199v1_genomic.fna",
    "hitcutoff": "Strict",
    "hitname": "Klebsiella pneumoniae acrR mutant resulting in high level antibiotic resistance",
    "hitorientation": "+",
    "hitstart": 107902,
    "hitstop": 108495
  },
  {
    "analysis": "Antimicrobial Resistance",
    "contigid": "MOHB01000036.1",
    "filename": "GCA_001891995.1_ASM189199v1_genomic.fna",
    "hitcutoff": "Strict",
    "hitname": "acrE",
    "hitorientation": "-",
    "hitstart": 106513,
    "hitstop": 107706
  },
  {
    "analysis": "Antimicrobial Resistance",
    "contigid": "MOHB01000036.1",
    "filename": "GCA_001891995.1_ASM189199v1_genomic.fna",
    "hitcutoff": "Strict",
    "hitname": "mexD",
    "hitorientation": "-",
    "hitstart": 103341,
    "hitstop": 106490
  },
  {
    "analysis": "Antimicrobial Resistance",
    "contigid": "MOHB01000036.1",
    "filename": "GCA_001891995.1_ASM189199v1_genomic.fna",
    "hitcutoff": "Strict",
    "hitname": "rosA",
    "hitorientation": "-",
    "hitstart": 125513,
    "hitstop": 126733
  },
  {
    "analysis": "Antimicrobial Resistance",
    "contigid": "MOHB01000036.1",
    "filename": "GCA_001891995.1_ASM189199v1_genomic.fna",
    "hitcutoff": "Strict",
    "hitname": "rosB",
    "hitorientation": "-",
    "hitstart": 123599,
    "hitstop": 125275
  },
  {
    "analysis": "Antimicrobial Resistance",
    "contigid": "MOHB01000036.1",
    "filename": "GCA_001891995.1_ASM189199v1_genomic.fna",
    "hitcutoff": "Strict",
    "hitname": "vanG",
    "hitorientation": "-",
    "hitstart": 19876,
    "hitstop": 20970
  },
  {
    "analysis": "Antimicrobial Resistance",
    "contigid": "MOHB01000037.1",
    "filename": "GCA_001891995.1_ASM189199v1_genomic.fna",
    "hitcutoff": "Perfect",
    "hitname": "MCR-1",
    "hitorientation": "+",
    "hitstart": 13553,
    "hitstop": 15178
  },
  {
    "analysis": "Antimicrobial Resistance",
    "contigid": "MOHB01000050.1",
    "filename": "GCA_001891995.1_ASM189199v1_genomic.fna",
    "hitcutoff": "Perfect",
    "hitname": "FosA3",
    "hitorientation": "+",
    "hitstart": 4459,
    "hitstop": 4875
  },
  {
    "analysis": "Antimicrobial Resistance",
    "contigid": "MOHB01000050.1",
    "filename": "GCA_001891995.1_ASM189199v1_genomic.fna",
    "hitcutoff": "Perfect",
    "hitname": "mphA",
    "hitorientation": "+",
    "hitstart": 89,
    "hitstop": 994
  },
  {
    "analysis": "Antimicrobial Resistance",
    "contigid": "MOHB01000053.1",
    "filename": "GCA_001891995.1_ASM189199v1_genomic.fna",
    "hitcutoff": "Strict",
    "hitname": "ErmB",
    "hitorientation": "-",
    "hitstart": 1455,
    "hitstop": 2192
  },
  {
    "analysis": "Antimicrobial Resistance",
    "contigid": "MOHB01000062.1",
    "filename": "GCA_001891995.1_ASM189199v1_genomic.fna",
    "hitcutoff": "Perfect",
    "hitname": "sul1",
    "hitorientation": "+",
    "hitstart": 452,
    "hitstop": 1291
  },
  {
    "analysis": "Antimicrobial Resistance",
    "contigid": "MOHB01000064.1",
    "filename": "GCA_001891995.1_ASM189199v1_genomic.fna",
    "hitcutoff": "Perfect",
    "hitname": "TEM-1",
    "hitorientation": "+",
    "hitstart": 3455,
    "hitstop": 4315
  },
  {
    "analysis": "Antimicrobial Resistance",
    "contigid": "MOHB01000080.1",
    "filename": "GCA_001891995.1_ASM189199v1_genomic.fna",
    "hitcutoff": "Perfect",
    "hitname": "NDM-1",
    "hitorientation": "+",
    "hitstart": 724,
    "hitstop": 1536
  },
  {
    "analysis": "Antimicrobial Resistance",
    "contigid": "MOHB01000090.1",
    "filename": "GCA_001891995.1_ASM189199v1_genomic.fna",
    "hitcutoff": "Strict",
    "hitname": "aadA11",
    "hitorientation": "+",
    "hitstart": 690,
    "hitstop": 1535
  },
  {
    "analysis": "Antimicrobial Resistance",
    "contigid": "MOHB01000090.1",
    "filename": "GCA_001891995.1_ASM189199v1_genomic.fna",
    "hitcutoff": "Strict",
    "hitname": "dfrA25",
    "hitorientation": "+",
    "hitstart": 36,
    "hitstop": 509
  },
  {
    "analysis": "Antimicrobial Resistance",
    "contigid": "MOHB01000098.1",
    "filename": "GCA_001891995.1_ASM189199v1_genomic.fna",
    "hitcutoff": "Perfect",
    "hitname": "catI",
    "hitorientation": "-",
    "hitstart": 166,
    "hitstop": 825
  },
  {
    "analysis": "Antimicrobial Resistance",
    "contigid": "MOHB01000101.1",
    "filename": "GCA_001891995.1_ASM189199v1_genomic.fna",
    "hitcutoff": "Perfect",
    "hitname": "arr-3",
    "hitorientation": "+",
    "hitstart": 37,
    "hitstop": 489
  },
  {
    "analysis": "Antimicrobial Resistance",
    "contigid": "MOHB01000104.1",
    "filename": "GCA_001891995.1_ASM189199v1_genomic.fna",
    "hitcutoff": "Perfect",
    "hitname": "rmtB",
    "hitorientation": "+",
    "hitstart": 43,
    "hitstop": 798
  },
  {
    "analysis": "Antimicrobial Resistance",
    "contigid": "MOHB01000106.1",
    "filename": "GCA_001891995.1_ASM189199v1_genomic.fna",
    "hitcutoff": "Perfect",
    "hitname": "aadA5",
    "hitorientation": "-",
    "hitstart": 115,
    "hitstop": 903
  }
]

BEAUTIFY_STX1 = [
  {
    "contig": "lcl|ECI-2644|NODE_8_length_178521_cov_25.218_ID_15",
    "genome": "ECI-2644_lcl.fasta",
    "probability": 0.9561446,
    "start": 174535,
    "stop": 175491,
    "subtype": "a",
    "subtype_gene": "stx1A"
  },
  {
    "contig": "lcl|ECI-2644|NODE_8_length_178521_cov_25.218_ID_15",
    "genome": "ECI-2644_lcl.fasta",
    "probability": 0.9561446,
    "start": 175501,
    "stop": 175770,
    "subtype": "a",
    "subtype_gene": "stx1B"
  },
  {
    "contig": "lcl|ECI-2644|NODE_8_length_178521_cov_25.218_ID_15",
    "genome": "ECI-2644_lcl.fasta",
    "probability": 0.9561446,
    "start": 174544,
    "stop": 175491,
    "subtype": "a",
    "subtype_gene": "stx1A"
  },
  {
    "contig": "lcl|ECI-2644|NODE_8_length_178521_cov_25.218_ID_15",
    "genome": "ECI-2644_lcl.fasta",
    "probability": 0.9561446,
    "start": 175501,
    "stop": 175770,
    "subtype": "a",
    "subtype_gene": "stx1B"
  }
]

BEAUTIFY_STX2 = [
  {
    "contig": "lcl|ECI-2644|NODE_51_length_5713_cov_24.063_ID_101",
    "genome": "ECI-2644_lcl.fasta",
    "probability": 0.9460619,
    "start": 4390,
    "stop": 5349,
    "subtype": "a",
    "subtype_gene": "stx2A"
  },
  {
    "contig": "lcl|ECI-2644|NODE_51_length_5713_cov_24.063_ID_101",
    "genome": "ECI-2644_lcl.fasta",
    "probability": 0.9460619,
    "start": 4109,
    "stop": 4378,
    "subtype": "a",
    "subtype_gene": "stx2B"
  }
]

BEAUTIFY_EAE = [
  {
    "contig": "N/A",
    "genome": "GCA_000005845.2_ASM584v2_genomic.fna",
    "probability": "N/A",
    "start": "N/A",
    "stop": "N/A",
    "subtype": "Subtype loci not found in genome",
    "subtype_gene": "N/A"
  }
]
