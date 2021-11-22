const jsdom = require("jsdom");
const { JSDOM } = jsdom;
const dom = new JSDOM(`<!DOCTYPE html><p>Hello world</p>`);
window = dom.window;
document = window.document;
window.MediaSource='';
window.onpageshow='';
window.onhashchange='';
window.WebSocket='';
window.FileReader='';
window.postMessage='';
window.EventSource='';
window.Promise='';
Promise.setImmediate='';
Promise.indexedDB='';

performance=window.performance={"timeOrigin":Date.now(),"timing":{"connectStart":Date.now(),"navigationStart":Date.now(),"loadEventEnd":Date.now(),"domLoading":Date.now(),"secureConnectionStart":0,"fetchStart":Date.now(),"domContentLoadedEventStart":Date.now(),"responseStart":Date.now(),"responseEnd":Date.now(),"domInteractive":Date.now(),"domainLookupEnd":Date.now(),"redirectStart":0,"requestStart":Date.now(),"unloadEventEnd":0,"unloadEventStart":0,"domComplete":Date.now(),"domainLookupStart":Date.now(),"loadEventStart":Date.now(),"domContentLoadedEventEnd":Date.now(),"redirectEnd":0,"connectEnd":Date.now()},"navigation":{"type":0,"redirectCount":0}}
window.navigator=navigator={
    'userAgent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36',
    'vibrate':'',
    'getUserMedia':'',
    'serviceWorker':'',
    'geolocation':'',
}
window.history=history={
    'pushState':''
}

var _n,_ft;
!function(e) {
    var t = {};
    function n(r) {
        if (t[r])
            return t[r].exports;
        var i = t[r] = {
            i: r,
            l: !1,
            exports: {
                __esModule: undefined
            }
        };
        return e[r].call(i.exports, i, i.exports, n),
        i.l = !0,
        i.exports
    }
    _n=n;
}({
    _30:function(e, t, n) {
        "use strict";
        var r = n('_50')
          , i = n('_3').arrIndexOf
          , o = n('_64')
          , a = {}
          , s = !1;

        function c(e) {
            (a = window.TDC || {}).initReport || (setTimeout(function() {
                !function(e) {
                    if (!e)
                        return;
                    var t = window.scriptSuccess.tdc
                      , n = "number" == typeof t && t > 1;
                    1 !== t || d() || (g(e),
                    window.scriptRunFailure = {
                        tdc: 1
                    });
                    n && (d() || g(e),
                    h(e),
                    p(e, t));
                    f() && h(e)
                }(e)
            }, 1200),
            a.initReport = !0)
        }
        function u(e) {
            a.setData && a.setData(e)
        }
        function l() {
            return "function" == typeof a.getInfo && a.getInfo() || {}
        }
        function d() {
            return "undefined" != typeof window.TDC && "function" == typeof a.getData
        }
        function f() {
            return i(window.scriptErrors, "tdc") > -1
        }
        function p(e, t) {
            e && e.send(e.type.ERROR_TYPE_TDC_DOWNLOAD_RETRY_SUCCESS, t)
        }
        function h(e) {
            e && e.send(e.type.ERROR_TYPE_TDC_DOWNLOAD_FAIL)
        }
        function g(e) {
            e && e.send(e.type.ERROR_TYPE_TDC_RUN_FAIL)
        }
        e.exports = {
            link: c,
            setData: u,
            getData: function() {
                u({
                    ft: r()
                });
                var e = window.scriptErrors || []
                  , t = i(e, "tdc") > -1;
                var collect_value= "function" == typeof a.getData ? a.getData(!0) || "---" : t ? "------" : "---";
                return collect_value
            },
            clearData: function() {
                a.clearTc && a.clearTc()
            },
            getInfo: l,
            getToken: function() {
                return (l() || {}).tokenid || ""
            },
            getEks: function() {
                return (l() || {}).info || ""
            },
            getTlg: function() {
                return "undefined" == typeof window.TDC ? 0 : 1
            },
            checkTdcSuccess: d,
            retryLoad: function(e) {
                try {
                    if (window.TDC || s || !e)
                        return;
                    var t = window.captchaConfig.tdcHtdocsPath + "/" + window.captchaConfig.dcFileName;
                    s = !0,
                    o(t, function(t) {
                        s = !1,
                        t || setTimeout(function() {
                            c(),
                            f() && (function() {
                                for (var e = void 0, t = 0; t < window.scriptErrors.length; t++)
                                    if ("tdc" === window.scriptErrors[t]) {
                                        e = t;
                                        break
                                    }
                                "number" == typeof e && window.scriptErrors.splice(e, 1)
                            }(),
                            p(e, 4)),
                            d() ? window.scriptRunFailure && 1 === window.scriptRunFailure.tdc && function(e) {
                                e && e.send(e.type.ERROR_TYPE_TDC_RUN_RETRY_SUCCESS)
                            }(e) : window.scriptRunFailure = {
                                tdc: 1
                            }
                        }, 500)
                    })
                } catch (n) {}
            }
        }
    },
    _50:function(e, t, n) {
        "use strict";
        function r(e) {
            return document.createElement(e)
        }
        function i() {
            return "history"in window && "pushState"in history
        }
        !function() {
            var e = 0
        }();
        var o, a, s = (o = [],
        a = [],
        {
            add: function(e) {
                Array.prototype.push.apply(o, e)
            },
            get: function() {
                for (var e = 0; e < o.length; e++)
                    a[e] = o[e]();
                return a
            }
        });
        s.add([function() {
            return "matches"in r("div")
        }
        , function() {
            return "msMatchesSelector"in r("div")
        }
        , function() {
            return "webkitMatchesSelector"in r("div")
        }
        , function() {
            return !!(window.matchMedia && window.matchMedia("(min-width: 400px)") && window.matchMedia("(min-width: 400px)").matches)
        }
        , function() {
            return !!(window.CSS && CSS.supports && CSS.supports("display", "block"))
        }
        , function() {
            return !!document.createRange
        }
        , function() {
            return !!window.CustomEvent
        }
        , function() {
            return "scrollIntoView"in r("div")
        }
        , function() {
            return "getUserMedia"in window.navigator
        }
        , function() {
            return !!window.IntersectionObserver
        }
        , function() {
            return "ontouchstart"in r("div")
        }
        , function() {
            return "performance"in window
        }
        , function() {
            return !(!window.performance || !performance.timing)
        }
        , function() {
            return "MediaSource"in window
        }
        , function() {
            return "onpageshow"in window
        }
        , function() {
            return "onhashchange"in window
        }
        , function() {
            return !(!window.requestFileSystem && !window.webkitRequestFileSystem)
        }
        , function() {
            return !!window.screen.orientation
        }
        , function() {
            return "WebSocket"in window
        }
        , function() {
            return !1
        }
        , function() {
            return "FileReader"in window
        }
        , function() {
            return !!window.atob
        }
        , function() {
            return !(!window.JSON || !JSON.parse)
        }
        , function() {
            return "postMessage"in window
        }
        , function() {
            return "EventSource"in window
        }
        , function() {
            return "vibrate"in navigator
        }
        , function() {
            return "Promise"in window
        }
        , function() {
            return "setImmediate"in window
        }
        , function() {
            return "isInfinite"in Number
        }
        , function() {
            return "indexedDB"in window
        }
        , function() {
            return "Proxy"in window
        }
        , function() {
            return "serviceWorker"in navigator
        }
        , function() {
            return "postMessage"in window
        }
        , function() {
            return "Crypto"in window
        }
        , function() {
            return "openDatabase"in window
        }
        , function() {
            return "Notification"in window
        }
        , function() {
            return "currentScript"in document
        }
        , function() {
            var e = !1;
            return "number" == typeof window.screenX && ["webkit", "moz", "ms", "o", ""].forEach(function(t) {
                0 == e && "" + document[t + (t ? "H" : "h") + "idden"] != "undefined" && (e = !0)
            }),
            e
        }
        , function() {
            var e = !1;
            try {
                e = "localStorage"in g && "setItem"in localStorage
            } catch (t) {}
            return e
        }
        , function() {
            var e = !1;
            try {
                e = "sessionStorage"in g && "setItem"in sessionStorage
            } catch (t) {}
            return e
        }
        , function() {
            return "console"in window
        }
        , function() {
            return "requestAnimationFrame"in window
        }
        , function() {
            return "geolocation"in window.navigator
        }
        , function() {
            return "webkitSpeechRecognition"in window
        }
        , i, function() {
            return "TextEncoder"in window
        }
        , i, i, function() {
            var e = !1
              , t = "https://sv.aq.qq.com/";
            try {
                new URL("/",t).href == t && (e = !0)
            } catch (n) {}
            return e
        }
        , function() {
            try {
                "a".localeCompare("b", "i")
            } catch (e) {
                return "RangeError" === e.name
            }
            return !1
        }
        ]);
        for (var c = new function() {
            var e = [];
            this.set = function(t) {
                e[t] = !0
            }
            ,
            this.encode = function() {
                for (var t = [], n = 0; n < e.length; n++)
                    e[n] && (t[Math.floor(n / 6)] ^= 1 << n % 6);
                for (n = 0; n < t.length; n++)
                    t[n] = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-_".charAt(t[n] || 0);
                return t.join("")
            }
        }
        , u = s.get(), l = 0; l < u.length; l++)
            u[l] && c.set(l + 1);
        var d = c.encode();
        _ft=d;
        e.exports = function() {
            return d
        }
    },
    _3:function(e, t, n) {
        "use strict";
        function r() {
            return Math.floor(1e8 * Math.random())
        }
        var i = function(e) {
            e = e ? 1 : 0;
            try {
                return c(location.search.substr(e))
            } catch (r) {
                try {
                    var t = document.URL
                      , n = t.indexOf("?");
                    if (n >= 0)
                        return c(t.substr(n + e))
                } catch (r) {}
            }
            return ""
        }
          , o = {};
        !function() {
            for (var e = i(!0).split("&"), t = 0; t < e.length; t++) {
                var n = /(.*?)=(.*)/.exec(e[t]);
                n && (o[n[1]] = n[2])
            }
        }();
        var a = o.sess;
        function s(e) {
            o.sess = e
        }
        function c(e) {
            try {
                return o ? e.replace(a, o.sess) : e
            } catch (t) {
                return e
            }
        }
        window.captchaConfig && window.captchaConfig.sess && s(window.captchaConfig.sess);
        e.exports = {
            href: function() {
                try {
                    return location.href
                } catch (e) {
                    try {
                        return document.URL
                    } catch (e) {}
                }
                return ""
            },
            getQuery: function(e) {
                var t = i();
                return t = t ? t.replace(/&rand=[^&]+/, "") + "&rand=" + r() : "?rand=" + r(),
                e = e ? 1 : 0,
                t.substr(e)
            },
            queryParam: function(e) {
                return o[e]
            },
            queryMap: function() {
                return $.extend({}, o)
            },
            parse2rgb: function(e) {
                if (!e || "string" != typeof e)
                    return null;
                e = e.replace(/^#?([a-f\d])([a-f\d])([a-f\d])$/i, function(e, t, n, r) {
                    return t + t + n + n + r + r
                });
                var t = /^#?([a-f\d]{2})([a-f\d]{2})([a-f\d]{2})$/i.exec(e);
                return t ? {
                    r: parseInt(t[1], 16),
                    g: parseInt(t[2], 16),
                    b: parseInt(t[3], 16),
                    s: "#" + t[1] + t[2] + t[3]
                } : null
            },
            arrIndexOf: function(e, t) {
                if ("function" == typeof e.indexOf)
                    return e.indexOf(t);
                for (var n = 0; n < e.length; n++)
                    if (e[n] === t)
                        return n;
                return -1
            },
            updateSession: s,
            isLowIE: function() {
                var e = navigator.userAgent.toLowerCase()
                  , t = e.indexOf("msie") > -1
                  , n = void 0
                  , r = void 0;
                if (t) {
                    if (n = e.match(/msie ([\d.]+)/)[1],
                    r = t && document.documentMode,
                    n && n <= 8)
                        return !0;
                    if (r && r < 9)
                        return !0
                }
                return !1
            }
        }
    },
    _64:function(e, t) {
        function n(e, t) {
            e.onload = function() {
                this.onerror = this.onload = null,
                t(null, e)
            }
            ,
            e.onerror = function() {
                this.onerror = this.onload = null,
                t(new Error("Failed to load " + this.src), e)
            }
        }
        function r(e, t) {
            e.onreadystatechange = function() {
                "complete" != this.readyState && "loaded" != this.readyState || (this.onreadystatechange = null,
                t(null, e))
            }
        }
        e.exports = function(e, t, i) {
            var o = document.head || document.getElementsByTagName("head")[0]
              , a = document.createElement("script");
            "function" == typeof t && (i = t,
            t = {}),
            t = t || {},
            i = i || function() {}
            ,
            a.type = t.type || "text/javascript",
            a.charset = t.charset || "utf8",
            a.async = !("async"in t) || !!t.async,
            a.src = e,
            t.attrs && function(e, t) {
                for (var n in t)
                    e.setAttribute(n, t[n])
            }(a, t.attrs),
            t.text && (a.text = "" + t.text),
            ("onload"in a ? n : r)(a, i),
            a.onload || n(a, i),
            o.appendChild(a)
        }
    }
})
_n('_30');
console.log(_ft);
//补环境（没补完）
console.log('MediaSource' in window);