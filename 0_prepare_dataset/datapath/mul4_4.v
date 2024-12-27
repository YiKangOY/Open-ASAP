module PartialProd(
  input  [3:0] io_multiplicand,
  input  [3:0] io_multiplier,
  output [3:0] io_outs_0,
  output [3:0] io_outs_1,
  output [3:0] io_outs_2,
  output [3:0] io_outs_3
);
  wire  _T_6 = io_multiplicand[0] & io_multiplier[0]; // @[partialprod.scala 16:36]
  wire  _T_9 = io_multiplicand[1] & io_multiplier[0]; // @[partialprod.scala 16:36]
  wire  _T_12 = io_multiplicand[2] & io_multiplier[0]; // @[partialprod.scala 16:36]
  wire  _T_15 = io_multiplicand[3] & io_multiplier[0]; // @[partialprod.scala 16:36]
  wire [2:0] _T_17 = {_T_15,_T_12,_T_9}; // @[Cat.scala 29:58]
  wire  _T_25 = io_multiplicand[0] & io_multiplier[1]; // @[partialprod.scala 16:36]
  wire  _T_28 = io_multiplicand[1] & io_multiplier[1]; // @[partialprod.scala 16:36]
  wire  _T_31 = io_multiplicand[2] & io_multiplier[1]; // @[partialprod.scala 16:36]
  wire  _T_34 = io_multiplicand[3] & io_multiplier[1]; // @[partialprod.scala 16:36]
  wire [2:0] _T_36 = {_T_34,_T_31,_T_28}; // @[Cat.scala 29:58]
  wire  _T_44 = io_multiplicand[0] & io_multiplier[2]; // @[partialprod.scala 16:36]
  wire  _T_47 = io_multiplicand[1] & io_multiplier[2]; // @[partialprod.scala 16:36]
  wire  _T_50 = io_multiplicand[2] & io_multiplier[2]; // @[partialprod.scala 16:36]
  wire  _T_53 = io_multiplicand[3] & io_multiplier[2]; // @[partialprod.scala 16:36]
  wire [2:0] _T_55 = {_T_53,_T_50,_T_47}; // @[Cat.scala 29:58]
  wire  _T_63 = io_multiplicand[0] & io_multiplier[3]; // @[partialprod.scala 16:36]
  wire  _T_66 = io_multiplicand[1] & io_multiplier[3]; // @[partialprod.scala 16:36]
  wire  _T_69 = io_multiplicand[2] & io_multiplier[3]; // @[partialprod.scala 16:36]
  wire  _T_72 = io_multiplicand[3] & io_multiplier[3]; // @[partialprod.scala 16:36]
  wire [2:0] _T_74 = {_T_72,_T_69,_T_66}; // @[Cat.scala 29:58]
  assign io_outs_0 = {_T_17,_T_6}; // @[partialprod.scala 18:16]
  assign io_outs_1 = {_T_36,_T_25}; // @[partialprod.scala 18:16]
  assign io_outs_2 = {_T_55,_T_44}; // @[partialprod.scala 18:16]
  assign io_outs_3 = {_T_74,_T_63}; // @[partialprod.scala 18:16]
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
  input  [3:0] io_pp_0,
  input  [3:0] io_pp_1,
  input  [3:0] io_pp_2,
  input  [3:0] io_pp_3,
  output [7:0] io_augend,
  output [7:0] io_addend
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
  wire  HalfAdder_1_io_a; // @[wallace.scala 57:25]
  wire  HalfAdder_1_io_b; // @[wallace.scala 57:25]
  wire  HalfAdder_1_io_s; // @[wallace.scala 57:25]
  wire  HalfAdder_1_io_co; // @[wallace.scala 57:25]
  wire  FullAdder_1_io_a; // @[wallace.scala 67:25]
  wire  FullAdder_1_io_b; // @[wallace.scala 67:25]
  wire  FullAdder_1_io_ci; // @[wallace.scala 67:25]
  wire  FullAdder_1_io_s; // @[wallace.scala 67:25]
  wire  FullAdder_1_io_co; // @[wallace.scala 67:25]
  wire  HalfAdder_2_io_a; // @[wallace.scala 57:25]
  wire  HalfAdder_2_io_b; // @[wallace.scala 57:25]
  wire  HalfAdder_2_io_s; // @[wallace.scala 57:25]
  wire  HalfAdder_2_io_co; // @[wallace.scala 57:25]
  wire  FullAdder_2_io_a; // @[wallace.scala 67:25]
  wire  FullAdder_2_io_b; // @[wallace.scala 67:25]
  wire  FullAdder_2_io_ci; // @[wallace.scala 67:25]
  wire  FullAdder_2_io_s; // @[wallace.scala 67:25]
  wire  FullAdder_2_io_co; // @[wallace.scala 67:25]
  wire  HalfAdder_3_io_a; // @[wallace.scala 57:25]
  wire  HalfAdder_3_io_b; // @[wallace.scala 57:25]
  wire  HalfAdder_3_io_s; // @[wallace.scala 57:25]
  wire  HalfAdder_3_io_co; // @[wallace.scala 57:25]
  wire  HalfAdder_4_io_a; // @[wallace.scala 57:25]
  wire  HalfAdder_4_io_b; // @[wallace.scala 57:25]
  wire  HalfAdder_4_io_s; // @[wallace.scala 57:25]
  wire  HalfAdder_4_io_co; // @[wallace.scala 57:25]
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
  wire  res0_0 = io_pp_0[0]; // @[wallace.scala 34:43]
  wire  res0_1 = io_pp_0[1]; // @[wallace.scala 34:43]
  wire  res1_1 = io_pp_1[0]; // @[wallace.scala 34:43]
  wire  res0_6 = FullAdder_4_io_s; // @[wallace.scala 78:49 wallace.scala 83:13]
  wire  res0_5 = FullAdder_3_io_s; // @[wallace.scala 78:49 wallace.scala 83:13]
  wire  res0_4 = FullAdder_2_io_co; // @[wallace.scala 78:49 wallace.scala 83:13]
  wire  res0_3 = FullAdder_2_io_s; // @[wallace.scala 78:49 wallace.scala 83:13]
  wire  res0_2 = HalfAdder_3_io_s; // @[wallace.scala 78:49 wallace.scala 83:13]
  wire [6:0] _T_21 = {res0_6,res0_5,res0_4,res0_3,res0_2,res0_1,res0_0}; // @[Cat.scala 29:58]
  wire  res1_4 = HalfAdder_4_io_s; // @[wallace.scala 79:49 wallace.scala 87:15]
  wire  res1_3 = HalfAdder_3_io_co; // @[wallace.scala 79:49 wallace.scala 87:15]
  wire [6:0] _T_27 = {2'h0,res1_4,res1_3,1'h0,res1_1,1'h0}; // @[Cat.scala 29:58]
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
  HalfAdder HalfAdder_1 ( // @[wallace.scala 57:25]
    .io_a(HalfAdder_1_io_a),
    .io_b(HalfAdder_1_io_b),
    .io_s(HalfAdder_1_io_s),
    .io_co(HalfAdder_1_io_co)
  );
  FullAdder FullAdder_1 ( // @[wallace.scala 67:25]
    .io_a(FullAdder_1_io_a),
    .io_b(FullAdder_1_io_b),
    .io_ci(FullAdder_1_io_ci),
    .io_s(FullAdder_1_io_s),
    .io_co(FullAdder_1_io_co)
  );
  HalfAdder HalfAdder_2 ( // @[wallace.scala 57:25]
    .io_a(HalfAdder_2_io_a),
    .io_b(HalfAdder_2_io_b),
    .io_s(HalfAdder_2_io_s),
    .io_co(HalfAdder_2_io_co)
  );
  FullAdder FullAdder_2 ( // @[wallace.scala 67:25]
    .io_a(FullAdder_2_io_a),
    .io_b(FullAdder_2_io_b),
    .io_ci(FullAdder_2_io_ci),
    .io_s(FullAdder_2_io_s),
    .io_co(FullAdder_2_io_co)
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
  assign io_augend = {{1'd0}, _T_21}; // @[wallace.scala 90:13]
  assign io_addend = {{1'd0}, _T_27}; // @[wallace.scala 91:13]
  assign HalfAdder_io_a = io_pp_1[3]; // @[wallace.scala 59:18]
  assign HalfAdder_io_b = io_pp_2[2]; // @[wallace.scala 60:18]
  assign FullAdder_io_a = io_pp_0[3]; // @[wallace.scala 69:18]
  assign FullAdder_io_b = io_pp_1[2]; // @[wallace.scala 70:18]
  assign FullAdder_io_ci = io_pp_2[1]; // @[wallace.scala 71:19]
  assign HalfAdder_1_io_a = io_pp_0[2]; // @[wallace.scala 59:18]
  assign HalfAdder_1_io_b = io_pp_1[1]; // @[wallace.scala 60:18]
  assign FullAdder_1_io_a = io_pp_2[3]; // @[wallace.scala 69:18]
  assign FullAdder_1_io_b = io_pp_3[2]; // @[wallace.scala 70:18]
  assign FullAdder_1_io_ci = HalfAdder_io_co; // @[wallace.scala 71:19]
  assign HalfAdder_2_io_a = io_pp_3[1]; // @[wallace.scala 59:18]
  assign HalfAdder_2_io_b = HalfAdder_io_s; // @[wallace.scala 60:18]
  assign FullAdder_2_io_a = io_pp_3[0]; // @[wallace.scala 69:18]
  assign FullAdder_2_io_b = FullAdder_io_s; // @[wallace.scala 70:18]
  assign FullAdder_2_io_ci = HalfAdder_1_io_co; // @[wallace.scala 71:19]
  assign HalfAdder_3_io_a = io_pp_2[0]; // @[wallace.scala 59:18]
  assign HalfAdder_3_io_b = HalfAdder_1_io_s; // @[wallace.scala 60:18]
  assign HalfAdder_4_io_a = FullAdder_io_co; // @[wallace.scala 59:18]
  assign HalfAdder_4_io_b = HalfAdder_2_io_s; // @[wallace.scala 60:18]
  assign FullAdder_3_io_a = FullAdder_1_io_s; // @[wallace.scala 69:18]
  assign FullAdder_3_io_b = HalfAdder_2_io_co; // @[wallace.scala 70:18]
  assign FullAdder_3_io_ci = HalfAdder_4_io_co; // @[wallace.scala 71:19]
  assign FullAdder_4_io_a = io_pp_3[3]; // @[wallace.scala 69:18]
  assign FullAdder_4_io_b = FullAdder_1_io_co; // @[wallace.scala 70:18]
  assign FullAdder_4_io_ci = FullAdder_3_io_co; // @[wallace.scala 71:19]
endmodule
module MUL(
  input  [3:0] io_multiplicand,
  input  [3:0] io_multiplier,
  output [6:0] io_outs
);
  wire [3:0] pp_io_multiplicand; // @[mul.scala 26:18]
  wire [3:0] pp_io_multiplier; // @[mul.scala 26:18]
  wire [3:0] pp_io_outs_0; // @[mul.scala 26:18]
  wire [3:0] pp_io_outs_1; // @[mul.scala 26:18]
  wire [3:0] pp_io_outs_2; // @[mul.scala 26:18]
  wire [3:0] pp_io_outs_3; // @[mul.scala 26:18]
  wire [3:0] wt_io_pp_0; // @[mul.scala 30:18]
  wire [3:0] wt_io_pp_1; // @[mul.scala 30:18]
  wire [3:0] wt_io_pp_2; // @[mul.scala 30:18]
  wire [3:0] wt_io_pp_3; // @[mul.scala 30:18]
  wire [7:0] wt_io_augend; // @[mul.scala 30:18]
  wire [7:0] wt_io_addend; // @[mul.scala 30:18]
  wire [7:0] _T_1 = wt_io_augend + wt_io_addend; // @[mul.scala 37:27]
  PartialProd pp ( // @[mul.scala 26:18]
    .io_multiplicand(pp_io_multiplicand),
    .io_multiplier(pp_io_multiplier),
    .io_outs_0(pp_io_outs_0),
    .io_outs_1(pp_io_outs_1),
    .io_outs_2(pp_io_outs_2),
    .io_outs_3(pp_io_outs_3)
  );
  Wallace wt ( // @[mul.scala 30:18]
    .io_pp_0(wt_io_pp_0),
    .io_pp_1(wt_io_pp_1),
    .io_pp_2(wt_io_pp_2),
    .io_pp_3(wt_io_pp_3),
    .io_augend(wt_io_augend),
    .io_addend(wt_io_addend)
  );
  assign io_outs = _T_1[6:0]; // @[mul.scala 37:11]
  assign pp_io_multiplicand = io_multiplicand; // @[mul.scala 27:22]
  assign pp_io_multiplier = io_multiplier; // @[mul.scala 28:20]
  assign wt_io_pp_0 = pp_io_outs_0; // @[mul.scala 31:12]
  assign wt_io_pp_1 = pp_io_outs_1; // @[mul.scala 31:12]
  assign wt_io_pp_2 = pp_io_outs_2; // @[mul.scala 31:12]
  assign wt_io_pp_3 = pp_io_outs_3; // @[mul.scala 31:12]
endmodule
