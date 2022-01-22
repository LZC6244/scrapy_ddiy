/**
 * fd 替换
 * Copyright(C) 2008 - 2021, Ctrip.com All rights reserved. 
 * Date: 2021/12/27
 */
 !function() {
    "use strict";
    var w = window;
    if (w.JSON && w.JSON.parse && w.JSON.stringify && "undefined" != typeof localStorage && (!w.$_bf || !0 !== w.$_bf.loaded)) {
        var c = "charCodeAt"
          , win = window
          , doc = win.document
          , nav = win.navigator
          , uag = nav.userAgent
          , loc = doc.location
          , perf = "performance"
          , isCtripApp = -1 != uag.indexOf("CtripWireless")
          , VERSION = "4.1.7"
          , ENTERTIME = (new Date).getTime()
          , noop = function() {}
          , toString = Object.prototype.toString
          , hasOwn = Object.prototype.hasOwnProperty
          , token = /d{1,4}|m{1,2}|yy(?:yy)?/g
          , rg_url = /^(?:([^:\/?#]+):)?(?:\/\/()(?:(?:()(?:([^:@]*):?([^:@]*))?@)?([^:\/?#]*)(?::(\d*))?))?()(?:(()(?:(?:[^?#\/]*\/)*)()(?:[^?#]*))(?:\?([^#]*))?(?:#(.*))?)/
          , url_key = ["source", "scheme", "authority", "userInfo", "user", "pass", "host", "port", "relative", "path", "directory", "file", "query", "fragment"]
          , logs = []
          , isSupportStorage = function() {
            if (win.Storage && win.localStorage) {
                try {
                    localStorage.setItem("__store__test", "1"),
                    localStorage.getItem("__store__test"),
                    localStorage.removeItem("__store__test")
                } catch (e) {
                    return log(19),
                    !1
                }
                return !0
            }
            return log(18),
            !1
        }()
          , isfile = "https:" != loc.protocol && "http:" != loc.protocol
          , hn = loc.hostname
          , u_app_uat = "" != getItem("isPreProduction")
          , u_renv = /((test[a-z]?|dev|uat|ui|local)\.sh\.(ctrip|huixuan)travel)|(qa\.nt\.ctripcorp)|(qa\.nt\.tripcorp)|(qa\.nt\.tripqate)/i
          , cfg = {
            fp: makeFP(),
            domain: getTopDomain(),
            env: isCtripApp || isfile ? "hybrid" : "h5",
            protocol: isfile ? "https:" : "",
            surl: u_app_uat || u_renv.test(hn) || "127.0.0.1" == hn ? "//s.uat.qa.nt.ctripcorp.com/bf.gif" : "trip" === (win || {}).__ubt_isTrip__ ? "//ubt.tripcdn.com/bf.gif" : "//s.c-ctrip.com/bf.gif",
            purl: u_app_uat || u_renv.test(hn) || "127.0.0.1" == hn ? "//s.uat.qa.nt.ctripcorp.com/bee/collect" : "trip" === (win || {}).__ubt_isTrip__ ? "//ubt.tripcdn.com/bee/collect" : "//s.c-ctrip.com/bee/collect",
            delay: 0,
            debug: !1,
            rms: (Math.random(),
            !0),
            markting: !0,
            promiseCatch: !1,
            isfile: isfile,
            tcp: 1,
            readyWait: 61,
            appid: "",
            sendPvByPost: !1,
            clientid: "",
            commonDomain: !1
        };
        try {
            var cwx_info = getQuery("_cwxobj"), setGUIDCookie, _domain, _domain, cwx_info;
            cwx_info && (cwx_info = JSON.parse(cwx_info),
            setItem("CTRIP_UBT_INFO", JSON.stringify({
                appid: cwx_info.appid,
                cid: cwx_info.cid,
                personalRecommendSwitch: cwx_info.personalRecommendSwitch,
                localRecommendSwitch: cwx_info.localRecommendSwitch,
                marketSwitch: cwx_info.marketSwitch
            })),
            window.__nfesGlobalDatas || (setItem("GUID", cwx_info.cid || ""),
            setGUIDCookie = function(e, t, n, i, r, a) {
                try {
                    document.cookie = e + "=" + encodeURIComponent(t) + (n ? "; expires=" + n.toGMTString() : "") + (i ? "; path=" + i : "") + (r ? "; domain=" + r : "") + (a ? "; secure" : "")
                } catch (e) {}
            }
            ,
            _domain = cfg.domain,
            _domain = /\.ctrip\.com/.test(cfg.domain) ? ".ctrip.com" : /\.trip\.com/.test(cfg.domain) ? ".trip.com" : ".ctripcorp.com",
            setGUIDCookie("GUID", cwx_info.cid || "", new Date((new Date).getTime() + 93312e6), "/", _domain)))
        } catch (e) {}
        try {
            var cinfo = getItem("CTRIP_UBT_INFO");
            cinfo && (cinfo = JSON.parse(cinfo) || {},
            cfg.appid = cinfo.appid || "",
            cfg.clientid = cinfo.cid || "")
        } catch (e) {}
        cfg.appid = cfg.appid || window.mcdAppID;
        for (var WIN_SIZE = 16384, MIN_MATCH = 3, MAX_MATCH = 130, HASH_MASK = 1023, B64_CHARS = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-_", DECODE_TABLE = [], i$1 = 0; i$1 < 64; i$1++)
            DECODE_TABLE[B64_CHARS.charCodeAt(i$1)] = i$1;
        DataStore.prototype.get = function(e) {
            return this.v.hasOwnProperty(":" + e) ? this.v[":" + e] : ""
        }
        ,
        DataStore.prototype.set = function(e, t) {
            this.k.push(e),
            this.v[":" + e] = t
        }
        ,
        DataStore.prototype.map = function(e) {
            for (var t = 0, n = this.k.length; t < n; t++) {
                var i = this.k[t]
                  , r = this.get(i);
                r && e(r, i)
            }
        }
        ;
        var T = new DataStore
          , STORAGE_KEY = "CTRIP_UBT_M"
          , SESSION_MAX_LIEFTIME = 18e5
          , proto$1 = Meta.prototype;
        proto$1.init = function() {
            var e, t = parseJSON(getItem(STORAGE_KEY)) || {}, n = parseBf(getCookie("_bfa", "", !0)), i = getCookie("bu_be_vid");
            t.vid && n.vid ? e = n.vid == t.vid || 1 < Math.max(t.sid, n.sid) ? t.sid > n.sid ? t : n : t.pvid > n.pvid ? t : n : n.vid ? e = n : t.vid && (e = t);
            t = getTime();
            e ? (t - e.ts > SESSION_MAX_LIEFTIME ? (this.sid = e.sid + 1,
            this.isnewsid = 1) : (this.sid = e.sid,
            this.isnewsid = 0,
            this.ppi = e.pid,
            this.ppv = e.pvid),
            this.vid = i || e.vid,
            this.pvid = e.pvid + 1,
            this.create = e.create) : (this.vid = i || t + "." + uuid(),
            this.sid = 1,
            this.pvid = 1,
            this.isnewvid = 1,
            this.isnewsid = 1,
            this.create = t),
            this.update(this.ppi)
        }
        ,
        proto$1.update = function(e) {
            var t = getTime()
              , n = "1." + this.vid + ".1." + this.create + "." + t + "." + this.sid + "." + this.pvid + "." + e
              , t = {
                pid: e,
                vid: this.vid,
                sid: this.sid,
                sid_ts: t,
                pvid: this.pvid,
                ts: t,
                create: this.create
            };
            debugger;
            setCookie("_bfa", n, 63072e6, cfg.domain),
            setItem(STORAGE_KEY, JSON.stringify(t))
        }
        ;
        var u_rvar = /\$\{(\w+)\}/g
          , u_prev_url = ""
          , memeryQueue = {
            useraction: [],
            matrix: []
        };
        try {
            coDefault(),
            coRid(),
            coSearch()
        } catch (e) {
            log(3)
        }
        Pageview.count = 0;
        var proto = Pageview.prototype;
        proto.init = function(e, t) {
            if ("object" == typeof e)
                for (var n in e) {
                    var i, r;
                    hasOwn.call(e, n) && ("string" != (r = typeof (i = e[n])) && "number" != r || this.set(n, i))
                }
            isFunction(t) && this._fn_.push(t),
            this.checkSend()
        }
        ,
        proto.set = function(e, t) {
            switch (e) {
            case "page_id":
                this.setPid(t);
                break;
            case "orderid":
                this.orderid = t;
                break;
            case "duid":
                T.set("user:duid", t),
                T.set("user:login", 1);
                break;
            case "loginName":
                T.set("user:id", t),
                T.set("user:login", 1);
                break;
            case "url":
            case "refer":
                this[e] = ("" + t).substring(0, 2800);
                break;
            default:
                validValue(t) ? T.set(e, isString(t) ? t.substring(0, 50) : t) : log(10)
            }
            return 1
        }
        ,
        proto.setPid = function(e) {
            this.pid = toSafeNumber(e)
        }
        ,
        proto.getCommon = function() {
            var e = this.meta
              , t = cfg.appid || T.get("appid");
            return [this.pid + "", e.vid, e.sid, e.pvid, T.get("tid"), T.get("abtest"), T.get("mid"), VERSION, cfg.fp, "", t, "", "", T.get("user:id"), cfg.env, T.get("idc")]
        }
        ,
        proto.getMeta = function() {
            var e = this.meta;
            return {
                pid: this.pid,
                vid: e.vid,
                sid: e.sid,
                pvid: e.pvid,
                abtest: T.get("abtest"),
                pv: this.done,
                uid: T.get("user:duid")
            }
        }
        ,
        proto.getUinfo = function() {
            var e = this.meta
              , t = "";
            try {
                t += "cl=" + document.cookie.length,
                t += ",ckl=" + (document.cookie.match(/[^=]+=[^;]*;?/g) || []).length,
                t += ",lk=" + localStorage.length,
                t += ",log=" + logEcode()
            } catch (e) {
                log(9)
            }
            var n = new Array(43);
            return n[0] = 17,
            n[1] = e.ppi,
            n[2] = e.ppv,
            n[3] = this.url,
            n[4] = T.get("screen:width"),
            n[5] = T.get("screen:height"),
            n[6] = t,
            n[7] = lang(),
            n[8] = T.get("search:engine"),
            n[9] = T.get("search:keyword"),
            n[10] = this.refer,
            n[11] = T.get("abtest"),
            n[12] = e.isnewvid,
            n[13] = T.get("user:login"),
            n[14] = T.get("user:id") || getCookie("weduid"),
            n[15] = T.get("user:grade"),
            n[16] = T.get("user:corp_id"),
            n[17] = T.get("product:startcity"),
            n[18] = T.get("alliance:id"),
            n[19] = T.get("alliance:sid"),
            n[20] = T.get("alliance:ouid"),
            n[21] = this.orderid,
            n[22] = T.get("user:duid"),
            n[23] = T.get("zdata"),
            n[24] = T.get("callid"),
            n[25] = T.get("bid"),
            n[26] = T.get("clientid"),
            n[27] = T.get("sourceid"),
            n[28] = T.get("appinfo"),
            n[29] = cfg.env,
            n[30] = getDevicePix(),
            n[31] = e.isnewsid,
            n[32] = T.get("other"),
            n[33] = T.get("product:id"),
            n[34] = T.get("traffic:source"),
            n[35] = T.get("rid"),
            n[36] = T.get("buData"),
            n[37] = T.get("alliance:createtime"),
            n[40] = T.get("alliance:innerouid"),
            n[41] = T.get("alliance:innersid"),
            n[42] = T.get("alliance:pushcode"),
            n
        }
        ,
        proto.sampled = function(e, t) {
            return t || (t = e,
            e = 0),
            this.h >= e && this.h < t
        }
        ,
        proto.ready = function(e) {
            isFunction(e) && (this.done ? e(1, this) : this._fn_.push(e))
        }
        ,
        proto.co = function() {
            this.refer || (1 < Pageview.count && "" != u_prev_url ? (this.refer = u_prev_url,
            log(7)) : this.refer = T.get("refer")),
            this.url ? log(6) : this.url = T.get("url");
            try {
                this.orderid ? log(11) : this.orderid = coOrderID(),
                T.get("user:login") ? log(8) : coUser(),
                T.set("abtest", coAbtest()),
                coProduct(),
                coUnion(),
                coInfo(),
                coAppInfo()
            } catch (e) {
                log(4)
            }
        }
        ,
        proto.checkSend = function() {
            var c;
            this.done || this.pid < -1 || (this.done = !0,
            cfg.readyWait = 0,
            this.co(),
            send({
                t: "uinfo",
                c: (c = this).getCommon(),
                d: this.getUinfo(),
                p: 10,
                f: function(e) {
                    if (c.meta.update(c.pid),
                    1 == e) {
                        for (var t = c._store_, n = 0, i = t.length; n < i; n++) {
                            var r = t[n];
                            r.c || (r.c = c.getCommon()),
                            "useraction" == r.t || "matrix" == r.t ? c._q(r.t, r) : ("t" != r.t && "pr_t" != r.t || (r.d = c._tl(r.d)),
                            send(r, "object" == typeof r ? r._extend : {}))
                        }
                        setInterval(function() {
                            c._qsend("useraction", !0),
                            c._qsend("matrix", !0)
                        }, 2e3);
                        for (var a = 0, o = c._fn_.length; a < o; a++)
                            c._fn_[a](1, c);
                        u_prev_url = c.url
                    }
                }
            }))
        }
        ,
        proto._q = function(e, t) {
            memeryQueue[e] && memeryQueue[e].push(t),
            this._qsend(e)
        }
        ,
        proto._qsend = function(e, t) {
            var n = memeryQueue[e]
              , i = n.length;
            if (t && 0 < i || 4 < i) {
                for (var r, a = [], o = [], c = 0; c < i; c++)
                    r = n[c],
                    a.push(r.d),
                    r.f && o.push(r.f);
                send({
                    t: r.t,
                    c: r.c,
                    p: 6,
                    d: a,
                    f: function(e) {
                        for (var t = 0; t < o.length; t++)
                            o[t](e)
                    }
                }),
                memeryQueue[e].splice(0, i)
            }
        }
        ,
        proto._tl = function(e) {
            var n = {
                duid: T.get("user:duid"),
                page_id: this.pid + "",
                is_login: T.get("user:login")
            };
            return e.duid = n.duid,
            e.clientid = T.get("clientid"),
            e.env = cfg.env,
            e.val = e.val.replace(u_rvar, function(e, t) {
                return t in n ? n[t] : e
            }),
            e
        }
        ,
        proto.send = function(e, t, n, i, r, a) {
            n = {
                t: e,
                d: t,
                p: r || 6,
                f: n = !isFunction(n) ? noop : n
            };
            if ("error" == n.t || this.done) {
                if (n.c = this.getCommon(),
                "error" == n.t && i && (n.c[0] = i),
                "useraction" == n.t || "matrix" == n.t) {
                    if (n.p < 10 && "matrix" == n.t && isString(n.d.name) && -1 != n.d.name.indexOf("JS.Lizard"))
                        return this._q(n.t, n);
                    n.d = [t]
                }
                "t" != n.t && "pr_t" != n.t || (n.d = this._tl(n.d)),
                "object" == typeof n ? (n._extend = a,
                send(n, n._extend)) : send(n, {})
            } else
                "object" == typeof n && (n._extend = a),
                this._store_.push(n)
        }
        ;
        var pv = new Pageview
          , u_unload = 1;
        eval(function(e, t, n, i, r) {
            if (i = function(e) {
                return (e < 62 ? "" : i(parseInt(e / 62))) + (35 < (e %= 62) ? String.fromCharCode(e + 29) : e.toString(36))
            }
            ,
            !"".replace(/^/, String)) {
                for (; t--; )
                    r[i(t)] = n[t] || i(t);
                n = [function(e) {
                    return r[e]
                }
                ],
                i = function() {
                    return "\\w+"
                }
                ,
                t = 1
            }
            for (; t--; )
                n[t] && (e = e.replace(new RegExp("\\b" + i(t) + "\\b","g"), n[t]));
            return e
        }('49(3X(d,e,a,c,b,f){b=3X(a){3Y(a<e?"":b(45(a/e)))+(35<(a%=e)?42.44(a+29):a.47(36))};43(!"".41(/^/,42)){3Z(;a--;)f[b(a)]=c[a]||b(a);c=[3X(a){3Y f[a]}];b=3X(){3Y"\\\\w+"};a=1}3Z(;a--;)c[a]&&(d=d.41(46 4a("\\\\b"+b(a)+"\\\\b","g"),c[a]));3Y d}(\'o N=j(x){o q=j(l,e){o d={},t=d.R={},n=t.1t=j(){j b(){}C{E:j(a){b.1Z=i;o g=2l b;a&&g.1K(a);g.$2N=i;C g},F:j(){o a=i.E();a.W.2D(a,3n);C a},W:j(){},1K:j(a){G(o b 3m a)a.2J(b)&&(i[b]=a[b]);a.2J("X")&&(i.X=a.X)},O:j(){C i.$2N.E(i)}}}(),f=t.1i=n.E({W:j(b,a){b=i.H=b||[];i.I=a!=e?a:4*b.Q},X:j(b){C(b||r).13(i)},18:j(b){o a=i.H,g=b.H,c=i.I;b=b.I;i.2c();V(c%4)G(o m=0;m<b;m++)a[c+m>>>2]|=(g[m>>>2]>>>24-m%4*8&D)<<24-(c+m)%4*8;1m V(35<g.Q)G(m=0;m<b;m+=4)a[c+m>>>2]=g[m>>>2];1m a.1b.2D(a,g);i.I+=b;C i},2c:j(){o b=i.H,a=i.I;b[a>>>2]&=3b<<32-a%4*8;b.Q=l.2C(a/4)},O:j(){o b=n.O.S(i);b.H=i.H.1s(0);C b},26:j(b){G(o a=[],g=0;g<b;g+=4)a.1b(2P*l.26()|0);C f.F(a,b)}}),h=d.Y={},r=h.1I={13:j(b){o a=b.H;b=b.I;G(o g=[],c=0;c<b;c++){o m=a[c>>>2]>>>24-c%4*8&D;g.1b((m>>>4).X(16));g.1b((m&15).X(16))}C g.1R("")},M:j(b){G(o a=b.Q,g=[],c=0;c<a;c+=2)g[c>>>3]|=37(b.39(c,2),16)<<24-c%8*4;C f.F(g,a/2)}},p=h.3c={13:j(b){o a=b.H;b=b.I;G(o g=[],c=0;c<b;c++)g.1b(3e.3g(a[c>>>2]>>>24-c%4*8&D));C g.1R("")},M:j(b){G(o a=b.Q,g=[],c=0;c<a;c++)g[c>>>2]|=(b.3j(c)&D)<<24-c%4*8;C f.F(g,a)}},u=h.1Q={13:j(b){3p{C 3y(3J(p.13(b)))}3N(a){3O 3Q("3R 2X-8 2Y");}},M:j(b){C p.M(33(34(b)))}},w=t.2j=n.E({K:j(){i.1d=f.F();i.1D=0},1x:j(b){"1y"==1o b&&(b=u.M(b));i.1d.18(b);i.1D+=b.I},Z:j(b){o a=i.1d,g=a.H,c=a.I,m=i.T,A=c/(4*m);A=b?l.2C(A):l.3o((A|0)-i.2d,0);b=A*m;c=l.3t(4*b,c);V(b){G(o y=0;y<b;y+=m)i.1B(g,y);y=g.2O(0,b);a.I-=c}C f.F(y,c)},O:j(){o b=n.O.S(i);b.1d=i.1d.O();C b},2d:0});t.28=w.E({W:j(){i.K()},K:j(){w.K.S(i);i.1w()},1h:j(b){i.1x(b);i.Z();C i},L:j(b){b&&i.1x(b);i.1k();C i.1c},O:j(){o b=w.O.S(i);b.1c=i.1c.O();C b},T:16,1n:j(b){C j(a,g){C b.F(g).L(a)}},1Y:j(b){C j(a,g){C k.1N.F(b,g).L(a)}}});o k=d.1f={};C d}(2o);(j(){o l=q.R.1i;q.Y.1G={13:j(e){o d=e.H,l=e.I,n=i.2g;e.2c();e=[];G(o f=0;f<l;f+=3)G(o h=(d[f>>>2]>>>24-f%4*8&D)<<16|(d[f+1>>>2]>>>24-(f+1)%4*8&D)<<8|d[f+2>>>2]>>>24-(f+2)%4*8&D,r=0;4>r&&f+.3h*r<l;r++)e.1b(n.1v(h>>>6*(3-r)&3W));V(d=n.1v(1a))G(;e.Q%4;)e.1b(d);C e.1R("")},M:j(e){e=e.2k(/\\\\s/g,"");o d=e.Q,q=i.2g,n=q.1v(1a);n&&(n=e.2i(n),-1!=n&&(d=n));n=[];G(o f=0,h=0;h<d;h++)V(h%4){o r=q.2i(e.1v(h-1))<<h%4*2,p=q.2i(e.1v(h))>>>6-h%4*2;n[f>>>2]|=(r|p)<<24-f%4*8;f++}C l.F(n,f)},2g:"3u+/="}})();(j(l){j e(u,d,k,b,a,g,c){u=u+(d&k|~d&b)+a+c;C(u<<g|u>>>32-g)+d}j d(d,e,k,b,a,g,c){d=d+(e&b|k&~b)+a+c;C(d<<g|d>>>32-g)+e}j t(d,e,k,b,a,g,c){d=d+(e^k^b)+a+c;C(d<<g|d>>>32-g)+e}j n(d,e,k,b,a,g,c){d=d+(k^(e|~b))+a+c;C(d<<g|d>>>32-g)+e}o f=q.R,h=f.1i;f=f.28;o r=q.1f,p=[];(j(){G(o d=0;1a>d;d++)p[d]=2P*l.3w(l.3x(d+1))|0})();r=r.1S=f.E({1w:j(){i.1c=h.F([2r,2s,2w,2z])},1B:j(f,h){G(o k=0;16>k;k++){o b=h+k,a=f[b];f[b]=(a<<8|a>>>24)&29|(a<<24|a>>>8)&2b}b=i.1c.H;a=b[0];o g=b[1],c=b[2],m=b[3];G(k=0;1a>k;k+=4)16>k?(a=e(a,g,c,m,f[h+k],7,p[k]),m=e(m,a,g,c,f[h+k+1],12,p[k+1]),c=e(c,m,a,g,f[h+k+2],17,p[k+2]),g=e(g,c,m,a,f[h+k+3],22,p[k+3])):32>k?(a=d(a,g,c,m,f[h+(k+1)%16],5,p[k]),m=d(m,a,g,c,f[h+(k+6)%16],9,p[k+1]),c=d(c,m,a,g,f[h+(k+11)%16],14,p[k+2]),g=d(g,c,m,a,f[h+k%16],20,p[k+3])):38>k?(a=t(a,g,c,m,f[h+(3*k+5)%16],4,p[k]),m=t(m,a,g,c,f[h+(3*k+8)%16],11,p[k+1]),c=t(c,m,a,g,f[h+(3*k+11)%16],16,p[k+2]),g=t(g,c,m,a,f[h+(3*k+14)%16],23,p[k+3])):(a=n(a,g,c,m,f[h+3*k%16],6,p[k]),m=n(m,a,g,c,f[h+(3*k+7)%16],10,p[k+1]),c=n(c,m,a,g,f[h+(3*k+14)%16],15,p[k+2]),g=n(g,c,m,a,f[h+(3*k+5)%16],21,p[k+3]));b[0]=b[0]+a|0;b[1]=b[1]+g|0;b[2]=b[2]+c|0;b[3]=b[3]+m|0},1k:j(){o d=i.1d,f=d.H,k=8*i.1D,b=8*d.I;f[b>>>5]|=1q<<24-b%32;f[(b+1a>>>9<<4)+14]=(k<<8|k>>>24)&29|(k<<24|k>>>8)&2b;d.I=4*(f.Q+1);i.Z();d=i.1c.H;G(f=0;4>f;f++)k=d[f],d[f]=(k<<8|k>>>24)&29|(k<<24|k>>>8)&2b}});q.1S=f.1n(r);q.3a=f.1Y(r)})(2o);(j(){o l=q.R,e=l.1t,d=l.1i;l=q.1f;o t=l.25=e.E({J:e.E({P:4,1C:l.1S,1r:1}),W:j(d){i.J=i.J.E(d)},1e:j(e,f){o h=i.J,r=h.1C.F(),p=d.F(),l=p.H,n=h.P;G(h=h.1r;l.Q<n;){k&&r.1h(k);o k=r.1h(e).L(f);r.K();G(o b=1;b<h;b++)k=r.L(k),r.K();p.18(k)}p.I=4*n;C p}});q.25=j(d,f,e){C t.F(e).1e(d,f)}})();q.R.2y||j(l){o e=q,d=e.R,t=d.1t,n=d.1i,f=d.2j,h=e.Y.1G,r=e.1f.25,p=d.2y=f.E({J:t.E(),1E:j(c,a){C i.F(i.1F,c,a)},1z:j(c,a){C i.F(i.2E,c,a)},W:j(c,a,b){i.J=i.J.E(b);i.1O=c;i.2G=a;i.K()},K:j(){f.K.S(i);i.1w()},3v:j(c){i.1x(c);C i.Z()},L:j(c){c&&i.1x(c);C i.1k()},P:4,1P:4,1F:1,2E:2,1n:j(){C j(c){C{19:j(b,d,f){C("1y"==1o d?g:a).19(c,b,d,f)},1g:j(b,d,f){C("1y"==1o d?g:a).1g(c,b,d,f)}}}}()});d.3I=p.E({1k:j(){C i.Z(!0)},T:1});o u=e.1u={},w=d.3K=t.E({1E:j(c,a){C i.2S.F(c,a)},1z:j(c,a){C i.2T.F(c,a)},W:j(c,a){i.1T=c;i.1U=a}});u=u.3U=j(){j c(c,a,b){o m=i.1U;m?i.1U=l:m=i.1V;G(o d=0;d<b;d++)c[a+d]^=m[d]}o a=w.E();a.2S=a.E({1W:j(a,b){o m=i.1T,d=m.T;c.S(i,a,b,d);m.2m(a,b);i.1V=a.1s(b,b+d)}});a.2T=a.E({1W:j(a,b){o m=i.1T,d=m.T,g=a.1s(b,b+d);m.2n(a,b);c.S(i,a,b,d);i.1V=g}});C a}();o k=(e.1X={}).2Z={1X:j(c,a){a*=4;a-=c.I%a;G(o b=a<<24|a<<16|a<<8|a,d=[],m=0;m<a;m+=4)d.1b(b);a=n.F(d,a);c.18(a)},2p:j(c){c.I-=c.H[c.I-1>>>2]&D}};d.2q=p.E({J:p.J.E({1u:u,1H:k}),K:j(){p.K.S(i);o c=i.J,a=c.U;c=c.1u;V(i.1O==i.1F)o b=c.1E;1m b=c.1z,i.2d=1;i.2t=b.S(c,i,a&&a.H)},1B:j(c,a){i.2t.1W(c,a)},1k:j(){o c=i.J.1H;V(i.1O==i.1F){c.1X(i.1d,i.T);o a=i.Z(!0)}1m a=i.Z(!0),c.2p(a);C a},T:4});o b=d.2u=t.E({W:j(c){i.1K(c)},X:j(c){C(c||i.2v).13(i)}});u=(e.1p={}).2x={13:j(c){o a=c.1l;c=c.1J;a=(c?n.F([2A,2B]).18(c).18(a):a).X(h);C a.2k(/(.{1a})/g,"$1\\\\n")},M:j(c){c=h.M(c);o a=c.H;V(2A==a[0]&&2B==a[1]){o d=n.F(a.1s(2,4));a.2O(0,4);c.I-=16}C b.F({1l:c,1J:d})}};o a=d.3d=t.E({J:t.E({1p:u}),19:j(a,d,g,f){f=i.J.E(f);o c=a.1E(g,f);d=c.L(d);c=c.J;C b.F({1l:d,1j:g,U:c.U,3f:a,1u:c.1u,1H:c.1H,T:a.T,2v:f.1p})},1g:j(a,b,d,g){g=i.J.E(g);b=i.2a(b,g.1p);C a.1z(d,g).L(b.1l)},2a:j(a,b){C"1y"==1o a?b.M(a):a}});e=(e.1L={}).2x={1e:j(a,d,g,f){f||(f=n.26(8));a=r.F({P:d+g}).1e(a,f);g=n.F(a.H.1s(d),4*g);a.I=4*d;C b.F({1j:a,U:g,1J:f})}};o g=d.3i=a.E({J:a.J.E({1L:e}),19:j(c,b,d,g){g=i.J.E(g);d=g.1L.1e(d,c.P,c.1P);g.U=d.U;c=a.19.S(i,c,b,d.1j,g);c.1K(d);C c},1g:j(c,b,d,g){g=i.J.E(g);b=i.2a(b,g.1p);d=g.1L.1e(d,c.P,c.1P,b.1J);g.U=d.U;C a.1g.S(i,c,b,d.1j,g)}})}();(j(){o l=q.R.2q,e=q.1f,d=[],t=[],n=[],f=[],h=[],r=[],p=[],u=[],w=[],k=[];(j(){G(o a=[],b=0;2F>b;b++)a[b]=1q>b?b<<1:b<<1^3k;o c=0,m=0;G(b=0;2F>b;b++){o e=m^m<<1^m<<2^m<<3^m<<4;e=e>>>8^e&D^3l;d[c]=e;t[e]=c;o l=a[c],q=a[l],B=a[q],v=2H*a[e]^2I*e;n[c]=v<<24|v>>>8;f[c]=v<<16|v>>>16;h[c]=v<<8|v>>>24;r[c]=v;v=3q*B^3r*q^2H*l^2I*c;p[e]=v<<24|v>>>8;u[e]=v<<16|v>>>16;w[e]=v<<8|v>>>24;k[e]=v;c?(c=l^a[a[a[B^l]]],m^=a[a[m]]):c=m=1}})();o b=[0,1,2,4,8,16,32,1a,1q,27,3s];e=e.1M=l.E({1w:j(){o a=i.2G,g=a.H,c=a.I/4;a=4*((i.2K=c+6)+1);G(o f=i.2L=[],e=0;e<a;e++)V(e<c)f[e]=g[e];1m{o h=f[e-1];e%c?6<c&&4==e%c&&(h=d[h>>>24]<<24|d[h>>>16&D]<<16|d[h>>>8&D]<<8|d[h&D]):(h=h<<8|h>>>24,h=d[h>>>24]<<24|d[h>>>16&D]<<16|d[h>>>8&D]<<8|d[h&D],h^=b[e/c|0]<<24);f[e]=f[e-c]^h}g=i.2M=[];G(c=0;c<a;c++)e=a-c,h=c%4?f[e]:f[e-4],g[c]=4>c||4>=e?h:p[d[h>>>24]]^u[d[h>>>16&D]]^w[d[h>>>8&D]]^k[d[h&D]]},2m:j(a,b){i.2e(a,b,i.2L,n,f,h,r,d)},2n:j(a,b){o c=a[b+1];a[b+1]=a[b+3];a[b+3]=c;i.2e(a,b,i.2M,p,u,w,k,t);c=a[b+1];a[b+1]=a[b+3];a[b+3]=c},2e:j(a,b,c,d,f,e,h,k){G(o g=i.2K,m=a[b]^c[0],l=a[b+1]^c[1],p=a[b+2]^c[2],r=a[b+3]^c[3],n=4,q=1;q<g;q++){o t=d[m>>>24]^f[l>>>16&D]^e[p>>>8&D]^h[r&D]^c[n++],u=d[l>>>24]^f[p>>>16&D]^e[r>>>8&D]^h[m&D]^c[n++],w=d[p>>>24]^f[r>>>16&D]^e[m>>>8&D]^h[l&D]^c[n++];r=d[r>>>24]^f[m>>>16&D]^e[l>>>8&D]^h[p&D]^c[n++];m=t;l=u;p=w}t=(k[m>>>24]<<24|k[l>>>16&D]<<16|k[p>>>8&D]<<8|k[r&D])^c[n++];u=(k[l>>>24]<<24|k[p>>>16&D]<<16|k[r>>>8&D]<<8|k[m&D])^c[n++];w=(k[p>>>24]<<24|k[r>>>16&D]<<16|k[m>>>8&D]<<8|k[l&D])^c[n++];r=(k[r>>>24]<<24|k[m>>>16&D]<<16|k[l>>>8&D]<<8|k[p&D])^c[n++];a[b]=t;a[b+1]=u;a[b+2]=w;a[b+3]=r},P:8});q.1M=l.1n(e)})();(j(){o l=q.R,e=l.1i;l=l.28;o d=[],t=q.1f.2f=l.E({1w:j(){i.1c=e.F([2r,2s,2w,2z,3z])},1B:j(e,f){G(o h=i.1c.H,l=h[0],p=h[1],n=h[2],q=h[3],k=h[4],b=0;3A>b;b++){V(16>b)d[b]=e[f+b]|0;1m{o a=d[b-3]^d[b-8]^d[b-14]^d[b-16];d[b]=a<<1|a>>>31}a=(l<<5|l>>>27)+k+d[b];a=20>b?a+((p&n|~p&q)+3B):3C>b?a+((p^n^q)+3D):3E>b?a+((p&n|p&q|n&q)-3F):a+((p^n^q)-3G);k=q;q=n;n=p<<30|p>>>2;p=l;l=a}h[0]=h[0]+l|0;h[1]=h[1]+p|0;h[2]=h[2]+n|0;h[3]=h[3]+q|0;h[4]=h[4]+k|0},1k:j(){o d=i.1d,f=d.H,e=8*i.1D,l=8*d.I;f[l>>>5]|=1q<<24-l%32;f[(l+1a>>>9<<4)+15]=e;d.I=4*f.Q;i.Z()}});q.2f=l.1n(t);q.3H=l.1Y(t)})();(j(){o l=q.Y.1Q;q.1f.1N=q.R.1t.E({W:j(e,d){e=i.1A=e.F();"1y"==1o d&&(d=l.M(d));o q=e.T,n=4*q;d.I>n&&(d=e.L(d));e=i.2Q=d.O();d=i.2R=d.O();G(o f=e.H,h=d.H,r=0;r<q;r++)f[r]^=3L,h[r]^=3M;e.I=d.I=n;i.K()},K:j(){o e=i.1A;e.K();e.1h(i.2R)},1h:j(e){i.1A.1h(e);C i},L:j(e){o d=i.1A;e=d.L(e);d.K();C d.L(i.2Q.O().18(e))}})})();(j(){o l=q.R,e=l.1t,d=l.1i;l=q.1f;o t=l.1N,n=l.2h=e.E({J:e.E({P:4,1C:l.2f,1r:1}),W:j(d){i.J=i.J.E(d)},1e:j(f,e){o h=i.J;f=t.F(h.1C,f);o l=d.F(),n=d.F([1]),q=l.H,k=n.H,b=h.P;G(h=h.1r;q.Q<b;){o a=f.1h(e).L(n);f.K();G(o g=a.H,c=g.Q,m=a,x=1;x<h;x++){m=f.L(m);f.K();G(o y=m.H,z=0;z<c;z++)g[z]^=y[z]}l.18(a);k[0]++}l.I=4*b;C l}});q.2h=j(d,e,l){C n.F(l).1e(d,e)}})();C x.N=q}(3P);j 2U(){o x=j(q,l){i.P=q/32;i.2V=l;i.1j=N.2h("3S",N.Y.1I.M("3T"),{P:i.P,1r:i.2V})};x.1Z.19=j(q,l){C N.1M.19(l,i.1j,{U:N.Y.1I.M(q)}).1l.X(N.Y.1G)};x.1Z.1g=j(q,l){l=N.R.2u.F({1l:N.Y.1G.M(l)});C N.1M.1g(l,i.1j,{U:N.Y.1I.M(q)}).X(N.Y.1Q)};C x}o 2W=2U();N.3V=j(x,q){C(2l 2W(1q,8)).19("36",x)};\',62,4b,"                  4c 3X     4d              3Y 4e 4f 4g 3Z 4h 4i 4j 4k 4l 4m 4n 4o 4p 4q 4r 4s 4t 4u 43 4v 47 4w 4x    4y     4z 4A 64 4B 4C 4D 4E 4F 4G 4H 4I 4J 4K 4L 4M 4N 4O 4P 4Q 4R 4S 4T 4U 4V 4W 4X 4Y 4Z 50 51 52 53 55 56 57 58 59 5a 5b 5c 5d 5e 5f 5g 5h 5i 5j 5k 5l 5m 5n 5o 5p 5q      5r 5s  5t 5u 5v 5w 5x 5y 5z 5A 5B 5C 5D 5E 41 46 5F 5G 5H 5I 5J 5K 5L 5M 5N 5O 5P 5Q 5R 5S 5T 5U 5V 5W 5X 5Y 5Z 61 65 66 67 68 69 6a 6b 6c 6d 6e 6f 6g 6h 6i 6j 6k 6l 6m    6n 6o 6p 6q 45 48 6r 6s 6t 6u 6v 42 6w 44 75 6x 6y 6z 6A 6B 6C 6D 6E 6F 6G 54 6H 6I 6J 6K 6L 6M 6N 6O 6P 40 6Q 60 6R 6S 6T 6U 6V 6W 6X 6Y 6Z 70 71 72 73 74 76 77 78 63".79(" "),0,{}));', 444, "|||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||function|return|for||replace|String|if|fromCharCode|parseInt|new|toString||eval|RegExp|245|this|var|255|extend|create|words|sigBytes|cfg|reset|finalize|parse|__ubtAES|clone|keySize|length|lib|call|blockSize|iv|init|enc|_process|stringify|concat|encrypt|push|_hash|_data|compute|algo|decrypt|update|WordArray|key|_doFinalize|ciphertext|else|_createHelper|typeof|format|128|iterations|slice|Base|mode|charAt|_doReset|_append|string|createDecryptor|_hasher|_doProcessBlock|hasher|_nDataBytes||createEncryptor|_ENC_XFORM_MODE|Base64|padding|Hex|salt|mixIn|kdf|AES|HMAC|_xformMode|ivSize|Utf8|join|MD5|_cipher|_iv|_prevBlock|processBlock|pad|_createHmacHelper|prototype|EvpKDF|random|Hasher|16711935|_parse|4278255360|clamp|_minBufferSize|_doCryptBlock|SHA1|_map|PBKDF2|indexOf|BufferedBlockAlgorithm|encryptBlock|decryptBlock|Math|unpad|BlockCipher|1732584193|4023233417|_mode|CipherParams|formatter|2562383102|OpenSSL|Cipher|271733878|1398893684|1701076831|ceil|apply|_DEC_XFORM_MODE|256|_key||257||||16843008|hasOwnProperty|_nRounds|_keySchedule|_invKeySchedule|super|splice|4294967296|_oKey|_iKey|Encryptor|Decryptor|initAesUtil|iterationCount|AesUtil|UTF|data|Pkcs7|unescape|encodeURIComponent|65535|2860ec00048f095eb88fb9e3c75fb4dd|substr|HmacMD5|4294967295|Latin1|SerializableCipher|algorithm|PasswordBasedCipher|charCodeAt|283|99|in|arguments|max|try|16843009|65537|min|ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789|process|abs|sin|decodeURIComponent|3285377520|80|1518500249|1859775393|1894007588|899497514|HmacSHA1|StreamCipher|escape|BlockCipherMode|1549556828|909522486|catch|throw|window|Error|Malformed|fqloJepum3Wu8CoK||c1eabdba1ea2366aaf00e6ab1226c443|CBC|JSAES|split".split("|"), 0, {}));
        var timeHash = {}
          , api = {
            _config: function(e, t, n) {
                if (isObject(e)) {
                    for (var i = objectKeys(e), r = 0; r < i.length; r++) {
                        var a = i[r];
                        cfg[a] = e[a]
                    }
                    n = t
                } else
                    cfg[e] = t;
                cfg.debug && (cfg.surl = "//s.uat.qa.nt.ctripcorp.com/bf.gif"),
                n && n()
            },
            _set: function(e, t, n) {
                var i = "Value Error";
                validValue(t) && (i = pv.set(e, t)),
                n && n(i)
            },
            _getFullPV: function(e) {
                var t = pv.getMeta()
                  , t = t.vid + "." + t.sid + "." + t.pvid;
                return e && e(t) || t
            },
            _getStatus: function(t) {
                if (isFunction(t) && "undefined" != typeof CtripUBT && CtripUBT.getCurrentPageInfo)
                    return CtripUBT.getCurrentPageInfo(function(e) {
                        return t && t({
                            abtest: "",
                            pid: e.page,
                            ps: !1,
                            pv: !0,
                            pvid: e.pvid,
                            sid: e.sid,
                            vid: e.vid,
                            hybrid: e.hybrid
                        })
                    });
                var e = pv.getMeta();
                return t && t(e) || e
            },
            _getFP: function(e, t) {
                var n = "a" + __ubtAES.JSAES(cfg.fp);
                return e && e(t ? "" : cfg.fp, n, cfg.fp)
            },
            _getPageid: function(n) {
                pv.done ? n(!1, pv.pid) : pv.ready(function(e, t) {
                    n(!1, t.pid)
                })
            },
            _unload: function(e) {
                var t;
                (void 0 !== window.$ && window.$.bindFastClick || "object" == typeof Lizard) && 1 == u_unload ? u_unload = 0 : ("object" == typeof CtripBusiness && isFunction(CtripBusiness.app_send_ubt_log) && (t = pv.getMeta(),
                CtripBusiness.app_send_ubt_log({
                    page: t.pid,
                    vid: t.vid,
                    sid: t.sid,
                    pvid: t.pvid,
                    ts: +new Date
                })),
                pv.done || pv.init(e),
                createPV())
            },
            _asynRefresh: function(e, t) {
                if (e && e.buData) {
                    for (var n = objectKeys(e.buData), i = n.length, r = i < 3, a = 0; a < i; a++) {
                        var o = e.buData[n[a]];
                        ("string" != typeof o || 30 < o.length) && (r = !1)
                    }
                    r && T.set("buData", e.buData)
                }
                createPV(e, t)
            },
            _tracklog: function(e, t, n) {
                validName(e) && validValue(t) ? pv.send("t", {
                    key: e,
                    val: t,
                    v: 6
                }, n) : n && n(0)
            },
            _cTrace: function(e, t, n, i) {
                var r;
                i = i || {
                    method: "post"
                },
                validName(e) && validMap(transToString(t)) ? (r = {},
                r = isObject(t) ? t : {
                    data: t
                },
                pv.send("tiled_tl", {
                    key: e,
                    val: r,
                    v: 0
                }, n, null, null, i)) : n && n(0, {
                    status: 1,
                    message: "Invalid data"
                })
            },
            _trace: function(e, t, n, i) {
                var r;
                i = i || {
                    method: ""
                },
                validName(e) && validMap(transToString(t)) ? (r = {},
                r = isObject(t) ? t : {
                    data: t
                },
                pv.send("tiled_tl", {
                    key: e,
                    val: r,
                    v: 0
                }, n, null, null, i)) : n && n(0, {
                    status: 1,
                    message: "Invalid data"
                })
            },
            _devTrace: function(e, t, n, i) {
                var r;
                i = i || {
                    method: ""
                },
                validName(e) && validMap(transToString(t)) ? (r = {},
                r = isObject(t) ? t : {
                    data: t
                },
                pv.send("tiled_tl", {
                    isDev: !0,
                    key: e,
                    val: r,
                    v: 0
                }, n, null, null, i)) : n && n(0, {
                    status: 1,
                    message: "Invalid data"
                })
            },
            _multiTrace: function(e, t) {
                validMultiTrace(e) ? pv.send("multiTrace", e, t) : t && t(0, {
                    status: 1,
                    message: "Invalid data"
                })
            },
            _privateTrace: function(e, t, n) {
                validName(e) && validValue(t) ? pv.send("pr_t", {
                    key: e,
                    val: t,
                    v: 7
                }, n) : n && n(0)
            },
            _trackError: function(e, t) {
                if ("object" != typeof e)
                    return t(0);
                for (var n = ["version", "message", "line", "file", "category", "framework", "time", "repeat", "islogin", "name", "column"], i = [e.version || 7, "", 0, "", "", "", getTime() - ENTERTIME, 1, T.get("user:login"), "", 0], r = 1, a = n.length; r < a; r++) {
                    var o = n[r];
                    if (e[o]) {
                        var c = e[o] + "";
                        switch (o) {
                        case "message":
                        case "file":
                            c = scut(c, 500);
                            break;
                        case "category":
                        case "framework":
                        case "name":
                            c = scut(c, 100);
                            break;
                        default:
                            c = toSafeNumber(c)
                        }
                        i[r] = c
                    }
                }
                var s = "";
                e.stack && (s = isArray(e.stack) ? e.stack.join("") : String(e.stack)),
                i.push(s.replace(/(\/|file:).+(\/webapp_work_)/gi, "$2")),
                10 <= +e.version && (i.push(""),
                i.push(e.organizationId),
                i.push(e.appVer)),
                pv.send("error", i, t, e.page_id)
            },
            _trackUserBlock: function(e, t) {
                if ("object" != typeof e)
                    return t(0, "erro");
                var n = [];
                n[0] = 6,
                n[1] = T.get("user:login"),
                n[2] = scut(e.message, 300),
                n[3] = scut(e.value, 300),
                n[4] = scut(e.type, 50),
                n[5] = scut(e.dom, 100),
                n[6] = scut(e.form, 100),
                n[7] = toSafeNumber(e.count),
                pv.send("ub", n, t)
            },
            _trackMetric: function(e, t) {
                if (!e || "object" != typeof e)
                    return "Error Param";
                t = t || pv;
                var n = extend({
                    name: "",
                    tag: {},
                    value: 0,
                    ts: getTime(),
                    callback: noop,
                    timeout: !1,
                    metricMaxLen: 30,
                    sample: 100
                }, e)
                  , i = validTag(n.tag, n.name);
                if (!validName(n.name) || 1 != i || !validMetricValue(n.value, n.metricMaxLen))
                    return n.callback(i);
                t.send("matrix", {
                    name: n.name,
                    tags: n.tag,
                    value: n.value,
                    ts: n.ts
                }, n.callback, null, e.priority),
                n.timeout && setTimeout(function() {
                    n.callback(i)
                }, n.timeout || 50)
            },
            _trackMatrix: function(e, t, n, i, r, a) {
                this._trackMetric({
                    name: e,
                    tag: t,
                    value: n,
                    ts: i,
                    callback: r,
                    priority: a
                })
            },
            _time: function(e, t) {
                timeHash[e + ""] = {
                    value: getTime(),
                    opt: t || {},
                    pv: pv
                }
            },
            _timeEnd: function(e, t) {
                var n = timeHash[e + ""];
                if (n && n.value) {
                    var i = getTime() - n.value
                      , t = extend(n.opt, t || {});
                    if (t.name)
                        return t.value = i,
                        this._trackMetric(t, n.pv),
                        delete timeHash[e],
                        i
                }
            },
            _require: function(e, t) {
                "markting" == e && loadMarkting(t)
            }
        }
          , readyList = []
          , isReady = !1;
        checkReady();
        var start_point, start_touch = !1, moveing = !1, ERROR_TYPES_RE = /^(?:[Uu]ncaught (?:exception: )?)?(?:((?:Eval|Internal|Range|Reference|Syntax|Type|URI|)Error): )?(.*)$/, UNKNOWN_FUNCTION = "?", _slice = [].slice, TraceKit = {
            remoteFetching: !1,
            collectWindowErrors: !0,
            linesOfContext: 11,
            wrap: function(e) {
                return function() {
                    try {
                        return e.apply(this, arguments)
                    } catch (e) {
                        throw TraceKit.report(e),
                        e
                    }
                }
            }
        }, Re, Se, Te, Ue, Le, Me, Ne;
        TraceKit.report = (Le = [],
        Me = null,
        Ne = null,
        a4.subscribe = function(e) {
            !0 !== Se && (Re = window.onerror,
            window.onerror = Ve,
            Se = !0),
            !0 !== Ue && (Te = window.onunhandledrejection,
            window.onunhandledrejection = We,
            Ue = !0),
            Le.push(e)
        }
        ,
        a4.unsubscribe = function(e) {
            for (var t = Le.length - 1; 0 <= t; --t)
                Le[t] === e && Le.splice(t, 1);
            0 === Le.length && (Se && (window.onerror = Re,
            Se = !1),
            Ue && (window.onunhandledrejection = Te,
            Ue = !1))
        }
        ,
        a4),
        TraceKit.computeStackTrace = (P4.augmentStackTraceWithInitialElement = N4,
        P4.computeStackTraceFromStackProp = K4,
        P4.guessFunctionName = D4,
        P4.gatherContext = E4,
        P4.ofCaller = function(t) {
            t = 1 + (null == t ? 0 : +t);
            try {
                throw new Error
            } catch (e) {
                return P4(e, t + 1)
            }
        }
        ,
        P4.getSource = C4,
        P4),
        TraceKit.extendToAsynchronousCallbacks = function() {
            function e(e) {
                var n = window[e];
                window[e] = function() {
                    var e = _slice.call(arguments)
                      , t = e[0];
                    return isFunction(t) && (e[0] = TraceKit.wrap(t)),
                    n.apply ? n.apply(this, e) : n(e[0], e[1])
                }
            }
            e("setTimeout"),
            e("setInterval")
        }
        ;
        var rg_domain_key = /^(file|chrome|asset)|\.(baidu|ctrip|google|bdimg|xiecheng|amap|tieyou|c-ctrip|ctripcorp|hhtravel)\./
          , matchs = [{
            bu: "HTL",
            rg: /^(P_HOTEL|U_HOTEL|P_SEARCH|S_HOTEL|F_HOTEL|BNB|SALE_HOTEL|P_INN_).*/i
        }, {
            bu: "FLT",
            rg: /^(FLIGHT|FLTMX|FLT_|AllAir|MATRIX_FLITHT|matrix-FlightList).*/i
        }, {
            bu: "TRN",
            rg: /^(TRAIN|TRAININFO|DISTRIBUTE|BOOKINFO).*/i
        }, {
            bu: "BUS",
            rg: /^(BUS_|SHIP_|AIRPORTS_|SHIPLINE|YUECHE|TOUR_BUS).*/i
        }, {
            bu: "TOUR",
            rg: /^(P_DIYSHX|DIY_HOTEL|P_TAOCAN|P_DIYSHX|TOUR|VACATION|AROUND|U_ACTIVITY_DAYTOUR|DIYFHX|DIYFHXSDP|VTM|TOURVTM|TUAN_|YouXue_|DIY_CITY|DIY_XRS|I_DIYTOUR|F_DIYSHX|DIYSHX_).*/i
        }, {
            bu: "TTD",
            rg: /^(P_TICKET|U_TICKET|TTD_|P_ACTIVITY).*/i
        }, {
            bu: "FNC",
            rg: /^(F_LIPIN|F_FX).*/i
        }, {
            bu: "TLS",
            rg: /^(P_SHOPPING).*/i
        }, {
            bu: "LT",
            rg: /^(S_HHTravel).*/i
        }, {
            bu: "MKT",
            rg: /^(UNION|SiteType|SiteID|BidAdCount|DyAdIndex|AdData|DyAd).*/i
        }, {
            bu: "CAR",
            rg: /^(CAR_|ISD_|P_CAR_ISD).*/i
        }, {
            bu: "CRU",
            rg: /^(CRUISE_|S_CRUISE_).*/i
        }, {
            bu: "BMAP",
            rg: /^(BMap).*/i
        }, {
            bu: "AMAP",
            rg: /^(_AMap).*/i
        }, {
            bu: "GS",
            rg: /^(GS_|POINT_TO_POINT_PARAM|DESTINATIONCITYSTORE|DESTINATIONLISTSTORE).*/i
        }, {
            bu: "INSURANCE_INSURE",
            rg: /^(INSURANCE_INSURE).*/i
        }, {
            bu: "SE",
            rg: /^(THEMETRAVEL_SEACH_LIST).*/i
        }, {
            bu: "IGT",
            rg: /^(P_CAR_IGT|B_CARCH|P_CARCH).*/i
        }]
          , coFCPDone = !1;
        if (isArray(win.__bfi))
            for (var i = 0, l = win.__bfi.length; i < l; i++)
                _push(win.__bfi[i]);
        else
            win.__bfi = [];
        win.__bfi.push = _push,
        win.$_bf = extend(win.$_bf || {}, {
            version: VERSION,
            loaded: !0,
            _getFullPV: api._getFullPV,
            _getStatus: api._getStatus,
            tracklog: api._tracklog,
            trackError: api._trackError,
            devTrace: api._devTrace,
            trace: api._trace,
            cDevTrace: api._cDevTrace,
            cTrace: api._cTrace,
            multiTrace: api._multiTrace,
            privateTrace: api._privateTrace,
            asynRefresh: createPV
        }),
        performance$1(pv),
        userAction(),
        collectError(),
        pv.sampled(5) && hijack(pv),
        pv.sampled(93, 100) && pv.id % 10 == 1 && collectStoreSize(),
        isCtripApp || !pv.sampled(10) && -480 == timezone() || restiming(pv),
        "http:" != loc.protocol && "https:" != loc.protocol || setTimeout(function() {
            cfg.rms && loadRiskRMS();
            var e = getInputValue("bf_ubt_markting_off");
            cfg.markting = (!e || "false" == e) && cfg.markting,
            cfg.markting && loadMarkting()
        }, 30),
        cfg.promiseCatch && hookPromise(),
        ready(function(e) {
            log(2),
            pv.setPid(e),
            pv.checkSend()
        })
    }
    function murmur_hash(e, t) {
        for (var n, i, r = 3 & e.length, a = e.length - r, o = t || 31, s = 3432918353, u = 461845907, l = 0; l < a; )
            i = 255 & e[c](l) | (255 & e[c](++l)) << 8 | (255 & e[c](++l)) << 16 | (255 & e[c](++l)) << 24,
            ++l,
            o = 27492 + (65535 & (n = 5 * (65535 & (o = (o ^= i = (65535 & (i = (i = (65535 & i) * s + (((i >>> 16) * s & 65535) << 16) & 4294967295) << 15 | i >>> 17)) * u + (((i >>> 16) * u & 65535) << 16) & 4294967295) << 13 | o >>> 19)) + ((5 * (o >>> 16) & 65535) << 16) & 4294967295)) + ((58964 + (n >>> 16) & 65535) << 16);
        switch (i = 0,
        r) {
        case 3:
            i ^= (255 & e[c](l + 2)) << 16;
        case 2:
            i ^= (255 & e[c](l + 1)) << 8;
        case 1:
            o ^= i = (65535 & (i = (i = (65535 & (i ^= 255 & e[c](l))) * s + (((i >>> 16) * s & 65535) << 16) & 4294967295) << 15 | i >>> 17)) * u + (((i >>> 16) * u & 65535) << 16) & 4294967295
        }
        return o ^= e.length,
        o = 2246822507 * (65535 & (o ^= o >>> 16)) + ((2246822507 * (o >>> 16) & 65535) << 16) & 4294967295,
        o = 3266489909 * (65535 & (o ^= o >>> 13)) + ((3266489909 * (o >>> 16) & 65535) << 16) & 4294967295,
        (o ^= o >>> 16) >>> 0
    }
    function multiply_uint32(e, t) {
        var n = 65535 & e
          , i = 65535 & t;
        return (((e >> 16 & 65535) * i + n * (t >> 16 & 65535) & 65535) << 16 >>> 0) + n * i
    }
    function murmur_hash2(e) {
        for (var t, n = e.length, i = n % 4, r = n - i, a = 1540483477, o = 0 ^ n, s = 0; s < r; )
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
    function getById(e) {
        return doc.getElementById(e)
    }
    function getInputValue(e) {
        e = getById(e);
        return e && e.value || ""
    }
    function getQuery(e) {
        var n = ""
          , e = new RegExp("[?&]" + e + "=([^&]+)");
        return win.location.search.replace(e, function(e, t) {
            return n = t,
            e
        }),
        decodeURIComponent(n)
    }
    function lang() {
        return nav.language || nav.userLanguage || nav.browserLanguage || ""
    }
    function timezone() {
        return (new Date).getTimezoneOffset()
    }
    function screenInfo() {
        var e = win.screen || {}
          , t = "";
        return e && (t += e.width + "x" + e.height + "|" + e.colorDepth,
        e.deviceYDPI && (t += "|DPI" + e.deviceXDPI + "x" + e.deviceYDPI)),
        {
            w: e.width || 0,
            h: e.height || 0,
            c: e.colorDepth,
            fp: t
        }
    }
    function getDevicePix() {
        return win.devicePixelRatio ? +win.devicePixelRatio : 1
    }
    function getReferrer() {
        var e = "";
        try {
            e = doc.referrer
        } catch (e) {}
        if (!e && win.opener)
            try {
                e = win.opener.location.href
            } catch (e) {}
        return e
    }
    function osInfo() {
        var e = []
          , t = screenInfo();
        return win.maxConnectionsPerServer && e.push("maxcon" + (window.maxConnectionsPerServer || "0")),
        nav.hardwareConcurrency && e.push("hdcon" + nav.hardwareConcurrency),
        e.push("zone" + timezone()),
        e.push(t.fp),
        e.join("")
    }
    function agentInfo() {
        var e = [];
        if (nav.mimeTypes) {
            for (var t = nav.mimeTypes, n = t.length || 0, i = "", r = 0; r < n; r++) {
                var a = t[r];
                i += a.type + a.suffixes + a.description
            }
            e.push(i)
        }
        if (nav.plugins) {
            for (var o = nav.plugins, c = "pls", s = 0; s < o.length; s++) {
                var u = o[s];
                if (c += u.filename || u.name || s,
                30 < s)
                    break
            }
            e.push(c)
        }
        return e.push(nav.userAgent),
        e.push(lang()),
        e.push(nav.doNotTrack || "0"),
        e.push(nav.platform || "None"),
        e.join("")
    }
    function canvasInfo() {
        var e = doc.createElement("canvas");
        if (void 0 === e.getContext)
            return "";
        e.width = 600,
        e.height = 30,
        e.style.border = "1px solid #3a3a3a";
        var t = e.getContext("2d")
          , n = t.createLinearGradient(0, 0, 200, 0);
        return n.addColorStop(0, "rgb(200,0,0)"),
        n.addColorStop(.5, "rgb(0,200,0)"),
        n.addColorStop(1, "rgb(200,0,0)"),
        t.fillStyle = n,
        t.fillRect(0, 0, 200, 30),
        t.fillStyle = "#360",
        t.font = "13px _sans",
        t.textBaseLine = "top",
        t.fillText("English中文Հայերենا繁體輸入لعربيةҚазақша`~1!2@3#4$5%6^7&8*9(0)-_=+[{]}|;:',<.>/?", 5, 18),
        t.beginPath(),
        t.strokeStyle = "blue",
        t.lineWidth = 5,
        t.shadowOffsetX = 2,
        t.shadowOffsetY = 2,
        t.shadowColor = "rgb(85,85,85)",
        t.shadowBlur = 3,
        t.arc(500, 15, 10, 0, 2 * Math.PI, !0),
        t.stroke(),
        t.closePath(),
        e.toDataURL() + glinfo()
    }
    function glinfo() {
        var e = doc.createElement("canvas");
        if (void 0 === e.getContext)
            return "";
        var t = null
          , n = ["webgl", "experimental-webgl", "moz-webgl", "webkit-3d"];
        try {
            for (var i = 0; i < n.length && null === t && !(t = e.getContext(n[i], {
                width: 600,
                height: 300
            })); i++)
                ;
            return t.getParameter(t.RENDERER) + "," + t.getParameter(t.VERSION)
        } catch (e) {}
        return ""
    }
    function makeFP() {
        var e = [];
        return e.push(murmur_hash(osInfo()).toString(36)),
        e.push(murmur_hash(agentInfo()).toString(36)),
        e.push(murmur_hash(canvasInfo()).toString(36)),
        e.join("-")
    }
    function uuid() {
        var e = win.screen;
        return murmur_hash2([nav.appName || "", nav.appVersion || "", nav.platform || "", nav.userAgent, e.width + "x" + e.height, e.colorDepth, doc.cookie || ""].join("")).toString(36)
    }
    function getTopDomain() {
        for (var e, t = "_bfp=cookie", n = loc.hostname.split("."), i = n.length - 1; 0 <= i; i--)
            if (e = "." + n.slice(i).join("."),
            doc.cookie = t + ";domain=" + e + ";",
            -1 < doc.cookie.indexOf(t))
                return doc.cookie = t.split("=")[0] + "=;domain=" + e + ";expires=Thu, 01 Jan 1970 00:00:01 GMT;",
                e
    }
    function xhr(t, e, n) {
        var i = win.ActiveXObject ? new win.ActiveXObject("Microsoft.XMLHTTP") : new win.XMLHttpRequest;
        i.open("POST", t, !0),
        i.setRequestHeader("content-type", "application/json"),
        i.onreadystatechange = function() {
            if (4 === i.readyState) {
                var e = i.status;
                if (0 !== e && 200 !== e)
                    throw new Error("Could not load " + t);
                e = [i.responseText];
                n && n(e)
            }
        }
        ,
        i.send(JSON.stringify({
            d: e
        }))
    }
    function trim(e) {
        return e && e.replace(/^\s+|\s+$/, "")
    }
    function isNumeric(e) {
        return !isNaN(parseFloat(e))
    }
    function isString(e) {
        return "string" == typeof e
    }
    function isFunction(e) {
        return "[object Function]" == toString.call(e)
    }
    function isArray(e) {
        return "[object Array]" == toString.call(e)
    }
    function isObject(e) {
        return "[object Object]" == toString.call(e)
    }
    function toSafeNumber(e) {
        e = parseFloat(e);
        return isNaN(e) ? 0 : e
    }
    function objectKeys(e) {
        if (Object.keys)
            return Object.keys(e);
        var t, n = [];
        for (t in e)
            hasOwn.call(e, t) && n.push(t);
        return n
    }
    function getTime() {
        return (new Date).getTime()
    }
    function validValue(e) {
        var t = typeof e;
        return e && (isString(e) || "number" == t || "boolean" == t)
    }
    function encode(e) {
        return encodeURIComponent(e || "")
    }
    function decode(e) {
        return decodeURIComponent(e || "")
    }
    function extend() {
        var e, t, n, i = arguments[0] || {}, r = 1, a = arguments.length;
        for (a === r && (i = this,
        --r); r < a; r++)
            if (null != (n = arguments[r]))
                for (t in n)
                    hasOwn.call(n, t) && i !== (e = n[t]) && void 0 !== e && (i[t] = e);
        return i
    }
    function makeRandom() {
        return ("" + Math.random()).slice(-8)
    }
    function pad(e, t) {
        for (e = String(e),
        t = t || 2; e.length < t; )
            e = "0" + e;
        return e
    }
    function getDateVer(e) {
        e = e || "yyyymmdd";
        var t = new Date
          , n = t.getFullYear()
          , i = t.getMonth()
          , r = t.getDate()
          , a = {
            d: r,
            dd: pad(r, 2),
            m: i + 1,
            mm: pad(i + 1),
            yy: t.getYear(),
            yyyy: n
        };
        return e.replace(token, function(e) {
            return a[e] || e
        })
    }
    function parseHost(e) {
        if ("string" != typeof e)
            return "";
        for (var t = rg_url.exec(e), n = {}, i = 14; i--; )
            t[i] && (n[url_key[i]] = t[i]);
        return n
    }
    function parseQuery(e) {
        var t, n = {}, i = e.split("&");
        if (i && i.length)
            for (var r = 0, a = i.length; r < a; r++)
                1 < (t = i[r].split("=")).length && (n[t[0]] = t[1]);
        return n
    }
    function parseJSON(e) {
        try {
            return JSON.parse(e)
        } catch (e) {}
    }
    function log(e) {
        logs[e] = !0
    }
    function logEcode() {
        for (var e = [], t = 0, n = logs.length; t < n; t++)
            logs[t] && (e[Math.floor(t / 6)] ^= 1 << t % 6);
        for (t = 0; t < e.length; t++)
            e[t] = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-_".charAt(e[t] || 0);
        return e.join("") + "~"
    }
    function getCookie(e, t, n) {
        e = new RegExp("(^| )" + e + "=([^;]*)(;|$)"),
        e = doc.cookie.match(e);
        return e && 1 < e.length ? n ? decode(e[2]) : e[2] : t || ""
    }
    function setCookie(e, t, n, i, r) {
        r = r || "/";
        var a = ";domain=" + i
          , i = "";
        0 < n && (i = ";expires=" + new Date(getTime() + n).toUTCString()),
        doc.cookie = e + "=" + encode(t) + a + ";path=" + r + i
    }
    function getItem(e) {
        return isSupportStorage && localStorage.getItem(e) || ""
    }
    function setItem(e, t) {
        return isSupportStorage && (localStorage.setItem(e, t),
        1)
    }
    function gz(c) {
        var s = []
          , u = []
          , l = -1
          , d = 0
          , f = 0
          , n = 0
          , i = 0
          , t = [];
        h(19);
        for (var p = 0; p < c.length && f < c.length; p += WIN_SIZE)
            0 < p && (u = u.slice(WIN_SIZE)),
            function() {
                for (var e = g(p + 2 * WIN_SIZE, c.length), t = g(e, c.length - MIN_MATCH + 1); f < e; f++) {
                    var n = 0
                      , i = 0;
                    if (f < t) {
                        var r = function() {
                            for (var e = 0, t = f; t < f + MIN_MATCH; t++)
                                e *= 16777619,
                                e ^= c[t];
                            return e & HASH_MASK
                        }();
                        if (d <= f)
                            for (var a = s[r] - 1; n != MAX_MATCH && 0 <= a && f - WIN_SIZE <= a; ) {
                                var o = function(e) {
                                    var t, n, i = g(e + MAX_MATCH, f);
                                    for (t = e,
                                    n = f; t < i && n < c.length && c[t] == c[n]; t++,
                                    n++)
                                        ;
                                    return t - e
                                }(a);
                                MIN_MATCH <= o && n < o && (i = f - a - (n = o)),
                                a = u[a - p]
                            }
                        u[f - p] = s[r] - 1,
                        s[r] = f + 1
                    }
                    if (MIN_MATCH <= n) {
                        for (d = f + n,
                        -1 != l && (m(),
                        l = -1),
                        h(n - MIN_MATCH); 127 < i; )
                            h(255 & (127 & i | 128)),
                            i >>= 7;
                        h(i)
                    } else
                        d <= f && -1 == l && (l = f)
                }
            }();
        return -1 != l && m(),
        function() {
            2 == i ? (r(n << 4 & 63),
            65 == B64_CHARS.length && (r(64),
            r(64))) : 4 == i && (r(n << 2 & 63),
            65 == B64_CHARS.length && r(64));
            return t.join("")
        }();
        function g(e, t) {
            return Math.min(e, t)
        }
        function m() {
            for (var e = l; e < f; e += 127) {
                var t = g(127, f - e);
                h(255 & -t);
                for (var n = e; n < f && n < e + t; n++)
                    h(c[n])
            }
        }
        function h(e) {
            var t = n << 6 - i;
            r(63 & (t |= (n = 255 & e) >> (i += 2))),
            6 <= i && r(63 & n >> (i -= 6))
        }
        function r(e) {
            t.push(B64_CHARS.charAt(e))
        }
    }
    function compress(e) {
        if (!e)
            return "";
        for (var t = [], n = 0, i = (e = unescape(encodeURIComponent(e))).length; n < i; n++)
            t[n] = e.charCodeAt(n);
        return gz(t)
    }
    function DataStore() {
        this.k = [],
        this.v = {}
    }
    function getRuntimeEnv() {
        return "miniprogram" == win.__wxjs_environment ? "&ure=wx_mini_webview" : void 0 !== win.my && -1 < uag.indexOf("AlipayClient") ? "&ure=my_mini_webview" : ""
    }
    function prepareMultiTrace(e, t) {
        for (var n = [], i = 0, r = e.length; i < r; i++) {
            var a = e[i];
            a.key || a.name;
            var o = a.val || a.data
              , o = {
                clientid: T.get("clientid"),
                duid: T.get("user:duid"),
                key: a.name || a.key,
                val: isString(o) ? {
                    data: o
                } : o
            };
            a.isDev && (o["$.ubt.hermes.topic.classifier"] = "DebugCustom"),
            t && (o.v = 0),
            n.push(o)
        }
        return n
    }
    function sendByImg(e, t) {
        var n = new Image;
        n.referrerPolicy = "no-referrer",
        n.width = n.height = 1,
        n.onload = n.onerror = function() {
            n.onload = n.onerror = null,
            t(1)
        }
        ,
        n.onerror = function() {
            n.onload = n.onerror = null,
            t(0, {
                status: 4,
                message: "UNKNOWN"
            })
        }
        ;
        var i = cfg.surl;
        cfg.commonDomain && (i = "//ubt-sin.tripcdn.com/bf.gif"),
        n.src = "https:" + i + "?" + e + "&_mt=" + getTime().toString(36) + (+makeRandom()).toString(32) + getRuntimeEnv()
    }
    function sendByPost(e, t) {
        var n = cfg.purl;
        xhr("https:" + (n = cfg.commonDomain ? "//ubt-sin.tripcdn.com/bee/collect" : n), "f00" + (new Date).getTime() + "!m1Legacy!" + e + "&_mt=" + getTime().toString(36) + (+makeRandom()).toString(32) + getRuntimeEnv(), function(e) {
            t(1)
        })
    }
    function sendByHttp(e, t, n) {
        var i;
        switch (n = n || {},
        e.t) {
        case "t":
        case "pr_t":
            var r = e.d
              , a = {};
            a[e.t] = [7, r.key, r.val, r.duid, r.clientid, r.env],
            a = {
                c: e.c,
                d: a
            },
            i = "ac=g&d=" + encode(JSON.stringify(a)) + "&v=" + VERSION;
            break;
        case "tiled_tl":
            r = e.d,
            a = {
                type: "tiled_tl",
                common: e.c,
                data: prepareMultiTrace([e.d], !1)
            },
            i = "ac=ntl&d=" + compress(JSON.stringify(a)) + "&c=1&v=" + VERSION;
            break;
        case "multiTrace":
            a = {
                type: "tiled_tl",
                common: e.c,
                data: prepareMultiTrace(e.d, !1)
            },
            i = "ac=ntl&d=" + compress(JSON.stringify(a)) + "&c=1&v=" + VERSION;
            break;
        case "uinfo":
        case "error":
        case "ub":
        case "ps":
            (a = {
                c: e.c,
                d: {}
            }).d[e.t] = e.d,
            i = "ac=g&d=" + encode(JSON.stringify(a)) + "&v=" + VERSION;
            break;
        case "useraction":
        case "matrix":
            a = [[2, e.t], e.c, e.d],
            i = "ac=a&d=" + compress(JSON.stringify(a)) + "&c=1&v=" + VERSION;
            break;
        case "restiming":
            a = [[1, "ctrip"], {
                pid: e.c[0],
                vid: e.c[1],
                sid: e.c[2],
                pvid: e.c[3],
                ver: VERSION,
                ifr: 0
            }, [[["ubt", e.t, 1], e.d]]],
            i = "a=z&d=" + compress(JSON.stringify(a))
        }
        i ? ("post" === n.method ? sendByPost : sendByImg)(i + "&t=" + getTime(), t) : t(0, {
            status: 5,
            message: e.t + " not support!"
        })
    }
    function sendByTcp(e, t) {
        e.c[9] = uag;
        var n = {
            c: e.c,
            dataType: e.t,
            priority: e.p || 6,
            __ubtEmbedded: function(e) {
                try {
                    var t = new RegExp("(^|&)" + e + "=([^&]*)(&|$)","i")
                      , n = (window.location.hash || window.location.search).substr(1).match(t);
                    return null != n ? unescape(n[2]) : null
                } catch (e) {
                    return ""
                }
            }("__ubtEmbedded") ? 1 : ""
        };
        switch (e.t) {
        case "uinfo":
        case "error":
        case "ub":
        case "ps":
        case "t":
        case "pr_t":
        case "useraction":
        case "matrix":
            n.d = e.d;
            break;
        case "tiled_tl":
            n.d = prepareMultiTrace([e.d], !0);
            break;
        case "multiTrace":
            n.d = prepareMultiTrace(e.d, !0),
            n.dataType = "tiled_tl";
            break;
        default:
            return
        }
        n.d ? (CtripBusiness.app_track_UBT_JS_log("ubt_js_sdk", n),
        t(1)) : t(0, {
            status: 1,
            message: "Invalid data"
        })
    }
    function isTcpFn(e) {
        return isFunction(e) && 20 < e.toString().length
    }
    function isTcpReady() {
        return (cfg.tcp || isCtripApp) && "undefined" != typeof CtripBusiness && isTcpFn(CtripBusiness.app_track_UBT_JS_log)
    }
    function send(e, t) {
        var n = isFunction(e.f) ? e.f : noop;
        cfg.debug;
        try {
            isTcpReady() ? sendByTcp(e, n) : sendByHttp(e, n, t)
        } catch (e) {
            n(0, {
                status: 6,
                message: e && e.message || ""
            }),
            log(5)
        }
    }
    function parseBf(e) {
        var t = {
            ts: 0
        };
        return !e || (e = e.split(".")) && 6 < e.length && (t.pid = e[8] || 0,
        t.vid = e[1] + "." + e[2],
        t.sid = toSafeNumber(e[6]),
        t.pvid = toSafeNumber(e[7]),
        t.ts = toSafeNumber(e[5]),
        t.create = toSafeNumber(e[4])),
        t
    }
    function Meta() {
        this.ppi = 0,
        this.ppv = 0,
        this.isnewvid = 0,
        this.isnewsid = 0,
        this.init()
    }
    function coOrderID() {
        var e = ""
          , t = parseJSON(getItem("PAYMENT2_ORDER_DETAIL"));
        return t && t.value && (e = t.value.oid,
        log(13)),
        e || (e = getInputValue("bf_ubt_orderid"),
        log(12)),
        e
    }
    function coUser() {
        var e = ""
          , t = getCookie("login_uid")
          , n = getCookie("DUID")
          , i = getCookie("CtripUserInfo");
        i && (i = parseQuery(i),
        n = n || i.U,
        e = i.VipGrade),
        n || t || (i = parseJSON(getItem("USER"))) && i.value && (t = (i = i.value).LoginName || i.UserName,
        e = i.VipGrade,
        n = i.UserID),
        t && T.set("user:id", t),
        n && T.set("user:duid", n),
        T.set("user:grade", e),
        T.set("user:corp_id", getCookie("corpid")),
        (t || n) && T.set("user:login", 1)
    }
    function coDefault() {
        var e = doc.location
          , t = screenInfo();
        T.set("url", e.href),
        T.set("refer", getReferrer()),
        T.set("screen:width", t.w),
        T.set("screen:height", t.h);
        t = "";
        try {
            var n = document.documentElement
              , t = n.dataset && n.dataset.idc || n.getAttribute("data-idc") || "";
            T.set("idc", t.substring(0, 30))
        } catch (e) {}
    }
    function coSearch() {
        var e = getCookie("Session");
        e && (e = parseQuery(e),
        T.set("search:engine", e.SmartLinkCode),
        T.set("search:keyword", e.SmartLinkQuary))
    }
    function coProduct() {
        var e = getInputValue("bf_ubt_product");
        e && T.set("product:id", e.substring(0, 30));
        var e = getCookie("StartCity_Pkg");
        e && (e = parseQuery(e),
        T.set("product:startcity", e.PkgStartCity))
    }
    function coUnion() {
        var t, e = getCookie("Union");
        try {
            (t = e ? "string" == typeof e ? parseQuery(e) : {} : parseJSON(e = getItem("UNION")) || {}).exmktID && "string" == typeof t.exmktID && (t.exmktID = parseJSON(t.exmktID) || {}),
            (t = t || {}).exmktID = t.exmktID || {};
            var n = parseQuery((document.location.search.replace("?", "") || "").toLocaleLowerCase());
            t.exmktID.innersid = t.exmktID.innersid || n.innersid,
            t.exmktID.innerouid = t.exmktID.innerouid || n.innerouid,
            t.exmktID.pushcode = t.exmktID.pushcode || n.pushcode,
            t && (T.set("alliance:id", t.AllianceID || t.ALLIANCEID || ""),
            T.set("alliance:sid", t.SID || ""),
            T.set("alliance:ouid", t.OUID || ""),
            T.set("alliance:createtime", t.createtime || ""),
            T.set("alliance:innersid", t.exmktID.innersid),
            T.set("alliance:innerouid", t.exmktID.innerouid),
            T.set("alliance:pushcode", t.exmktID.pushcode))
        } catch (e) {
            t.exmktID = {}
        }
    }
    function coAbtest() {
        for (var e = getById("ab_testing_tracker"), t = [], n = ""; e; )
            n += e.value,
            t.push(e),
            e.removeAttribute("id"),
            e.removeAttribute("name"),
            e = getById("ab_testing_tracker"),
            n && ";" != n[n.length - 1] && (n += ";");
        for (var i = 0; i < t.length; i++)
            t[i].setAttribute("id", "ab_testing_tracker");
        var r = loc.hash;
        return r && -1 !== r.indexOf("abtest=") && (n += decode(r.replace(/.*(abtest=)/i, "").replace(/#.*/i, ""))),
        280 < n.length ? (log(14),
        n.substring(0, 280)) : n
    }
    function coAppInfo() {
        var e = ""
          , t = parseJSON(getItem("CINFO"));
        t && t.version && (e = JSON.stringify({
            version: t.internalVersion || "",
            ver: t.version,
            net: t.networkStatus || "None",
            platform: t.platform || ""
        })),
        T.set("clientid", cfg.clientid || getItem("GUID")),
        T.set("sourceid", getItem("SOURCEID")),
        T.set("appinfo", e)
    }
    function coInfo() {
        var e = "";
        "object" == typeof window.Lizard && Lizard.selfCollection && (e = Lizard.selfCollection || Lizard.version || ""),
        T.set("other", JSON.stringify({
            fef_name: T.get("framework:name"),
            fef_ver: T.get("framework:version"),
            lizard: e,
            rg: getCookie("_RSG", ""),
            lang: doc.documentElement.getAttribute("lang") || ""
        }))
    }
    function coRid() {
        var e = "RID-" + murmur_hash2(loc.pathname + loc.search);
        T.set("rid", getCookie(e))
    }
    function Pageview(e, t) {
        Pageview.count++,
        this._store_ = [],
        this._fn_ = [],
        this.pid = -4,
        this.done = !1,
        this.meta = new Meta,
        this.h = murmur_hash2(this.meta.vid) % 100,
        this.id = this.meta.pvid,
        this.orderid = "",
        this.url = "",
        this.refer = "",
        T.set("user:login", 0),
        this.init(e, t)
    }
    function createPV(e, t) {
        pv.done ? pv = new Pageview(e,t) : pv.init(e, t)
    }
    function load(t) {
        t = t || {};
        var n = !1
          , e = doc.createElement("script");
        e.type = "text/javascript",
        e.async = !0,
        e.setAttribute("crossorigin", "anonymous"),
        e.onload = e.onreadystatechange = function(e) {
            n || this.readyState && "loaded" !== this.readyState && "complete" !== this.readyState || (this.onload = this.onreadystatechange = null,
            n = !0,
            t.onload && t.onload(e))
        }
        ,
        e.src = t.url + (t.mask ? "?v=" + getDateVer(t.mask) : "");
        var i = doc.getElementsByTagName("script")[0];
        i.parentNode.insertBefore(e, i)
    }
    function loadRiskRMS() {
        load({
            mask: "yyyymmdd",
            url: "https://webresource.english.c-ctrip.com/resaresenglish/risk/ubtrms/latest/default/mrms.js"
        })
    }
    function loadMarkting(e) {
        "trip" === (win || {}).__ubt_isTrip__ || load({
            mask: "yyyymmdd",
            url: "https://webresource.c-ctrip.com/ResUnionOnline/R7/common/h5Redirect.js",
            onload: e
        })
    }
    function validTag(e, t) {
        if (!e)
            return 1;
        var n = objectKeys(e)
          , i = n.length;
        if ("http_request_perf" != t && "o_page_render_check" != t && 8 < i)
            return 8;
        for (var r = 0; r < i; r++) {
            var a = e[n[r]];
            switch (typeof a) {
            case "string":
                e[n[r]] = scut(a, 300);
                break;
            case "number":
            case "boolean":
                break;
            default:
                return 110
            }
        }
        return 1
    }
    function validMetricValue(e, t) {
        t = t || 30;
        if (isNumeric(e))
            return 1;
        if (isObject(e)) {
            var n = objectKeys(e)
              , i = n.length;
            if (t < i)
                return;
            for (var r = 0; r < i; r++)
                if (!validName(n[r]) || !isNumeric(e[n[r]]))
                    return;
            return 1
        }
    }
    function validName(e) {
        return e && (isString(e) || isNumeric(e))
    }
    function validMap(e) {
        for (var t = objectKeys(e), n = t.length, i = 0; i < n; i++) {
            var r = e[t[i]];
            if (!isString(r) && !isNumeric(r) && "boolean" != typeof r)
                return
        }
        return 1
    }
    function transToString(e) {
        for (var t = objectKeys(e), n = t.length, i = 0; i < n; i++) {
            var r = t[i];
            void 0 === e[r] ? e[r] = "" : "object" == typeof e[r] && (e[r] = JSON.stringify(e[r]))
        }
        return e
    }
    function validMultiTrace(e) {
        if (isArray(e)) {
            for (var t = 0, n = e.length; t < n; t++) {
                var i = e[t];
                if (!i.name || !i.data || !isString(i.data) && !validMap(transToString(i.data)))
                    return
            }
            return 1
        }
    }
    function scut(e, t) {
        return isString(e) && e.substring(0, t) || ""
    }
    function runReady(e) {
        for (var t = 0; t < readyList.length; t++)
            readyList[t](e)
    }
    function checkReady() {
        var e = trim(getInputValue("page_id"));
        "wait" == e ? log(1) : e && "0" != e ? (isReady = !0,
        runReady(e)) : "complete" == doc.readyState && (isReady = !0,
        runReady(0)),
        !isReady && 0 < --cfg.readyWait && setTimeout(checkReady, 500)
    }
    function ready(e) {
        1 == isReady ? e(getInputValue("page_id")) : readyList.push(e)
    }
    function getPSData() {
        for (var e = ["navigationStart", "redirectStart", "unloadEventStart", "unloadEventEnd", "redirectEnd", "fetchStart", "domainLookupStart", "domainLookupEnd", "connectStart", "connectEnd", "requestStart", "responseStart", "responseEnd", "domLoading", "domInteractive", "domContentLoadedEventStart", "domContentLoadedEventEnd", "domComplete", "loadEventStart", "loadEventEnd"], t = win[perf].timing, n = [6], i = 0; i < e.length; i++)
            n.push(t[e[i]]);
        return n.push(win[perf].navigation.type || 0),
        n.push(win[perf].navigation.redirectCount || 0),
        n
    }
    function performance$1(t) {
        if (win[perf] && win[perf].timing) {
            var n = 0;
            return function e() {
                win[perf].timing.loadEventEnd ? t.send("ps", getPSData()) : ++n < 300 && setTimeout(e, 1e3)
            }(),
            1
        }
    }
    function getTagIndex(e, t) {
        var n = 0;
        if ("DIV" == t && (e.attributes["page-url"] || e.getAttribute("page-url")))
            return "";
        if (e.parentNode)
            for (var i = e.parentNode.firstChild; i && i != e; )
                1 == i.nodeType && i.tagName == e.tagName && n++,
                i = i.nextSibling;
        return 0 < n ? "[" + ++n + "]" : ""
    }
    function getXpah(e) {
        for (var t, n, i = [], r = 0; e && 9 != e.nodeType; )
            1 == e.nodeType && (n = (e.nodeName || "").toUpperCase(),
            t = e.id || "",
            n = n + getTagIndex(e, n),
            t && -1 == t.indexOf("client_id_viewport") && (n += "[@id='" + t + "']"),
            (t = e.getAttribute("data-ubt-key")) && (n += "[@cid='" + t + "']"),
            i[r++] = n),
            e = e.parentNode;
        return 2 < i.length ? i.reverse().join("/") : ""
    }
    function triggerClick(e) {
        var t, n, i, r, a, o, c, s, u, l;
        e && e.target && (u = e.target,
        t = doc.documentElement,
        s = doc.body,
        u && 1 == u.nodeType && u.nodeName && u.getBoundingClientRect && (n = u.nodeName.toUpperCase(),
        i = u.getBoundingClientRect(),
        r = "",
        a = Math.max(t.scrollLeft, s.scrollLeft),
        l = Math.max(t.scrollTop, s.scrollTop),
        o = start_point.pageX || e.pageX || 0,
        e = start_point.pageY || e.pageY || 0,
        s = parseInt((t.clientWidth || s.clientWidth) / 2, 10),
        l = "SELECT" == n && e - i.top - l < 0 ? (r += "[@x='" + parseInt(o + i.left + a - s, 10) + "'][@y='" + parseInt(e + i.top, 10) + "']",
        c = o,
        e - l) : (r += "[@x='" + (o - s) + "'][@y='" + e + "']",
        c = parseInt(o - i.left - a, 10) || 0,
        parseInt(e - i.top - l, 10) || 0),
        0 <= c && 0 <= l && c <= screen.width + a && (r += "[@rx='" + c + "']",
        r += "[@ry='" + l + "']",
        (u = getXpah(u)) && pv.send("useraction", {
            action: "click",
            xpath: u + r,
            ts: +new Date
        }))))
    }
    function userAction() {
        var e = "ontouchstart"in win
          , t = e ? "touchmove" : "mousemove"
          , n = e ? "touchend" : "mouseup";
        doc.addEventListener(e ? "touchstart" : "mousedown", function(e) {
            start_point = e.touches && e.touches[0] || e,
            start_touch = !(moveing = !1)
        }, !0),
        doc.addEventListener(t, function(e) {
            var t, n;
            start_touch && (t = e.touches && e.touches[0] || e,
            e = n = 0,
            n = Math.abs(t.pageX - start_point.pageX),
            e = Math.abs(t.pageY - start_point.pageY),
            moveing = !(n < 6 || e < 6))
        }, !0),
        doc.addEventListener(n, function(e) {
            if (!moveing && start_touch)
                try {
                    triggerClick(e)
                } catch (e) {
                    log(15)
                }
            start_touch = !1,
            start_point = null
        }, !0)
    }
    function _isUndefined(e) {
        return void 0 === e
    }
    function Qe(e, t, n) {
        var i = null;
        if (!t || TraceKit.collectWindowErrors) {
            for (var r = 0, a = Le.length; r < a; r++)
                try {
                    Le[r](e, t, n)
                } catch (e) {
                    i = e
                }
            if (i)
                throw i
        }
    }
    function Ve(e, t, n, i, r) {
        var a;
        return Ne ? (TraceKit.computeStackTrace.augmentStackTraceWithInitialElement(Ne, t, n, e),
        _e()) : r ? Qe(TraceKit.computeStackTrace(r), !0, r) : (n = {
            url: t,
            line: n,
            column: i
        },
        "[object String]" !== {}.toString.call(i = e) || (e = e.match(ERROR_TYPES_RE)) && (a = e[1],
        i = e[2]),
        n.func = TraceKit.computeStackTrace.guessFunctionName(n.url, n.line),
        n.context = TraceKit.computeStackTrace.gatherContext(n.url, n.line),
        Qe({
            name: a,
            message: i,
            mode: "onerror",
            stack: [n]
        }, !0, null)),
        !!Re && Re.apply(this, arguments)
    }
    function We(e) {
        e && e.reason ? Qe(TraceKit.computeStackTrace(e.reason), !0, e.reason) : Qe({}, !0, "Uncaught (in promise) undefined")
    }
    function _e() {
        var e = Ne
          , t = Me;
        Me = Ne = null,
        Qe(e, !1, t)
    }
    function a4(e) {
        if (Ne) {
            if (Me === e)
                return;
            _e()
        }
        var t = TraceKit.computeStackTrace(e);
        throw Ne = t,
        Me = e,
        setTimeout(function() {
            Me === e && _e()
        }, t.incomplete ? 2e3 : 0),
        e
    }
    function C4() {
        return []
    }
    function D4() {
        return UNKNOWN_FUNCTION
    }
    function E4() {
        return null
    }
    function F4(e) {
        return e.replace(/[\-\[\]{}()*+?.,\\\^$|#]/g, "\\$&")
    }
    function G4(e) {
        return F4(e).replace("<", "(?:<|&lt;)").replace(">", "(?:>|&gt;)").replace("&", "(?:&|&amp;)").replace('"', '(?:"|&quot;)').replace(/\s+/g, "\\s+")
    }
    function H4(e, t) {
        for (var n, i, r = 0, a = t.length; r < a; ++r)
            if ((n = C4(t[r])).length && (n = n.join("\n"),
            i = e.exec(n)))
                return {
                    url: t[r],
                    line: n.substring(0, i.index).split("\n").length,
                    column: i.index - n.lastIndexOf("\n", i.index) - 1
                };
        return null
    }
    function I4(e, t, n) {
        var i, r = [], e = new RegExp("\\b" + F4(e) + "\\b");
        return --n < r.length && (i = e.exec(r[n])) ? i.index : null
    }
    function K4(e) {
        if (!e.stack)
            return null;
        for (var t, n, i = /^\s*at (.*?) ?\(((?:file|https?|blob|chrome-extension|native|eval|webpack|<anonymous>|\/).*?)(?::(\d+))?(?::(\d+))?\)?\s*$/i, r = /^\s*(.*?)(?:\((.*?)\))?(?:^|@)((?:file|https?|blob|chrome|webpack|resource|\[native).*?|[^@]*bundle)(?::(\d+))?(?::(\d+))?\s*$/i, a = /^\s*at (?:((?:\[object object\])?.+) )?\(?((?:file|ms-appx|https?|webpack|blob):.*?):(\d+)(?::(\d+))?\)?\s*$/i, o = /(\S+) line (\d+)(?: > eval line \d+)* > eval/i, c = /\((\S*)(?::(\d+))(?::(\d+))\)/, s = e.stack.split("\n"), u = [], l = /^(.*) is undefined$/.exec(e.message), d = 0, f = s.length; d < f; ++d) {
            if (n = i.exec(s[d])) {
                var p = n[2] && 0 === n[2].indexOf("native");
                n[2] && 0 === n[2].indexOf("eval") && (t = c.exec(n[2])) && (n[2] = t[1],
                n[3] = t[2],
                n[4] = t[3]),
                p = {
                    url: p ? null : n[2],
                    func: n[1] || UNKNOWN_FUNCTION,
                    args: p ? [n[2]] : [],
                    line: n[3] ? +n[3] : null,
                    column: n[4] ? +n[4] : null
                }
            } else if (n = a.exec(s[d]))
                p = {
                    url: n[2],
                    func: n[1] || UNKNOWN_FUNCTION,
                    args: [],
                    line: +n[3],
                    column: n[4] ? +n[4] : null
                };
            else {
                if (!(n = r.exec(s[d])))
                    continue;
                n[3] && -1 < n[3].indexOf(" > eval") && (t = o.exec(n[3])) ? (n[3] = t[1],
                n[4] = t[2],
                n[5] = null) : 0 !== d || n[5] || _isUndefined(e.columnNumber) || (u[0].column = e.columnNumber + 1),
                p = {
                    url: n[3],
                    func: n[1] || UNKNOWN_FUNCTION,
                    args: n[2] ? n[2].split(",") : [],
                    line: n[4] ? +n[4] : null,
                    column: n[5] ? +n[5] : null
                }
            }
            !p.func && p.line && (p.func = D4(p.url, p.line)),
            p.context = p.line ? E4(p.url, p.line) : null,
            u.push(p)
        }
        return u.length ? (u[0] && u[0].line && !u[0].column && l && (u[0].column = I4(l[1], u[0].url, u[0].line)),
        {
            mode: "stack",
            name: e.name,
            message: e.message,
            stack: u
        }) : null
    }
    function N4(e, t, n, i) {
        n = {
            url: t,
            line: n
        };
        if (n.url && n.line) {
            e.incomplete = !1,
            n.func || (n.func = D4(n.url, n.line)),
            n.context || (n.context = E4(n.url, n.line));
            i = / '([^']+)' /.exec(i);
            if (i && (n.column = I4(i[1], n.url, n.line)),
            0 < e.stack.length && e.stack[0].url === n.url) {
                if (e.stack[0].line === n.line)
                    return !1;
                if (!e.stack[0].line && e.stack[0].func === n.func)
                    return e.stack[0].line = n.line,
                    e.stack[0].context = n.context,
                    !1
            }
            return e.stack.unshift(n),
            e.partial = !0
        }
        return !(e.incomplete = !0)
    }
    function O4(e, t) {
        for (var n, i, r, a, o = /function\s+([_$a-zA-Z\xA0-\uFFFF][_$a-zA-Z0-9\xA0-\uFFFF]*)?\s*\(/i, c = [], s = {}, u = !1, l = O4.caller; l && !u; l = l.caller)
            if (l !== P4 && l !== TraceKit.report) {
                if (i = {
                    url: null,
                    func: UNKNOWN_FUNCTION,
                    args: [],
                    line: null,
                    column: null
                },
                l.name ? i.func = l.name : (n = o.exec(l.toString())) && (i.func = n[1]),
                void 0 === i.func)
                    try {
                        i.func = n.input.substring(0, n.input.indexOf("{"))
                    } catch (e) {}
                (r = function(e) {
                    if (!window || !window.document) {
                        for (var t, n, i, r = [window.location.href], a = window.document.getElementsByTagName("script"), o = "" + e, c = 0; c < a.length; ++c) {
                            var s = a[c];
                            s.src && r.push(s.src)
                        }
                        if (n = H4((t = /^function(?:\s+([\w$]+))?\s*\(([\w\s,]*)\)\s*\{\s*(\S[\s\S]*\S)\s*\}\s*$/.exec(o)) ? (e = t[1] ? "\\s+" + t[1] : "",
                        n = t[2].split(",").join("\\s*,\\s*"),
                        i = F4(t[3]).replace(/;$/, ";?"),
                        new RegExp("function" + e + "\\s*\\(\\s*" + n + "\\s*\\)\\s*{\\s*" + i + "\\s*}")) : new RegExp(F4(o).replace(/\s+/g, "\\s+")), r))
                            return n;
                        if (t = /^function on([\w$]+)\s*\(event\)\s*\{\s*(\S[\s\S]*\S)\s*\}\s*$/.exec(o)) {
                            o = t[1];
                            if (i = G4(t[2]),
                            n = H4(new RegExp("on" + o + "=[\\'\"]\\s*" + i + "\\s*[\\'\"]","i"), r[0]))
                                return n;
                            if (n = H4(new RegExp(i), r))
                                return n
                        }
                        return null
                    }
                }(l)) && (i.url = r.url,
                i.line = r.line,
                i.func === UNKNOWN_FUNCTION && (i.func = D4(i.url, i.line)),
                (a = / '([^']+)' /.exec(e.message || e.description)) && (i.column = I4(a[1], r.url, r.line))),
                s["" + l] ? u = !0 : s["" + l] = !0,
                c.push(i)
            }
        t && c.splice(0, t);
        t = {
            mode: "callers",
            name: e.name,
            message: e.message,
            stack: c
        };
        return N4(t, e.sourceURL || e.fileName, e.line || e.lineNumber, e.message || e.description),
        t
    }
    function P4(e, t) {
        var n = null;
        t = null == t ? 0 : +t;
        try {
            if (n = function(e) {
                var t = e.stacktrace;
                if (t) {
                    for (var n, i = / line (\d+).*script (?:in )?(\S+)(?:: in function (\S+))?$/i, r = / line (\d+), column (\d+)\s*(?:in (?:<anonymous function: ([^>]+)>|([^\)]+))\((.*)\))? in (.*):\s*$/i, a = t.split("\n"), o = [], c = 0; c < a.length; c += 2) {
                        var s = null;
                        if ((n = i.exec(a[c])) ? s = {
                            url: n[2],
                            line: +n[1],
                            column: null,
                            func: n[3],
                            args: []
                        } : (n = r.exec(a[c])) && (s = {
                            url: n[6],
                            line: +n[1],
                            column: +n[2],
                            func: n[3] || n[4],
                            args: n[5] ? n[5].split(",") : []
                        }),
                        s) {
                            if (!s.func && s.line && (s.func = D4(s.url, s.line)),
                            s.line)
                                try {
                                    s.context = E4(s.url, s.line)
                                } catch (e) {}
                            s.context || (s.context = [a[c + 1]]),
                            o.push(s)
                        }
                    }
                    return o.length ? {
                        mode: "stacktrace",
                        name: e.name,
                        message: e.message,
                        stack: o
                    } : null
                }
            }(e))
                return n
        } catch (e) {}
        try {
            if (n = K4(e))
                return n
        } catch (e) {}
        try {
            if (n = function(e) {
                var t = e.message.split("\n");
                if (t.length < 4)
                    return null;
                for (var n, i = /^\s*Line (\d+) of linked script ((?:file|https?|blob)\S+)(?:: in function (\S+))?\s*$/i, r = /^\s*Line (\d+) of inline#(\d+) script in ((?:file|https?|blob)\S+)(?:: in function (\S+))?\s*$/i, a = /^\s*Line (\d+) of function script\s*$/i, o = [], c = window && window.document && window.document.getElementsByTagName("script"), s = [], u = 0, l = c.length; u < l; u++) {
                    var d = c[u];
                    d && !d.src && s.push(d)
                }
                for (var f = 2; f < t.length; f += 2) {
                    var p, g, m, h, v = null;
                    (n = i.exec(t[f])) ? v = {
                        url: n[2],
                        func: n[3],
                        args: [],
                        line: +n[1],
                        column: null
                    } : (n = r.exec(t[f])) ? (v = {
                        url: n[3],
                        func: n[4],
                        args: [],
                        line: +n[1],
                        column: null
                    },
                    p = +n[1],
                    (g = s[n[2] - 1]) && (!(m = C4(v.url)) || 0 <= (h = (m = m.join("\n")).indexOf(g.innerText)) && (v.line = p + m.substring(0, h).split("\n").length))) : (n = a.exec(t[f])) && (v = {
                        url: h = window.location.href.replace(/#.*$/, ""),
                        func: "",
                        args: [],
                        line: (h = H4(new RegExp(G4(t[f + 1])), [h])) ? h.line : n[1],
                        column: null
                    }),
                    v && (v.func || (v.func = D4(v.url, v.line)),
                    E4(v.url, v.line),
                    v.context = [t[f + 1]],
                    o.push(v))
                }
                return o.length ? {
                    mode: "multiline",
                    name: e.name,
                    message: t[0],
                    stack: o
                } : null
            }(e))
                return n
        } catch (e) {}
        try {
            if (n = O4(e, t + 1))
                return n
        } catch (e) {}
        return {
            name: e.name,
            message: e.message,
            mode: "failed"
        }
    }
    function collectError() {
        var c;
        null === win.onerror && (c = {},
        TraceKit.report.subscribe(function(e, t, n) {
            try {
                var i, r, a, o = "err_" + murmur_hash2((a = isArray(e.stack) ? (i = e.stack[0] || {},
                r = e.stack.map(function(e) {
                    var t = "";
                    return e.url && (t += "(" + e.url,
                    e.line && (t += ":" + e.line,
                    e.column && (t += ":" + e.column)),
                    t += ")"),
                    e.func + " " + t
                }),
                {
                    message: e.message,
                    file: i.url,
                    line: i.line,
                    column: i.column,
                    category: e.name,
                    framework: "normal",
                    time: getTime() - ENTERTIME,
                    stack: r.join("\r\n"),
                    repeat: 1,
                    version: 10
                }) : {
                    message: n + "",
                    file: "",
                    line: null,
                    column: null,
                    category: "ThrowString",
                    framework: "normal",
                    time: getTime() - ENTERTIME,
                    stack: "",
                    repeat: 1,
                    version: 10
                }).message + a.file + a.line);
                c[o] || (c[o] = !0,
                api._trackError(a))
            } catch (e) {
                log(16)
            }
        }))
    }
    function getNetType() {
        return nav.connection && nav.connection.type || "unknown"
    }
    function collectUnsafeJS() {
        for (var e = [], t = getNetType(), n = doc.scripts, i = n.length, r = 0; r < i; r++) {
            var a = n[r];
            a.src && (rg_domain_key.test(a.src) || e.push({
                name: "ubt.hijack",
                tag: {
                    type: "script",
                    url: a.src,
                    net: t
                },
                value: 1,
                ts: getTime()
            }))
        }
        return e
    }
    function hijack(e) {
        var t, n = collectUnsafeJS();
        win.top !== win && 0 < win.length && win.top.location.href && (t = win.top.location.href || "",
        rg_domain_key.test(t) || n.push({
            name: "ubt.hijack",
            tag: {
                type: "iframe",
                url: t,
                net: getNetType()
            },
            value: 1,
            ts: getTime()
        })),
        n.length && e.send("matrix", n)
    }
    function sizeOf(e) {
        if (!e)
            return 0;
        for (var t = 0, n = 0, i = (e += "").length; n < i; n++)
            t += e.charCodeAt(n) <= 65535 ? 2 : 4;
        return t
    }
    function collectStoreSize() {
        var e, t = "", n = "_CACHE", i = {
            other: 0
        }, r = 0, a = {}, o = 0, c = win.localStorage;
        for (e in c) {
            var s = c[e];
            if (hasOwn.call(c, e) && "function" != typeof s && "object" != typeof s) {
                var u = !1
                  , l = sizeOf(s) + sizeOf(e);
                102400 < l && (a[e] = l,
                o++);
                for (var d = 0, f = matchs.length; d < f; d++) {
                    var p = matchs[d];
                    if (p.rg.test(e)) {
                        r += l,
                        /.*(_cache)$/i.test(e) ? i[p.bu + n] ? i[p.bu + n] += l : i[p.bu + n] = l : i[p.bu] ? i[p.bu] += l : i[p.bu] = l,
                        u = !0;
                        break
                    }
                }
                u || (r += l,
                i.other += l)
            }
        }
        if (r) {
            for (var g in t = "all=" + r,
            i)
                t += "&" + g + "=" + i[g];
            api._tracklog("ubt_m_localstorage", t)
        }
        0 < o && api._tracklog("101941", JSON.stringify(a))
    }
    function shuffle(e) {
        for (var t = e.length - 1; 0 <= t; t--) {
            var n = Math.floor(Math.random() * (t + 1))
              , i = e[n];
            e[n] = e[t],
            e[t] = i
        }
        return e
    }
    function resourTiming() {
        for (var t = /^([a-z]+\d*|(webresource|pic)\.english)\.((c-)?c?trip.com)/i, n = /(-s|static)\.tripcdn\.(com|cn)$/, e = shuffle(win[perf].getEntriesByType("resource") || []).filter(function(e) {
            e = parseHost(e.name);
            return !("string" != typeof e.host || !t.test(e.host) && !n.test(e.host))
        }), i = [], r = [], a = 0, o = 0; o < e.length && !(10 < e.length && a === Math.round(.1 * e.length)); o++) {
            5 === r.length && (i.push(r),
            r = []);
            for (var c = e[o], s = ["entryType", "initiatorType", "startTime", "redirectStart", "redirectEnd", "fetchStart", "domainLookupStart", "domainLookupEnd", "connectStart", "connectEnd", "secureConnectionStart", "requestStart", "responseStart", "responseEnd", "transferSize", "encodedBodySize", "decodedBodySize"], u = {
                name: c.name,
                nextHopProtocol: ""
            }, l = 0, d = s.length; l < d; l++)
                u[s[l]] = c[s[l]] || 0;
            r.push(u),
            ++a
        }
        return 0 < r.length && i.push(r),
        i
    }
    function coFCP(e) {
        for (var t = {
            name: "106376",
            tag: {
                fp_status: 0,
                fcp_status: 0
            },
            value: {
                fp: 0,
                fcp: 0
            }
        }, n = performance.getEntriesByType("paint"), i = 0, r = n.length; i < r; i++) {
            var a = n[i];
            switch (a.name) {
            case "first-paint":
                t.tag.fp_status = 1,
                t.value.fp = Math.floor(a.startTime + a.duration);
                break;
            case "first-contentful-paint":
                t.tag.fcp_status = 1,
                t.value.fcp = Math.floor(a.startTime + a.duration)
            }
        }
        !coFCPDone && t.value.fcp && t.value.fp && (coFCPDone = !0,
        e.send("matrix", t))
    }
    function coPerfNav(e) {
        var t = performance.getEntriesByType("navigation");
        if (t && 0 < t.length) {
            var n, i = {
                name: "133077",
                tag: {},
                value: {}
            }, r = t[0];
            for (n in r) {
                var a = r[n]
                  , o = typeof a;
                "number" == o && 0 < a ? i.value[n] = parseFloat(a.toFixed(4)) : "string" == o && a.length < 100 && (i.tag[n] = a)
            }
            e.send("matrix", i)
        }
    }
    function pwm(t) {
        window.PerformanceObserver && "function" == typeof PerformanceObserver && PerformanceObserver.supportedEntryTypes && -1 != PerformanceObserver.supportedEntryTypes.indexOf("paint") && window.PerformancePaintTiming && performance.getEntriesByType && (1 < performance.getEntriesByType("paint") ? coFCP(t) : new PerformanceObserver(function(e) {
            coFCP(t)
        }
        ).observe({
            entryTypes: ["paint"]
        }),
        coPerfNav(t))
    }
    function restiming(r) {
        win[perf] && win[perf].getEntriesByType && (win.addEventListener("load", function() {
            var n = resourTiming();
            if (0 < n.length)
                try {
                    var i = function(e) {
                        for (; (5 < e.timeRemaining() || e.didTimeout) && 0 < n.length; ) {
                            var t = n.shift();
                            r.send("restiming", t)
                        }
                        0 < n.length && window.requestIdleCallback(i)
                    };
                    "requestIdleCallback"in window && window.requestIdleCallback(i)
                } catch (e) {}
        }),
        log(17));
        try {
            pwm(r)
        } catch (e) {}
    }
    function hookPromise() {
        var t;
        function n(e) {
            if (!(this instanceof n))
                return t(e);
            if ("function" != typeof e)
                return new t(e);
            return new t(function() {
                try {
                    return e.apply(this, arguments)
                } catch (e) {
                    throw e instanceof Error || (e = new Error(e + "")),
                    t = {
                        message: (t = e).message || "",
                        file: "",
                        category: t.name || "promise-catch",
                        framework: "ubt-promise-catch",
                        time: 0,
                        line: 0,
                        column: 0,
                        stack: t.stack || "",
                        repeat: 1
                    },
                    api._trackError(t),
                    e
                }
                var t
            }
            )
        }
        "function" != typeof win.Promise || -1 < (t = win.Promise).toString().indexOf("[native code]") && t.resolve.toString().indexOf("[native code]") && (win.Promise = n,
        log(20))
    }
    function _push() {
        for (var e, t = arguments, n = 0, i = 0, r = t.length; n < r; n++) {
            var a = t[n];
            isArray(a) ? (e = a[0],
            api[e] && api[e].apply(api, Array.prototype.slice.call(a, 1))) : i++
        }
        return i
    }
}();
