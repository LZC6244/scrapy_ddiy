var c = "charCodeAt";

function murmur_hash2(e) {
    for (var t, n = e.length, i = n % 4, r = n - i, a = 1540483477, o = 0 ^ n, s = 0; s < r;)
        t = e[c](s++),
            t |= e[c](s++) << 8,
            t |= e[c](s++) << 16,
            t = multiply_uint32(t |= e[c](s++) << 24, a),
            t = multiply_uint32((t ^ t >>> 24) >>> 0, a),
            o = ((o = multiply_uint32(o, a)) ^ t) >>> 0;
    switch (i) {
        case 3:
            o = (o ^ e[c](s + 2) << 16) >>> 0;
        case 2:
            o = (o ^ e[c](s + 1) << 8) >>> 0;
        case 1:
            o = multiply_uint32(o ^= e[c](s), a)
    }
    return o = ((o = multiply_uint32(o = (o ^ o >>> 13) >>> 0, a)) ^ o >>> 15) >>> 0
}

function multiply_uint32(e, t) {
    var n = 65535 & e
        , i = 65535 & t;
    return (((e >> 16 & 65535) * i + n * (t >> 16 & 65535) & 65535) << 16 >>> 0) + n * i
}

process.argv.length > 2 ? screen_width = process.argv[2] : screen_width = '1360';
process.argv.length > 3 ? screen_height = process.argv[3] : screen_height = '768';
process.argv.length > 4 ? ua = process.argv[4] : ua = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36';
// 原始逻辑，可看情况进行替换，虽然实际上不校验 uuid ，但是不影响我们想扣出来啊 = =
// var args = [nav.appName || "", nav.appVersion || "", nav.platform || "", nav.userAgent, e.width + "x" + e.height, e.colorDepth, doc.cookie || ""].join("")
var args = 'Netscape5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36Win32' + ua + screen_width + 'x' + screen_height + '24';
var uuid = murmur_hash2(args).toString(36)
console.log(uuid)