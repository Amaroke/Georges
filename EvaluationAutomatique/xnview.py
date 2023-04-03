import time
from PIL import Image
import numpy as np

tripletsExpert = [
    ["barb_0001-4133_1919_num_5_1_T1_0032_0000", 55, 236, 0.75],
    ["barb_0001-4133_1920_num_6_1_T1_0051_0000", 30, 233, 0.8],
    ["barb_0001-4133_1929_num_15_1_T1_0046_0000", 35, 228, 0.8],
    ["barb_0001-4133_1939_num_25_1_T1_0123_0000", 30, 235, 0.8],
    ["barb_0001-4133_1941_num_27_1_T1_0032_0000", 30, 240, 1],
    ["barb_0001-4133_1963_num_49_1_T1_0020_0000", 30, 240, 1],
    ["barb_0001-4141_1907_num_9_1_T1_0010_0000", 35, 214, 0.85],
    ["barb_0001-4141_1909_num_11_1_T1_0011_0000", 30, 222, 1],
    ["barb_0001-4141_1910_num_12_1_T1_0034_0000", 30, 215, 1],
    ["barb_0001-4141_1919_num_5_1_T1_0002_0000", 35, 200, 0.7],
    ["rnord_0035-2624_1925_num_11_43_T1_0171_0000", 10, 230, 1],
    ["rnord_0035-2624_1927_num_13_51_T1_0206_0000", 15, 220, 1],
    ["rnord_0035-2624_1928_num_14_53_T1_0059_0000", 25, 200, 1],
    ["rnord_0035-2624_1933_num_19_75_T1_0211_0000", 1, 200, 0.8],
    ["rnord_0035-2624_1934_num_20_78_T1_0156_0000", 20, 230, 1],
    ["rnord_0035-2624_1934_num_20_80_T1_0342_0000", 10, 245, 1],
    ["rnord_0035-2624_1952_num_34_133_T1_0005_0000", 1, 215, 0.8],
    ["rnord_0035-2624_1960_num_42_167_T1_0007_0000", 1, 195, 0.85],
    ["rnord_0035-2624_1964_num_46_181_T1_0131_0000", 1, 210, 0.85],
    ["rnord_0035-2624_1967_num_49_192_T1_0005_0000", 1, 210, 0.9],
    ["rnord_0035-2624_1970_num_52_204_T1_0007_0000", 1, 210, 0.9],
    ["rnord_0035-2624_1976_num_58_228_T1_0042_0000", 1, 230, 0.9],
    ["rnord_0035-2624_1976_num_58_230_T1_0373_0000", 1, 225, 0.8],
    ["rnord_0035-2624_1979_num_61_241_T1_0315_0000", 1, 215, 1],
    ["rnord_0035-2624_1979_num_61_242_T1_0541_0000", 1, 215, 0.9],
    ["rnord_0035-2624_1989_num_71_282_T1_0615_0000", 1, 205, 0.75],
    ["rnord_0035-2624_1991_num_73_290_T1_0241_0000", 30, 255, 0.75],
    ["rnord_0035-2624_1994_num_76_306_T1_0467_0000", 30, 255, 0.7],
    ["binet_0750-7496_1900_num_1_1_T1_0006_0000", 90, 230, 1],
    ["binet_0750-750X_1918_num_18_120_T1_0078_0000", 70, 172, 0.8],
    ["asgn_0767-7367_1980_num_100_1_T1_0006_0000", 0, 228, 0.85],
    ["asgn_0767-7367_1980_num_100_2_T1_0062_0000", 0, 228, 0.85],
    ["asgn_0767-7367_1980_num_100_3_T1_0113_0000", 30, 220, 0.85],
    ["asgn_0767-7367_1980_num_100_4_T1_0161_0000", 30, 230, 0.85],
    ["asgn_0767-7367_1981_num_101_1_T1_0006_0000", 1, 230, 0.85],
    ["asgn_0767-7367_1981_num_101_2_T1_0052_0000", 1, 225, 0.85],
    ["lesb_0754-944X_1988_num_65_1_T1_0011_0000", 60, 204, 1],
    ["femou_0180-4162_1978_num_6_1_T1_0019_0000", 45, 198, 1],
    ["nbeur_0000-0007_1996_num_0_1_T1_0004_0000", 53, 210, 1]
]

tripletsApproximation1x1 = [
    ["barb_0001-4133_1919_num_5_1_T1_0032_0000", 0, 230, 0.7],
    ["barb_0001-4133_1920_num_6_1_T1_0051_0000", 0, 230, 0.7],
    ["barb_0001-4133_1929_num_15_1_T1_0046_0000", 30, 250, 0.85],
    ["barb_0001-4133_1939_num_25_1_T1_0123_0000", 30, 240, 1.0],
    ["barb_0001-4133_1941_num_27_1_T1_0032_0000", 0, 225, 0.8],
    ["barb_0001-4133_1963_num_49_1_T1_0020_0000", 60, 240, 1.0],
    ["barb_0001-4141_1907_num_9_1_T1_0010_0000", 60, 240, 1.0],
    ["barb_0001-4141_1909_num_11_1_T1_0011_0000", 0, 225, 0.8],
    ["barb_0001-4141_1910_num_12_1_T1_0034_0000", 0, 235, 0.9],
    ["barb_0001-4141_1919_num_5_1_T1_0002_0000", 30, 240, 1.0],
    ["rnord_0035-2624_1925_num_11_43_T1_0171_0000", 0, 235, 0.9],
    ["rnord_0035-2624_1927_num_13_51_T1_0206_0000", 0, 230, 0.9],
    ["rnord_0035-2624_1928_num_14_53_T1_0059_0000", 0, 230, 0.9],
    ["rnord_0035-2624_1933_num_19_75_T1_0211_0000", 0, 240, 0.9],
    ["rnord_0035-2624_1934_num_20_78_T1_0156_0000", 30, 220, 1.0],
    ["rnord_0035-2624_1934_num_20_80_T1_0342_0000", 0, 240, 0.9],
    ["rnord_0035-2624_1952_num_34_133_T1_0005_0000", 30, 240, 1.0],
    ["rnord_0035-2624_1960_num_42_167_T1_0007_0000", 30, 220, 1.0],
    ["rnord_0035-2624_1964_num_46_181_T1_0131_0000", 30, 220, 1.0],
    ["rnord_0035-2624_1967_num_49_192_T1_0005_0000", 30, 220, 1.0],
    ["rnord_0035-2624_1970_num_52_204_T1_0007_0000", 30, 220, 1.0],
    ["rnord_0035-2624_1976_num_58_228_T1_0042_0000", 0, 235, 0.9],
    ["rnord_0035-2624_1976_num_58_230_T1_0373_0000", 0, 235, 0.9],
    ["rnord_0035-2624_1979_num_61_241_T1_0315_0000", 30, 220, 1.0],
    ["rnord_0035-2624_1979_num_61_242_T1_0541_0000", 30, 220, 1.0],
    ["rnord_0035-2624_1989_num_71_282_T1_0615_0000", 30, 240, 1.0],
    ["rnord_0035-2624_1991_num_73_290_T1_0241_0000", 0, 240, 0.8],
    ["rnord_0035-2624_1994_num_76_306_T1_0467_0000", 0, 230, 0.7],
    ["binet_0750-7496_1900_num_1_1_T1_0006_0000", 0, 225, 0.8],
    ["binet_0750-750X_1918_num_18_120_T1_0078_0000", 30, 220, 1.0],
    ["asgn_0767-7367_1980_num_100_1_T1_0006_0000", 30, 220, 1.0],
    ["asgn_0767-7367_1980_num_100_2_T1_0062_0000", 30, 220, 1.0],
    ["asgn_0767-7367_1980_num_100_3_T1_0113_0000", 30, 240, 1.0],
    ["asgn_0767-7367_1980_num_100_4_T1_0161_0000", 30, 220, 1.0],
    ["asgn_0767-7367_1981_num_101_1_T1_0006_0000", 30, 240, 1.0],
    ["asgn_0767-7367_1981_num_101_2_T1_0052_0000", 30, 220, 1.0],
    ["lesb_0754-944X_1988_num_65_1_T1_0011_0000", 30, 220, 1.0],
    ["femou_0180-4162_1978_num_6_1_T1_0019_0000", 30, 220, 1.0],
    ["nbeur_0000-0007_1996_num_0_1_T1_0004_0000", 30, 240, 1.0]
]

tripletsApproximation2x3 = [
    ["barb_0001-4133_1919_num_5_1_T1_0032_0000", 30, 240, 0.7],
    ["barb_0001-4133_1920_num_6_1_T1_0051_0000", 20, 250, 0.7],
    ["barb_0001-4133_1929_num_15_1_T1_0046_0000", 0, 225, 0.8],
    ["barb_0001-4133_1939_num_25_1_T1_0123_0000", 0, 245, 0.8],
    ["barb_0001-4133_1941_num_27_1_T1_0032_0000", 30, 250, 0.85],
    ["barb_0001-4133_1963_num_49_1_T1_0020_0000", 0, 245, 0.8],
    ["barb_0001-4141_1907_num_9_1_T1_0010_0000", 30, 240, 1.0],
    ["barb_0001-4141_1909_num_11_1_T1_0011_0000", 0, 230, 0.9],
    ["barb_0001-4141_1910_num_12_1_T1_0034_0000", 0, 235, 0.9],
    ["barb_0001-4141_1919_num_5_1_T1_0002_0000", 20, 250, 0.7],
    ["rnord_0035-2624_1925_num_11_43_T1_0171_0000", 0, 230, 0.7],
    ["rnord_0035-2624_1927_num_13_51_T1_0206_0000", 0, 230, 0.9],
    ["rnord_0035-2624_1928_num_14_53_T1_0059_0000", 30, 245, 1.0],
    ["rnord_0035-2624_1933_num_19_75_T1_0211_0000", 0, 240, 0.9],
    ["rnord_0035-2624_1934_num_20_78_T1_0156_0000", 0, 240, 0.9],
    ["rnord_0035-2624_1934_num_20_80_T1_0342_0000", 30, 240, 1.0],
    ["rnord_0035-2624_1952_num_34_133_T1_0005_0000", 30, 220, 1.0],
    ["rnord_0035-2624_1960_num_42_167_T1_0007_0000", 30, 220, 1.0],
    ["rnord_0035-2624_1964_num_46_181_T1_0131_0000", 30, 220, 1.0],
    ["rnord_0035-2624_1967_num_49_192_T1_0005_0000", 30, 220, 1.0],
    ["rnord_0035-2624_1970_num_52_204_T1_0007_0000", 30, 220, 1.0],
    ["rnord_0035-2624_1976_num_58_228_T1_0042_0000", 30, 245, 1.0],
    ["rnord_0035-2624_1976_num_58_230_T1_0373_0000", 30, 250, 0.85],
    ["rnord_0035-2624_1979_num_61_241_T1_0315_0000", 30, 220, 1.0],
    ["rnord_0035-2624_1979_num_61_242_T1_0541_0000", 30, 240, 1.0],
    ["rnord_0035-2624_1989_num_71_282_T1_0615_0000", 30, 220, 1.0],
    ["rnord_0035-2624_1991_num_73_290_T1_0241_0000", 60, 240, 1.0],
    ["rnord_0035-2624_1994_num_76_306_T1_0467_0000", 30, 240, 1.0],
    ["binet_0750-7496_1900_num_1_1_T1_0006_0000", 0, 225, 0.8],
    ["binet_0750-750X_1918_num_18_120_T1_0078_0000", 0, 230, 0.9],
    ["asgn_0767-7367_1980_num_100_1_T1_0006_0000", 30, 240, 1.0],
    ["asgn_0767-7367_1980_num_100_2_T1_0062_0000", 0, 230, 0.9],
    ["asgn_0767-7367_1980_num_100_3_T1_0113_0000", 0, 230, 0.9],
    ["asgn_0767-7367_1980_num_100_4_T1_0161_0000", 0, 230, 0.9],
    ["asgn_0767-7367_1981_num_101_1_T1_0006_0000", 30, 240, 1.0],
    ["asgn_0767-7367_1981_num_101_2_T1_0052_0000", 30, 240, 1.0],
    ["lesb_0754-944X_1988_num_65_1_T1_0011_0000", 30, 220, 1.0],
    ["femou_0180-4162_1978_num_6_1_T1_0019_0000", 0, 230, 0.9],
    ["nbeur_0000-0007_1996_num_0_1_T1_0004_0000", 30, 220, 1.0]
]

tripletsExtrapolation1x1 = [
    ["barb_0001-4133_1919_num_5_1_T1_0032_0000", 0, 230, 0.7],
    ["barb_0001-4133_1920_num_6_1_T1_0051_0000", 0, 230, 0.7],
    ["barb_0001-4133_1929_num_15_1_T1_0046_0000", 30, 250, 0.85],
    ["barb_0001-4133_1939_num_25_1_T1_0123_0000", 30, 240, 1.0],
    ["barb_0001-4133_1941_num_27_1_T1_0032_0000", 0, 225, 0.8],
    ["barb_0001-4133_1963_num_49_1_T1_0020_0000", 60, 240, 1.0],
    ["barb_0001-4141_1907_num_9_1_T1_0010_0000", 60, 240, 1.0],
    ["barb_0001-4141_1909_num_11_1_T1_0011_0000", 0, 225, 0.8],
    ["barb_0001-4141_1910_num_12_1_T1_0034_0000", 0, 235, 0.9],
    ["barb_0001-4141_1919_num_5_1_T1_0002_0000", 30, 240, 1.0],
    ["rnord_0035-2624_1925_num_11_43_T1_0171_0000", 0, 235, 0.9],
    ["rnord_0035-2624_1927_num_13_51_T1_0206_0000", 0, 230, 0.9],
    ["rnord_0035-2624_1928_num_14_53_T1_0059_0000", 0, 230, 0.9],
    ["rnord_0035-2624_1933_num_19_75_T1_0211_0000", 0, 240, 0.9],
    ["rnord_0035-2624_1934_num_20_78_T1_0156_0000", 30, 220, 1.0],
    ["rnord_0035-2624_1934_num_20_80_T1_0342_0000", 0, 240, 0.9],
    ["rnord_0035-2624_1952_num_34_133_T1_0005_0000", 30, 240, 1.0],
    ["rnord_0035-2624_1960_num_42_167_T1_0007_0000", 30, 195, 0.95],
    ["rnord_0035-2624_1964_num_46_181_T1_0131_0000", 30, 230, 0.85],
    ["rnord_0035-2624_1967_num_49_192_T1_0005_0000", 30, 210, 1.15],
    ["rnord_0035-2624_1970_num_52_204_T1_0007_0000", 30, 220, 1.0],
    ["rnord_0035-2624_1976_num_58_228_T1_0042_0000", 0, 235, 0.9],
    ["rnord_0035-2624_1976_num_58_230_T1_0373_0000", 0, 235, 0.9],
    ["rnord_0035-2624_1979_num_61_241_T1_0315_0000", 30, 220, 1.0],
    ["rnord_0035-2624_1979_num_61_242_T1_0541_0000", 30, 220, 1.0],
    ["rnord_0035-2624_1989_num_71_282_T1_0615_0000", 30, 240, 1.0],
    ["rnord_0035-2624_1991_num_73_290_T1_0241_0000", 0, 240, 0.8],
    ["rnord_0035-2624_1994_num_76_306_T1_0467_0000", 0, 230, 0.7],
    ["binet_0750-7496_1900_num_1_1_T1_0006_0000", 0, 225, 0.8],
    ["binet_0750-750X_1918_num_18_120_T1_0078_0000", 30, 220, 1.0],
    ["asgn_0767-7367_1980_num_100_1_T1_0006_0000", 30, 220, 1.0],
    ["asgn_0767-7367_1980_num_100_2_T1_0062_0000", 30, 220, 1.0],
    ["asgn_0767-7367_1980_num_100_3_T1_0113_0000", 30, 240, 1.0],
    ["asgn_0767-7367_1980_num_100_4_T1_0161_0000", 30, 220, 1.0],
    ["asgn_0767-7367_1981_num_101_1_T1_0006_0000", 30, 240, 1.0],
    ["asgn_0767-7367_1981_num_101_2_T1_0052_0000", 30, 220, 1.0],
    ["lesb_0754-944X_1988_num_65_1_T1_0011_0000", 30, 220, 1.0],
    ["femou_0180-4162_1978_num_6_1_T1_0019_0000", 30, 210, 1.15],
    ["nbeur_0000-0007_1996_num_0_1_T1_0004_0000", 30, 240, 1.0]
]

tripletsExtrapolation2x3 = [
    ["barb_0001-4133_1919_num_5_1_T1_0032_0000", 0, 245, 0.8],
    ["barb_0001-4133_1920_num_6_1_T1_0051_0000", 20, 250, 0.7],
    ["barb_0001-4133_1929_num_15_1_T1_0046_0000", 0, 225, 0.8],
    ["barb_0001-4133_1939_num_25_1_T1_0123_0000", 0, 245, 0.8],
    ["barb_0001-4133_1941_num_27_1_T1_0032_0000", 30, 250, 0.85],
    ["barb_0001-4133_1963_num_49_1_T1_0020_0000", 0, 245, 0.8],
    ["barb_0001-4141_1907_num_9_1_T1_0010_0000", 30, 240, 1.0],
    ["barb_0001-4141_1909_num_11_1_T1_0011_0000", 0, 230, 0.9],
    ["barb_0001-4141_1910_num_12_1_T1_0034_0000", 0, 235, 0.9],
    ["barb_0001-4141_1919_num_5_1_T1_0002_0000", 20, 250, 0.7],
    ["rnord_0035-2624_1925_num_11_43_T1_0171_0000", 0, 230, 0.7],
    ["rnord_0035-2624_1927_num_13_51_T1_0206_0000", 0, 230, 0.9],
    ["rnord_0035-2624_1928_num_14_53_T1_0059_0000", 30, 245, 1.0],
    ["rnord_0035-2624_1933_num_19_75_T1_0211_0000", 0, 240, 0.9],
    ["rnord_0035-2624_1934_num_20_78_T1_0156_0000", 0, 240, 0.9],
    ["rnord_0035-2624_1934_num_20_80_T1_0342_0000", 30, 240, 1.0],
    ["rnord_0035-2624_1952_num_34_133_T1_0005_0000", 30, 225, 1.1],
    ["rnord_0035-2624_1960_num_42_167_T1_0007_0000", 30, 230, 0.85],
    ["rnord_0035-2624_1964_num_46_181_T1_0131_0000", 30, 220, 1.0],
    ["rnord_0035-2624_1967_num_49_192_T1_0005_0000", 30, 220, 1.0],
    ["rnord_0035-2624_1970_num_52_204_T1_0007_0000", 30, 220, 1.0],
    ["rnord_0035-2624_1976_num_58_228_T1_0042_0000", 30, 245, 1.0],
    ["rnord_0035-2624_1976_num_58_230_T1_0373_0000", 30, 250, 0.85],
    ["rnord_0035-2624_1979_num_61_241_T1_0315_0000", 0, 220, 1.0],
    ["rnord_0035-2624_1979_num_61_242_T1_0541_0000", 30, 250, 0.85],
    ["rnord_0035-2624_1989_num_71_282_T1_0615_0000", 30, 220, 1.0],
    ["rnord_0035-2624_1991_num_73_290_T1_0241_0000", 60, 240, 1.0],
    ["rnord_0035-2624_1994_num_76_306_T1_0467_0000", 30, 240, 1.0],
    ["binet_0750-7496_1900_num_1_1_T1_0006_0000", 0, 225, 0.8],
    ["binet_0750-750X_1918_num_18_120_T1_0078_0000", 30, 255, 0.95],
    ["asgn_0767-7367_1980_num_100_1_T1_0006_0000", 30, 265, 1.04],
    ["asgn_0767-7367_1980_num_100_2_T1_0062_0000", 0, 230, 0.9],
    ["asgn_0767-7367_1980_num_100_3_T1_0113_0000", 0, 230, 0.9],
    ["asgn_0767-7367_1980_num_100_4_T1_0161_0000", 0, 230, 0.9],
    ["asgn_0767-7367_1981_num_101_1_T1_0006_0000", 30, 240, 1.0],
    ["asgn_0767-7367_1981_num_101_2_T1_0052_0000", 30, 240, 1.0],
    ["lesb_0754-944X_1988_num_65_1_T1_0011_0000", 30, 215, 0.95],
    ["femou_0180-4162_1978_num_6_1_T1_0019_0000", 30, 255, 0.95],
    ["nbeur_0000-0007_1996_num_0_1_T1_0004_0000", 0, 220, 1.0]
]

tripletsInterpolation = [
    ["barb_0001-4133_1919_num_5_1_T1_0032_0000", 0, 234, 0.73],
    ["barb_0001-4133_1920_num_6_1_T1_0051_0000", 0, 232, 0.75],
    ["barb_0001-4133_1929_num_15_1_T1_0046_0000", 30, 246, 0.90],
    ["barb_0001-4133_1939_num_25_1_T1_0123_0000", 26, 240, 0.97],
    ["barb_0001-4133_1941_num_27_1_T1_0032_0000", 0, 225, 0.8],
    ["barb_0001-4133_1963_num_49_1_T1_0020_0000", 30, 232, 0.9],
    ["barb_0001-4141_1907_num_9_1_T1_0010_0000", 59, 239, 0.99],
    ["barb_0001-4141_1909_num_11_1_T1_0011_0000", 3, 226, 0.82],
    ["barb_0001-4141_1910_num_12_1_T1_0034_0000", 12, 237, 0.94],
    ["barb_0001-4141_1919_num_5_1_T1_0002_0000", 26, 241, 0.98],
    ["rnord_0035-2624_1925_num_11_43_T1_0171_0000", 0, 231, 0.86],
    ["rnord_0035-2624_1927_num_13_51_T1_0206_0000", 0, 233, 0.9],
    ["rnord_0035-2624_1928_num_14_53_T1_0059_0000", 8, 232, 0.92],
    ["rnord_0035-2624_1933_num_19_75_T1_0211_0000", 0, 238, 0.9],
    ["rnord_0035-2624_1934_num_20_78_T1_0156_0000", 28, 220, 0.99],
    ["rnord_0035-2624_1934_num_20_80_T1_0342_0000", 0, 236, 0.9],
    ["rnord_0035-2624_1952_num_34_133_T1_0005_0000", 30, 236, 1.0],
    ["rnord_0035-2624_1960_num_42_167_T1_0007_0000", 30, 220, 1.0],
    ["rnord_0035-2624_1964_num_46_181_T1_0131_0000", 30, 220, 1.0],
    ["rnord_0035-2624_1967_num_49_192_T1_0005_0000", 30, 220, 1.0],
    ["rnord_0035-2624_1970_num_52_204_T1_0007_0000", 30, 220, 1.0],
    ["rnord_0035-2624_1976_num_58_228_T1_0042_0000", 0, 235, 0.89],
    ["rnord_0035-2624_1976_num_58_230_T1_0373_0000", 0, 235, 0.9],
    ["rnord_0035-2624_1979_num_61_241_T1_0315_0000", 30, 220, 1.0],
    ["rnord_0035-2624_1979_num_61_242_T1_0541_0000", 30, 221, 1.0],
    ["rnord_0035-2624_1989_num_71_282_T1_0615_0000", 30, 234, 1.0],
    ["rnord_0035-2624_1991_num_73_290_T1_0241_0000", 0, 241, 0.8],
    ["rnord_0035-2624_1994_num_76_306_T1_0467_0000", 0, 232, 0.72],
    ["binet_0750-7496_1900_num_1_1_T1_0006_0000", 0, 228, 0.80],
    ["binet_0750-750X_1918_num_18_120_T1_0078_0000", 30, 222, 1.0],
    ["asgn_0767-7367_1980_num_100_1_T1_0006_0000", 30, 220, 1.0],
    ["asgn_0767-7367_1980_num_100_2_T1_0062_0000", 30, 220, 1.0],
    ["asgn_0767-7367_1980_num_100_3_T1_0113_0000", 30, 233, 1.0],
    ["asgn_0767-7367_1980_num_100_4_T1_0161_0000", 30, 220, 1.0],
    ["asgn_0767-7367_1981_num_101_1_T1_0006_0000", 30, 240, 1.0],
    ["asgn_0767-7367_1981_num_101_2_T1_0052_0000", 30, 227, 1.0],
    ["lesb_0754-944X_1988_num_65_1_T1_0011_0000", 30, 220, 1.0],
    ["femou_0180-4162_1978_num_6_1_T1_0019_0000", 30, 220, 1.0],
    ["nbeur_0000-0007_1996_num_0_1_T1_0004_0000", 30, 240, 1.0]
]

tripletsApproximation1x1Propre = [
    ["barb_0001-4133_1919_num_5_1_T1_0021_0000", 20, 250, 0.7],
    ["barb_0001-4133_1919_num_5_1_T1_0613_0000", 60, 240, 1.0],
    ["barb_0001-4133_1920_num_6_1_T1_0012_0000", 0, 225, 0.8],
    ["barb_0001-4133_1920_num_6_1_T1_0296_0000", 50, 250, 1.0],
    ["barb_0001-4133_1929_num_15_1_T1_0235_0000", 60, 240, 1.0],
    ["barb_0001-4133_1939_num_25_1_T1_0321_0000", 30, 250, 0.85],
    ["barb_0001-4133_1941_num_27_1_T1_0022_0000", 30, 240, 1.0],
    ["barb_0001-4133_1963_num_49_1_T1_0135_0000", 60, 240, 1.0],
    ["barb_0001-4141_1907_num_9_1_T1_0675_0000", 0, 240, 0.9],
    ["rnord_0035-2624_1934_num_20_78_T1_0117_0000", 0, 230, 0.9],
    ["rnord_0035-2624_1952_num_34_133_T1_0080_0000", 0, 235, 0.9],
]

tripletsApproximation2x3Propre = [
    ["barb_0001-4133_1919_num_5_1_T1_0021_0000", 0, 225, 0.8],
    ["barb_0001-4133_1919_num_5_1_T1_0613_0000", 30, 240, 0.7],
    ["barb_0001-4133_1920_num_6_1_T1_0012_0000", 30, 250, 0.85],
    ["barb_0001-4133_1920_num_6_1_T1_0296_0000", 0, 240, 0.9],
    ["barb_0001-4133_1929_num_15_1_T1_0235_0000", 0, 225, 0.8],
    ["barb_0001-4133_1939_num_25_1_T1_0321_0000", 60, 240, 1.0],
    ["barb_0001-4133_1941_num_27_1_T1_0022_0000", 30, 250, 0.85],
    ["barb_0001-4133_1963_num_49_1_T1_0135_0000", 0, 225, 0.8],
    ["barb_0001-4141_1907_num_9_1_T1_0675_0000", 0, 230, 0.9],
    ["rnord_0035-2624_1934_num_20_78_T1_0117_0000", 30, 240, 1.0],
    ["rnord_0035-2624_1952_num_34_133_T1_0080_0000", 30, 245, 1.0],
]

tripletsExtrapolation1x1Propre = [
    ["barb_0001-4133_1919_num_5_1_T1_0021_0000", 20, 250, 0.7],
    ["barb_0001-4133_1919_num_5_1_T1_0613_0000", 60, 240, 1.0],
    ["barb_0001-4133_1920_num_6_1_T1_0012_0000", 0, 225, 0.8],
    ["barb_0001-4133_1920_num_6_1_T1_0296_0000", 50, 250, 1.0],
    ["barb_0001-4133_1929_num_15_1_T1_0235_0000", 60, 240, 1.0],
    ["barb_0001-4133_1939_num_25_1_T1_0321_0000", 30, 250, 0.85],
    ["barb_0001-4133_1941_num_27_1_T1_0022_0000", 30, 240, 1.0],
    ["barb_0001-4133_1963_num_49_1_T1_0135_0000", 60, 240, 1.0],
    ["barb_0001-4141_1907_num_9_1_T1_0675_0000", 0, 240, 0.9],
    ["rnord_0035-2624_1934_num_20_78_T1_0117_0000", 0, 230, 0.9],
    ["rnord_0035-2624_1952_num_34_133_T1_0080_0000", 0, 235, 0.9],
]

tripletsExtrapolation2x3Propre = [
    ["barb_0001-4133_1919_num_5_1_T1_0021_0000", 0, 225, 0.8],
    ["barb_0001-4133_1919_num_5_1_T1_0613_0000", 30, 240, 0.7],
    ["barb_0001-4133_1920_num_6_1_T1_0012_0000", 30, 250, 0.85],
    ["barb_0001-4133_1920_num_6_1_T1_0296_0000", 0, 240, 0.9],
    ["barb_0001-4133_1929_num_15_1_T1_0235_0000", 0, 225, 0.8],
    ["barb_0001-4133_1939_num_25_1_T1_0321_0000", 60, 240, 1.0],
    ["barb_0001-4133_1941_num_27_1_T1_0022_0000", 30, 250, 0.85],
    ["barb_0001-4133_1963_num_49_1_T1_0135_0000", 0, 225, 0.8],
    ["barb_0001-4141_1907_num_9_1_T1_0675_0000", 0, 230, 0.9],
    ["rnord_0035-2624_1934_num_20_78_T1_0117_0000", 30, 240, 1.0],
    ["rnord_0035-2624_1952_num_34_133_T1_0080_0000", 30, 245, 1.0],
]

tripletsInterpolationPropre = [
    ["barb_0001-4133_1919_num_5_1_T1_0021_0000", 20, 250, 0.7],
    ["barb_0001-4133_1919_num_5_1_T1_0613_0000", 59, 240, 0.99],
    ["barb_0001-4133_1920_num_6_1_T1_0012_0000", 0, 229, 0.83],
    ["barb_0001-4133_1920_num_6_1_T1_0296_0000", 44, 247, 1.0],
    ["barb_0001-4133_1929_num_15_1_T1_0235_0000", 36, 241, 0.92],
    ["barb_0001-4133_1939_num_25_1_T1_0321_0000", 15, 247, 0.83],
    ["barb_0001-4133_1941_num_27_1_T1_0022_0000", 25, 237, 0.97],
    ["barb_0001-4133_1963_num_49_1_T1_0135_0000", 47, 236, 0.96],
    ["barb_0001-4141_1907_num_9_1_T1_0675_0000", 20, 244, 0.94],
    ["rnord_0035-2624_1934_num_20_78_T1_0117_0000", 0, 230, 0.90],
    ["rnord_0035-2624_1952_num_34_133_T1_0080_0000", 0, 235, 0.90],
]

tripletsApproximation1x1Sale = [
    ["barb_0001-4133_1919_num_5_1_T1_0005_0000", 30, 240, 0.7],
    ["barb_0001-4133_1919_num_5_1_T1_0006_0000", 20, 250, 0.7],
    ["barb_0001-4141_1910_num_12_1_F_0001_0000", 50, 210, 1.0],
    ["barb_0001-4141_1910_num_12_1_F_0002_0000", 30, 220, 1.0],
    ["barb_0001-4141_1910_num_12_1_T1_0017_0000", 30, 240, 1.0],
    ["barb_0001-4141_1919_num_5_1_T1_0007_0000", 0, 230, 0.7],
    ["rnord_0035-2624_1927_num_13_51_T1_0172_0000", 30, 240, 1.0],
    ["rnord_0035-2624_1927_num_13_51_T1_0180_0001", 30, 220, 1.0],
    ["rnord_0035-2624_1928_num_14_53_T1_0023_0000", 30, 240, 1.0]
]

tripletsApproximation2x3Sale = [
    ["barb_0001-4133_1919_num_5_1_T1_0005_0000", 0, 235, 0.9],
    ["barb_0001-4133_1919_num_5_1_T1_0006_0000", 0, 245, 0.8],
    ["barb_0001-4141_1910_num_12_1_F_0001_0000", 50, 210, 1.0],
    ["barb_0001-4141_1910_num_12_1_F_0002_0000", 30, 220, 1.0],
    ["barb_0001-4141_1910_num_12_1_T1_0017_0000", 0, 235, 0.9],
    ["barb_0001-4141_1919_num_5_1_T1_0007_0000", 20, 250, 0.7],
    ["rnord_0035-2624_1927_num_13_51_T1_0172_0000", 30, 240, 1.0],
    ["rnord_0035-2624_1927_num_13_51_T1_0180_0001", 30, 220, 1.0],
    ["rnord_0035-2624_1928_num_14_53_T1_0023_0000", 30, 240, 1.0]
]

tripletsExtrapolation1x1Sale = [
    ["barb_0001-4133_1919_num_5_1_T1_0005_0000", 30, 240, 0.7],
    ["barb_0001-4133_1919_num_5_1_T1_0006_0000", 20, 260, 0.55],
    ["barb_0001-4141_1910_num_12_1_F_0001_0000", 50, 210, 1.0],
    ["barb_0001-4141_1910_num_12_1_F_0002_0000", 30, 220, 1.0],
    ["barb_0001-4141_1910_num_12_1_T1_0017_0000", 30, 240, 1.0],
    ["barb_0001-4141_1919_num_5_1_T1_0007_0000", 0, 230, 0.7],
    ["rnord_0035-2624_1927_num_13_51_T1_0172_0000", 30, 240, 1.0],
    ["rnord_0035-2624_1927_num_13_51_T1_0180_0001", 30, 220, 1.0],
    ["rnord_0035-2624_1928_num_14_53_T1_0023_0000", 0, 265, 0.8]
]

tripletsExtrapolation2x3Sale = [
    ["barb_0001-4133_1919_num_5_1_T1_0005_0000", 0, 235, 0.9],
    ["barb_0001-4133_1919_num_5_1_T1_0006_0000", 0, 245, 0.8],
    ["barb_0001-4141_1910_num_12_1_F_0001_0000", 50, 210, 1.0],
    ["barb_0001-4141_1910_num_12_1_F_0002_0000", 0, 220, 1.0],
    ["barb_0001-4141_1910_num_12_1_T1_0017_0000", 0, 235, 0.9],
    ["barb_0001-4141_1919_num_5_1_T1_0007_0000", 20, 250, 0.7],
    ["rnord_0035-2624_1927_num_13_51_T1_0172_0000", 30, 240, 1.0],
    ["rnord_0035-2624_1927_num_13_51_T1_0180_0001", 50, 220, 0.85],
    ["rnord_0035-2624_1928_num_14_53_T1_0023_0000", 30, 250, 0.9]
]

tripletsInterpolationSale = [
    ["barb_0001-4133_1919_num_5_1_T1_0005_0000", 30, 240, 0.71],
    ["barb_0001-4133_1919_num_5_1_T1_0006_0000", 12, 244, 0.77],
    ["barb_0001-4141_1910_num_12_1_F_0001_0000", 48, 210, 1.0],
    ["barb_0001-4141_1910_num_12_1_F_0002_0000", 30, 220, 1.0],
    ["barb_0001-4141_1910_num_12_1_T1_0017_0000", 25, 239, 0.98],
    ["barb_0001-4141_1919_num_5_1_T1_0007_0000", 0, 234, 0.75],
    ["rnord_0035-2624_1927_num_13_51_T1_0172_0000", 23, 237, 0.98],
    ["rnord_0035-2624_1927_num_13_51_T1_0180_0001", 30, 220, 1.0],
    ["rnord_0035-2624_1928_num_14_53_T1_0023_0000", 30, 230, 1.0]
]


def lookup(pixel, params, delta, invGamma):
    if pixel < params["minLevel"]:
        return 0
    elif pixel > params["maxLevel"]:
        return 255
    return int(((pixel - params["minLevel"]) / delta) ** invGamma * 255)


def appliquer_triplets_base_automatique(fichier, noir, blanc, gamma, methode):
    # Ouvrir l'image et la convertir en tableau NumPy
    image = np.array(Image.open("../datas/BasesDeCas/TestsAutomatiques/Origine/" + fichier + ".png").convert("L"))

    # Appliquer le point noir et le point blanc
    image = np.where(image <= noir, 0, image)
    image = np.where(image >= blanc, 255, image)

    # Normaliser l'image
    image = image / 255

    # Calculer les paramètres de lookup
    params = {"minLevel": noir / 255, "maxLevel": blanc / 255}
    delta = params["maxLevel"] - params["minLevel"]
    invGamma = 1.0 / gamma

    # Appliquer la fonction de lookup
    image = np.vectorize(lambda x: lookup(x, params, delta, invGamma))(image)

    # Arrondir et convertir le tableau NumPy en image PIL
    image = Image.fromarray(image.astype(np.uint8))

    # Sauvegarder l'image modifiée
    image.save("../datas/BasesDeCas/TestsAutomatiques/" + methode + "/" + fichier + ".png")


def appliquer_triplets_base_propre(fichier, noir, blanc, gamma, methode):
    # Ouvrir l'image et la convertir en tableau NumPy
    image = np.array(Image.open("../datas/BasesDeCas/TestsManuels/Propre/Origine/" + fichier + ".png").convert("L"))

    # Appliquer le point noir et le point blanc
    image = np.where(image <= noir, 0, image)
    image = np.where(image >= blanc, 255, image)

    # Normaliser l'image
    image = image / 255

    # Calculer les paramètres de lookup
    params = {"minLevel": noir / 255, "maxLevel": blanc / 255}
    delta = params["maxLevel"] - params["minLevel"]
    invGamma = 1.0 / gamma

    # Appliquer la fonction de lookup
    image = np.vectorize(lambda x: lookup(x, params, delta, invGamma))(image)

    # Arrondir et convertir le tableau NumPy en image PIL
    image = Image.fromarray(image.astype(np.uint8))

    # Sauvegarder l'image modifiée
    image.save("../datas/BasesDeCas/TestsManuels/Propre/" + methode + "/" + fichier + ".png")


def appliquer_triplets_base_sale(fichier, noir, blanc, gamma, methode):
    # Ouvrir l'image et la convertir en tableau NumPy
    image = np.array(Image.open("../datas/BasesDeCas/TestsManuels/Sale/Origine/" + fichier + ".png").convert("L"))

    # Appliquer le point noir et le point blanc
    image = np.where(image <= noir, 0, image)
    image = np.where(image >= blanc, 255, image)

    # Normaliser l'image
    image = image / 255

    # Calculer les paramètres de lookup
    params = {"minLevel": noir / 255, "maxLevel": blanc / 255}
    delta = params["maxLevel"] - params["minLevel"]
    invGamma = 1.0 / gamma

    # Appliquer la fonction de lookup
    image = np.vectorize(lambda x: lookup(x, params, delta, invGamma))(image)

    # Arrondir et convertir le tableau NumPy en image PIL
    image = Image.fromarray(image.astype(np.uint8))

    # Sauvegarder l'image modifiée
    image.save("../datas/BasesDeCas/TestsManuels/Sale/" + methode + "/" + fichier + ".png")


debut = time.time()

# On génère les images en appliquant les triplets experts
for image in tripletsExpert:
    # Afficher la taille des tableaux
    fichier = image[0]
    noir = image[1]
    blanc = image[2]
    gamma = image[3]
    appliquer_triplets_base_automatique(fichier, noir, blanc, gamma, "Expert")

# On génère les images en appliquant les triplets approximation 1x1
for image in tripletsApproximation1x1:
    # Afficher la taille des tableaux
    fichier = image[0]
    noir = image[1]
    blanc = image[2]
    gamma = image[3]
    appliquer_triplets_base_automatique(fichier, noir, blanc, gamma, "Approximation1x1")

# On génère les images en appliquant les triplets approximation 2x3
for image in tripletsApproximation2x3:
    # Afficher la taille des tableaux
    fichier = image[0]
    noir = image[1]
    blanc = image[2]
    gamma = image[3]
    appliquer_triplets_base_automatique(fichier, noir, blanc, gamma, "Approximation2x3")

# On génère les images en appliquant les triplets extrapolation 1x1
for image in tripletsExtrapolation1x1:
    # Afficher la taille des tableaux
    fichier = image[0]
    noir = image[1]
    blanc = image[2]
    gamma = image[3]
    appliquer_triplets_base_automatique(fichier, noir, blanc, gamma, "Extrapolation1x1")

# On génère les images en appliquant les triplets extrapolation 2x3
for image in tripletsExtrapolation2x3:
    # Afficher la taille des tableaux
    fichier = image[0]
    noir = image[1]
    blanc = image[2]
    gamma = image[3]
    appliquer_triplets_base_automatique(fichier, noir, blanc, gamma, "Extrapolation2x3")

# On génère les images en appliquant les triplets interpolation
for image in tripletsInterpolation:
    # Afficher la taille des tableaux
    fichier = image[0]
    noir = image[1]
    blanc = image[2]
    gamma = image[3]
    appliquer_triplets_base_automatique(fichier, noir, blanc, gamma, "Interpolation1x1")

# On génère les images en appliquant les triplets approximation 1x1
for image in tripletsApproximation1x1Propre:
    # Afficher la taille des tableaux
    fichier = image[0]
    noir = image[1]
    blanc = image[2]
    gamma = image[3]
    appliquer_triplets_base_propre(fichier, noir, blanc, gamma, "Approximation1x1")

# On génère les images en appliquant les triplets approximation 2x3
for image in tripletsApproximation2x3Propre:
    # Afficher la taille des tableaux
    fichier = image[0]
    noir = image[1]
    blanc = image[2]
    gamma = image[3]
    appliquer_triplets_base_propre(fichier, noir, blanc, gamma, "Approximation2x3")

# On génère les images en appliquant les triplets extrapolation 1x1
for image in tripletsExtrapolation1x1Propre:
    # Afficher la taille des tableaux
    fichier = image[0]
    noir = image[1]
    blanc = image[2]
    gamma = image[3]
    appliquer_triplets_base_propre(fichier, noir, blanc, gamma, "Extrapolation1x1")

# On génère les images en appliquant les triplets extrapolation 2x3
for image in tripletsExtrapolation2x3Propre:
    # Afficher la taille des tableaux
    fichier = image[0]
    noir = image[1]
    blanc = image[2]
    gamma = image[3]
    appliquer_triplets_base_propre(fichier, noir, blanc, gamma, "Extrapolation2x3")

# On génère les images en appliquant les triplets interpolation
for image in tripletsInterpolationPropre:
    # Afficher la taille des tableaux
    fichier = image[0]
    noir = image[1]
    blanc = image[2]
    gamma = image[3]
    appliquer_triplets_base_propre(fichier, noir, blanc, gamma, "Interpolation1x1")

# On génère les images en appliquant les triplets approximation 1x1
for image in tripletsApproximation1x1Sale:
    # Afficher la taille des tableaux
    fichier = image[0]
    noir = image[1]
    blanc = image[2]
    gamma = image[3]
    appliquer_triplets_base_sale(fichier, noir, blanc, gamma, "Approximation1x1")

# On génère les images en appliquant les triplets approximation 2x3
for image in tripletsApproximation2x3Sale:
    # Afficher la taille des tableaux
    fichier = image[0]
    noir = image[1]
    blanc = image[2]
    gamma = image[3]
    appliquer_triplets_base_sale(fichier, noir, blanc, gamma, "Approximation2x3")

# On génère les images en appliquant les triplets extrapolation 1x1
for image in tripletsExtrapolation1x1Sale:
    # Afficher la taille des tableaux
    fichier = image[0]
    noir = image[1]
    blanc = image[2]
    gamma = image[3]
    appliquer_triplets_base_sale(fichier, noir, blanc, gamma, "Extrapolation1x1")

# On génère les images en appliquant les triplets extrapolation 2x3
for image in tripletsExtrapolation2x3Sale:
    # Afficher la taille des tableaux
    fichier = image[0]
    noir = image[1]
    blanc = image[2]
    gamma = image[3]
    appliquer_triplets_base_sale(fichier, noir, blanc, gamma, "Extrapolation2x3")

# On génère les images en appliquant les triplets interpolation
for image in tripletsInterpolationSale:
    # Afficher la taille des tableaux
    fichier = image[0]
    noir = image[1]
    blanc = image[2]
    gamma = image[3]
    appliquer_triplets_base_sale(fichier, noir, blanc, gamma, "Interpolation1x1")

fin = time.time()
temps_execution = fin - debut
print("Temps d'exécution : ", temps_execution, " secondes")
