module kn8 (in0, in1, in2, in3, in4, in5, in6, in7, in8, in9, in10, in11, in12, in13, in14, in15, out0, out1, out2, out3, out4, out5, out6, out7, out8, );
input in0;
input in1;
input in2;
input in3;
input in4;
input in5;
input in6;
input in7;
input in8;
input in9;
input in10;
input in11;
input in12;
input in13;
input in14;
input in15;
output out0;
output out1;
output out2;
output out3;
output out4;
output out5;
output out6;
output out7;
output out8;
wire var0;
wire var1;
wire var2;
wire var3;
wire var4;
wire var5;
wire var6;
wire var7;
wire var8;
wire var9;
wire var10;
wire var11;
wire var12;
wire var13;
wire var14;
wire var15;
wire var16;
wire var17;
wire var18;
wire var19;
wire var20;
wire var21;
wire var22;
wire var23;
wire var24;
wire var25;
wire var26;
wire var27;
wire var28;
wire var29;
wire var30;
wire var31;
wire var32;
wire var33;
wire var34;
wire var35;
wire var36;
wire var37;
wire var38;
wire var39;
wire var40;
wire var41;
wire var42;
wire var43;
wire var44;
wire var45;
wire var46;
wire var47;
wire var48;
wire var49;
wire var50;
wire var51;
wire var52;
wire var53;
wire var54;
wire var55;
wire var56;
wire var57;
wire var58;
wire var59;
wire var60;
assign var0 = in15 & in7;
assign var1 = in14 & in6;
assign var2 = in13 & in5;
assign var3 = in12 & in4;
assign var4 = in11 & in3;
assign var5 = in10 & in2;
assign var6 = in9 & in1;
assign var7 = in8 & in0;
assign var8 = in15 ^ in7;
assign var9 = in14 ^ in6;
assign var10 = in13 ^ in5;
assign var11 = in12 ^ in4;
assign var12 = in11 ^ in3;
assign var13 = in10 ^ in2;
assign var14 = in9 ^ in1;
assign var15 = in8 ^ in0;
assign var16 = var15 & var6;
assign var17 = var7 | var16;
assign var18 = var15 & var14;
assign var19 = var14 & var5;
assign var20 = var6 | var19;
assign var21 = var14 & var13;
assign var22 = var13 & var4;
assign var23 = var5 | var22;
assign var24 = var13 & var12;
assign var25 = var12 & var3;
assign var26 = var4 | var25;
assign var27 = var12 & var11;
assign var28 = var11 & var2;
assign var29 = var3 | var28;
assign var30 = var11 & var10;
assign var31 = var10 & var1;
assign var32 = var2 | var31;
assign var33 = var10 & var9;
assign var34 = var9 & var0;
assign var35 = var1 | var34;
assign var36 = var18 & var23;
assign var37 = var17 | var36;
assign var38 = var18 & var24;
assign var39 = var21 & var26;
assign var40 = var20 | var39;
assign var41 = var21 & var27;
assign var42 = var30 & var35;
assign var43 = var29 | var42;
assign var44 = var33 & var0;
assign var45 = var32 | var44;
assign var46 = var38 & var43;
assign var47 = var37 | var46;
assign var48 = var41 & var43;
assign var49 = var40 | var48;
assign var50 = var24 & var43;
assign var51 = var23 | var50;
assign var52 = var27 & var43;
assign var53 = var26 | var52;
assign var54 = var9 ^ var0;
assign var55 = var10 ^ var35;
assign var56 = var11 ^ var45;
assign var57 = var12 ^ var43;
assign var58 = var13 ^ var53;
assign var59 = var14 ^ var51;
assign var60 = var15 ^ var49;
assign out0 = var47;
assign out1 = var60;
assign out2 = var59;
assign out3 = var58;
assign out4 = var57;
assign out5 = var56;
assign out6 = var55;
assign out7 = var54;
assign out8 = var8;
endmodule 
