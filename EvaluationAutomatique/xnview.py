import time
from PIL import Image
import numpy as np

tripletsExpert = [
    ["barb_0001-4133_1919_num_5_1_T1_0032_0000.png", 55, 236, 0.75],
    ["barb_0001-4133_1920_num_6_1_T1_0051_0000.png", 30, 233, 0.8],
    ["barb_0001-4133_1929_num_15_1_T1_0046_0000.png", 35, 228, 0.8],
    ["barb_0001-4133_1939_num_25_1_T1_0123_0000.png", 30, 235, 0.8],
    ["barb_0001-4133_1941_num_27_1_T1_0032_0000.png", 30, 240, 1],
    ["barb_0001-4133_1963_num_49_1_T1_0020_0000.png", 30, 240, 1],
    ["barb_0001-4141_1907_num_9_1_T1_0010_0000.png", 35, 214, 0.85],
    ["barb_0001-4141_1909_num_11_1_T1_0011_0000.png", 30, 222, 1],
    ["barb_0001-4141_1910_num_12_1_T1_0034_0000.png", 30, 215, 1],
    ["barb_0001-4141_1919_num_5_1_T1_0002_0000.png", 35, 200, 0.7],
    ["rnord_0035-2624_1925_num_11_43_T1_0171_0000.png", 10, 230, 1],
    ["rnord_0035-2624_1927_num_13_51_T1_0206_0000.png", 15, 220, 1],
    ["rnord_0035-2624_1928_num_14_53_T1_0059_0000.png", 25, 200, 1],
    ["rnord_0035-2624_1933_num_19_75_T1_0211_0000.png", 1, 200, 0.8],
    ["rnord_0035-2624_1934_num_20_78_T1_0156_0000.png", 20, 230, 1],
    ["rnord_0035-2624_1934_num_20_80_T1_0342_0000.png", 10, 245, 1],
    ["rnord_0035-2624_1952_num_34_133_T1_0005_0000.png", 1, 215, 0.8],
    ["rnord_0035-2624_1960_num_42_167_T1_0007_0000.png", 1, 195, 0.85],
    ["rnord_0035-2624_1964_num_46_181_T1_0131_0000.png", 1, 210, 0.85],
    ["rnord_0035-2624_1967_num_49_192_T1_0005_0000.png", 1, 210, 0.9],
    ["rnord_0035-2624_1970_num_52_204_T1_0007_0000.png", 1, 210, 0.9],
    ["rnord_0035-2624_1976_num_58_228_T1_0042_0000.png", 1, 230, 0.9],
    ["rnord_0035-2624_1976_num_58_230_T1_0373_0000.png", 1, 225, 0.8],
    ["rnord_0035-2624_1979_num_61_241_T1_0315_0000.png", 1, 215, 1],
    ["rnord_0035-2624_1979_num_61_242_T1_0541_0000.png", 1, 215, 0.9],
    ["rnord_0035-2624_1989_num_71_282_T1_0615_0000.png", 1, 205, 0.75],
    ["rnord_0035-2624_1991_num_73_290_T1_0241_0000.png", 30, 255, 0.75],
    ["rnord_0035-2624_1994_num_76_306_T1_0467_0000.png", 30, 255, 0.7],
    ["binet_0750-7496_1900_num_1_1_T1_0006_0000.png", 90, 230, 1],
    ["binet_0750-750X_1918_num_18_120_T1_0078_0000.png", 70, 172, 0.8],
    ["asgn_0767-7367_1980_num_100_1_T1_0006_0000.png", 0, 228, 0.85],
    ["asgn_0767-7367_1980_num_100_2_T1_0062_0000.png", 0, 228, 0.85],
    ["asgn_0767-7367_1980_num_100_3_T1_0113_0000.png", 30, 220, 0.85],
    ["asgn_0767-7367_1980_num_100_4_T1_0161_0000.png", 30, 230, 0.85],
    ["asgn_0767-7367_1981_num_101_1_T1_0006_0000.png", 1, 230, 0.85],
    ["asgn_0767-7367_1981_num_101_2_T1_0052_0000.png", 1, 225, 0.85],
    ["lesb_0754-944X_1988_num_65_1_T1_0011_0000.png", 60, 204, 1],
    ["femou_0180-4162_1978_num_6_1_T1_0019_0000.png", 45, 198, 1],
    ["nbeur_0000-0007_1996_num_0_1_T1_0004_0000.png", 53, 210, 1]
]

tripletsApproximation1x1 = [
    ["asgn_0767-7367_1980_num_100_1_T1_0006_0000.png", 30, 220, 1.0],
    ["asgn_0767-7367_1980_num_100_2_T1_0062_0000.png", 30, 220, 1.0],
    ["asgn_0767-7367_1980_num_100_3_T1_0113_0000.png", 30, 240, 1.0],
    ["asgn_0767-7367_1980_num_100_4_T1_0161_0000.png", 30, 220, 1.0],
    ["asgn_0767-7367_1981_num_101_1_T1_0006_0000.png", 30, 240, 1.0],
    ["asgn_0767-7367_1981_num_101_2_T1_0052_0000.png", 30, 220, 1.0],
    ["barb_0001-4133_1919_num_5_1_T1_0032_0000.png", 0, 230, 0.7],
    ["barb_0001-4133_1920_num_6_1_T1_0051_0000.png", 0, 230, 0.7],
    ["barb_0001-4133_1929_num_15_1_T1_0046_0000.png", 30, 250, 0.85],
    ["barb_0001-4133_1939_num_25_1_T1_0123_0000.png", 30, 240, 1.0],
    ["barb_0001-4133_1941_num_27_1_T1_0032_0000.png", 0, 225, 0.8],
    ["barb_0001-4133_1963_num_49_1_T1_0020_0000.png", 60, 240, 1.0],
    ["barb_0001-4141_1907_num_9_1_T1_0010_0000.png", 60, 240, 1.0],
    ["barb_0001-4141_1909_num_11_1_T1_0011_0000.png", 0, 225, 0.8],
    ["barb_0001-4141_1910_num_12_1_T1_0034_0000.png", 0, 230, 0.9],
    ["barb_0001-4141_1919_num_5_1_T1_0002_0000.png", 0, 225, 0.8],
    ["binet_0750-7496_1900_num_1_1_T1_0006_0000.png", 0, 225, 0.8],
    ["binet_0750-750X_1918_num_18_120_T1_0078_0000.png", 30, 220, 1.0],
    ["femou_0180-4162_1978_num_6_1_T1_0019_0000.png", 30, 220, 1.0],
    ["lesb_0754-944X_1988_num_65_1_T1_0011_0000.png", 30, 220, 1.0],
    ["nbeur_0000-0007_1996_num_0_1_T1_0004_0000.png", 30, 240, 1.0],
    ["rnord_0035-2624_1925_num_11_43_T1_0171_0000.png", 0, 235, 0.9],
    ["rnord_0035-2624_1927_num_13_51_T1_0206_0000.png", 0, 230, 0.9],
    ["rnord_0035-2624_1928_num_14_53_T1_0059_0000.png", 0, 230, 0.9],
    ["rnord_0035-2624_1933_num_19_75_T1_0211_0000.png", 0, 240, 0.9],
    ["rnord_0035-2624_1934_num_20_78_T1_0156_0000.png", 30, 220, 1.0],
    ["rnord_0035-2624_1934_num_20_80_T1_0342_0000.png", 0, 240, 0.9],
    ["rnord_0035-2624_1952_num_34_133_T1_0005_0000.png", 30, 240, 1.0],
    ["rnord_0035-2624_1960_num_42_167_T1_0007_0000.png", 30, 220, 1.0],
    ["rnord_0035-2624_1964_num_46_181_T1_0131_0000.png", 30, 220, 1.0],
    ["rnord_0035-2624_1967_num_49_192_T1_0005_0000.png", 30, 220, 1.0],
    ["rnord_0035-2624_1970_num_52_204_T1_0007_0000.png", 30, 220, 1.0],
    ["rnord_0035-2624_1976_num_58_228_T1_0042_0000.png", 0, 235, 0.9],
    ["rnord_0035-2624_1976_num_58_230_T1_0373_0000.png", 0, 235, 0.9],
    ["rnord_0035-2624_1979_num_61_241_T1_0315_0000.png", 30, 240, 1.0],
    ["rnord_0035-2624_1979_num_61_242_T1_0541_0000.png", 30, 220, 1.0],
    ["rnord_0035-2624_1989_num_71_282_T1_0615_0000.png", 30, 240, 1.0],
    ["rnord_0035-2624_1991_num_73_290_T1_0241_0000.png", 0, 240, 0.8],
    ["rnord_0035-2624_1994_num_76_306_T1_0467_0000.png", 0, 230, 0.7]
]

tripletsApproximation2x3 = [
    ["asgn_0767-7367_1980_num_100_1_T1_0006_0000.png", 30, 240, 1.0],
    ["asgn_0767-7367_1980_num_100_2_T1_0062_0000.png", 0, 230, 0.9],
    ["asgn_0767-7367_1980_num_100_3_T1_0113_0000.png", 0, 230, 0.9],
    ["asgn_0767-7367_1980_num_100_4_T1_0161_0000.png", 0, 230, 0.9],
    ["asgn_0767-7367_1981_num_101_1_T1_0006_0000.png", 30, 240, 1.0],
    ["asgn_0767-7367_1981_num_101_2_T1_0052_0000.png", 30, 240, 1.0],
    ["barb_0001-4133_1919_num_5_1_T1_0032_0000.png", 0, 245, 0.8],
    ["barb_0001-4133_1920_num_6_1_T1_0051_0000.png", 20, 250, 0.7],
    ["barb_0001-4133_1929_num_15_1_T1_0046_0000.png", 0, 225, 0.8],
    ["barb_0001-4133_1939_num_25_1_T1_0123_0000.png", 0, 245, 0.8],
    ["barb_0001-4133_1941_num_27_1_T1_0032_0000.png", 30, 250, 0.85],
    ["barb_0001-4133_1963_num_49_1_T1_0020_0000.png", 30, 250, 0.85],
    ["barb_0001-4141_1907_num_9_1_T1_0010_0000.png", 30, 240, 1.0],
    ["barb_0001-4141_1909_num_11_1_T1_0011_0000.png", 0, 230, 0.9],
    ["barb_0001-4141_1910_num_12_1_T1_0034_0000.png", 0, 235, 0.9],
    ["barb_0001-4141_1919_num_5_1_T1_0002_0000.png", 20, 250, 0.7],
    ["binet_0750-7496_1900_num_1_1_T1_0006_0000.png", 0, 225, 0.8],
    ["binet_0750-750X_1918_num_18_120_T1_0078_0000.png", 0, 230, 0.9],
    ["femou_0180-4162_1978_num_6_1_T1_0019_0000.png", 0, 230, 0.9],
    ["lesb_0754-944X_1988_num_65_1_T1_0011_0000.png", 30, 220, 1.0],
    ["nbeur_0000-0007_1996_num_0_1_T1_0004_0000.png", 30, 220, 1.0],
    ["rnord_0035-2624_1925_num_11_43_T1_0171_0000.png", 0, 230, 0.7],
    ["rnord_0035-2624_1927_num_13_51_T1_0206_0000.png", 0, 230, 0.9],
    ["rnord_0035-2624_1928_num_14_53_T1_0059_0000.png", 30, 245, 1.0],
    ["rnord_0035-2624_1933_num_19_75_T1_0211_0000.png", 0, 240, 0.9],
    ["rnord_0035-2624_1934_num_20_78_T1_0156_0000.png", 30, 245, 1.0],
    ["rnord_0035-2624_1934_num_20_80_T1_0342_0000.png", 30, 240, 1.0],
    ["rnord_0035-2624_1952_num_34_133_T1_0005_0000.png", 30, 220, 1.0],
    ["rnord_0035-2624_1960_num_42_167_T1_0007_0000.png", 30, 220, 1.0],
    ["rnord_0035-2624_1964_num_46_181_T1_0131_0000.png", 30, 220, 1.0],
    ["rnord_0035-2624_1967_num_49_192_T1_0005_0000.png", 30, 220, 1.0],
    ["rnord_0035-2624_1970_num_52_204_T1_0007_0000.png", 30, 220, 1.0],
    ["rnord_0035-2624_1976_num_58_228_T1_0042_0000.png", 30, 240, 1.0],
    ["rnord_0035-2624_1976_num_58_230_T1_0373_0000.png", 30, 240, 1.0],
    ["rnord_0035-2624_1979_num_61_241_T1_0315_0000.png", 30, 240, 1.0],
    ["rnord_0035-2624_1979_num_61_242_T1_0541_0000.png", 30, 240, 1.0],
    ["rnord_0035-2624_1989_num_71_282_T1_0615_0000.png", 30, 220, 1.0],
    ["rnord_0035-2624_1991_num_73_290_T1_0241_0000.png", 30, 240, 1.0],
    ["rnord_0035-2624_1994_num_76_306_T1_0467_0000.png", 30, 240, 1.0]
]

tripletsExtrapolation1x1 = [
    ["asgn_0767-7367_1980_num_100_1_T1_0006_0000.png", 30, 230, 0.85],
    ["asgn_0767-7367_1980_num_100_2_T1_0062_0000.png", 30, 230, 0.85],
    ["asgn_0767-7367_1980_num_100_3_T1_0113_0000.png", 30, 250, 0.85],
    ["asgn_0767-7367_1980_num_100_4_T1_0161_0000.png", 30, 220, 1.00],
    ["asgn_0767-7367_1981_num_101_1_T1_0006_0000.png", 30, 250, 0.85],
    ["asgn_0767-7367_1981_num_101_2_T1_0052_0000.png", 30, 220, 1.00],
    ["barb_0001-4133_1919_num_5_1_T1_0032_0000.png", 0, 230, 0.70],
    ["barb_0001-4133_1920_num_6_1_T1_0051_0000.png", 0, 230, 0.70],
    ["barb_0001-4133_1929_num_15_1_T1_0046_0000.png", 30, 250, 0.85],
    ["barb_0001-4133_1939_num_25_1_T1_0123_0000.png", 30, 240, 1.00],
    ["barb_0001-4133_1941_num_27_1_T1_0032_0000.png", 0, 225, 0.80],
    ["barb_0001-4133_1963_num_49_1_T1_0020_0000.png", 60, 240, 1.00],
    ["barb_0001-4141_1907_num_9_1_T1_0010_0000.png", 60, 240, 1.00],
    ["barb_0001-4141_1909_num_11_1_T1_0011_0000.png", 0, 225, 0.80],
    ["barb_0001-4141_1910_num_12_1_T1_0034_0000.png", 0, 230, 0.90],
    ["barb_0001-4141_1919_num_5_1_T1_0002_0000.png", 0, 225, 0.80],
    ["binet_0750-7496_1900_num_1_1_T1_0006_0000.png", 0, 225, 0.80],
    ["binet_0750-750X_1918_num_18_120_T1_0078_0000.png", 30, 220, 1.00],
    ["femou_0180-4162_1978_num_6_1_T1_0019_0000.png", 60, 225, 1.10],
    ["lesb_0754-944X_1988_num_65_1_T1_0011_0000.png", 30, 220, 1.00],
    ["nbeur_0000-0007_1996_num_0_1_T1_0004_0000.png", 30, 240, 1.00],
    ["rnord_0035-2624_1925_num_11_43_T1_0171_0000.png", 0, 235, 0.90],
    ["rnord_0035-2624_1927_num_13_51_T1_0206_0000.png", 0, 230, 0.90],
    ["rnord_0035-2624_1928_num_14_53_T1_0059_0000.png", 0, 230, 0.90],
    ["rnord_0035-2624_1933_num_19_75_T1_0211_0000.png", 0, 240, 0.90],
    ["rnord_0035-2624_1934_num_20_78_T1_0156_0000.png", 30, 220, 1.00],
    ["rnord_0035-2624_1934_num_20_80_T1_0342_0000.png", 0, 240, 0.90],
    ["rnord_0035-2624_1952_num_34_133_T1_0005_0000.png", 30, 250, 0.85],
    ["rnord_0035-2624_1960_num_42_167_T1_0007_0000.png", 30, 230, 0.85],
    ["rnord_0035-2624_1964_num_46_181_T1_0131_0000.png", 30, 230, 0.85],
    ["rnord_0035-2624_1967_num_49_192_T1_0005_0000.png", 30, 230, 0.85],
    ["rnord_0035-2624_1970_num_52_204_T1_0007_0000.png", 60, 220, 1.00],
    ["rnord_0035-2624_1976_num_58_228_T1_0042_0000.png", 0, 235, 0.90],
    ["rnord_0035-2624_1976_num_58_230_T1_0373_0000.png", 0, 235, 0.90],
    ["rnord_0035-2624_1979_num_61_241_T1_0315_0000.png", 30, 240, 1.00],
    ["rnord_0035-2624_1979_num_61_242_T1_0541_0000.png", 30, 220, 1.00],
    ["rnord_0035-2624_1989_num_71_282_T1_0615_0000.png", 30, 250, 0.85],
    ["rnord_0035-2624_1991_num_73_290_T1_0241_0000.png", 0, 240, 0.80],
    ["rnord_0035-2624_1994_num_76_306_T1_0467_0000.png", 0, 230, 0.70]
]

tripletsExtrapolation2x3 = [
    ["asgn_0767-7367_1980_num_100_1_T1_0006_0000.png", 0, 235, 0.95],
    ["asgn_0767-7367_1980_num_100_2_T1_0062_0000.png", 0, 230, 0.90],
    ["asgn_0767-7367_1980_num_100_3_T1_0113_0000.png", 0, 225, 0.85],
    ["asgn_0767-7367_1980_num_100_4_T1_0161_0000.png", 0, 255, 0.95],
    ["asgn_0767-7367_1981_num_101_1_T1_0006_0000.png", 30, 240, 1.00],
    ["asgn_0767-7367_1981_num_101_2_T1_0052_0000.png", 0, 235, 0.95],
    ["barb_0001-4133_1919_num_5_1_T1_0032_0000.png", 0, 255, 0.85],
    ["barb_0001-4133_1920_num_6_1_T1_0051_0000.png", 20, 250, 0.70],
    ["barb_0001-4133_1929_num_15_1_T1_0046_0000.png", 0, 225, 0.80],
    ["barb_0001-4133_1939_num_25_1_T1_0123_0000.png", 0, 245, 0.80],
    ["barb_0001-4133_1941_num_27_1_T1_0032_0000.png", 30, 250, 0.85],
    ["barb_0001-4133_1963_num_49_1_T1_0020_0000.png", 30, 250, 0.85],
    ["barb_0001-4141_1907_num_9_1_T1_0010_0000.png", 30, 255, 1.05],
    ["barb_0001-4141_1909_num_11_1_T1_0011_0000.png", 0, 255, 0.95],
    ["barb_0001-4141_1910_num_12_1_T1_0034_0000.png", 0, 235, 0.90],
    ["barb_0001-4141_1919_num_5_1_T1_0002_0000.png", 20, 250, 0.70],
    ["binet_0750-7496_1900_num_1_1_T1_0006_0000.png", 0, 225, 0.80],
    ["binet_0750-750X_1918_num_18_120_T1_0078_0000.png", 30, 250, 0.85],
    ["femou_0180-4162_1978_num_6_1_T1_0019_0000.png", 0, 215, 0.70],
    ["lesb_0754-944X_1988_num_65_1_T1_0011_0000.png", 60, 240, 0.95],
    ["nbeur_0000-0007_1996_num_0_1_T1_0004_0000.png", 50, 220, 0.85],
    ["rnord_0035-2624_1925_num_11_43_T1_0171_0000.png", 0, 230, 0.70],
    ["rnord_0035-2624_1927_num_13_51_T1_0206_0000.png", 0, 230, 0.90],
    ["rnord_0035-2624_1928_num_14_53_T1_0059_0000.png", 30, 245, 1.00],
    ["rnord_0035-2624_1933_num_19_75_T1_0211_0000.png", 0, 235, 0.85],
    ["rnord_0035-2624_1934_num_20_78_T1_0156_0000.png", 30, 245, 1.00],
    ["rnord_0035-2624_1934_num_20_80_T1_0342_0000.png", 30, 240, 1.00],
    ["rnord_0035-2624_1952_num_34_133_T1_0005_0000.png", 50, 220, 0.85],
    ["rnord_0035-2624_1960_num_42_167_T1_0007_0000.png", 30, 215, 0.95],
    ["rnord_0035-2624_1964_num_46_181_T1_0131_0000.png", 30, 220, 1.00],
    ["rnord_0035-2624_1967_num_49_192_T1_0005_0000.png", 30, 220, 1.00],
    ["rnord_0035-2624_1970_num_52_204_T1_0007_0000.png", 0, 215, 0.95],
    ["rnord_0035-2624_1976_num_58_228_T1_0042_0000.png", 30, 240, 1.00],
    ["rnord_0035-2624_1976_num_58_230_T1_0373_0000.png", 30, 240, 1.00],
    ["rnord_0035-2624_1979_num_61_241_T1_0315_0000.png", 30, 255, 1.05],
    ["rnord_0035-2624_1979_num_61_242_T1_0541_0000.png", 50, 240, 0.85],
    ["rnord_0035-2624_1989_num_71_282_T1_0615_0000.png", 30, 220, 1.00],
    ["rnord_0035-2624_1991_num_73_290_T1_0241_0000.png", 30, 240, 1.00],
    ["rnord_0035-2624_1994_num_76_306_T1_0467_0000.png", 30, 255, 1.05]
]

tripletsInterpolation1x1 = [
    ["asgn_0767-7367_1980_num_100_1_T1_0006_0000.png", 30, 220, 1.00],
    ["asgn_0767-7367_1980_num_100_2_T1_0062_0000.png", 30, 220, 1.00],
    ["asgn_0767-7367_1980_num_100_3_T1_0113_0000.png", 30, 233, 1.00],
    ["asgn_0767-7367_1980_num_100_4_T1_0161_0000.png", 30, 220, 1.00],
    ["asgn_0767-7367_1981_num_101_1_T1_0006_0000.png", 30, 240, 1.00],
    ["asgn_0767-7367_1981_num_101_2_T1_0052_0000.png", 30, 227, 1.00],
    ["barb_0001-4133_1919_num_5_1_T1_0032_0000.png", 0, 234, 0.73],
    ["barb_0001-4133_1920_num_6_1_T1_0051_0000.png", 0, 232, 0.75],
    ["barb_0001-4133_1929_num_15_1_T1_0046_0000.png", 30, 246, 0.90],
    ["barb_0001-4133_1939_num_25_1_T1_0123_0000.png", 26, 240, 0.97],
    ["barb_0001-4133_1941_num_27_1_T1_0032_0000.png", 0, 225, 0.80],
    ["barb_0001-4133_1963_num_49_1_T1_0020_0000.png", 30, 232, 0.90],
    ["barb_0001-4141_1907_num_9_1_T1_0010_0000.png", 59, 239, 1.00],
    ["barb_0001-4141_1909_num_11_1_T1_0011_0000.png", 0, 229, 0.83],
    ["barb_0001-4141_1910_num_12_1_T1_0034_0000.png", 0, 230, 0.90],
    ["barb_0001-4141_1919_num_5_1_T1_0002_0000.png", 0, 226, 0.80],
    ["binet_0750-7496_1900_num_1_1_T1_0006_0000.png", 0, 228, 0.81],
    ["binet_0750-750X_1918_num_18_120_T1_0078_0000.png", 30, 222, 1.00],
    ["femou_0180-4162_1978_num_6_1_T1_0019_0000.png", 30, 220, 1.00],
    ["lesb_0754-944X_1988_num_65_1_T1_0011_0000.png", 30, 220, 1.00],
    ["nbeur_0000-0007_1996_num_0_1_T1_0004_0000.png", 30, 240, 1.00],
    ["rnord_0035-2624_1925_num_11_43_T1_0171_0000.png", 0, 231, 0.87],
    ["rnord_0035-2624_1927_num_13_51_T1_0206_0000.png", 0, 233, 0.90],
    ["rnord_0035-2624_1928_num_14_53_T1_0059_0000.png", 8, 232, 0.93],
    ["rnord_0035-2624_1933_num_19_75_T1_0211_0000.png", 0, 238, 0.90],
    ["rnord_0035-2624_1934_num_20_78_T1_0156_0000.png", 28, 220, 0.99],
    ["rnord_0035-2624_1934_num_20_80_T1_0342_0000.png", 0, 236, 0.90],
    ["rnord_0035-2624_1952_num_34_133_T1_0005_0000.png", 30, 236, 1.00],
    ["rnord_0035-2624_1960_num_42_167_T1_0007_0000.png", 30, 220, 1.00],
    ["rnord_0035-2624_1964_num_46_181_T1_0131_0000.png", 30, 220, 1.00],
    ["rnord_0035-2624_1967_num_49_192_T1_0005_0000.png", 30, 220, 1.00],
    ["rnord_0035-2624_1970_num_52_204_T1_0007_0000.png", 30, 220, 1.00],
    ["rnord_0035-2624_1976_num_58_228_T1_0042_0000.png", 0, 235, 0.90],
    ["rnord_0035-2624_1976_num_58_230_T1_0373_0000.png", 4, 235, 0.92],
    ["rnord_0035-2624_1979_num_61_241_T1_0315_0000.png", 30, 240, 1.00],
    ["rnord_0035-2624_1979_num_61_242_T1_0541_0000.png", 30, 221, 1.00],
    ["rnord_0035-2624_1989_num_71_282_T1_0615_0000.png", 30, 234, 1.00],
    ["rnord_0035-2624_1991_num_73_290_T1_0241_0000.png", 0, 241, 0.80],
    ["rnord_0035-2624_1994_num_76_306_T1_0467_0000.png", 0, 232, 0.73]
]

tripletsInterpolation2x3 = [
    ["asgn_0767-7367_1980_num_100_1_T1_0006_0000.png", 11, 233, 0.94],
    ["asgn_0767-7367_1980_num_100_2_T1_0062_0000.png", 0, 230, 0.90],
    ["asgn_0767-7367_1980_num_100_3_T1_0113_0000.png", 15, 235, 0.95],
    ["asgn_0767-7367_1980_num_100_4_T1_0161_0000.png", 6, 232, 0.92],
    ["asgn_0767-7367_1981_num_101_1_T1_0006_0000.png", 14, 234, 0.95],
    ["asgn_0767-7367_1981_num_101_2_T1_0052_0000.png", 0, 230, 0.90],
    ["barb_0001-4133_1919_num_5_1_T1_0032_0000.png", 0, 240, 0.80],
    ["barb_0001-4133_1920_num_6_1_T1_0051_0000.png", 0, 242, 0.80],
    ["barb_0001-4133_1929_num_15_1_T1_0046_0000.png", 11, 239, 0.74],
    ["barb_0001-4133_1939_num_25_1_T1_0123_0000.png", 0, 245, 0.80],
    ["barb_0001-4133_1941_num_27_1_T1_0032_0000.png", 0, 238, 0.83],
    ["barb_0001-4133_1963_num_49_1_T1_0020_0000.png", 30, 245, 0.78],
    ["barb_0001-4141_1907_num_9_1_T1_0010_0000.png", 0, 240, 0.90],
    ["barb_0001-4141_1909_num_11_1_T1_0011_0000.png", 10, 233, 0.93],
    ["barb_0001-4141_1910_num_12_1_T1_0034_0000.png", 0, 231, 0.90],
    ["barb_0001-4141_1919_num_5_1_T1_0002_0000.png", 0, 245, 0.83],
    ["binet_0750-7496_1900_num_1_1_T1_0006_0000.png", 0, 225, 0.80],
    ["binet_0750-750X_1918_num_18_120_T1_0078_0000.png", 10, 226, 0.94],
    ["femou_0180-4162_1978_num_6_1_T1_0019_0000.png", 30, 229, 1.00],
    ["lesb_0754-944X_1988_num_65_1_T1_0011_0000.png", 30, 220, 1.00],
    ["nbeur_0000-0007_1996_num_0_1_T1_0004_0000.png", 20, 223, 0.97],
    ["rnord_0035-2624_1925_num_11_43_T1_0171_0000.png", 0, 239, 0.77],
    ["rnord_0035-2624_1927_num_13_51_T1_0206_0000.png", 0, 240, 0.90],
    ["rnord_0035-2624_1928_num_14_53_T1_0059_0000.png", 30, 242, 1.00],
    ["rnord_0035-2624_1933_num_19_75_T1_0211_0000.png", 0, 230, 0.90],
    ["rnord_0035-2624_1934_num_20_78_T1_0156_0000.png", 18, 239, 0.96],
    ["rnord_0035-2624_1934_num_20_80_T1_0342_0000.png", 30, 243, 1.00],
    ["rnord_0035-2624_1952_num_34_133_T1_0005_0000.png", 30, 220, 1.00],
    ["rnord_0035-2624_1960_num_42_167_T1_0007_0000.png", 30, 220, 1.00],
    ["rnord_0035-2624_1964_num_46_181_T1_0131_0000.png", 30, 230, 1.00],
    ["rnord_0035-2624_1967_num_49_192_T1_0005_0000.png", 30, 220, 1.00],
    ["rnord_0035-2624_1970_num_52_204_T1_0007_0000.png", 30, 220, 1.00],
    ["rnord_0035-2624_1976_num_58_228_T1_0042_0000.png", 30, 242, 1.00],
    ["rnord_0035-2624_1976_num_58_230_T1_0373_0000.png", 30, 240, 1.00],
    ["rnord_0035-2624_1979_num_61_241_T1_0315_0000.png", 30, 240, 1.00],
    ["rnord_0035-2624_1979_num_61_242_T1_0541_0000.png", 30, 240, 1.00],
    ["rnord_0035-2624_1989_num_71_282_T1_0615_0000.png", 30, 220, 1.00],
    ["rnord_0035-2624_1991_num_73_290_T1_0241_0000.png", 30, 240, 1.00],
    ["rnord_0035-2624_1994_num_76_306_T1_0467_0000.png", 39, 240, 1.00]
]

tripletsApproximation1x1Manuel = [
    ["barb_0001-4133_1919_num_5_1_T1_0005_0000.png", 0, 240, 0.8],
    ["barb_0001-4133_1919_num_5_1_T1_0006_0000.png", 0, 240, 0.8],
    ["barb_0001-4133_1919_num_5_1_T1_0021_0000.png", 0, 240, 0.8],
    ["barb_0001-4133_1919_num_5_1_T1_0613_0000.png", 0, 240, 0.8],
    ["barb_0001-4133_1920_num_6_1_T1_0012_0000.png", 0, 245, 0.8],
    ["barb_0001-4133_1920_num_6_1_T1_0296_0000.png", 0, 245, 0.8],
    ["barb_0001-4133_1929_num_15_1_T1_0235_0000.png", 20, 250, 0.7],
    ["barb_0001-4133_1939_num_25_1_T1_0321_0000.png", 0, 230, 0.7],
    ["barb_0001-4133_1941_num_27_1_T1_0022_0000.png", 0, 250, 0.85],
    ["barb_0001-4133_1963_num_49_1_T1_0135_0000.png", 60, 240, 1.0],
    ["barb_0001-4141_1907_num_9_1_T1_0675_0000.png", 0, 235, 0.9],
    ["barb_0001-4141_1910_num_12_1_F_0001_0000.png", 0, 230, 0.9],
    ["barb_0001-4141_1910_num_12_1_F_0002_0000.png", 0, 230, 0.9],
    ["barb_0001-4141_1910_num_12_1_T1_0017_0000.png", 0, 230, 0.9],
    ["barb_0001-4141_1919_num_5_1_T1_0007_0000.png", 0, 225, 0.8],
    ["rnord_0035-2624_1927_num_13_51_T1_0172_0000.png", 30, 230, 1.0],
    ["rnord_0035-2624_1928_num_14_53_T1_0023_0000.png", 30, 240, 1.0],
    ["rnord_0035-2624_1934_num_20_78_T1_0117_0000.png", 30, 245, 1.0],
    ["rnord_0035-2624_1952_num_34_133_T1_0080_0000.png", 50, 210, 1.0]
]

tripletsApproximation2x3Manuel = [
    ["barb_0001-4133_1919_num_5_1_T1_0005_0000.png", 0, 240, 0.8],
    ["barb_0001-4133_1919_num_5_1_T1_0006_0000.png", 0, 240, 0.8],
    ["barb_0001-4133_1919_num_5_1_T1_0021_0000.png", 0, 240, 0.8],
    ["barb_0001-4133_1919_num_5_1_T1_0613_0000.png", 0, 240, 0.8],
    ["barb_0001-4133_1920_num_6_1_T1_0012_0000.png", 0, 245, 0.8],
    ["barb_0001-4133_1920_num_6_1_T1_0296_0000.png", 0, 245, 0.8],
    ["barb_0001-4133_1929_num_15_1_T1_0235_0000.png", 0, 225, 0.8],
    ["barb_0001-4133_1939_num_25_1_T1_0321_0000.png", 0, 230, 0.7],
    ["barb_0001-4133_1941_num_27_1_T1_0022_0000.png", 0, 250, 0.85],
    ["barb_0001-4133_1963_num_49_1_T1_0135_0000.png", 0, 225, 0.8],
    ["barb_0001-4141_1907_num_9_1_T1_0675_0000.png", 0, 235, 0.9],
    ["barb_0001-4141_1910_num_12_1_F_0001_0000.png", 0, 230, 0.9],
    ["barb_0001-4141_1910_num_12_1_F_0002_0000.png", 0, 230, 0.9],
    ["barb_0001-4141_1910_num_12_1_T1_0017_0000.png", 0, 230, 0.9],
    ["barb_0001-4141_1919_num_5_1_T1_0007_0000.png", 0, 225, 0.8],
    ["rnord_0035-2624_1927_num_13_51_T1_0172_0000.png", 30, 230, 1.0],
    ["rnord_0035-2624_1928_num_14_53_T1_0023_0000.png", 30, 240, 1.0],
    ["rnord_0035-2624_1934_num_20_78_T1_0117_0000.png", 30, 245, 1.0],
    ["rnord_0035-2624_1952_num_34_133_T1_0080_0000.png", 50, 210, 1.0]
]

tripletsExtrapolation1x1Manuel = [
    ["barb_0001-4133_1919_num_5_1_T1_0005_0000.png", 0, 240, 0.80],
    ["barb_0001-4133_1919_num_5_1_T1_0006_0000.png", 0, 240, 0.80],
    ["barb_0001-4133_1919_num_5_1_T1_0021_0000.png", 0, 240, 0.80],
    ["barb_0001-4133_1919_num_5_1_T1_0613_0000.png", 0, 240, 0.80],
    ["barb_0001-4133_1920_num_6_1_T1_0012_0000.png", 0, 245, 0.80],
    ["barb_0001-4133_1920_num_6_1_T1_0296_0000.png", 0, 245, 0.80],
    ["barb_0001-4133_1929_num_15_1_T1_0235_0000.png", 20, 250, 0.70],
    ["barb_0001-4133_1939_num_25_1_T1_0321_0000.png", 0, 230, 0.70],
    ["barb_0001-4133_1941_num_27_1_T1_0022_0000.png", 0, 250, 0.85],
    ["barb_0001-4133_1963_num_49_1_T1_0135_0000.png", 60, 240, 1.00],
    ["barb_0001-4141_1907_num_9_1_T1_0675_0000.png", 0, 235, 0.90],
    ["barb_0001-4141_1910_num_12_1_F_0001_0000.png", 0, 230, 0.90],
    ["barb_0001-4141_1910_num_12_1_F_0002_0000.png", 0, 230, 0.90],
    ["barb_0001-4141_1910_num_12_1_T1_0017_0000.png", 0, 230, 0.90],
    ["barb_0001-4141_1919_num_5_1_T1_0007_0000.png", 0, 225, 0.80],
    ["rnord_0035-2624_1927_num_13_51_T1_0172_0000.png", 30, 230, 1.00],
    ["rnord_0035-2624_1928_num_14_53_T1_0023_0000.png", 30, 240, 1.00],
    ["rnord_0035-2624_1934_num_20_78_T1_0117_0000.png", 30, 245, 1.00],
    ["rnord_0035-2624_1952_num_34_133_T1_0080_0000.png", 50, 210, 1.00]
]

tripletsExtrapolation2x3Manuel = [
    ["barb_0001-4133_1919_num_5_1_T1_0005_0000.png", 0, 240, 0.80],
    ["barb_0001-4133_1919_num_5_1_T1_0006_0000.png", 0, 240, 0.80],
    ["barb_0001-4133_1919_num_5_1_T1_0021_0000.png", 0, 240, 0.80],
    ["barb_0001-4133_1919_num_5_1_T1_0613_0000.png", 0, 240, 0.80],
    ["barb_0001-4133_1920_num_6_1_T1_0012_0000.png", 0, 245, 0.80],
    ["barb_0001-4133_1920_num_6_1_T1_0296_0000.png", 0, 245, 0.80],
    ["barb_0001-4133_1929_num_15_1_T1_0235_0000.png", 0, 225, 0.80],
    ["barb_0001-4133_1939_num_25_1_T1_0321_0000.png", 0, 230, 0.70],
    ["barb_0001-4133_1941_num_27_1_T1_0022_0000.png", 0, 250, 0.85],
    ["barb_0001-4133_1963_num_49_1_T1_0135_0000.png", 0, 225, 0.80],
    ["barb_0001-4141_1907_num_9_1_T1_0675_0000.png", 0, 235, 0.90],
    ["barb_0001-4141_1910_num_12_1_F_0001_0000.png", 0, 230, 0.90],
    ["barb_0001-4141_1910_num_12_1_F_0002_0000.png", 0, 230, 0.90],
    ["barb_0001-4141_1910_num_12_1_T1_0017_0000.png", 0, 230, 0.90],
    ["barb_0001-4141_1919_num_5_1_T1_0007_0000.png", 0, 225, 0.80],
    ["rnord_0035-2624_1927_num_13_51_T1_0172_0000.png", 30, 230, 1.00],
    ["rnord_0035-2624_1928_num_14_53_T1_0023_0000.png", 30, 240, 1.00],
    ["rnord_0035-2624_1934_num_20_78_T1_0117_0000.png", 30, 245, 1.00],
    ["rnord_0035-2624_1952_num_34_133_T1_0080_0000.png", 50, 210, 1.00]
]

tripletsInterpolation1x1Manuel = [
    ["barb_0001-4133_1919_num_5_1_T1_0005_0000.png", 0, 240, 0.80],
    ["barb_0001-4133_1919_num_5_1_T1_0006_0000.png", 0, 240, 0.80],
    ["barb_0001-4133_1919_num_5_1_T1_0021_0000.png", 0, 240, 0.80],
    ["barb_0001-4133_1919_num_5_1_T1_0613_0000.png", 0, 240, 0.80],
    ["barb_0001-4133_1920_num_6_1_T1_0012_0000.png", 0, 245, 0.80],
    ["barb_0001-4133_1920_num_6_1_T1_0296_0000.png", 0, 245, 0.80],
    ["barb_0001-4133_1929_num_15_1_T1_0235_0000.png", 12, 248, 0.74],
    ["barb_0001-4133_1939_num_25_1_T1_0321_0000.png", 0, 230, 0.70],
    ["barb_0001-4133_1941_num_27_1_T1_0022_0000.png", 0, 250, 0.85],
    ["barb_0001-4133_1963_num_49_1_T1_0135_0000.png", 47, 236, 0.96],
    ["barb_0001-4141_1907_num_9_1_T1_0675_0000.png", 0, 235, 0.90],
    ["barb_0001-4141_1910_num_12_1_F_0001_0000.png", 0, 230, 0.90],
    ["barb_0001-4141_1910_num_12_1_F_0002_0000.png", 0, 230, 0.90],
    ["barb_0001-4141_1910_num_12_1_T1_0017_0000.png", 0, 230, 0.90],
    ["barb_0001-4141_1919_num_5_1_T1_0007_0000.png", 0, 225, 0.80],
    ["rnord_0035-2624_1927_num_13_51_T1_0172_0000.png", 30, 230, 1.00],
    ["rnord_0035-2624_1928_num_14_53_T1_0023_0000.png", 30, 240, 1.00],
    ["rnord_0035-2624_1934_num_20_78_T1_0117_0000.png", 30, 245, 1.00],
    ["rnord_0035-2624_1952_num_34_133_T1_0080_0000.png", 50, 210, 1.00]
]

tripletsInterpolation2x3Manuel = [
    ["barb_0001-4133_1919_num_5_1_T1_0005_0000.png", 15, 235, 0.70],
    ["barb_0001-4133_1919_num_5_1_T1_0006_0000.png", 0, 240, 0.80],
    ["barb_0001-4133_1919_num_5_1_T1_0021_0000.png", 0, 232, 0.80],
    ["barb_0001-4133_1919_num_5_1_T1_0613_0000.png", 15, 240, 0.75],
    ["barb_0001-4133_1920_num_6_1_T1_0012_0000.png", 20, 248, 0.83],
    ["barb_0001-4133_1920_num_6_1_T1_0296_0000.png", 15, 242, 0.95],
    ["barb_0001-4133_1929_num_15_1_T1_0235_0000.png", 9, 239, 0.70],
    ["barb_0001-4133_1939_num_25_1_T1_0321_0000.png", 0, 242, 0.80],
    ["barb_0001-4133_1941_num_27_1_T1_0022_0000.png", 0, 229, 0.85],
    ["barb_0001-4133_1963_num_49_1_T1_0135_0000.png", 0, 225, 0.80],
    ["barb_0001-4141_1907_num_9_1_T1_0675_0000.png", 0, 234, 0.90],
    ["barb_0001-4141_1910_num_12_1_F_0001_0000.png", 35, 215, 0.97],
    ["barb_0001-4141_1910_num_12_1_F_0002_0000.png", 30, 220, 1.00],
    ["barb_0001-4141_1910_num_12_1_T1_0017_0000.png", 0, 230, 0.90],
    ["barb_0001-4141_1919_num_5_1_T1_0007_0000.png", 12, 248, 0.74],
    ["rnord_0035-2624_1927_num_13_51_T1_0172_0000.png", 30, 232, 1.00],
    ["rnord_0035-2624_1928_num_14_53_T1_0023_0000.png", 30, 220, 1.00],
    ["rnord_0035-2624_1934_num_20_78_T1_0117_0000.png", 30, 245, 1.00],
    ["rnord_0035-2624_1952_num_34_133_T1_0080_0000.png", 0, 237, 0.90]
]

tripletsPersee = [
    ["barb_0001-4133_1919_num_5_1_T1_0005_0000.png", 0, 240, 0.8],
    ["barb_0001-4133_1919_num_5_1_T1_0006_0000.png", 0, 240, 0.8],
    ["barb_0001-4133_1919_num_5_1_T1_0021_0000.png", 0, 240, 0.8],
    ["barb_0001-4133_1919_num_5_1_T1_0613_0000.png", 0, 240, 0.8],
    ["barb_0001-4133_1920_num_6_1_T1_0012_0000.png", 0, 245, 0.8],
    ["barb_0001-4133_1920_num_6_1_T1_0296_0000.png", 0, 245, 0.8],
    ["barb_0001-4133_1929_num_15_1_T1_0235_0000.png", 20, 250, 0.7],
    ["barb_0001-4133_1939_num_25_1_T1_0321_0000.png", 0, 230, 0.7],
    ["barb_0001-4133_1941_num_27_1_T1_0022_0000.png", 0, 250, 0.85],
    ["barb_0001-4133_1963_num_49_1_T1_0135_0000.png", 30, 250, 0.85],
    ["barb_0001-4141_1907_num_9_1_T1_0675_0000.png", 0, 235, 0.9],
    ["barb_0001-4141_1910_num_12_1_F_0001_0000.png", 0, 230, 0.9],
    ["barb_0001-4141_1910_num_12_1_F_0002_0000.png", 0, 230, 0.9],
    ["barb_0001-4141_1910_num_12_1_T1_0017_0000.png", 0, 230, 0.9],
    ["barb_0001-4141_1919_num_5_1_T1_0007_0000.png", 0, 240, 0.8],
    ["rnord_0035-2624_1927_num_13_51_T1_0172_0000.png", 30, 230, 1.0],
    ["rnord_0035-2624_1928_num_14_53_T1_0023_0000.png", 30, 240, 1.0],
    ["rnord_0035-2624_1934_num_20_78_T1_0117_0000.png", 30, 245, 1.0],
    ["rnord_0035-2624_1952_num_34_133_T1_0080_0000.png", 50, 210, 1.0]
]


def lookup(pixel, params, delta, invGamma):
    if pixel < params["minLevel"]:
        return 0
    elif pixel > params["maxLevel"]:
        return 255
    return int(((pixel - params["minLevel"]) / delta) ** invGamma * 255)


def appliquer_triplets_base_automatique(fichier, noir, blanc, gamma, methode):
    # Ouvrir l'image et la convertir en tableau NumPy
    image = np.array(Image.open("../datas/BasesDeCas/TestsAutomatiques/Origine/" + fichier).convert("L"))

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
    image.save("../datas/BasesDeCas/TestsAutomatiques/" + methode + "/" + fichier)


def appliquer_triplets_base_manuelle(fichier, noir, blanc, gamma, methode):
    # Ouvrir l'image et la convertir en tableau NumPy
    image = np.array(Image.open("../datas/BasesDeCas/TestsManuels/Origine/" + fichier).convert("L"))

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
    image.save("../datas/BasesDeCas/TestsManuels/" + methode + "/" + fichier)


# Définir une fonction pour générer des images en appliquant des triplets de base automatique
def generer_images_automatique(triplets, approximation):
    for image in triplets:
        fichier, noir, blanc, gamma = image[:4]
        appliquer_triplets_base_automatique(fichier, noir, blanc, gamma, approximation)


# Définir une fonction pour générer des images en appliquant des triplets de base manuelle
def generer_images_manuelle(triplets, approximation):
    for image in triplets:
        fichier, noir, blanc, gamma = image[:4]
        appliquer_triplets_base_manuelle(fichier, noir, blanc, gamma, approximation)


debut = time.time()

# Générer les images en appliquant les triplets
generer_images_automatique(tripletsExpert, "Expert")
generer_images_automatique(tripletsApproximation1x1, "Approximation1x1")
generer_images_automatique(tripletsApproximation2x3, "Approximation2x3")
generer_images_automatique(tripletsExtrapolation1x1, "Extrapolation1x1")
generer_images_automatique(tripletsExtrapolation2x3, "Extrapolation2x3")
generer_images_automatique(tripletsInterpolation1x1, "Interpolation1x1")
generer_images_automatique(tripletsInterpolation2x3, "Interpolation2x3")

# Générer les images en appliquant les triplets manuels
generer_images_manuelle(tripletsApproximation1x1Manuel, "Approximation1x1")
generer_images_manuelle(tripletsApproximation2x3Manuel, "Approximation2x3")
generer_images_manuelle(tripletsExtrapolation1x1Manuel, "Extrapolation1x1")
generer_images_manuelle(tripletsExtrapolation2x3Manuel, "Extrapolation2x3")
generer_images_manuelle(tripletsInterpolation1x1Manuel, "Interpolation1x1")
generer_images_manuelle(tripletsInterpolation2x3Manuel, "Interpolation2x3")
generer_images_manuelle(tripletsPersee, "Persee")

fin = time.time()
temps_execution = fin - debut
print("Temps d'exécution : ", temps_execution, " secondes")
