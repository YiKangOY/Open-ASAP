module bk32 (in0, in1, in2, in3, in4, in5, in6, in7, in8, in9, in10, in11, in12, in13, in14, in15, in16, in17, in18, in19, in20, in21, in22, in23, in24, in25, in26, in27, in28, in29, in30, in31, in32, in33, in34, in35, in36, in37, in38, in39, in40, in41, in42, in43, in44, in45, in46, in47, in48, in49, in50, in51, in52, in53, in54, in55, in56, in57, in58, in59, in60, in61, in62, in63, out0, out1, out2, out3, out4, out5, out6, out7, out8, out9, out10, out11, out12, out13, out14, out15, out16, out17, out18, out19, out20, out21, out22, out23, out24, out25, out26, out27, out28, out29, out30, out31, out32, );
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
input in16;
input in17;
input in18;
input in19;
input in20;
input in21;
input in22;
input in23;
input in24;
input in25;
input in26;
input in27;
input in28;
input in29;
input in30;
input in31;
input in32;
input in33;
input in34;
input in35;
input in36;
input in37;
input in38;
input in39;
input in40;
input in41;
input in42;
input in43;
input in44;
input in45;
input in46;
input in47;
input in48;
input in49;
input in50;
input in51;
input in52;
input in53;
input in54;
input in55;
input in56;
input in57;
input in58;
input in59;
input in60;
input in61;
input in62;
input in63;
output out0;
output out1;
output out2;
output out3;
output out4;
output out5;
output out6;
output out7;
output out8;
output out9;
output out10;
output out11;
output out12;
output out13;
output out14;
output out15;
output out16;
output out17;
output out18;
output out19;
output out20;
output out21;
output out22;
output out23;
output out24;
output out25;
output out26;
output out27;
output out28;
output out29;
output out30;
output out31;
output out32;
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
wire var61;
wire var62;
wire var63;
wire var64;
wire var65;
wire var66;
wire var67;
wire var68;
wire var69;
wire var70;
wire var71;
wire var72;
wire var73;
wire var74;
wire var75;
wire var76;
wire var77;
wire var78;
wire var79;
wire var80;
wire var81;
wire var82;
wire var83;
wire var84;
wire var85;
wire var86;
wire var87;
wire var88;
wire var89;
wire var90;
wire var91;
wire var92;
wire var93;
wire var94;
wire var95;
wire var96;
wire var97;
wire var98;
wire var99;
wire var100;
wire var101;
wire var102;
wire var103;
wire var104;
wire var105;
wire var106;
wire var107;
wire var108;
wire var109;
wire var110;
wire var111;
wire var112;
wire var113;
wire var114;
wire var115;
wire var116;
wire var117;
wire var118;
wire var119;
wire var120;
wire var121;
wire var122;
wire var123;
wire var124;
wire var125;
wire var126;
wire var127;
wire var128;
wire var129;
wire var130;
wire var131;
wire var132;
wire var133;
wire var134;
wire var135;
wire var136;
wire var137;
wire var138;
wire var139;
wire var140;
wire var141;
wire var142;
wire var143;
wire var144;
wire var145;
wire var146;
wire var147;
wire var148;
wire var149;
wire var150;
wire var151;
wire var152;
wire var153;
wire var154;
wire var155;
wire var156;
wire var157;
wire var158;
wire var159;
wire var160;
wire var161;
wire var162;
wire var163;
wire var164;
wire var165;
wire var166;
wire var167;
wire var168;
wire var169;
wire var170;
wire var171;
wire var172;
wire var173;
wire var174;
wire var175;
wire var176;
wire var177;
wire var178;
wire var179;
wire var180;
wire var181;
wire var182;
wire var183;
wire var184;
wire var185;
wire var186;
wire var187;
wire var188;
wire var189;
wire var190;
wire var191;
wire var192;
wire var193;
wire var194;
wire var195;
wire var196;
wire var197;
wire var198;
wire var199;
wire var200;
wire var201;
wire var202;
wire var203;
wire var204;
wire var205;
wire var206;
wire var207;
wire var208;
wire var209;
wire var210;
wire var211;
wire var212;
wire var213;
wire var214;
wire var215;
wire var216;
wire var217;
wire var218;
wire var219;
wire var220;
wire var221;
wire var222;
wire var223;
wire var224;
wire var225;
wire var226;
wire var227;
wire var228;
wire var229;
wire var230;
wire var231;
wire var232;
wire var233;
wire var234;
wire var235;
wire var236;
wire var237;
wire var238;
wire var239;
wire var240;
wire var241;
wire var242;
wire var243;
wire var244;
wire var245;
wire var246;
wire var247;
wire var248;
wire var249;
assign var0 = in63 & in31;
assign var1 = in62 & in30;
assign var2 = in61 & in29;
assign var3 = in60 & in28;
assign var4 = in59 & in27;
assign var5 = in58 & in26;
assign var6 = in57 & in25;
assign var7 = in56 & in24;
assign var8 = in55 & in23;
assign var9 = in54 & in22;
assign var10 = in53 & in21;
assign var11 = in52 & in20;
assign var12 = in51 & in19;
assign var13 = in50 & in18;
assign var14 = in49 & in17;
assign var15 = in48 & in16;
assign var16 = in47 & in15;
assign var17 = in46 & in14;
assign var18 = in45 & in13;
assign var19 = in44 & in12;
assign var20 = in43 & in11;
assign var21 = in42 & in10;
assign var22 = in41 & in9;
assign var23 = in40 & in8;
assign var24 = in39 & in7;
assign var25 = in38 & in6;
assign var26 = in37 & in5;
assign var27 = in36 & in4;
assign var28 = in35 & in3;
assign var29 = in34 & in2;
assign var30 = in33 & in1;
assign var31 = in32 & in0;
assign var32 = in63 ^ in31;
assign var33 = in62 ^ in30;
assign var34 = in61 ^ in29;
assign var35 = in60 ^ in28;
assign var36 = in59 ^ in27;
assign var37 = in58 ^ in26;
assign var38 = in57 ^ in25;
assign var39 = in56 ^ in24;
assign var40 = in55 ^ in23;
assign var41 = in54 ^ in22;
assign var42 = in53 ^ in21;
assign var43 = in52 ^ in20;
assign var44 = in51 ^ in19;
assign var45 = in50 ^ in18;
assign var46 = in49 ^ in17;
assign var47 = in48 ^ in16;
assign var48 = in47 ^ in15;
assign var49 = in46 ^ in14;
assign var50 = in45 ^ in13;
assign var51 = in44 ^ in12;
assign var52 = in43 ^ in11;
assign var53 = in42 ^ in10;
assign var54 = in41 ^ in9;
assign var55 = in40 ^ in8;
assign var56 = in39 ^ in7;
assign var57 = in38 ^ in6;
assign var58 = in37 ^ in5;
assign var59 = in36 ^ in4;
assign var60 = in35 ^ in3;
assign var61 = in34 ^ in2;
assign var62 = in33 ^ in1;
assign var63 = in32 ^ in0;
assign var64 = var63 & var30;
assign var65 = var31 | var64;
assign var66 = var63 & var62;
assign var67 = var61 & var28;
assign var68 = var29 | var67;
assign var69 = var61 & var60;
assign var70 = var59 & var26;
assign var71 = var27 | var70;
assign var72 = var59 & var58;
assign var73 = var57 & var24;
assign var74 = var25 | var73;
assign var75 = var57 & var56;
assign var76 = var55 & var22;
assign var77 = var23 | var76;
assign var78 = var55 & var54;
assign var79 = var53 & var20;
assign var80 = var21 | var79;
assign var81 = var53 & var52;
assign var82 = var51 & var18;
assign var83 = var19 | var82;
assign var84 = var51 & var50;
assign var85 = var49 & var16;
assign var86 = var17 | var85;
assign var87 = var49 & var48;
assign var88 = var47 & var14;
assign var89 = var15 | var88;
assign var90 = var47 & var46;
assign var91 = var45 & var12;
assign var92 = var13 | var91;
assign var93 = var45 & var44;
assign var94 = var43 & var10;
assign var95 = var11 | var94;
assign var96 = var43 & var42;
assign var97 = var41 & var8;
assign var98 = var9 | var97;
assign var99 = var41 & var40;
assign var100 = var39 & var6;
assign var101 = var7 | var100;
assign var102 = var39 & var38;
assign var103 = var37 & var4;
assign var104 = var5 | var103;
assign var105 = var37 & var36;
assign var106 = var35 & var2;
assign var107 = var3 | var106;
assign var108 = var35 & var34;
assign var109 = var33 & var0;
assign var110 = var1 | var109;
assign var111 = var66 & var68;
assign var112 = var65 | var111;
assign var113 = var66 & var69;
assign var114 = var72 & var74;
assign var115 = var71 | var114;
assign var116 = var72 & var75;
assign var117 = var78 & var80;
assign var118 = var77 | var117;
assign var119 = var78 & var81;
assign var120 = var84 & var86;
assign var121 = var83 | var120;
assign var122 = var84 & var87;
assign var123 = var90 & var92;
assign var124 = var89 | var123;
assign var125 = var90 & var93;
assign var126 = var96 & var98;
assign var127 = var95 | var126;
assign var128 = var96 & var99;
assign var129 = var102 & var104;
assign var130 = var101 | var129;
assign var131 = var102 & var105;
assign var132 = var108 & var110;
assign var133 = var107 | var132;
assign var134 = var113 & var115;
assign var135 = var112 | var134;
assign var136 = var113 & var116;
assign var137 = var119 & var121;
assign var138 = var118 | var137;
assign var139 = var119 & var122;
assign var140 = var125 & var127;
assign var141 = var124 | var140;
assign var142 = var125 & var128;
assign var143 = var131 & var133;
assign var144 = var130 | var143;
assign var145 = var136 & var138;
assign var146 = var135 | var145;
assign var147 = var136 & var139;
assign var148 = var142 & var144;
assign var149 = var141 | var148;
assign var150 = var147 & var149;
assign var151 = var146 | var150;
assign var152 = var139 & var149;
assign var153 = var138 | var152;
assign var154 = var116 & var153;
assign var155 = var115 | var154;
assign var156 = var122 & var149;
assign var157 = var121 | var156;
assign var158 = var128 & var144;
assign var159 = var127 | var158;
assign var160 = var69 & var155;
assign var161 = var68 | var160;
assign var162 = var75 & var153;
assign var163 = var74 | var162;
assign var164 = var81 & var157;
assign var165 = var80 | var164;
assign var166 = var87 & var149;
assign var167 = var86 | var166;
assign var168 = var93 & var159;
assign var169 = var92 | var168;
assign var170 = var99 & var144;
assign var171 = var98 | var170;
assign var172 = var105 & var133;
assign var173 = var104 | var172;
assign var174 = var62 & var161;
assign var175 = var30 | var174;
assign var176 = var62 & var69;
assign var177 = var60 & var155;
assign var178 = var28 | var177;
assign var179 = var60 & var116;
assign var180 = var58 & var163;
assign var181 = var26 | var180;
assign var182 = var58 & var75;
assign var183 = var56 & var153;
assign var184 = var24 | var183;
assign var185 = var56 & var139;
assign var186 = var54 & var165;
assign var187 = var22 | var186;
assign var188 = var54 & var81;
assign var189 = var52 & var157;
assign var190 = var20 | var189;
assign var191 = var52 & var122;
assign var192 = var50 & var167;
assign var193 = var18 | var192;
assign var194 = var50 & var87;
assign var195 = var48 & var149;
assign var196 = var16 | var195;
assign var197 = var48 & var142;
assign var198 = var46 & var169;
assign var199 = var14 | var198;
assign var200 = var46 & var93;
assign var201 = var44 & var159;
assign var202 = var12 | var201;
assign var203 = var44 & var128;
assign var204 = var42 & var171;
assign var205 = var10 | var204;
assign var206 = var42 & var99;
assign var207 = var40 & var144;
assign var208 = var8 | var207;
assign var209 = var40 & var131;
assign var210 = var38 & var173;
assign var211 = var6 | var210;
assign var212 = var38 & var105;
assign var213 = var36 & var133;
assign var214 = var4 | var213;
assign var215 = var36 & var108;
assign var216 = var34 & var110;
assign var217 = var2 | var216;
assign var218 = var34 & var33;
assign var219 = var33 ^ var0;
assign var220 = var34 ^ var110;
assign var221 = var35 ^ var217;
assign var222 = var36 ^ var133;
assign var223 = var37 ^ var214;
assign var224 = var38 ^ var173;
assign var225 = var39 ^ var211;
assign var226 = var40 ^ var144;
assign var227 = var41 ^ var208;
assign var228 = var42 ^ var171;
assign var229 = var43 ^ var205;
assign var230 = var44 ^ var159;
assign var231 = var45 ^ var202;
assign var232 = var46 ^ var169;
assign var233 = var47 ^ var199;
assign var234 = var48 ^ var149;
assign var235 = var49 ^ var196;
assign var236 = var50 ^ var167;
assign var237 = var51 ^ var193;
assign var238 = var52 ^ var157;
assign var239 = var53 ^ var190;
assign var240 = var54 ^ var165;
assign var241 = var55 ^ var187;
assign var242 = var56 ^ var153;
assign var243 = var57 ^ var184;
assign var244 = var58 ^ var163;
assign var245 = var59 ^ var181;
assign var246 = var60 ^ var155;
assign var247 = var61 ^ var178;
assign var248 = var62 ^ var161;
assign var249 = var63 ^ var175;
assign out0 = var151;
assign out1 = var249;
assign out2 = var248;
assign out3 = var247;
assign out4 = var246;
assign out5 = var245;
assign out6 = var244;
assign out7 = var243;
assign out8 = var242;
assign out9 = var241;
assign out10 = var240;
assign out11 = var239;
assign out12 = var238;
assign out13 = var237;
assign out14 = var236;
assign out15 = var235;
assign out16 = var234;
assign out17 = var233;
assign out18 = var232;
assign out19 = var231;
assign out20 = var230;
assign out21 = var229;
assign out22 = var228;
assign out23 = var227;
assign out24 = var226;
assign out25 = var225;
assign out26 = var224;
assign out27 = var223;
assign out28 = var222;
assign out29 = var221;
assign out30 = var220;
assign out31 = var219;
assign out32 = var32;
endmodule 
