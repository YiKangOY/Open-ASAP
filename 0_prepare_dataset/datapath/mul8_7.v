module PartialProd(
  input  [7:0] io_multiplicand,
  input  [7:0] io_multiplier,
  output [7:0] io_outs_0,
  output [7:0] io_outs_1,
  output [7:0] io_outs_2,
  output [7:0] io_outs_3,
  output [7:0] io_outs_4,
  output [7:0] io_outs_5,
  output [7:0] io_outs_6,
  output [7:0] io_outs_7
);
  wire  _T_10 = io_multiplicand[0] & io_multiplier[0]; // @[partialprod.scala 16:36]
  wire  _T_13 = io_multiplicand[1] & io_multiplier[0]; // @[partialprod.scala 16:36]
  wire  _T_16 = io_multiplicand[2] & io_multiplier[0]; // @[partialprod.scala 16:36]
  wire  _T_19 = io_multiplicand[3] & io_multiplier[0]; // @[partialprod.scala 16:36]
  wire  _T_22 = io_multiplicand[4] & io_multiplier[0]; // @[partialprod.scala 16:36]
  wire  _T_25 = io_multiplicand[5] & io_multiplier[0]; // @[partialprod.scala 16:36]
  wire  _T_28 = io_multiplicand[6] & io_multiplier[0]; // @[partialprod.scala 16:36]
  wire  _T_31 = io_multiplicand[7] & io_multiplier[0]; // @[partialprod.scala 16:36]
  wire [6:0] _T_37 = {_T_31,_T_28,_T_25,_T_22,_T_19,_T_16,_T_13}; // @[Cat.scala 29:58]
  wire  _T_49 = io_multiplicand[0] & io_multiplier[1]; // @[partialprod.scala 16:36]
  wire  _T_52 = io_multiplicand[1] & io_multiplier[1]; // @[partialprod.scala 16:36]
  wire  _T_55 = io_multiplicand[2] & io_multiplier[1]; // @[partialprod.scala 16:36]
  wire  _T_58 = io_multiplicand[3] & io_multiplier[1]; // @[partialprod.scala 16:36]
  wire  _T_61 = io_multiplicand[4] & io_multiplier[1]; // @[partialprod.scala 16:36]
  wire  _T_64 = io_multiplicand[5] & io_multiplier[1]; // @[partialprod.scala 16:36]
  wire  _T_67 = io_multiplicand[6] & io_multiplier[1]; // @[partialprod.scala 16:36]
  wire  _T_70 = io_multiplicand[7] & io_multiplier[1]; // @[partialprod.scala 16:36]
  wire [6:0] _T_76 = {_T_70,_T_67,_T_64,_T_61,_T_58,_T_55,_T_52}; // @[Cat.scala 29:58]
  wire  _T_88 = io_multiplicand[0] & io_multiplier[2]; // @[partialprod.scala 16:36]
  wire  _T_91 = io_multiplicand[1] & io_multiplier[2]; // @[partialprod.scala 16:36]
  wire  _T_94 = io_multiplicand[2] & io_multiplier[2]; // @[partialprod.scala 16:36]
  wire  _T_97 = io_multiplicand[3] & io_multiplier[2]; // @[partialprod.scala 16:36]
  wire  _T_100 = io_multiplicand[4] & io_multiplier[2]; // @[partialprod.scala 16:36]
  wire  _T_103 = io_multiplicand[5] & io_multiplier[2]; // @[partialprod.scala 16:36]
  wire  _T_106 = io_multiplicand[6] & io_multiplier[2]; // @[partialprod.scala 16:36]
  wire  _T_109 = io_multiplicand[7] & io_multiplier[2]; // @[partialprod.scala 16:36]
  wire [6:0] _T_115 = {_T_109,_T_106,_T_103,_T_100,_T_97,_T_94,_T_91}; // @[Cat.scala 29:58]
  wire  _T_127 = io_multiplicand[0] & io_multiplier[3]; // @[partialprod.scala 16:36]
  wire  _T_130 = io_multiplicand[1] & io_multiplier[3]; // @[partialprod.scala 16:36]
  wire  _T_133 = io_multiplicand[2] & io_multiplier[3]; // @[partialprod.scala 16:36]
  wire  _T_136 = io_multiplicand[3] & io_multiplier[3]; // @[partialprod.scala 16:36]
  wire  _T_139 = io_multiplicand[4] & io_multiplier[3]; // @[partialprod.scala 16:36]
  wire  _T_142 = io_multiplicand[5] & io_multiplier[3]; // @[partialprod.scala 16:36]
  wire  _T_145 = io_multiplicand[6] & io_multiplier[3]; // @[partialprod.scala 16:36]
  wire  _T_148 = io_multiplicand[7] & io_multiplier[3]; // @[partialprod.scala 16:36]
  wire [6:0] _T_154 = {_T_148,_T_145,_T_142,_T_139,_T_136,_T_133,_T_130}; // @[Cat.scala 29:58]
  wire  _T_166 = io_multiplicand[0] & io_multiplier[4]; // @[partialprod.scala 16:36]
  wire  _T_169 = io_multiplicand[1] & io_multiplier[4]; // @[partialprod.scala 16:36]
  wire  _T_172 = io_multiplicand[2] & io_multiplier[4]; // @[partialprod.scala 16:36]
  wire  _T_175 = io_multiplicand[3] & io_multiplier[4]; // @[partialprod.scala 16:36]
  wire  _T_178 = io_multiplicand[4] & io_multiplier[4]; // @[partialprod.scala 16:36]
  wire  _T_181 = io_multiplicand[5] & io_multiplier[4]; // @[partialprod.scala 16:36]
  wire  _T_184 = io_multiplicand[6] & io_multiplier[4]; // @[partialprod.scala 16:36]
  wire  _T_187 = io_multiplicand[7] & io_multiplier[4]; // @[partialprod.scala 16:36]
  wire [6:0] _T_193 = {_T_187,_T_184,_T_181,_T_178,_T_175,_T_172,_T_169}; // @[Cat.scala 29:58]
  wire  _T_205 = io_multiplicand[0] & io_multiplier[5]; // @[partialprod.scala 16:36]
  wire  _T_208 = io_multiplicand[1] & io_multiplier[5]; // @[partialprod.scala 16:36]
  wire  _T_211 = io_multiplicand[2] & io_multiplier[5]; // @[partialprod.scala 16:36]
  wire  _T_214 = io_multiplicand[3] & io_multiplier[5]; // @[partialprod.scala 16:36]
  wire  _T_217 = io_multiplicand[4] & io_multiplier[5]; // @[partialprod.scala 16:36]
  wire  _T_220 = io_multiplicand[5] & io_multiplier[5]; // @[partialprod.scala 16:36]
  wire  _T_223 = io_multiplicand[6] & io_multiplier[5]; // @[partialprod.scala 16:36]
  wire  _T_226 = io_multiplicand[7] & io_multiplier[5]; // @[partialprod.scala 16:36]
  wire [6:0] _T_232 = {_T_226,_T_223,_T_220,_T_217,_T_214,_T_211,_T_208}; // @[Cat.scala 29:58]
  wire  _T_244 = io_multiplicand[0] & io_multiplier[6]; // @[partialprod.scala 16:36]
  wire  _T_247 = io_multiplicand[1] & io_multiplier[6]; // @[partialprod.scala 16:36]
  wire  _T_250 = io_multiplicand[2] & io_multiplier[6]; // @[partialprod.scala 16:36]
  wire  _T_253 = io_multiplicand[3] & io_multiplier[6]; // @[partialprod.scala 16:36]
  wire  _T_256 = io_multiplicand[4] & io_multiplier[6]; // @[partialprod.scala 16:36]
  wire  _T_259 = io_multiplicand[5] & io_multiplier[6]; // @[partialprod.scala 16:36]
  wire  _T_262 = io_multiplicand[6] & io_multiplier[6]; // @[partialprod.scala 16:36]
  wire  _T_265 = io_multiplicand[7] & io_multiplier[6]; // @[partialprod.scala 16:36]
  wire [6:0] _T_271 = {_T_265,_T_262,_T_259,_T_256,_T_253,_T_250,_T_247}; // @[Cat.scala 29:58]
  wire  _T_283 = io_multiplicand[0] & io_multiplier[7]; // @[partialprod.scala 16:36]
  wire  _T_286 = io_multiplicand[1] & io_multiplier[7]; // @[partialprod.scala 16:36]
  wire  _T_289 = io_multiplicand[2] & io_multiplier[7]; // @[partialprod.scala 16:36]
  wire  _T_292 = io_multiplicand[3] & io_multiplier[7]; // @[partialprod.scala 16:36]
  wire  _T_295 = io_multiplicand[4] & io_multiplier[7]; // @[partialprod.scala 16:36]
  wire  _T_298 = io_multiplicand[5] & io_multiplier[7]; // @[partialprod.scala 16:36]
  wire  _T_301 = io_multiplicand[6] & io_multiplier[7]; // @[partialprod.scala 16:36]
  wire  _T_304 = io_multiplicand[7] & io_multiplier[7]; // @[partialprod.scala 16:36]
  wire [6:0] _T_310 = {_T_304,_T_301,_T_298,_T_295,_T_292,_T_289,_T_286}; // @[Cat.scala 29:58]
  assign io_outs_0 = {_T_37,_T_10}; // @[partialprod.scala 18:16]
  assign io_outs_1 = {_T_76,_T_49}; // @[partialprod.scala 18:16]
  assign io_outs_2 = {_T_115,_T_88}; // @[partialprod.scala 18:16]
  assign io_outs_3 = {_T_154,_T_127}; // @[partialprod.scala 18:16]
  assign io_outs_4 = {_T_193,_T_166}; // @[partialprod.scala 18:16]
  assign io_outs_5 = {_T_232,_T_205}; // @[partialprod.scala 18:16]
  assign io_outs_6 = {_T_271,_T_244}; // @[partialprod.scala 18:16]
  assign io_outs_7 = {_T_310,_T_283}; // @[partialprod.scala 18:16]
endmodule
module HalfAdder(
  input   io_a,
  input   io_b,
  output  io_s,
  output  io_co
);
  assign io_s = io_a ^ io_b; // @[comp.scala 15:8]
  assign io_co = io_a & io_b; // @[comp.scala 16:9]
endmodule
module FullAdder(
  input   io_a,
  input   io_b,
  input   io_ci,
  output  io_s,
  output  io_co
);
  wire  a_xor_b = io_a ^ io_b; // @[comp.scala 28:22]
  wire  a_and_b = io_a & io_b; // @[comp.scala 31:22]
  wire  a_and_cin = io_a & io_ci; // @[comp.scala 32:24]
  wire  b_and_cin = io_b & io_ci; // @[comp.scala 33:24]
  wire  _T_1 = a_and_b | b_and_cin; // @[comp.scala 34:20]
  assign io_s = a_xor_b ^ io_ci; // @[comp.scala 29:8]
  assign io_co = _T_1 | a_and_cin; // @[comp.scala 34:9]
endmodule
module Wallace(
  input  [7:0]  io_pp_0,
  input  [7:0]  io_pp_1,
  input  [7:0]  io_pp_2,
  input  [7:0]  io_pp_3,
  input  [7:0]  io_pp_4,
  input  [7:0]  io_pp_5,
  input  [7:0]  io_pp_6,
  input  [7:0]  io_pp_7,
  output [15:0] io_augend,
  output [15:0] io_addend
);
  wire  HalfAdder_io_a; // @[wallace.scala 57:25]
  wire  HalfAdder_io_b; // @[wallace.scala 57:25]
  wire  HalfAdder_io_s; // @[wallace.scala 57:25]
  wire  HalfAdder_io_co; // @[wallace.scala 57:25]
  wire  FullAdder_io_a; // @[wallace.scala 67:25]
  wire  FullAdder_io_b; // @[wallace.scala 67:25]
  wire  FullAdder_io_ci; // @[wallace.scala 67:25]
  wire  FullAdder_io_s; // @[wallace.scala 67:25]
  wire  FullAdder_io_co; // @[wallace.scala 67:25]
  wire  FullAdder_1_io_a; // @[wallace.scala 67:25]
  wire  FullAdder_1_io_b; // @[wallace.scala 67:25]
  wire  FullAdder_1_io_ci; // @[wallace.scala 67:25]
  wire  FullAdder_1_io_s; // @[wallace.scala 67:25]
  wire  FullAdder_1_io_co; // @[wallace.scala 67:25]
  wire  FullAdder_2_io_a; // @[wallace.scala 67:25]
  wire  FullAdder_2_io_b; // @[wallace.scala 67:25]
  wire  FullAdder_2_io_ci; // @[wallace.scala 67:25]
  wire  FullAdder_2_io_s; // @[wallace.scala 67:25]
  wire  FullAdder_2_io_co; // @[wallace.scala 67:25]
  wire  FullAdder_3_io_a; // @[wallace.scala 67:25]
  wire  FullAdder_3_io_b; // @[wallace.scala 67:25]
  wire  FullAdder_3_io_ci; // @[wallace.scala 67:25]
  wire  FullAdder_3_io_s; // @[wallace.scala 67:25]
  wire  FullAdder_3_io_co; // @[wallace.scala 67:25]
  wire  FullAdder_4_io_a; // @[wallace.scala 67:25]
  wire  FullAdder_4_io_b; // @[wallace.scala 67:25]
  wire  FullAdder_4_io_ci; // @[wallace.scala 67:25]
  wire  FullAdder_4_io_s; // @[wallace.scala 67:25]
  wire  FullAdder_4_io_co; // @[wallace.scala 67:25]
  wire  FullAdder_5_io_a; // @[wallace.scala 67:25]
  wire  FullAdder_5_io_b; // @[wallace.scala 67:25]
  wire  FullAdder_5_io_ci; // @[wallace.scala 67:25]
  wire  FullAdder_5_io_s; // @[wallace.scala 67:25]
  wire  FullAdder_5_io_co; // @[wallace.scala 67:25]
  wire  FullAdder_6_io_a; // @[wallace.scala 67:25]
  wire  FullAdder_6_io_b; // @[wallace.scala 67:25]
  wire  FullAdder_6_io_ci; // @[wallace.scala 67:25]
  wire  FullAdder_6_io_s; // @[wallace.scala 67:25]
  wire  FullAdder_6_io_co; // @[wallace.scala 67:25]
  wire  FullAdder_7_io_a; // @[wallace.scala 67:25]
  wire  FullAdder_7_io_b; // @[wallace.scala 67:25]
  wire  FullAdder_7_io_ci; // @[wallace.scala 67:25]
  wire  FullAdder_7_io_s; // @[wallace.scala 67:25]
  wire  FullAdder_7_io_co; // @[wallace.scala 67:25]
  wire  FullAdder_8_io_a; // @[wallace.scala 67:25]
  wire  FullAdder_8_io_b; // @[wallace.scala 67:25]
  wire  FullAdder_8_io_ci; // @[wallace.scala 67:25]
  wire  FullAdder_8_io_s; // @[wallace.scala 67:25]
  wire  FullAdder_8_io_co; // @[wallace.scala 67:25]
  wire  HalfAdder_1_io_a; // @[wallace.scala 57:25]
  wire  HalfAdder_1_io_b; // @[wallace.scala 57:25]
  wire  HalfAdder_1_io_s; // @[wallace.scala 57:25]
  wire  HalfAdder_1_io_co; // @[wallace.scala 57:25]
  wire  FullAdder_9_io_a; // @[wallace.scala 67:25]
  wire  FullAdder_9_io_b; // @[wallace.scala 67:25]
  wire  FullAdder_9_io_ci; // @[wallace.scala 67:25]
  wire  FullAdder_9_io_s; // @[wallace.scala 67:25]
  wire  FullAdder_9_io_co; // @[wallace.scala 67:25]
  wire  FullAdder_10_io_a; // @[wallace.scala 67:25]
  wire  FullAdder_10_io_b; // @[wallace.scala 67:25]
  wire  FullAdder_10_io_ci; // @[wallace.scala 67:25]
  wire  FullAdder_10_io_s; // @[wallace.scala 67:25]
  wire  FullAdder_10_io_co; // @[wallace.scala 67:25]
  wire  FullAdder_11_io_a; // @[wallace.scala 67:25]
  wire  FullAdder_11_io_b; // @[wallace.scala 67:25]
  wire  FullAdder_11_io_ci; // @[wallace.scala 67:25]
  wire  FullAdder_11_io_s; // @[wallace.scala 67:25]
  wire  FullAdder_11_io_co; // @[wallace.scala 67:25]
  wire  FullAdder_12_io_a; // @[wallace.scala 67:25]
  wire  FullAdder_12_io_b; // @[wallace.scala 67:25]
  wire  FullAdder_12_io_ci; // @[wallace.scala 67:25]
  wire  FullAdder_12_io_s; // @[wallace.scala 67:25]
  wire  FullAdder_12_io_co; // @[wallace.scala 67:25]
  wire  FullAdder_13_io_a; // @[wallace.scala 67:25]
  wire  FullAdder_13_io_b; // @[wallace.scala 67:25]
  wire  FullAdder_13_io_ci; // @[wallace.scala 67:25]
  wire  FullAdder_13_io_s; // @[wallace.scala 67:25]
  wire  FullAdder_13_io_co; // @[wallace.scala 67:25]
  wire  HalfAdder_2_io_a; // @[wallace.scala 57:25]
  wire  HalfAdder_2_io_b; // @[wallace.scala 57:25]
  wire  HalfAdder_2_io_s; // @[wallace.scala 57:25]
  wire  HalfAdder_2_io_co; // @[wallace.scala 57:25]
  wire  FullAdder_14_io_a; // @[wallace.scala 67:25]
  wire  FullAdder_14_io_b; // @[wallace.scala 67:25]
  wire  FullAdder_14_io_ci; // @[wallace.scala 67:25]
  wire  FullAdder_14_io_s; // @[wallace.scala 67:25]
  wire  FullAdder_14_io_co; // @[wallace.scala 67:25]
  wire  FullAdder_15_io_a; // @[wallace.scala 67:25]
  wire  FullAdder_15_io_b; // @[wallace.scala 67:25]
  wire  FullAdder_15_io_ci; // @[wallace.scala 67:25]
  wire  FullAdder_15_io_s; // @[wallace.scala 67:25]
  wire  FullAdder_15_io_co; // @[wallace.scala 67:25]
  wire  FullAdder_16_io_a; // @[wallace.scala 67:25]
  wire  FullAdder_16_io_b; // @[wallace.scala 67:25]
  wire  FullAdder_16_io_ci; // @[wallace.scala 67:25]
  wire  FullAdder_16_io_s; // @[wallace.scala 67:25]
  wire  FullAdder_16_io_co; // @[wallace.scala 67:25]
  wire  FullAdder_17_io_a; // @[wallace.scala 67:25]
  wire  FullAdder_17_io_b; // @[wallace.scala 67:25]
  wire  FullAdder_17_io_ci; // @[wallace.scala 67:25]
  wire  FullAdder_17_io_s; // @[wallace.scala 67:25]
  wire  FullAdder_17_io_co; // @[wallace.scala 67:25]
  wire  FullAdder_18_io_a; // @[wallace.scala 67:25]
  wire  FullAdder_18_io_b; // @[wallace.scala 67:25]
  wire  FullAdder_18_io_ci; // @[wallace.scala 67:25]
  wire  FullAdder_18_io_s; // @[wallace.scala 67:25]
  wire  FullAdder_18_io_co; // @[wallace.scala 67:25]
  wire  FullAdder_19_io_a; // @[wallace.scala 67:25]
  wire  FullAdder_19_io_b; // @[wallace.scala 67:25]
  wire  FullAdder_19_io_ci; // @[wallace.scala 67:25]
  wire  FullAdder_19_io_s; // @[wallace.scala 67:25]
  wire  FullAdder_19_io_co; // @[wallace.scala 67:25]
  wire  FullAdder_20_io_a; // @[wallace.scala 67:25]
  wire  FullAdder_20_io_b; // @[wallace.scala 67:25]
  wire  FullAdder_20_io_ci; // @[wallace.scala 67:25]
  wire  FullAdder_20_io_s; // @[wallace.scala 67:25]
  wire  FullAdder_20_io_co; // @[wallace.scala 67:25]
  wire  FullAdder_21_io_a; // @[wallace.scala 67:25]
  wire  FullAdder_21_io_b; // @[wallace.scala 67:25]
  wire  FullAdder_21_io_ci; // @[wallace.scala 67:25]
  wire  FullAdder_21_io_s; // @[wallace.scala 67:25]
  wire  FullAdder_21_io_co; // @[wallace.scala 67:25]
  wire  HalfAdder_3_io_a; // @[wallace.scala 57:25]
  wire  HalfAdder_3_io_b; // @[wallace.scala 57:25]
  wire  HalfAdder_3_io_s; // @[wallace.scala 57:25]
  wire  HalfAdder_3_io_co; // @[wallace.scala 57:25]
  wire  HalfAdder_4_io_a; // @[wallace.scala 57:25]
  wire  HalfAdder_4_io_b; // @[wallace.scala 57:25]
  wire  HalfAdder_4_io_s; // @[wallace.scala 57:25]
  wire  HalfAdder_4_io_co; // @[wallace.scala 57:25]
  wire  HalfAdder_5_io_a; // @[wallace.scala 57:25]
  wire  HalfAdder_5_io_b; // @[wallace.scala 57:25]
  wire  HalfAdder_5_io_s; // @[wallace.scala 57:25]
  wire  HalfAdder_5_io_co; // @[wallace.scala 57:25]
  wire  FullAdder_22_io_a; // @[wallace.scala 67:25]
  wire  FullAdder_22_io_b; // @[wallace.scala 67:25]
  wire  FullAdder_22_io_ci; // @[wallace.scala 67:25]
  wire  FullAdder_22_io_s; // @[wallace.scala 67:25]
  wire  FullAdder_22_io_co; // @[wallace.scala 67:25]
  wire  FullAdder_23_io_a; // @[wallace.scala 67:25]
  wire  FullAdder_23_io_b; // @[wallace.scala 67:25]
  wire  FullAdder_23_io_ci; // @[wallace.scala 67:25]
  wire  FullAdder_23_io_s; // @[wallace.scala 67:25]
  wire  FullAdder_23_io_co; // @[wallace.scala 67:25]
  wire  FullAdder_24_io_a; // @[wallace.scala 67:25]
  wire  FullAdder_24_io_b; // @[wallace.scala 67:25]
  wire  FullAdder_24_io_ci; // @[wallace.scala 67:25]
  wire  FullAdder_24_io_s; // @[wallace.scala 67:25]
  wire  FullAdder_24_io_co; // @[wallace.scala 67:25]
  wire  FullAdder_25_io_a; // @[wallace.scala 67:25]
  wire  FullAdder_25_io_b; // @[wallace.scala 67:25]
  wire  FullAdder_25_io_ci; // @[wallace.scala 67:25]
  wire  FullAdder_25_io_s; // @[wallace.scala 67:25]
  wire  FullAdder_25_io_co; // @[wallace.scala 67:25]
  wire  HalfAdder_6_io_a; // @[wallace.scala 57:25]
  wire  HalfAdder_6_io_b; // @[wallace.scala 57:25]
  wire  HalfAdder_6_io_s; // @[wallace.scala 57:25]
  wire  HalfAdder_6_io_co; // @[wallace.scala 57:25]
  wire  FullAdder_26_io_a; // @[wallace.scala 67:25]
  wire  FullAdder_26_io_b; // @[wallace.scala 67:25]
  wire  FullAdder_26_io_ci; // @[wallace.scala 67:25]
  wire  FullAdder_26_io_s; // @[wallace.scala 67:25]
  wire  FullAdder_26_io_co; // @[wallace.scala 67:25]
  wire  FullAdder_27_io_a; // @[wallace.scala 67:25]
  wire  FullAdder_27_io_b; // @[wallace.scala 67:25]
  wire  FullAdder_27_io_ci; // @[wallace.scala 67:25]
  wire  FullAdder_27_io_s; // @[wallace.scala 67:25]
  wire  FullAdder_27_io_co; // @[wallace.scala 67:25]
  wire  FullAdder_28_io_a; // @[wallace.scala 67:25]
  wire  FullAdder_28_io_b; // @[wallace.scala 67:25]
  wire  FullAdder_28_io_ci; // @[wallace.scala 67:25]
  wire  FullAdder_28_io_s; // @[wallace.scala 67:25]
  wire  FullAdder_28_io_co; // @[wallace.scala 67:25]
  wire  HalfAdder_7_io_a; // @[wallace.scala 57:25]
  wire  HalfAdder_7_io_b; // @[wallace.scala 57:25]
  wire  HalfAdder_7_io_s; // @[wallace.scala 57:25]
  wire  HalfAdder_7_io_co; // @[wallace.scala 57:25]
  wire  HalfAdder_8_io_a; // @[wallace.scala 57:25]
  wire  HalfAdder_8_io_b; // @[wallace.scala 57:25]
  wire  HalfAdder_8_io_s; // @[wallace.scala 57:25]
  wire  HalfAdder_8_io_co; // @[wallace.scala 57:25]
  wire  HalfAdder_9_io_a; // @[wallace.scala 57:25]
  wire  HalfAdder_9_io_b; // @[wallace.scala 57:25]
  wire  HalfAdder_9_io_s; // @[wallace.scala 57:25]
  wire  HalfAdder_9_io_co; // @[wallace.scala 57:25]
  wire  HalfAdder_10_io_a; // @[wallace.scala 57:25]
  wire  HalfAdder_10_io_b; // @[wallace.scala 57:25]
  wire  HalfAdder_10_io_s; // @[wallace.scala 57:25]
  wire  HalfAdder_10_io_co; // @[wallace.scala 57:25]
  wire  FullAdder_29_io_a; // @[wallace.scala 67:25]
  wire  FullAdder_29_io_b; // @[wallace.scala 67:25]
  wire  FullAdder_29_io_ci; // @[wallace.scala 67:25]
  wire  FullAdder_29_io_s; // @[wallace.scala 67:25]
  wire  FullAdder_29_io_co; // @[wallace.scala 67:25]
  wire  HalfAdder_11_io_a; // @[wallace.scala 57:25]
  wire  HalfAdder_11_io_b; // @[wallace.scala 57:25]
  wire  HalfAdder_11_io_s; // @[wallace.scala 57:25]
  wire  HalfAdder_11_io_co; // @[wallace.scala 57:25]
  wire  FullAdder_30_io_a; // @[wallace.scala 67:25]
  wire  FullAdder_30_io_b; // @[wallace.scala 67:25]
  wire  FullAdder_30_io_ci; // @[wallace.scala 67:25]
  wire  FullAdder_30_io_s; // @[wallace.scala 67:25]
  wire  FullAdder_30_io_co; // @[wallace.scala 67:25]
  wire  FullAdder_31_io_a; // @[wallace.scala 67:25]
  wire  FullAdder_31_io_b; // @[wallace.scala 67:25]
  wire  FullAdder_31_io_ci; // @[wallace.scala 67:25]
  wire  FullAdder_31_io_s; // @[wallace.scala 67:25]
  wire  FullAdder_31_io_co; // @[wallace.scala 67:25]
  wire  HalfAdder_12_io_a; // @[wallace.scala 57:25]
  wire  HalfAdder_12_io_b; // @[wallace.scala 57:25]
  wire  HalfAdder_12_io_s; // @[wallace.scala 57:25]
  wire  HalfAdder_12_io_co; // @[wallace.scala 57:25]
  wire  FullAdder_32_io_a; // @[wallace.scala 67:25]
  wire  FullAdder_32_io_b; // @[wallace.scala 67:25]
  wire  FullAdder_32_io_ci; // @[wallace.scala 67:25]
  wire  FullAdder_32_io_s; // @[wallace.scala 67:25]
  wire  FullAdder_32_io_co; // @[wallace.scala 67:25]
  wire  HalfAdder_13_io_a; // @[wallace.scala 57:25]
  wire  HalfAdder_13_io_b; // @[wallace.scala 57:25]
  wire  HalfAdder_13_io_s; // @[wallace.scala 57:25]
  wire  HalfAdder_13_io_co; // @[wallace.scala 57:25]
  wire  HalfAdder_14_io_a; // @[wallace.scala 57:25]
  wire  HalfAdder_14_io_b; // @[wallace.scala 57:25]
  wire  HalfAdder_14_io_s; // @[wallace.scala 57:25]
  wire  HalfAdder_14_io_co; // @[wallace.scala 57:25]
  wire  HalfAdder_15_io_a; // @[wallace.scala 57:25]
  wire  HalfAdder_15_io_b; // @[wallace.scala 57:25]
  wire  HalfAdder_15_io_s; // @[wallace.scala 57:25]
  wire  HalfAdder_15_io_co; // @[wallace.scala 57:25]
  wire  HalfAdder_16_io_a; // @[wallace.scala 57:25]
  wire  HalfAdder_16_io_b; // @[wallace.scala 57:25]
  wire  HalfAdder_16_io_s; // @[wallace.scala 57:25]
  wire  HalfAdder_16_io_co; // @[wallace.scala 57:25]
  wire  FullAdder_33_io_a; // @[wallace.scala 67:25]
  wire  FullAdder_33_io_b; // @[wallace.scala 67:25]
  wire  FullAdder_33_io_ci; // @[wallace.scala 67:25]
  wire  FullAdder_33_io_s; // @[wallace.scala 67:25]
  wire  FullAdder_33_io_co; // @[wallace.scala 67:25]
  wire  FullAdder_34_io_a; // @[wallace.scala 67:25]
  wire  FullAdder_34_io_b; // @[wallace.scala 67:25]
  wire  FullAdder_34_io_ci; // @[wallace.scala 67:25]
  wire  FullAdder_34_io_s; // @[wallace.scala 67:25]
  wire  FullAdder_34_io_co; // @[wallace.scala 67:25]
  wire  HalfAdder_17_io_a; // @[wallace.scala 57:25]
  wire  HalfAdder_17_io_b; // @[wallace.scala 57:25]
  wire  HalfAdder_17_io_s; // @[wallace.scala 57:25]
  wire  HalfAdder_17_io_co; // @[wallace.scala 57:25]
  wire  FullAdder_35_io_a; // @[wallace.scala 67:25]
  wire  FullAdder_35_io_b; // @[wallace.scala 67:25]
  wire  FullAdder_35_io_ci; // @[wallace.scala 67:25]
  wire  FullAdder_35_io_s; // @[wallace.scala 67:25]
  wire  FullAdder_35_io_co; // @[wallace.scala 67:25]
  wire  HalfAdder_18_io_a; // @[wallace.scala 57:25]
  wire  HalfAdder_18_io_b; // @[wallace.scala 57:25]
  wire  HalfAdder_18_io_s; // @[wallace.scala 57:25]
  wire  HalfAdder_18_io_co; // @[wallace.scala 57:25]
  wire  HalfAdder_19_io_a; // @[wallace.scala 57:25]
  wire  HalfAdder_19_io_b; // @[wallace.scala 57:25]
  wire  HalfAdder_19_io_s; // @[wallace.scala 57:25]
  wire  HalfAdder_19_io_co; // @[wallace.scala 57:25]
  wire  FullAdder_36_io_a; // @[wallace.scala 67:25]
  wire  FullAdder_36_io_b; // @[wallace.scala 67:25]
  wire  FullAdder_36_io_ci; // @[wallace.scala 67:25]
  wire  FullAdder_36_io_s; // @[wallace.scala 67:25]
  wire  FullAdder_36_io_co; // @[wallace.scala 67:25]
  wire  FullAdder_37_io_a; // @[wallace.scala 67:25]
  wire  FullAdder_37_io_b; // @[wallace.scala 67:25]
  wire  FullAdder_37_io_ci; // @[wallace.scala 67:25]
  wire  FullAdder_37_io_s; // @[wallace.scala 67:25]
  wire  FullAdder_37_io_co; // @[wallace.scala 67:25]
  wire  HalfAdder_20_io_a; // @[wallace.scala 57:25]
  wire  HalfAdder_20_io_b; // @[wallace.scala 57:25]
  wire  HalfAdder_20_io_s; // @[wallace.scala 57:25]
  wire  HalfAdder_20_io_co; // @[wallace.scala 57:25]
  wire  FullAdder_38_io_a; // @[wallace.scala 67:25]
  wire  FullAdder_38_io_b; // @[wallace.scala 67:25]
  wire  FullAdder_38_io_ci; // @[wallace.scala 67:25]
  wire  FullAdder_38_io_s; // @[wallace.scala 67:25]
  wire  FullAdder_38_io_co; // @[wallace.scala 67:25]
  wire  HalfAdder_21_io_a; // @[wallace.scala 57:25]
  wire  HalfAdder_21_io_b; // @[wallace.scala 57:25]
  wire  HalfAdder_21_io_s; // @[wallace.scala 57:25]
  wire  HalfAdder_21_io_co; // @[wallace.scala 57:25]
  wire  HalfAdder_22_io_a; // @[wallace.scala 57:25]
  wire  HalfAdder_22_io_b; // @[wallace.scala 57:25]
  wire  HalfAdder_22_io_s; // @[wallace.scala 57:25]
  wire  HalfAdder_22_io_co; // @[wallace.scala 57:25]
  wire  FullAdder_39_io_a; // @[wallace.scala 67:25]
  wire  FullAdder_39_io_b; // @[wallace.scala 67:25]
  wire  FullAdder_39_io_ci; // @[wallace.scala 67:25]
  wire  FullAdder_39_io_s; // @[wallace.scala 67:25]
  wire  FullAdder_39_io_co; // @[wallace.scala 67:25]
  wire  HalfAdder_23_io_a; // @[wallace.scala 57:25]
  wire  HalfAdder_23_io_b; // @[wallace.scala 57:25]
  wire  HalfAdder_23_io_s; // @[wallace.scala 57:25]
  wire  HalfAdder_23_io_co; // @[wallace.scala 57:25]
  wire  FullAdder_40_io_a; // @[wallace.scala 67:25]
  wire  FullAdder_40_io_b; // @[wallace.scala 67:25]
  wire  FullAdder_40_io_ci; // @[wallace.scala 67:25]
  wire  FullAdder_40_io_s; // @[wallace.scala 67:25]
  wire  FullAdder_40_io_co; // @[wallace.scala 67:25]
  wire  res0_0 = io_pp_0[0]; // @[wallace.scala 34:43]
  wire  res0_1 = io_pp_0[1]; // @[wallace.scala 34:43]
  wire  res1_1 = io_pp_1[0]; // @[wallace.scala 34:43]
  wire  res0_14 = FullAdder_33_io_s; // @[wallace.scala 78:49 wallace.scala 83:13]
  wire  res0_13 = FullAdder_30_io_s; // @[wallace.scala 78:49 wallace.scala 83:13]
  wire  res0_12 = FullAdder_36_io_s; // @[wallace.scala 78:49 wallace.scala 83:13]
  wire  res0_11 = FullAdder_40_io_s; // @[wallace.scala 78:49 wallace.scala 83:13]
  wire  res0_10 = FullAdder_39_io_s; // @[wallace.scala 78:49 wallace.scala 83:13]
  wire  res0_9 = HalfAdder_23_io_s; // @[wallace.scala 78:49 wallace.scala 83:13]
  wire  res0_8 = FullAdder_38_io_s; // @[wallace.scala 78:49 wallace.scala 83:13]
  wire  res0_7 = HalfAdder_19_io_co; // @[wallace.scala 78:49 wallace.scala 83:13]
  wire  res0_6 = HalfAdder_16_io_co; // @[wallace.scala 78:49 wallace.scala 83:13]
  wire  res0_5 = HalfAdder_16_io_s; // @[wallace.scala 78:49 wallace.scala 83:13]
  wire [9:0] _T_72 = {res0_14,res0_13,res0_12,res0_11,res0_10,res0_9,res0_8,res0_7,res0_6,res0_5}; // @[Cat.scala 29:58]
  wire  res0_4 = HalfAdder_11_io_s; // @[wallace.scala 78:49 wallace.scala 83:13]
  wire  res0_3 = FullAdder_24_io_s; // @[wallace.scala 78:49 wallace.scala 83:13]
  wire  res0_2 = FullAdder_15_io_s; // @[wallace.scala 78:49 wallace.scala 83:13]
  wire [14:0] _T_77 = {_T_72,res0_4,res0_3,res0_2,res0_1,res0_0}; // @[Cat.scala 29:58]
  wire  res1_13 = FullAdder_36_io_co; // @[wallace.scala 79:49 wallace.scala 87:15]
  wire  res1_12 = FullAdder_40_io_co; // @[wallace.scala 79:49 wallace.scala 87:15]
  wire  res1_10 = HalfAdder_23_io_co; // @[wallace.scala 79:49 wallace.scala 87:15]
  wire  res1_8 = HalfAdder_21_io_co; // @[wallace.scala 79:49 wallace.scala 87:15]
  wire  res1_7 = HalfAdder_21_io_s; // @[wallace.scala 79:49 wallace.scala 87:15]
  wire  res1_6 = HalfAdder_19_io_s; // @[wallace.scala 79:49 wallace.scala 87:15]
  wire [9:0] _T_86 = {1'h0,res1_13,res1_12,1'h0,res1_10,1'h0,res1_8,res1_7,res1_6,1'h0}; // @[Cat.scala 29:58]
  wire [14:0] _T_91 = {_T_86,1'h0,1'h0,1'h0,res1_1,1'h0}; // @[Cat.scala 29:58]
  HalfAdder HalfAdder ( // @[wallace.scala 57:25]
    .io_a(HalfAdder_io_a),
    .io_b(HalfAdder_io_b),
    .io_s(HalfAdder_io_s),
    .io_co(HalfAdder_io_co)
  );
  FullAdder FullAdder ( // @[wallace.scala 67:25]
    .io_a(FullAdder_io_a),
    .io_b(FullAdder_io_b),
    .io_ci(FullAdder_io_ci),
    .io_s(FullAdder_io_s),
    .io_co(FullAdder_io_co)
  );
  FullAdder FullAdder_1 ( // @[wallace.scala 67:25]
    .io_a(FullAdder_1_io_a),
    .io_b(FullAdder_1_io_b),
    .io_ci(FullAdder_1_io_ci),
    .io_s(FullAdder_1_io_s),
    .io_co(FullAdder_1_io_co)
  );
  FullAdder FullAdder_2 ( // @[wallace.scala 67:25]
    .io_a(FullAdder_2_io_a),
    .io_b(FullAdder_2_io_b),
    .io_ci(FullAdder_2_io_ci),
    .io_s(FullAdder_2_io_s),
    .io_co(FullAdder_2_io_co)
  );
  FullAdder FullAdder_3 ( // @[wallace.scala 67:25]
    .io_a(FullAdder_3_io_a),
    .io_b(FullAdder_3_io_b),
    .io_ci(FullAdder_3_io_ci),
    .io_s(FullAdder_3_io_s),
    .io_co(FullAdder_3_io_co)
  );
  FullAdder FullAdder_4 ( // @[wallace.scala 67:25]
    .io_a(FullAdder_4_io_a),
    .io_b(FullAdder_4_io_b),
    .io_ci(FullAdder_4_io_ci),
    .io_s(FullAdder_4_io_s),
    .io_co(FullAdder_4_io_co)
  );
  FullAdder FullAdder_5 ( // @[wallace.scala 67:25]
    .io_a(FullAdder_5_io_a),
    .io_b(FullAdder_5_io_b),
    .io_ci(FullAdder_5_io_ci),
    .io_s(FullAdder_5_io_s),
    .io_co(FullAdder_5_io_co)
  );
  FullAdder FullAdder_6 ( // @[wallace.scala 67:25]
    .io_a(FullAdder_6_io_a),
    .io_b(FullAdder_6_io_b),
    .io_ci(FullAdder_6_io_ci),
    .io_s(FullAdder_6_io_s),
    .io_co(FullAdder_6_io_co)
  );
  FullAdder FullAdder_7 ( // @[wallace.scala 67:25]
    .io_a(FullAdder_7_io_a),
    .io_b(FullAdder_7_io_b),
    .io_ci(FullAdder_7_io_ci),
    .io_s(FullAdder_7_io_s),
    .io_co(FullAdder_7_io_co)
  );
  FullAdder FullAdder_8 ( // @[wallace.scala 67:25]
    .io_a(FullAdder_8_io_a),
    .io_b(FullAdder_8_io_b),
    .io_ci(FullAdder_8_io_ci),
    .io_s(FullAdder_8_io_s),
    .io_co(FullAdder_8_io_co)
  );
  HalfAdder HalfAdder_1 ( // @[wallace.scala 57:25]
    .io_a(HalfAdder_1_io_a),
    .io_b(HalfAdder_1_io_b),
    .io_s(HalfAdder_1_io_s),
    .io_co(HalfAdder_1_io_co)
  );
  FullAdder FullAdder_9 ( // @[wallace.scala 67:25]
    .io_a(FullAdder_9_io_a),
    .io_b(FullAdder_9_io_b),
    .io_ci(FullAdder_9_io_ci),
    .io_s(FullAdder_9_io_s),
    .io_co(FullAdder_9_io_co)
  );
  FullAdder FullAdder_10 ( // @[wallace.scala 67:25]
    .io_a(FullAdder_10_io_a),
    .io_b(FullAdder_10_io_b),
    .io_ci(FullAdder_10_io_ci),
    .io_s(FullAdder_10_io_s),
    .io_co(FullAdder_10_io_co)
  );
  FullAdder FullAdder_11 ( // @[wallace.scala 67:25]
    .io_a(FullAdder_11_io_a),
    .io_b(FullAdder_11_io_b),
    .io_ci(FullAdder_11_io_ci),
    .io_s(FullAdder_11_io_s),
    .io_co(FullAdder_11_io_co)
  );
  FullAdder FullAdder_12 ( // @[wallace.scala 67:25]
    .io_a(FullAdder_12_io_a),
    .io_b(FullAdder_12_io_b),
    .io_ci(FullAdder_12_io_ci),
    .io_s(FullAdder_12_io_s),
    .io_co(FullAdder_12_io_co)
  );
  FullAdder FullAdder_13 ( // @[wallace.scala 67:25]
    .io_a(FullAdder_13_io_a),
    .io_b(FullAdder_13_io_b),
    .io_ci(FullAdder_13_io_ci),
    .io_s(FullAdder_13_io_s),
    .io_co(FullAdder_13_io_co)
  );
  HalfAdder HalfAdder_2 ( // @[wallace.scala 57:25]
    .io_a(HalfAdder_2_io_a),
    .io_b(HalfAdder_2_io_b),
    .io_s(HalfAdder_2_io_s),
    .io_co(HalfAdder_2_io_co)
  );
  FullAdder FullAdder_14 ( // @[wallace.scala 67:25]
    .io_a(FullAdder_14_io_a),
    .io_b(FullAdder_14_io_b),
    .io_ci(FullAdder_14_io_ci),
    .io_s(FullAdder_14_io_s),
    .io_co(FullAdder_14_io_co)
  );
  FullAdder FullAdder_15 ( // @[wallace.scala 67:25]
    .io_a(FullAdder_15_io_a),
    .io_b(FullAdder_15_io_b),
    .io_ci(FullAdder_15_io_ci),
    .io_s(FullAdder_15_io_s),
    .io_co(FullAdder_15_io_co)
  );
  FullAdder FullAdder_16 ( // @[wallace.scala 67:25]
    .io_a(FullAdder_16_io_a),
    .io_b(FullAdder_16_io_b),
    .io_ci(FullAdder_16_io_ci),
    .io_s(FullAdder_16_io_s),
    .io_co(FullAdder_16_io_co)
  );
  FullAdder FullAdder_17 ( // @[wallace.scala 67:25]
    .io_a(FullAdder_17_io_a),
    .io_b(FullAdder_17_io_b),
    .io_ci(FullAdder_17_io_ci),
    .io_s(FullAdder_17_io_s),
    .io_co(FullAdder_17_io_co)
  );
  FullAdder FullAdder_18 ( // @[wallace.scala 67:25]
    .io_a(FullAdder_18_io_a),
    .io_b(FullAdder_18_io_b),
    .io_ci(FullAdder_18_io_ci),
    .io_s(FullAdder_18_io_s),
    .io_co(FullAdder_18_io_co)
  );
  FullAdder FullAdder_19 ( // @[wallace.scala 67:25]
    .io_a(FullAdder_19_io_a),
    .io_b(FullAdder_19_io_b),
    .io_ci(FullAdder_19_io_ci),
    .io_s(FullAdder_19_io_s),
    .io_co(FullAdder_19_io_co)
  );
  FullAdder FullAdder_20 ( // @[wallace.scala 67:25]
    .io_a(FullAdder_20_io_a),
    .io_b(FullAdder_20_io_b),
    .io_ci(FullAdder_20_io_ci),
    .io_s(FullAdder_20_io_s),
    .io_co(FullAdder_20_io_co)
  );
  FullAdder FullAdder_21 ( // @[wallace.scala 67:25]
    .io_a(FullAdder_21_io_a),
    .io_b(FullAdder_21_io_b),
    .io_ci(FullAdder_21_io_ci),
    .io_s(FullAdder_21_io_s),
    .io_co(FullAdder_21_io_co)
  );
  HalfAdder HalfAdder_3 ( // @[wallace.scala 57:25]
    .io_a(HalfAdder_3_io_a),
    .io_b(HalfAdder_3_io_b),
    .io_s(HalfAdder_3_io_s),
    .io_co(HalfAdder_3_io_co)
  );
  HalfAdder HalfAdder_4 ( // @[wallace.scala 57:25]
    .io_a(HalfAdder_4_io_a),
    .io_b(HalfAdder_4_io_b),
    .io_s(HalfAdder_4_io_s),
    .io_co(HalfAdder_4_io_co)
  );
  HalfAdder HalfAdder_5 ( // @[wallace.scala 57:25]
    .io_a(HalfAdder_5_io_a),
    .io_b(HalfAdder_5_io_b),
    .io_s(HalfAdder_5_io_s),
    .io_co(HalfAdder_5_io_co)
  );
  FullAdder FullAdder_22 ( // @[wallace.scala 67:25]
    .io_a(FullAdder_22_io_a),
    .io_b(FullAdder_22_io_b),
    .io_ci(FullAdder_22_io_ci),
    .io_s(FullAdder_22_io_s),
    .io_co(FullAdder_22_io_co)
  );
  FullAdder FullAdder_23 ( // @[wallace.scala 67:25]
    .io_a(FullAdder_23_io_a),
    .io_b(FullAdder_23_io_b),
    .io_ci(FullAdder_23_io_ci),
    .io_s(FullAdder_23_io_s),
    .io_co(FullAdder_23_io_co)
  );
  FullAdder FullAdder_24 ( // @[wallace.scala 67:25]
    .io_a(FullAdder_24_io_a),
    .io_b(FullAdder_24_io_b),
    .io_ci(FullAdder_24_io_ci),
    .io_s(FullAdder_24_io_s),
    .io_co(FullAdder_24_io_co)
  );
  FullAdder FullAdder_25 ( // @[wallace.scala 67:25]
    .io_a(FullAdder_25_io_a),
    .io_b(FullAdder_25_io_b),
    .io_ci(FullAdder_25_io_ci),
    .io_s(FullAdder_25_io_s),
    .io_co(FullAdder_25_io_co)
  );
  HalfAdder HalfAdder_6 ( // @[wallace.scala 57:25]
    .io_a(HalfAdder_6_io_a),
    .io_b(HalfAdder_6_io_b),
    .io_s(HalfAdder_6_io_s),
    .io_co(HalfAdder_6_io_co)
  );
  FullAdder FullAdder_26 ( // @[wallace.scala 67:25]
    .io_a(FullAdder_26_io_a),
    .io_b(FullAdder_26_io_b),
    .io_ci(FullAdder_26_io_ci),
    .io_s(FullAdder_26_io_s),
    .io_co(FullAdder_26_io_co)
  );
  FullAdder FullAdder_27 ( // @[wallace.scala 67:25]
    .io_a(FullAdder_27_io_a),
    .io_b(FullAdder_27_io_b),
    .io_ci(FullAdder_27_io_ci),
    .io_s(FullAdder_27_io_s),
    .io_co(FullAdder_27_io_co)
  );
  FullAdder FullAdder_28 ( // @[wallace.scala 67:25]
    .io_a(FullAdder_28_io_a),
    .io_b(FullAdder_28_io_b),
    .io_ci(FullAdder_28_io_ci),
    .io_s(FullAdder_28_io_s),
    .io_co(FullAdder_28_io_co)
  );
  HalfAdder HalfAdder_7 ( // @[wallace.scala 57:25]
    .io_a(HalfAdder_7_io_a),
    .io_b(HalfAdder_7_io_b),
    .io_s(HalfAdder_7_io_s),
    .io_co(HalfAdder_7_io_co)
  );
  HalfAdder HalfAdder_8 ( // @[wallace.scala 57:25]
    .io_a(HalfAdder_8_io_a),
    .io_b(HalfAdder_8_io_b),
    .io_s(HalfAdder_8_io_s),
    .io_co(HalfAdder_8_io_co)
  );
  HalfAdder HalfAdder_9 ( // @[wallace.scala 57:25]
    .io_a(HalfAdder_9_io_a),
    .io_b(HalfAdder_9_io_b),
    .io_s(HalfAdder_9_io_s),
    .io_co(HalfAdder_9_io_co)
  );
  HalfAdder HalfAdder_10 ( // @[wallace.scala 57:25]
    .io_a(HalfAdder_10_io_a),
    .io_b(HalfAdder_10_io_b),
    .io_s(HalfAdder_10_io_s),
    .io_co(HalfAdder_10_io_co)
  );
  FullAdder FullAdder_29 ( // @[wallace.scala 67:25]
    .io_a(FullAdder_29_io_a),
    .io_b(FullAdder_29_io_b),
    .io_ci(FullAdder_29_io_ci),
    .io_s(FullAdder_29_io_s),
    .io_co(FullAdder_29_io_co)
  );
  HalfAdder HalfAdder_11 ( // @[wallace.scala 57:25]
    .io_a(HalfAdder_11_io_a),
    .io_b(HalfAdder_11_io_b),
    .io_s(HalfAdder_11_io_s),
    .io_co(HalfAdder_11_io_co)
  );
  FullAdder FullAdder_30 ( // @[wallace.scala 67:25]
    .io_a(FullAdder_30_io_a),
    .io_b(FullAdder_30_io_b),
    .io_ci(FullAdder_30_io_ci),
    .io_s(FullAdder_30_io_s),
    .io_co(FullAdder_30_io_co)
  );
  FullAdder FullAdder_31 ( // @[wallace.scala 67:25]
    .io_a(FullAdder_31_io_a),
    .io_b(FullAdder_31_io_b),
    .io_ci(FullAdder_31_io_ci),
    .io_s(FullAdder_31_io_s),
    .io_co(FullAdder_31_io_co)
  );
  HalfAdder HalfAdder_12 ( // @[wallace.scala 57:25]
    .io_a(HalfAdder_12_io_a),
    .io_b(HalfAdder_12_io_b),
    .io_s(HalfAdder_12_io_s),
    .io_co(HalfAdder_12_io_co)
  );
  FullAdder FullAdder_32 ( // @[wallace.scala 67:25]
    .io_a(FullAdder_32_io_a),
    .io_b(FullAdder_32_io_b),
    .io_ci(FullAdder_32_io_ci),
    .io_s(FullAdder_32_io_s),
    .io_co(FullAdder_32_io_co)
  );
  HalfAdder HalfAdder_13 ( // @[wallace.scala 57:25]
    .io_a(HalfAdder_13_io_a),
    .io_b(HalfAdder_13_io_b),
    .io_s(HalfAdder_13_io_s),
    .io_co(HalfAdder_13_io_co)
  );
  HalfAdder HalfAdder_14 ( // @[wallace.scala 57:25]
    .io_a(HalfAdder_14_io_a),
    .io_b(HalfAdder_14_io_b),
    .io_s(HalfAdder_14_io_s),
    .io_co(HalfAdder_14_io_co)
  );
  HalfAdder HalfAdder_15 ( // @[wallace.scala 57:25]
    .io_a(HalfAdder_15_io_a),
    .io_b(HalfAdder_15_io_b),
    .io_s(HalfAdder_15_io_s),
    .io_co(HalfAdder_15_io_co)
  );
  HalfAdder HalfAdder_16 ( // @[wallace.scala 57:25]
    .io_a(HalfAdder_16_io_a),
    .io_b(HalfAdder_16_io_b),
    .io_s(HalfAdder_16_io_s),
    .io_co(HalfAdder_16_io_co)
  );
  FullAdder FullAdder_33 ( // @[wallace.scala 67:25]
    .io_a(FullAdder_33_io_a),
    .io_b(FullAdder_33_io_b),
    .io_ci(FullAdder_33_io_ci),
    .io_s(FullAdder_33_io_s),
    .io_co(FullAdder_33_io_co)
  );
  FullAdder FullAdder_34 ( // @[wallace.scala 67:25]
    .io_a(FullAdder_34_io_a),
    .io_b(FullAdder_34_io_b),
    .io_ci(FullAdder_34_io_ci),
    .io_s(FullAdder_34_io_s),
    .io_co(FullAdder_34_io_co)
  );
  HalfAdder HalfAdder_17 ( // @[wallace.scala 57:25]
    .io_a(HalfAdder_17_io_a),
    .io_b(HalfAdder_17_io_b),
    .io_s(HalfAdder_17_io_s),
    .io_co(HalfAdder_17_io_co)
  );
  FullAdder FullAdder_35 ( // @[wallace.scala 67:25]
    .io_a(FullAdder_35_io_a),
    .io_b(FullAdder_35_io_b),
    .io_ci(FullAdder_35_io_ci),
    .io_s(FullAdder_35_io_s),
    .io_co(FullAdder_35_io_co)
  );
  HalfAdder HalfAdder_18 ( // @[wallace.scala 57:25]
    .io_a(HalfAdder_18_io_a),
    .io_b(HalfAdder_18_io_b),
    .io_s(HalfAdder_18_io_s),
    .io_co(HalfAdder_18_io_co)
  );
  HalfAdder HalfAdder_19 ( // @[wallace.scala 57:25]
    .io_a(HalfAdder_19_io_a),
    .io_b(HalfAdder_19_io_b),
    .io_s(HalfAdder_19_io_s),
    .io_co(HalfAdder_19_io_co)
  );
  FullAdder FullAdder_36 ( // @[wallace.scala 67:25]
    .io_a(FullAdder_36_io_a),
    .io_b(FullAdder_36_io_b),
    .io_ci(FullAdder_36_io_ci),
    .io_s(FullAdder_36_io_s),
    .io_co(FullAdder_36_io_co)
  );
  FullAdder FullAdder_37 ( // @[wallace.scala 67:25]
    .io_a(FullAdder_37_io_a),
    .io_b(FullAdder_37_io_b),
    .io_ci(FullAdder_37_io_ci),
    .io_s(FullAdder_37_io_s),
    .io_co(FullAdder_37_io_co)
  );
  HalfAdder HalfAdder_20 ( // @[wallace.scala 57:25]
    .io_a(HalfAdder_20_io_a),
    .io_b(HalfAdder_20_io_b),
    .io_s(HalfAdder_20_io_s),
    .io_co(HalfAdder_20_io_co)
  );
  FullAdder FullAdder_38 ( // @[wallace.scala 67:25]
    .io_a(FullAdder_38_io_a),
    .io_b(FullAdder_38_io_b),
    .io_ci(FullAdder_38_io_ci),
    .io_s(FullAdder_38_io_s),
    .io_co(FullAdder_38_io_co)
  );
  HalfAdder HalfAdder_21 ( // @[wallace.scala 57:25]
    .io_a(HalfAdder_21_io_a),
    .io_b(HalfAdder_21_io_b),
    .io_s(HalfAdder_21_io_s),
    .io_co(HalfAdder_21_io_co)
  );
  HalfAdder HalfAdder_22 ( // @[wallace.scala 57:25]
    .io_a(HalfAdder_22_io_a),
    .io_b(HalfAdder_22_io_b),
    .io_s(HalfAdder_22_io_s),
    .io_co(HalfAdder_22_io_co)
  );
  FullAdder FullAdder_39 ( // @[wallace.scala 67:25]
    .io_a(FullAdder_39_io_a),
    .io_b(FullAdder_39_io_b),
    .io_ci(FullAdder_39_io_ci),
    .io_s(FullAdder_39_io_s),
    .io_co(FullAdder_39_io_co)
  );
  HalfAdder HalfAdder_23 ( // @[wallace.scala 57:25]
    .io_a(HalfAdder_23_io_a),
    .io_b(HalfAdder_23_io_b),
    .io_s(HalfAdder_23_io_s),
    .io_co(HalfAdder_23_io_co)
  );
  FullAdder FullAdder_40 ( // @[wallace.scala 67:25]
    .io_a(FullAdder_40_io_a),
    .io_b(FullAdder_40_io_b),
    .io_ci(FullAdder_40_io_ci),
    .io_s(FullAdder_40_io_s),
    .io_co(FullAdder_40_io_co)
  );
  assign io_augend = {{1'd0}, _T_77}; // @[wallace.scala 90:13]
  assign io_addend = {{1'd0}, _T_91}; // @[wallace.scala 91:13]
  assign HalfAdder_io_a = io_pp_6[7]; // @[wallace.scala 59:18]
  assign HalfAdder_io_b = io_pp_7[6]; // @[wallace.scala 60:18]
  assign FullAdder_io_a = io_pp_5[7]; // @[wallace.scala 69:18]
  assign FullAdder_io_b = io_pp_6[6]; // @[wallace.scala 70:18]
  assign FullAdder_io_ci = io_pp_7[5]; // @[wallace.scala 71:19]
  assign FullAdder_1_io_a = io_pp_4[7]; // @[wallace.scala 69:18]
  assign FullAdder_1_io_b = io_pp_5[6]; // @[wallace.scala 70:18]
  assign FullAdder_1_io_ci = io_pp_6[5]; // @[wallace.scala 71:19]
  assign FullAdder_2_io_a = io_pp_3[7]; // @[wallace.scala 69:18]
  assign FullAdder_2_io_b = io_pp_4[6]; // @[wallace.scala 70:18]
  assign FullAdder_2_io_ci = io_pp_5[5]; // @[wallace.scala 71:19]
  assign FullAdder_3_io_a = io_pp_2[7]; // @[wallace.scala 69:18]
  assign FullAdder_3_io_b = io_pp_3[6]; // @[wallace.scala 70:18]
  assign FullAdder_3_io_ci = io_pp_4[5]; // @[wallace.scala 71:19]
  assign FullAdder_4_io_a = io_pp_5[4]; // @[wallace.scala 69:18]
  assign FullAdder_4_io_b = io_pp_6[3]; // @[wallace.scala 70:18]
  assign FullAdder_4_io_ci = io_pp_7[2]; // @[wallace.scala 71:19]
  assign FullAdder_5_io_a = io_pp_1[7]; // @[wallace.scala 69:18]
  assign FullAdder_5_io_b = io_pp_2[6]; // @[wallace.scala 70:18]
  assign FullAdder_5_io_ci = io_pp_3[5]; // @[wallace.scala 71:19]
  assign FullAdder_6_io_a = io_pp_4[4]; // @[wallace.scala 69:18]
  assign FullAdder_6_io_b = io_pp_5[3]; // @[wallace.scala 70:18]
  assign FullAdder_6_io_ci = io_pp_6[2]; // @[wallace.scala 71:19]
  assign FullAdder_7_io_a = io_pp_0[7]; // @[wallace.scala 69:18]
  assign FullAdder_7_io_b = io_pp_1[6]; // @[wallace.scala 70:18]
  assign FullAdder_7_io_ci = io_pp_2[5]; // @[wallace.scala 71:19]
  assign FullAdder_8_io_a = io_pp_3[4]; // @[wallace.scala 69:18]
  assign FullAdder_8_io_b = io_pp_4[3]; // @[wallace.scala 70:18]
  assign FullAdder_8_io_ci = io_pp_5[2]; // @[wallace.scala 71:19]
  assign HalfAdder_1_io_a = io_pp_6[1]; // @[wallace.scala 59:18]
  assign HalfAdder_1_io_b = io_pp_7[0]; // @[wallace.scala 60:18]
  assign FullAdder_9_io_a = io_pp_0[6]; // @[wallace.scala 69:18]
  assign FullAdder_9_io_b = io_pp_1[5]; // @[wallace.scala 70:18]
  assign FullAdder_9_io_ci = io_pp_2[4]; // @[wallace.scala 71:19]
  assign FullAdder_10_io_a = io_pp_3[3]; // @[wallace.scala 69:18]
  assign FullAdder_10_io_b = io_pp_4[2]; // @[wallace.scala 70:18]
  assign FullAdder_10_io_ci = io_pp_5[1]; // @[wallace.scala 71:19]
  assign FullAdder_11_io_a = io_pp_0[5]; // @[wallace.scala 69:18]
  assign FullAdder_11_io_b = io_pp_1[4]; // @[wallace.scala 70:18]
  assign FullAdder_11_io_ci = io_pp_2[3]; // @[wallace.scala 71:19]
  assign FullAdder_12_io_a = io_pp_3[2]; // @[wallace.scala 69:18]
  assign FullAdder_12_io_b = io_pp_4[1]; // @[wallace.scala 70:18]
  assign FullAdder_12_io_ci = io_pp_5[0]; // @[wallace.scala 71:19]
  assign FullAdder_13_io_a = io_pp_0[4]; // @[wallace.scala 69:18]
  assign FullAdder_13_io_b = io_pp_1[3]; // @[wallace.scala 70:18]
  assign FullAdder_13_io_ci = io_pp_2[2]; // @[wallace.scala 71:19]
  assign HalfAdder_2_io_a = io_pp_3[1]; // @[wallace.scala 59:18]
  assign HalfAdder_2_io_b = io_pp_4[0]; // @[wallace.scala 60:18]
  assign FullAdder_14_io_a = io_pp_0[3]; // @[wallace.scala 69:18]
  assign FullAdder_14_io_b = io_pp_1[2]; // @[wallace.scala 70:18]
  assign FullAdder_14_io_ci = io_pp_2[1]; // @[wallace.scala 71:19]
  assign FullAdder_15_io_a = io_pp_0[2]; // @[wallace.scala 69:18]
  assign FullAdder_15_io_b = io_pp_1[1]; // @[wallace.scala 70:18]
  assign FullAdder_15_io_ci = io_pp_2[0]; // @[wallace.scala 71:19]
  assign FullAdder_16_io_a = io_pp_7[4]; // @[wallace.scala 69:18]
  assign FullAdder_16_io_b = FullAdder_1_io_s; // @[wallace.scala 70:18]
  assign FullAdder_16_io_ci = FullAdder_2_io_co; // @[wallace.scala 71:19]
  assign FullAdder_17_io_a = io_pp_6[4]; // @[wallace.scala 69:18]
  assign FullAdder_17_io_b = io_pp_7[3]; // @[wallace.scala 70:18]
  assign FullAdder_17_io_ci = FullAdder_2_io_s; // @[wallace.scala 71:19]
  assign FullAdder_18_io_a = FullAdder_3_io_s; // @[wallace.scala 69:18]
  assign FullAdder_18_io_b = FullAdder_4_io_s; // @[wallace.scala 70:18]
  assign FullAdder_18_io_ci = FullAdder_5_io_co; // @[wallace.scala 71:19]
  assign FullAdder_19_io_a = io_pp_7[1]; // @[wallace.scala 69:18]
  assign FullAdder_19_io_b = FullAdder_5_io_s; // @[wallace.scala 70:18]
  assign FullAdder_19_io_ci = FullAdder_6_io_s; // @[wallace.scala 71:19]
  assign FullAdder_20_io_a = FullAdder_7_io_co; // @[wallace.scala 69:18]
  assign FullAdder_20_io_b = FullAdder_8_io_co; // @[wallace.scala 70:18]
  assign FullAdder_20_io_ci = HalfAdder_1_io_co; // @[wallace.scala 71:19]
  assign FullAdder_21_io_a = FullAdder_7_io_s; // @[wallace.scala 69:18]
  assign FullAdder_21_io_b = FullAdder_8_io_s; // @[wallace.scala 70:18]
  assign FullAdder_21_io_ci = HalfAdder_1_io_s; // @[wallace.scala 71:19]
  assign HalfAdder_3_io_a = FullAdder_9_io_co; // @[wallace.scala 59:18]
  assign HalfAdder_3_io_b = FullAdder_10_io_co; // @[wallace.scala 60:18]
  assign HalfAdder_4_io_a = io_pp_6[0]; // @[wallace.scala 59:18]
  assign HalfAdder_4_io_b = FullAdder_9_io_s; // @[wallace.scala 60:18]
  assign HalfAdder_5_io_a = FullAdder_10_io_s; // @[wallace.scala 59:18]
  assign HalfAdder_5_io_b = FullAdder_11_io_co; // @[wallace.scala 60:18]
  assign FullAdder_22_io_a = FullAdder_11_io_s; // @[wallace.scala 69:18]
  assign FullAdder_22_io_b = FullAdder_12_io_s; // @[wallace.scala 70:18]
  assign FullAdder_22_io_ci = FullAdder_13_io_co; // @[wallace.scala 71:19]
  assign FullAdder_23_io_a = FullAdder_13_io_s; // @[wallace.scala 69:18]
  assign FullAdder_23_io_b = HalfAdder_2_io_s; // @[wallace.scala 70:18]
  assign FullAdder_23_io_ci = FullAdder_14_io_co; // @[wallace.scala 71:19]
  assign FullAdder_24_io_a = io_pp_3[0]; // @[wallace.scala 69:18]
  assign FullAdder_24_io_b = FullAdder_14_io_s; // @[wallace.scala 70:18]
  assign FullAdder_24_io_ci = FullAdder_15_io_co; // @[wallace.scala 71:19]
  assign FullAdder_25_io_a = FullAdder_io_s; // @[wallace.scala 69:18]
  assign FullAdder_25_io_b = FullAdder_1_io_co; // @[wallace.scala 70:18]
  assign FullAdder_25_io_ci = FullAdder_16_io_co; // @[wallace.scala 71:19]
  assign HalfAdder_6_io_a = FullAdder_16_io_s; // @[wallace.scala 59:18]
  assign HalfAdder_6_io_b = FullAdder_17_io_co; // @[wallace.scala 60:18]
  assign FullAdder_26_io_a = FullAdder_3_io_co; // @[wallace.scala 69:18]
  assign FullAdder_26_io_b = FullAdder_4_io_co; // @[wallace.scala 70:18]
  assign FullAdder_26_io_ci = FullAdder_17_io_s; // @[wallace.scala 71:19]
  assign FullAdder_27_io_a = FullAdder_6_io_co; // @[wallace.scala 69:18]
  assign FullAdder_27_io_b = FullAdder_18_io_s; // @[wallace.scala 70:18]
  assign FullAdder_27_io_ci = FullAdder_19_io_co; // @[wallace.scala 71:19]
  assign FullAdder_28_io_a = FullAdder_19_io_s; // @[wallace.scala 69:18]
  assign FullAdder_28_io_b = FullAdder_20_io_s; // @[wallace.scala 70:18]
  assign FullAdder_28_io_ci = FullAdder_21_io_co; // @[wallace.scala 71:19]
  assign HalfAdder_7_io_a = FullAdder_21_io_s; // @[wallace.scala 59:18]
  assign HalfAdder_7_io_b = HalfAdder_3_io_s; // @[wallace.scala 60:18]
  assign HalfAdder_8_io_a = HalfAdder_4_io_co; // @[wallace.scala 59:18]
  assign HalfAdder_8_io_b = HalfAdder_5_io_co; // @[wallace.scala 60:18]
  assign HalfAdder_9_io_a = FullAdder_12_io_co; // @[wallace.scala 59:18]
  assign HalfAdder_9_io_b = HalfAdder_4_io_s; // @[wallace.scala 60:18]
  assign HalfAdder_10_io_a = HalfAdder_5_io_s; // @[wallace.scala 59:18]
  assign HalfAdder_10_io_b = FullAdder_22_io_co; // @[wallace.scala 60:18]
  assign FullAdder_29_io_a = HalfAdder_2_io_co; // @[wallace.scala 69:18]
  assign FullAdder_29_io_b = FullAdder_22_io_s; // @[wallace.scala 70:18]
  assign FullAdder_29_io_ci = FullAdder_23_io_co; // @[wallace.scala 71:19]
  assign HalfAdder_11_io_a = FullAdder_23_io_s; // @[wallace.scala 59:18]
  assign HalfAdder_11_io_b = FullAdder_24_io_co; // @[wallace.scala 60:18]
  assign FullAdder_30_io_a = HalfAdder_io_s; // @[wallace.scala 69:18]
  assign FullAdder_30_io_b = FullAdder_io_co; // @[wallace.scala 70:18]
  assign FullAdder_30_io_ci = FullAdder_25_io_co; // @[wallace.scala 71:19]
  assign FullAdder_31_io_a = FullAdder_18_io_co; // @[wallace.scala 69:18]
  assign FullAdder_31_io_b = FullAdder_26_io_s; // @[wallace.scala 70:18]
  assign FullAdder_31_io_ci = FullAdder_27_io_co; // @[wallace.scala 71:19]
  assign HalfAdder_12_io_a = FullAdder_20_io_co; // @[wallace.scala 59:18]
  assign HalfAdder_12_io_b = FullAdder_27_io_s; // @[wallace.scala 60:18]
  assign FullAdder_32_io_a = HalfAdder_3_io_co; // @[wallace.scala 69:18]
  assign FullAdder_32_io_b = FullAdder_28_io_s; // @[wallace.scala 70:18]
  assign FullAdder_32_io_ci = HalfAdder_7_io_co; // @[wallace.scala 71:19]
  assign HalfAdder_13_io_a = HalfAdder_7_io_s; // @[wallace.scala 59:18]
  assign HalfAdder_13_io_b = HalfAdder_8_io_s; // @[wallace.scala 60:18]
  assign HalfAdder_14_io_a = HalfAdder_9_io_co; // @[wallace.scala 59:18]
  assign HalfAdder_14_io_b = HalfAdder_10_io_co; // @[wallace.scala 60:18]
  assign HalfAdder_15_io_a = HalfAdder_9_io_s; // @[wallace.scala 59:18]
  assign HalfAdder_15_io_b = HalfAdder_10_io_s; // @[wallace.scala 60:18]
  assign HalfAdder_16_io_a = FullAdder_29_io_s; // @[wallace.scala 59:18]
  assign HalfAdder_16_io_b = HalfAdder_11_io_co; // @[wallace.scala 60:18]
  assign FullAdder_33_io_a = io_pp_7[7]; // @[wallace.scala 69:18]
  assign FullAdder_33_io_b = HalfAdder_io_co; // @[wallace.scala 70:18]
  assign FullAdder_33_io_ci = FullAdder_30_io_co; // @[wallace.scala 71:19]
  assign FullAdder_34_io_a = HalfAdder_6_io_s; // @[wallace.scala 69:18]
  assign FullAdder_34_io_b = FullAdder_26_io_co; // @[wallace.scala 70:18]
  assign FullAdder_34_io_ci = FullAdder_31_io_co; // @[wallace.scala 71:19]
  assign HalfAdder_17_io_a = FullAdder_28_io_co; // @[wallace.scala 59:18]
  assign HalfAdder_17_io_b = HalfAdder_12_io_s; // @[wallace.scala 60:18]
  assign FullAdder_35_io_a = HalfAdder_8_io_co; // @[wallace.scala 69:18]
  assign FullAdder_35_io_b = FullAdder_32_io_s; // @[wallace.scala 70:18]
  assign FullAdder_35_io_ci = HalfAdder_13_io_co; // @[wallace.scala 71:19]
  assign HalfAdder_18_io_a = HalfAdder_13_io_s; // @[wallace.scala 59:18]
  assign HalfAdder_18_io_b = HalfAdder_14_io_s; // @[wallace.scala 60:18]
  assign HalfAdder_19_io_a = FullAdder_29_io_co; // @[wallace.scala 59:18]
  assign HalfAdder_19_io_b = HalfAdder_15_io_s; // @[wallace.scala 60:18]
  assign FullAdder_36_io_a = FullAdder_25_io_s; // @[wallace.scala 69:18]
  assign FullAdder_36_io_b = HalfAdder_6_io_co; // @[wallace.scala 70:18]
  assign FullAdder_36_io_ci = FullAdder_34_io_co; // @[wallace.scala 71:19]
  assign FullAdder_37_io_a = FullAdder_31_io_s; // @[wallace.scala 69:18]
  assign FullAdder_37_io_b = HalfAdder_12_io_co; // @[wallace.scala 70:18]
  assign FullAdder_37_io_ci = HalfAdder_17_io_co; // @[wallace.scala 71:19]
  assign HalfAdder_20_io_a = FullAdder_32_io_co; // @[wallace.scala 59:18]
  assign HalfAdder_20_io_b = HalfAdder_17_io_s; // @[wallace.scala 60:18]
  assign FullAdder_38_io_a = HalfAdder_14_io_co; // @[wallace.scala 69:18]
  assign FullAdder_38_io_b = FullAdder_35_io_s; // @[wallace.scala 70:18]
  assign FullAdder_38_io_ci = HalfAdder_18_io_co; // @[wallace.scala 71:19]
  assign HalfAdder_21_io_a = HalfAdder_15_io_co; // @[wallace.scala 59:18]
  assign HalfAdder_21_io_b = HalfAdder_18_io_s; // @[wallace.scala 60:18]
  assign HalfAdder_22_io_a = FullAdder_35_io_co; // @[wallace.scala 59:18]
  assign HalfAdder_22_io_b = HalfAdder_20_io_s; // @[wallace.scala 60:18]
  assign FullAdder_39_io_a = FullAdder_37_io_s; // @[wallace.scala 69:18]
  assign FullAdder_39_io_b = HalfAdder_20_io_co; // @[wallace.scala 70:18]
  assign FullAdder_39_io_ci = HalfAdder_22_io_co; // @[wallace.scala 71:19]
  assign HalfAdder_23_io_a = FullAdder_38_io_co; // @[wallace.scala 59:18]
  assign HalfAdder_23_io_b = HalfAdder_22_io_s; // @[wallace.scala 60:18]
  assign FullAdder_40_io_a = FullAdder_34_io_s; // @[wallace.scala 69:18]
  assign FullAdder_40_io_b = FullAdder_37_io_co; // @[wallace.scala 70:18]
  assign FullAdder_40_io_ci = FullAdder_39_io_co; // @[wallace.scala 71:19]
endmodule
module MUL(
  input  [7:0]  io_multiplicand,
  input  [7:0]  io_multiplier,
  output [14:0] io_outs
);
  wire [7:0] pp_io_multiplicand; // @[mul.scala 26:18]
  wire [7:0] pp_io_multiplier; // @[mul.scala 26:18]
  wire [7:0] pp_io_outs_0; // @[mul.scala 26:18]
  wire [7:0] pp_io_outs_1; // @[mul.scala 26:18]
  wire [7:0] pp_io_outs_2; // @[mul.scala 26:18]
  wire [7:0] pp_io_outs_3; // @[mul.scala 26:18]
  wire [7:0] pp_io_outs_4; // @[mul.scala 26:18]
  wire [7:0] pp_io_outs_5; // @[mul.scala 26:18]
  wire [7:0] pp_io_outs_6; // @[mul.scala 26:18]
  wire [7:0] pp_io_outs_7; // @[mul.scala 26:18]
  wire [7:0] wt_io_pp_0; // @[mul.scala 30:18]
  wire [7:0] wt_io_pp_1; // @[mul.scala 30:18]
  wire [7:0] wt_io_pp_2; // @[mul.scala 30:18]
  wire [7:0] wt_io_pp_3; // @[mul.scala 30:18]
  wire [7:0] wt_io_pp_4; // @[mul.scala 30:18]
  wire [7:0] wt_io_pp_5; // @[mul.scala 30:18]
  wire [7:0] wt_io_pp_6; // @[mul.scala 30:18]
  wire [7:0] wt_io_pp_7; // @[mul.scala 30:18]
  wire [15:0] wt_io_augend; // @[mul.scala 30:18]
  wire [15:0] wt_io_addend; // @[mul.scala 30:18]
  wire [15:0] _T_1 = wt_io_augend + wt_io_addend; // @[mul.scala 37:27]
  PartialProd pp ( // @[mul.scala 26:18]
    .io_multiplicand(pp_io_multiplicand),
    .io_multiplier(pp_io_multiplier),
    .io_outs_0(pp_io_outs_0),
    .io_outs_1(pp_io_outs_1),
    .io_outs_2(pp_io_outs_2),
    .io_outs_3(pp_io_outs_3),
    .io_outs_4(pp_io_outs_4),
    .io_outs_5(pp_io_outs_5),
    .io_outs_6(pp_io_outs_6),
    .io_outs_7(pp_io_outs_7)
  );
  Wallace wt ( // @[mul.scala 30:18]
    .io_pp_0(wt_io_pp_0),
    .io_pp_1(wt_io_pp_1),
    .io_pp_2(wt_io_pp_2),
    .io_pp_3(wt_io_pp_3),
    .io_pp_4(wt_io_pp_4),
    .io_pp_5(wt_io_pp_5),
    .io_pp_6(wt_io_pp_6),
    .io_pp_7(wt_io_pp_7),
    .io_augend(wt_io_augend),
    .io_addend(wt_io_addend)
  );
  assign io_outs = _T_1[14:0]; // @[mul.scala 37:11]
  assign pp_io_multiplicand = io_multiplicand; // @[mul.scala 27:22]
  assign pp_io_multiplier = io_multiplier; // @[mul.scala 28:20]
  assign wt_io_pp_0 = pp_io_outs_0; // @[mul.scala 31:12]
  assign wt_io_pp_1 = pp_io_outs_1; // @[mul.scala 31:12]
  assign wt_io_pp_2 = pp_io_outs_2; // @[mul.scala 31:12]
  assign wt_io_pp_3 = pp_io_outs_3; // @[mul.scala 31:12]
  assign wt_io_pp_4 = pp_io_outs_4; // @[mul.scala 31:12]
  assign wt_io_pp_5 = pp_io_outs_5; // @[mul.scala 31:12]
  assign wt_io_pp_6 = pp_io_outs_6; // @[mul.scala 31:12]
  assign wt_io_pp_7 = pp_io_outs_7; // @[mul.scala 31:12]
endmodule
