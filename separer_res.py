def extraire_manu_auto(input):
    with open(input + ".txt", 'r') as input_file, open(input + '_manu.txt', 'w') as output_file_1, open(
            input + "_auto.txt", 'w') as output_file_2:
        for line in input_file:
            if any(filename in line for filename in ["barb_0001-4133_1919_num_5_1_T1_0021_0000",
                                                     "barb_0001-4133_1919_num_5_1_T1_0613_0000",
                                                     "barb_0001-4133_1920_num_6_1_T1_0012_0000",
                                                     "barb_0001-4133_1920_num_6_1_T1_0296_0000",
                                                     "barb_0001-4133_1929_num_15_1_T1_0235_0000",
                                                     "barb_0001-4133_1939_num_25_1_T1_0321_0000",
                                                     "barb_0001-4133_1941_num_27_1_T1_0022_0000",
                                                     "barb_0001-4133_1963_num_49_1_T1_0135_0000",
                                                     "barb_0001-4141_1907_num_9_1_T1_0675_0000",
                                                     "rnord_0035-2624_1934_num_20_78_T1_0117_0000",
                                                     "rnord_0035-2624_1952_num_34_133_T1_0080_0000",
                                                     "barb_0001-4133_1919_num_5_1_T1_0005_0000",
                                                     "barb_0001-4133_1919_num_5_1_T1_0006_0000",
                                                     "barb_0001-4141_1910_num_12_1_F_0001_0000",
                                                     "barb_0001-4141_1910_num_12_1_F_0002_0000",
                                                     "barb_0001-4141_1910_num_12_1_T1_0017_0000",
                                                     "barb_0001-4141_1919_num_5_1_T1_0007_0000",
                                                     "rnord_0035-2624_1927_num_13_51_T1_0172_0000",
                                                     "rnord_0035-2624_1928_num_14_53_T1_0023_0000"]):
                output_file_1.write(line)
            else:
                output_file_2.write(line)


extraire_manu_auto("approximation1x1")
extraire_manu_auto("approximation2x3")
extraire_manu_auto("extrapolation1x1")
extraire_manu_auto("extrapolation2x3")
extraire_manu_auto("interpolation1x1")
extraire_manu_auto("interpolation2x3")
