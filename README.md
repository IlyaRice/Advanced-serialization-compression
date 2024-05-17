# Serialization Compression

Welcome to my repository, where I've tackled a data compression challenge with a bit of an over-the-top approach. The task was to serialize and deserialize an array of integers into a compact string, aiming for at least 50% compression using only ASCII characters. While delta encoding alone provided excellent compression, I decided to add a custom Base91 encoding for extra fun and complexity.

This project isn't really about practicality — it's more about me taking a chance to practice and show off some coding tricks. Dive in to see how I've blended these techniques to achieve significant data reduction and appreciate the art of overengineering for learning's sake!


## Task Description

The task involves managing an array where the order of elements does not matter and contains up to 1000 random integers ranging from 1 to 300. The challenge is to write serialization and deserialization functions that convert this array into a compact string that only contains ASCII characters, aiming for at least a 50% compression ratio on average without utilizing a traditional compression algorithm.

## How to Run

1. Clone the repository:
    ```bash
    git clone https://github.com/IlyaRice/Advanced-serialization-compression.git
    cd Advanced-serialization-compression
    ```

2. Run the `main.py` file using Python:
    ```bash
    python main.py
    ```

## Test Output

Below are the results of several tests demonstrating the serialization and compression algorithms.

### Example Test: Random 100

<details>
<summary>Baseline serialization: (length: 363)</summary>
<pre><span>91;26;165;237;119;273;256;263;257;215;218;280;233;184;27;177;280;79;99;251;293;63;50;158;181;114;281;278;205;56;46;103;104;281;84;207;145;39;247;93;146;241;48;66;115;6;236;228;53;41;267;61;23;85;149;182;192;113;157;298;252;146;151;21;175;87;255;140;142;117;117;201;95;293;67;165;236;262;54;17;56;297;174;263;270;69;8;18;217;108;279;247;3;286;175;263;38;239;190;52</span></pre>
</details>

<details>
<summary>First step, delta serialization: (length: 108)</summary>
<pre><span>332913231~11125222112052312~105124224414511202~212310326170910241262942821~105301226041311510043351101057041</span></pre>
</details>

<details>
<summary>Second step, Base91 compression: (length: 70)</summary>
<pre><span>0123456789~~!v&Q&1SPh3Q]p&VEU?gLRsM%:5}dQhuoIb._Q[!mcTZJxSHf&]=7IKgEgj</span></pre>
</details>

Compression Ratio: 5.19

---

### Example Test: Random 100 One Digit

<details>
<summary>Baseline serialization: (length: 199)</summary>
<pre><span>9;7;8;1;1;2;6;9;3;8;8;4;9;1;5;4;3;5;7;6;7;1;4;6;5;1;2;9;2;9;5;8;1;1;5;5;5;6;8;7;1;7;5;6;6;8;7;9;1;8;3;5;3;1;4;7;5;9;2;5;9;6;4;8;9;7;2;7;1;8;7;2;9;9;3;6;1;7;1;8;1;2;2;1;9;4;9;9;4;8;8;8;2;7;8;2;1;2;8;2</span></pre>
</details>

<details>
<summary>First step, delta serialization: (length: 100)</summary>
<pre><span>1000000000000000100000000000100001000000100000000001000000010000000000010000000000000010000000000000</span></pre>
</details>

<details>
<summary>Second step, Base91 compression: (length: 19)</summary>
<pre><span>01~#YB60VNTJ?wR_|Db</span></pre>
</details>

Compression Ratio: 10.47

---

### Example Test: Random 100 Two Digit

<details>
<summary>Baseline serialization: (length: 299)</summary>
<pre><span>56;26;79;70;10;27;47;57;49;68;13;68;69;82;54;89;75;61;96;36;29;45;24;76;35;82;79;42;24;62;21;70;13;63;87;17;36;21;86;94;78;69;92;60;46;96;69;28;65;72;96;84;82;70;21;28;47;88;57;21;37;90;72;61;25;43;99;11;46;91;65;76;16;79;69;32;12;63;58;26;13;23;21;10;98;64;19;59;25;79;39;12;81;17;29;60;84;20;12;92</span></pre>
</details>

<details>
<summary>First step, delta serialization: (length: 102)</summary>
<pre><span>~10011001003102110000210101011010331012312101025210111010110110301000100203102100021002021111110220021</span></pre>
</details>

<details>
<summary>Second step, Base91 compression: (length: 48)</summary>
<pre><span>01235~~*lV}H#Ak#zK`crDXWhyNqX-kNYEHwtcgk{Z7AQHzO</span></pre>
</details>

Compression Ratio: 6.23

---

### Example Test: Random 100 Three Digit

<details>
<summary>Baseline serialization: (length: 399)</summary>
<pre><span>106;190;142;189;197;199;139;164;147;154;282;280;275;198;238;200;181;141;206;269;217;130;222;233;212;188;214;221;105;300;130;244;169;204;198;203;276;105;185;292;188;180;131;282;283;266;163;225;154;124;153;271;285;148;125;140;213;168;274;202;107;268;300;250;233;185;194;272;283;237;213;234;255;126;178;108;117;265;139;259;237;145;199;259;177;129;238;197;140;134;239;276;296;121;262;206;140;190;292;274</span></pre>
</details>

<details>
<summary>First step, delta serialization: (length: 104)</summary>
<pre><span>~~105011194311310135010011321510914181214030110430101012112061013413801301015654033121212011042010270440</span></pre>
</details>

<details>
<summary>Second step, Base91 compression: (length: 68)</summary>
<pre><span>0123456789~~$W*R/2.dfPoT<H^x//!}XZjC%O1do9@b9^QV%{`U#DlFR-X98M 7VE-D</span></pre>
</details>

Compression Ratio: 5.87

---

### Example Test: One Digit Sequential

<details>
<summary>Baseline serialization: (length: 17)</summary>
<pre><span>1;2;3;4;5;6;7;8;9</span></pre>
</details>

<details>
<summary>First step, delta serialization: (length: 9)</summary>
<pre><span>111111111</span></pre>
</details>

<details>
<summary>Second step, Base91 compression: (length: 5)</summary>
<pre><span>~1~&Z</span></pre>
</details>

Compression Ratio: 3.40

---

### Example Test: Two Digit Sequential

<details>
<summary>Baseline serialization: (length: 269)</summary>
<pre><span>10;11;12;13;14;15;16;17;18;19;20;21;22;23;24;25;26;27;28;29;30;31;32;33;34;35;36;37;38;39;40;41;42;43;44;45;46;47;48;49;50;51;52;53;54;55;56;57;58;59;60;61;62;63;64;65;66;67;68;69;70;71;72;73;74;75;76;



77;78;79;80;81;82;83;84;85;86;87;88;89;90;91;92;93;94;95;96;97;98;99</span></pre>
</details>

<details>
<summary>First step, delta serialization: (length: 92)</summary>
<pre><span>~1011111111111111111111111111111111111111111111111111111111111111111111111111111111111111111</span></pre>
</details>

<details>
<summary>Second step, Base91 compression: (length: 27)</summary>
<pre><span>01~~%|:xcTeC_.hKRlUv^UA/_jG</span></pre>
</details>

Compression Ratio: 9.96

---

### Example Test: Three Digit Sequential

<details>
<summary>Baseline serialization: (length: 803)</summary>
<pre><span>100;101;102;103;104;105;106;107;108;109;110;111;112;113;114;115;116;117;118;119;120;121;122;123;124;125;126;127;128;129;130;131;132;133;134;135;136;137;138;139;140;141;142;143;144;145;146;147;148;149;150;151;152;153;154;155;156;157;158;159;160;161;162;163;164;165;166;167;168;169;170;171;172;173;174;175;176;177;178;179;180;181;182;183;184;185;186;187;188;189;190;191;192;193;194;195;196;197;198;199;200;201;202;203;204;205;206;207;208;209;210;211;212;213;214;215;216;217;218;219;220;221;222;223;224;225;226;227;228;229;230;231;232;233;234;235;236;237;238;239;240;241;242;243;244;245;246;247;248;249;250;251;252;253;254;255;256;257;258;259;260;261;262;263;264;265;266;267;268;269;270;271;272;273;274;275;276;277;278;279;280;281;282;283;284;285;286;287;288;289;290;291;292;293;294;295;296;297;298;299;300</span></pre>
</details>

<details>
<summary>First step, delta serialization: (length: 205)</summary>
<pre><span>~~10011111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111</span></pre>
</details>

<details>
<summary>Second step, Base91 compression: (length: 54)</summary>
<pre><span>01~~_qe{-3l4G$3$&w5nJln{V4qXFd-}UWdVPBx-CA^t @o}?SQV#=</span></pre>
</details>

Compression Ratio: 14.87
