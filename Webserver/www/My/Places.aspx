<?php
  session_start();
  include_once $_SERVER["DOCUMENT_ROOT"] . '/global.php';
  ?>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en" xmlns:fb="http://www.facebook.com/2008/fbml">
  <!-- MachineID: WEB201 -->
  <meta http-equiv="X-UA-Compatible" content="IE=edge,requiresActiveX=true"/>
  <title>
    ROBLOX Login
  </title>
  <link rel="icon" type="image/vnd.microsoft.icon" href="/favicon.ico"/>
  <meta http-equiv="Content-Type" content="text/html; charset=utf-8"/>
  <meta http-equiv="Content-Language" content="en-us"/>
  <meta name="author" content="ROBLONIUM"/>
  <meta id="ctl00_metadescription" name="description" content="User-generated MMO gaming site for kids, teens, and adults. Players architect their own worlds. Builders create free online games that simulate the real world. Create and play amazing 3D games. An online gaming cloud and distributed physics engine."/>
  <meta id="ctl00_metakeywords" name="keywords" content="free games, online games, building games, virtual worlds, free mmo, gaming cloud, physics engine"/>
  <script type="text/javascript">
    var _gaq = _gaq || [];
    _gaq.push(['_setAccount', 'UA-11419793-1']);
    _gaq.push(['_setCampSourceKey', 'rbx_source']);
    _gaq.push(['_setCampMediumKey', 'rbx_medium']);
    _gaq.push(['_setCampContentKey', 'rbx_campaign']);
    
    _gaq.push(['b._setAccount', 'UA-486632-1']);
    _gaq.push(['b._setCampSourceKey', 'rbx_source']);
    _gaq.push(['b._setCampMediumKey', 'rbx_medium']);
    _gaq.push(['b._setCampContentKey', 'rbx_campaign']);
    _gaq.push(['c._setAccount', 'UA-26810151-2']);
    
    (function() {
        var ga = document.createElement('script');
        ga.type = 'text/javascript';
        ga.async = true;
        ga.src = ('https:' == document.location.protocol ? 'https://ssl/' : 'http://www') + '.google-analytics.com/ga.js';
        var s = document.getElementsByTagName('script')[0];
        s.parentNode.insertBefore(ga, s);
    })();
    
  </script>
  <?php include $_SERVER["DOCUMENT_ROOT"] . "/puzzle/ScriptGlobals.php";?>
  </script>
  <script type="text/javascript" src="https://s3.amazonaws.com/js.roblox.com/6b6d4f697b68f7c847ed0aa00e9e913d.js"></script>
  </head>
  <body>
    <script type="text/javascript">Roblox.XsrfToken.setToken('');</script>
    <script type="text/javascript">
      if (top.location != self.location) {
          top.location = self.location.href;
      }
    </script>
    <style type="text/css">
    <style type="text/css"></style>
    <link rel="Stylesheet" href="/CSS/Themes/Halloween2013/Halloween2013.css"/>
    </style>
    <form name="aspnetForm" method="post" action="/login/index.html" id="aspnetForm">
      <div>
        <input type="hidden" name="__VIEWSTATE" id="__VIEWSTATE" value="/wEPDwUKMTg5NjA1Njg2Nw9kFgJmD2QWAgIBEBYCHgZhY3Rpb24FEy9sb2dpbi9EZWZhdWx0LmFzcHhkFgoCAg8PFgIeB1Zpc2libGVoZBYCZg9kFggCAQ8QZGQWAGQCAg8QZGQWAWZkAgMPEGRkFgFmZAIEDxBkZBYBZmQCAw8PFgIfAWhkZAIJDw8WAh8BaGRkAgwPZBYGAgEPFgIfAWgWBgIDDxYCHwFoZAIFDxYCHwFoZAIHDxYCHwFoZAIDDxYCHwFoZAILD2QWCAIBDxAPFgIeC18hRGF0YUJvdW5kZ2RkZGQCAw8QDxYCHwJnZA8WHwIBAgICAwIEAgUCBgIHAggCCQIKAgsCDAINAg4CDwIQAhECEgITAhQCFQIWAhcCGAIZAhoCGwIcAh0CHgIfFh8QBQExBQExZxAFATIFATJnEAUBMwUBM2cQBQE0BQE0ZxAFATUFATVnEAUBNgUBNmcQBQE3BQE3ZxAFATgFAThnEAUBOQUBOWcQBQIxMAUCMTBnEAUCMTEFAjExZxAFAjEyBQIxMmcQBQIxMwUCMTNnEAUCMTQFAjE0ZxAFAjE1BQIxNWcQBQIxNgUCMTZnEAUCMTcFAjE3ZxAFAjE4BQIxOGcQBQIxOQUCMTlnEAUCMjAFAjIwZxAFAjIxBQIyMWcQBQIyMgUCMjJnEAUCMjMFAjIzZxAFAjI0BQIyNGcQBQIyNQUCMjVnEAUCMjYFAjI2ZxAFAjI3BQIyN2cQBQIyOAUCMjhnEAUCMjkFAjI5ZxAFAjMwBQIzMGcQBQIzMQUCMzFnZGQCBQ8QDxYCHwJnZA8WZAIBAgICAwIEAgUCBgIHAggCCQIKAgsCDAINAg4CDwIQAhECEgITAhQCFQIWAhcCGAIZAhoCGwIcAh0CHgIfAiACIQIiAiMCJAIlAiYCJwIoAikCKgIrAiwCLQIuAi8CMAIxAjICMwI0AjUCNgI3AjgCOQI6AjsCPAI9Aj4CPwJAAkECQgJDAkQCRQJGAkcCSAJJAkoCSwJMAk0CTgJPAlACUQJSAlMCVAJVAlYCVwJYAlkCWgJbAlwCXQJeAl8CYAJhAmICYwJkFmQQBQQyMDEyBQQyMDEyZxAFBDIwMTEFBDIwMTFnEAUEMjAxMAUEMjAxMGcQBQQyMDA5BQQyMDA5ZxAFBDIwMDgFBDIwMDhnEAUEMjAwNwUEMjAwN2cQBQQyMDA2BQQyMDA2ZxAFBDIwMDUFBDIwMDVnEAUEMjAwNAUEMjAwNGcQBQQyMDAzBQQyMDAzZxAFBDIwMDIFBDIwMDJnEAUEMjAwMQUEMjAwMWcQBQQyMDAwBQQyMDAwZxAFBDE5OTkFBDE5OTlnEAUEMTk5OAUEMTk5OGcQBQQxOTk3BQQxOTk3ZxAFBDE5OTYFBDE5OTZnEAUEMTk5NQUEMTk5NWcQBQQxOTk0BQQxOTk0ZxAFBDE5OTMFBDE5OTNnEAUEMTk5MgUEMTk5MmcQBQQxOTkxBQQxOTkxZxAFBDE5OTAFBDE5OTBnEAUEMTk4OQUEMTk4OWcQBQQxOTg4BQQxOTg4ZxAFBDE5ODcFBDE5ODdnEAUEMTk4NgUEMTk4NmcQBQQxOTg1BQQxOTg1ZxAFBDE5ODQFBDE5ODRnEAUEMTk4MwUEMTk4M2cQBQQxOTgyBQQxOTgyZxAFBDE5ODEFBDE5ODFnEAUEMTk4MAUEMTk4MGcQBQQxOTc5BQQxOTc5ZxAFBDE5NzgFBDE5NzhnEAUEMTk3NwUEMTk3N2cQBQQxOTc2BQQxOTc2ZxAFBDE5NzUFBDE5NzVnEAUEMTk3NAUEMTk3NGcQBQQxOTczBQQxOTczZxAFBDE5NzIFBDE5NzJnEAUEMTk3MQUEMTk3MWcQBQQxOTcwBQQxOTcwZxAFBDE5NjkFBDE5NjlnEAUEMTk2OAUEMTk2OGcQBQQxOTY3BQQxOTY3ZxAFBDE5NjYFBDE5NjZnEAUEMTk2NQUEMTk2NWcQBQQxOTY0BQQxOTY0ZxAFBDE5NjMFBDE5NjNnEAUEMTk2MgUEMTk2MmcQBQQxOTYxBQQxOTYxZxAFBDE5NjAFBDE5NjBnEAUEMTk1OQUEMTk1OWcQBQQxOTU4BQQxOTU4ZxAFBDE5NTcFBDE5NTdnEAUEMTk1NgUEMTk1NmcQBQQxOTU1BQQxOTU1ZxAFBDE5NTQFBDE5NTRnEAUEMTk1MwUEMTk1M2cQBQQxOTUyBQQxOTUyZxAFBDE5NTEFBDE5NTFnEAUEMTk1MAUEMTk1MGcQBQQxOTQ5BQQxOTQ5ZxAFBDE5NDgFBDE5NDhnEAUEMTk0NwUEMTk0N2cQBQQxOTQ2BQQxOTQ2ZxAFBDE5NDUFBDE5NDVnEAUEMTk0NAUEMTk0NGcQBQQxOTQzBQQxOTQzZxAFBDE5NDIFBDE5NDJnEAUEMTk0MQUEMTk0MWcQBQQxOTQwBQQxOTQwZxAFBDE5MzkFBDE5MzlnEAUEMTkzOAUEMTkzOGcQBQQxOTM3BQQxOTM3ZxAFBDE5MzYFBDE5MzZnEAUEMTkzNQUEMTkzNWcQBQQxOTM0BQQxOTM0ZxAFBDE5MzMFBDE5MzNnEAUEMTkzMgUEMTkzMmcQBQQxOTMxBQQxOTMxZxAFBDE5MzAFBDE5MzBnEAUEMTkyOQUEMTkyOWcQBQQxOTI4BQQxOTI4ZxAFBDE5MjcFBDE5MjdnEAUEMTkyNgUEMTkyNmcQBQQxOTI1BQQxOTI1ZxAFBDE5MjQFBDE5MjRnEAUEMTkyMwUEMTkyM2cQBQQxOTIyBQQxOTIyZxAFBDE5MjEFBDE5MjFnEAUEMTkyMAUEMTkyMGcQBQQxOTE5BQQxOTE5ZxAFBDE5MTgFBDE5MThnEAUEMTkxNwUEMTkxN2cQBQQxOTE2BQQxOTE2ZxAFBDE5MTUFBDE5MTVnEAUEMTkxNAUEMTkxNGcQBQQxOTEzBQQxOTEzZ2RkAgkPZBYEZg8WAh4Dc3JjBUtodHRwczovL3MzLmFtYXpvbmF3cy5jb206NDQzL3Q1LnJvYmxveC5jb20vODk5YjcwOGRmM2ZmYWE1ODg0OGM0YjQzODNkYzQ1YzNkAgIPFgIfAwVLaHR0cHM6Ly9zMy5hbWF6b25hd3MuY29tOjQ0My90My5yb2Jsb3guY29tLzk0NThmYmE2MDhhZDY5ZTVkODhjY2I1OGI3NGM3ZGM0ZAIPDw8WAh8BaGRkGAQFHl9fQ29udHJvbHNSZXF1aXJlUG9zdEJhY2tLZXlfXxYEBShjdGwwMCRjcGhSb2Jsb3gkU2VsZWN0R2VuZGVyUGFuZSRNYWxlQnRuBShjdGwwMCRjcGhSb2Jsb3gkU2VsZWN0R2VuZGVyUGFuZSRNYWxlQnRuBSpjdGwwMCRjcGhSb2Jsb3gkU2VsZWN0R2VuZGVyUGFuZSRGZW1hbGVCdG4FKmN0bDAwJGNwaFJvYmxveCRTZWxlY3RHZW5kZXJQYW5lJEZlbWFsZUJ0bgUjY3RsMDAkcmJ4R29vZ2xlQW5hbHl0aWNzJE11bHRpVmlldzEPD2QCAWQFJGN0bDAwJFJpZ2h0R3V0dGVyQWQkQXN5bmNBZE11bHRpVmlldw8PZAIDZAUjY3RsMDAkTGVmdEd1dHRlckFkJEFzeW5jQWRNdWx0aVZpZXcPD2QCA2QvwL6uUBt2xOMZLoK1cI9m+m7nHA=="/>
      </div>
      <script src="/ScriptResource.axd?d=7staQf3Xy38cRSAHWPf7sFfilPK9gBMXjJVfmYoSrXzuJ0DHeB7XBSCbuymxv8LUL_qoYLOlfUjgFCuFTPo4DUQH1S6es4PSCthN1jdC7suhk3eoCVzz9SaC0Qo2YthbCSWRdk8yqfo6O1NcTgK1Yb2wxtvmOcZqTCa1yRcNwwJ2lqzhDIhAoJXDxqjYPJqa-KX6aGGjM8coZmCMUGs7wSCKK17nXzec_q5fM7MmPADbkiH17aF09K2AYPZyvpW0SKxZ_r1ZX4DMMTTLuBq1Ea4OBd1BQLfJVUq_ZCgnGjm3uwMG0G_u_N1FWMYymepwtoef6cScHPdfxM4RRI4vO3NgadeSzHCzm3KigGt9nUWZ_luEme1hQG6uAuJ3bBa5ZN_6cW0Ft1xKb2fvWlUGMx0PbsSmDH2HOSaZAsB6dGB-jP7WCD0tR1D51snRmFfxVQUO0A2" type="text/javascript"></script>
      <div>
        <input type="hidden" name="__EVENTVALIDATION" id="__EVENTVALIDATION" value="/wEWmQECrtDFrwgCqdGmlwQC/5/U4gcC0q+nzQsCwdSDvwcC3tSDvwcC39SDvwcC3NSDvwcC3dSDvwcC2tSDvwcC29SDvwcC2NSDvwcCydSDvwcCxtSDvwcC3tTDvAcC3tTPvAcC3tTLvAcCuavNcQKmq81xAqerzXECpKvNcQKlq81xAqKrzXECo6vNcQKgq81xArGrzXECvqvNcQKmq41yAqargXICpquFcgKmq7lyAqarvXICpquxcgKmq7VyAqarqXICpqvtcQKmq+FxAqerjXICp6uBcgKnq4VyAqeruXICp6u9cgKnq7FyAqertXICp6upcgKnq+1xAqer4XECpKuNcgKkq4FyAoK0o4EJAtHMyokNAtHM3q4EAtHM4vMPArr10OoIArr15A8CuvXI5gYCuvXciw4CuvXg0AECuvX09QgCuvWYGQK69ay+CwK69bDDAgK69cToBQL+lq0eAv6WsaMLAv6WhZoOAv6Wqb8BAv6WvcQIAv6WwekDAv6W1Y4LAv6W+dMCAv6WjfcFAv6WkZwNAsO/j7MOAsO/k9gBAsO/57AEAsO/i9QPAsO/n/kGAsO/o54OAsO/t6MBAsO/28gIAsO/7+0DAsO/87ILAvTVz/UBAvTV05oJAvTVp/EPAvTVy5YHAvTV37sOAvTV48ABAvTV9+UIAvTVmwkC9NWvrgsC9NWz8wIC2f6h6g8C2f61jwcC2f6Z5gUC2f6tiw0C2f6x0AQC2f7F9Q8C2f7pmgcC2f79vw4C2f6BwwEC2f6V6AgCoueDnwoCoueXpA0Couf7HAKi54+gCwKi55PFAgKi56fqBQKi58uPDQKi59/UBAKi5+P5DwKi5/eeBwKHiOU1AoeIidkLAoeI3bEOAoeI4dYBAoeI9fsIAoeImR8Ch4itpAsCh4ixyQICh4jF7gUCh4jpsw0C6LLHqg4C6LLrzwEC6LK/pgQC6LLDyw8C6LLXkAcC6LL7tQ4C6LKP2QEC6LKT/ggC6LKnAwLossuoCwLN27jfBALN28zkDwLN25DbAgLN26TgBQLN28iFDQLN29yqBALN2+DPDwLN2/SUBwLN25i4DgLN26zdAQLWzJr0AgLWzK6ZCgLWzPLxCALWzIYVAtbMqroLAtbMvt8CAtbMwuQFAozJwd4CAvGMmbsHApCi0e0H0bUaRFsSHlLPAJMNSridbiXIO70="/>
      </div>
      <div id="fb-root">
      </div>
      <div id="MasterContainer">
        <script type="text/javascript">
          $(function(){
              function trackReturns() {
                function dayDiff(d1, d2) {
                    return Math.floor((d1-d2)/86400000);
                }
          
                var cookieName = 'RBXReturn';
                var cookieOptions = {expires:9001};
                  var cookie = $.getJSONCookie(cookieName);
          
                if (typeof cookie.ts === "undefined" || isNaN(new Date(cookie.ts))) {
                    $.setJSONCookie(cookieName, { ts: new Date().toDateString() }, cookieOptions);
                    return;
                }
          
                var daysSinceFirstVisit = dayDiff(new Date(), new Date(cookie.ts));
                if (daysSinceFirstVisit == 1 && typeof cookie.odr === "undefined") {
                    RobloxEventManager.triggerEvent('rbx_evt_odr', {});
                    cookie.odr = 1;
                }
                if (daysSinceFirstVisit >= 1 && daysSinceFirstVisit <= 7 && typeof cookie.sdr === "undefined") {
                    RobloxEventManager.triggerEvent('rbx_evt_sdr', {});
                    cookie.sdr = 1;
                }
            
                $.setJSONCookie(cookieName, cookie, cookieOptions);
              }
          
              
                  RobloxListener.restUrl = window.location.protocol + "//" + "roblox.com/Game/EventTracker.ashx";
                  RobloxListener.init();
              
              
                  GoogleListener.init();
              
              
              
              
                  RobloxEventManager.initialize(true);
                  RobloxEventManager.triggerEvent('rbx_evt_pageview');
                  trackReturns();
              
              
              
                  RobloxEventManager._idleInterval = 450000;
                  RobloxEventManager.registerCookieStoreEvent('rbx_evt_initial_install_start');
                  RobloxEventManager.registerCookieStoreEvent('rbx_evt_ftp');
                  RobloxEventManager.registerCookieStoreEvent('rbx_evt_initial_install_success');
                  RobloxEventManager.registerCookieStoreEvent('rbx_evt_fmp');
                  RobloxEventManager.startMonitor();
              
          
          });
          
        </script>
        <script type="text/javascript">Roblox.FixedUI.gutterAdsEnabled=false;</script>
        <?php include $_SERVER["DOCUMENT_ROOT"] . '/Banner' ;?>
        <script type="text/javascript">
          $(function () {
              $('.more-list-item').bind('showDropDown', function () {
                  var maxWidth = $('#navigation-menu .dropdownnavcontainer').width();
                  $('a.dropdownoption span').each(function (index, elem) {
                      elem = $(elem);
                      if (elem.outerWidth() > maxWidth) {
                          maxWidth = elem.outerWidth();
                      }
                  });
                  maxWidth = maxWidth + 5;
                  $('#navigation-menu .dropdownoption').each(function (index, elem) {
                      elem = $(elem);
                      if (elem.width() < maxWidth) {
                          elem.width(maxWidth);
                      }
                  });
              });
          });
          
          
        </script>
      </div>
      <div class="forceSpace">&nbsp;</div>
      <div id="BodyWrapper">
        <div id="RepositionBody">
          <div id="Body" style="">
            <div class="LoginNewStyle">
              <div class="MyRobloxContainer">
                <script type="text/javascript">
                  $(function() {
                      var $username = $("#ctl00_cphRoblox_lRobloxLogin_UserName");
                      var $password = $("#ctl00_cphRoblox_lRobloxLogin_Password");
                  
                      $username.focus(function() {
                          $(this).css("border-color", "#A5D0FF");
                      });
                      $username.blur(function() {
                          $(this).css("border-color", "#CCCCCC");
                      });
                      $password.focus(function() {
                          $(this).css("border-color", "#A5D0FF");
                      });
                      $password.blur(function() {
                          $(this).css("border-color", "#CCCCCC");
                  });
                  });
                </script>
                <div style="clear: both;"></div>
                <div class="Column1a">
                  <div class="StandardBoxHeader" id="newLoginHeader" style="width:300px;">
                    <span id="ctl00_cphRoblox_LoginHeader2">Login</span>
                  </div>
                  <div class="StandardBox" id="newLogin" style="height: 170px;width:300px;">
                    <div id="ctl00_cphRoblox_LOLOLOLOL">
                      <div class="AspNet-Login">
                        <table style="margin: 0px auto;">
                          <tr>
                            <td colspan="2" style="color: #FF0000">
                            </td>
                          </tr>
                          <tr>
                            <td style="text-align: right;">
                              Username:
                            </td>
                            <td>
                              <div><input name="ctl00$cphRoblox$lRobloxLogin$UserName" type="text" id="ctl00_cphRoblox_lRobloxLogin_UserName" class="TextBox" name="UserName" style="border: 2px solid #CCCCCC;width:130px;"/></div>
                              <div></div>
                            </td>
                          </tr>
                          <tr>
                            <td style="text-align: right;">
                              Password:
                            </td>
                            <td style="position:relative;display:block;">
                              <div style="float:left;width:215px;">
                                <div><input name="ctl00$cphRoblox$lRobloxLogin$Password" type="password" id="ctl00_cphRoblox_lRobloxLogin_Password" class="TextBox" style="border: 2px solid #CCCCCC; width:130px;"/></div>
                                <div></div>
                              </div>
                              <div style="position:absolute;top:2px;*top:1px;left:150px;">
                                <input type="submit" name="ctl00$cphRoblox$lRobloxLogin$Login" value="Login" onclick="javascript:WebForm_DoPostBackWithOptions(new WebForm_PostBackOptions(&quot;ctl00$cphRoblox$lRobloxLogin$Login&quot;, &quot;&quot;, true, &quot;logingroup&quot;, &quot;&quot;, false, false))" id="ctl00_cphRoblox_lRobloxLogin_Login" class="MediumButton tranlsate"/>
                              </div>
                            </td>
                          </tr>
                          <tr>
                            <td colspan="2" align="center" style="padding-bottom:10px;">
                              <div style="font-size: 11px;">
                                <a href="ResetPasswordRequest.aspx">Forgot your password?</a>
                              </div>
                            </td>
                          </tr>
                          <tr>
                            <td colspan="2" class="FacebookConnectTD" style="text-align: center;border-top: 1px solid #CCC;padding:0;margin:0;">
                              <div id="ctl00_cphRoblox_lRobloxLogin_fbMVCLogin" class="fbSplashPageConnect">
                                <a class="facebook-login" href="/Facebook/SignIn?returnTo=%2fMy%2findex.html" ref="form-facebook">
                                <span class="left"></span>
                                <span class="middle">Login with Facebook<span>Login with Facebook</span></span>
                                <span class="right"></span>
                                </a>     
                              </div>
                            </td>
                          </tr>
                        </table>
                      </div>
                    </div>
                  </div>
                </div>
                <div class="Column2a">
                  <div id="ctl00_cphRoblox_NewUserPanel2">
                    <div class="StandardBoxHeader" style="width: 558px;float:right;">
                      <span>Create a Free ROBLOX Account</span>
                    </div>
                    <div class="StandardBox" id="newSignupBox" style="width: 558px;float:right;min-height:170px;">
                      <div id="ChooseBirthdate" style="height:111px">
                        <p>
                          Creating an account on ROBLOX allows you to customize your character, make friends,
                          build places, earn money, and more!
                        </p>
                        <center>
                          <span>Your Date of Birth: </span>
                          <select name="ctl00$cphRoblox$lstMonths" id="lstMonths">
                            <option value="0">Select Month</option>
                            <option value="1">January</option>
                            <option value="2">February</option>
                            <option value="3">March</option>
                            <option value="4">April</option>
                            <option value="5">May</option>
                            <option value="6">June</option>
                            <option value="7">July</option>
                            <option value="8">August</option>
                            <option value="9">September</option>
                            <option value="10">October</option>
                            <option value="11">November</option>
                            <option value="12">December</option>
                          </select>
                          <select name="ctl00$cphRoblox$lstDays" id="lstDays">
                            <option value="0">Select Day</option>
                            <option value="1">1</option>
                            <option value="2">2</option>
                            <option value="3">3</option>
                            <option value="4">4</option>
                            <option value="5">5</option>
                            <option value="6">6</option>
                            <option value="7">7</option>
                            <option value="8">8</option>
                            <option value="9">9</option>
                            <option value="10">10</option>
                            <option value="11">11</option>
                            <option value="12">12</option>
                            <option value="13">13</option>
                            <option value="14">14</option>
                            <option value="15">15</option>
                            <option value="16">16</option>
                            <option value="17">17</option>
                            <option value="18">18</option>
                            <option value="19">19</option>
                            <option value="20">20</option>
                            <option value="21">21</option>
                            <option value="22">22</option>
                            <option value="23">23</option>
                            <option value="24">24</option>
                            <option value="25">25</option>
                            <option value="26">26</option>
                            <option value="27">27</option>
                            <option value="28">28</option>
                            <option value="29">29</option>
                            <option value="30">30</option>
                            <option value="31">31</option>
                          </select>
                          <select name="ctl00$cphRoblox$lstYears" id="lstYears">
                            <option value="0">Select Year</option>
                            <option value="2018">2018</option>
                            <option value="2017">2017</option>
                            <option value="2016">2016</option>
                            <option value="2015">2015</option>
                            <option value="2014">2014</option>
                            <option value="2013">2013</option>
                            <option value="2012">2012</option>
                            <option value="2011">2011</option>
                            <option value="2010">2010</option>
                            <option value="2009">2009</option>
                            <option value="2008">2008</option>
                            <option value="2007">2007</option>
                            <option value="2006">2006</option>
                            <option value="2005">2005</option>
                            <option value="2004">2004</option>
                            <option value="2003">2003</option>
                            <option value="2002">2002</option>
                            <option value="2001">2001</option>
                            <option value="2000">2000</option>
                            <option value="1999">1999</option>
                            <option value="1998">1998</option>
                            <option value="1997">1997</option>
                            <option value="1996">1996</option>
                            <option value="1995">1995</option>
                            <option value="1994">1994</option>
                            <option value="1993">1993</option>
                            <option value="1992">1992</option>
                            <option value="1991">1991</option>
                            <option value="1990">1990</option>
                            <option value="1989">1989</option>
                            <option value="1988">1988</option>
                            <option value="1987">1987</option>
                            <option value="1986">1986</option>
                            <option value="1985">1985</option>
                            <option value="1984">1984</option>
                            <option value="1983">1983</option>
                            <option value="1982">1982</option>
                            <option value="1981">1981</option>
                            <option value="1980">1980</option>
                            <option value="1979">1979</option>
                            <option value="1978">1978</option>
                            <option value="1977">1977</option>
                            <option value="1976">1976</option>
                            <option value="1975">1975</option>
                            <option value="1974">1974</option>
                            <option value="1973">1973</option>
                            <option value="1972">1972</option>
                            <option value="1971">1971</option>
                            <option value="1970">1970</option>
                            <option value="1969">1969</option>
                            <option value="1968">1968</option>
                            <option value="1967">1967</option>
                            <option value="1966">1966</option>
                            <option value="1965">1965</option>
                            <option value="1964">1964</option>
                            <option value="1963">1963</option>
                            <option value="1962">1962</option>
                            <option value="1961">1961</option>
                            <option value="1960">1960</option>
                            <option value="1959">1959</option>
                            <option value="1958">1958</option>
                            <option value="1957">1957</option>
                            <option value="1956">1956</option>
                            <option value="1955">1955</option>
                            <option value="1954">1954</option>
                            <option value="1953">1953</option>
                            <option value="1952">1952</option>
                            <option value="1951">1951</option>
                            <option value="1950">1950</option>
                            <option value="1949">1949</option>
                            <option value="1948">1948</option>
                            <option value="1947">1947</option>
                            <option value="1946">1946</option>
                            <option value="1945">1945</option>
                            <option value="1944">1944</option>
                            <option value="1943">1943</option>
                            <option value="1942">1942</option>
                            <option value="1941">1941</option>
                            <option value="1940">1940</option>
                            <option value="1939">1939</option>
                            <option value="1938">1938</option>
                            <option value="1937">1937</option>
                            <option value="1936">1936</option>
                            <option value="1935">1935</option>
                            <option value="1934">1934</option>
                            <option value="1933">1933</option>
                            <option value="1932">1932</option>
                            <option value="1931">1931</option>
                            <option value="1930">1930</option>
                            <option value="1929">1929</option>
                            <option value="1928">1928</option>
                            <option value="1927">1927</option>
                            <option value="1926">1926</option>
                            <option value="1925">1925</option>
                            <option value="1924">1924</option>
                            <option value="1923">1923</option>
                            <option value="1922">1922</option>
                            <option value="1921">1921</option>
                            <option value="1920">1920</option>
                            <option value="1919">1919</option>
                            <option value="1918">1918</option>
                            <option value="1917">1917</option>
                            <option value="1916">1916</option>
                            <option value="1915">1915</option>
                            <option value="1914">1914</option>
                            <option value="1913">1913</option>
                          </select>
                          &nbsp;&nbsp;
                          <input id="btnContinue" type="button" class="MediumButton translate" onclick="CheckDate()" value="Continue"/>
                          <div id="lblError" style="display: none">
                            <b>Please choose a valid date</b>
                          </div>
                          <div style="font-style:italic;margin-top:15px">Your birthday will not be given out to any third party!</div>
                        </center>
                      </div>
                      <div id="ChooseGender" style="text-align:center;display:none">
                        <div style="text-align:left">Are you a boy or a girl?</div>
                        <div style="text-align:center;position:relative;height:250px">
                          <div style="position:absolute;left:50%;margin-left:-175px">
                            <label for="MaleBtn"><img src="/images/Accounts/boy.png" id="ctl00_cphRoblox_SelectGenderPane_BoyThumbnail" style="cursor:pointer"/><br/></label>
                            <input id="MaleBtn" type="radio" name="ctl00$cphRoblox$SelectGenderPane$Gender" value="MaleBtn"/><label for="MaleBtn">Boy</label>
                          </div>
                          <div style="position:absolute;left:50%;margin-left:25px">
                            <label for="FemaleBtn"><img src="/images/Accounts/girl.png" id="ctl00_cphRoblox_SelectGenderPane_GirlThumbnail" style="cursor:pointer"/><br/></label>
                            <input id="FemaleBtn" type="radio" name="ctl00$cphRoblox$SelectGenderPane$Gender" value="FemaleBtn"/><label for="FemaleBtn">Girl</label>
                          </div>
                        </div>
                        <div id="genderError" style="color:Red;font-weight:bold;margin-bottom:10px;display:none">Please select a gender</div>
                        <input type="submit" name="ctl00$cphRoblox$btnSignup2" value="Continue" onclick="return CheckGender();" id="ctl00_cphRoblox_btnSignup2" class="MediumButton translate"/>
                      </div>
                      <br/>
                    </div>
                  </div>
                </div>
                <div style="clear: both;"></div>
                <div id="ExpandBorder" style="float:right; width:568px;height:40px;border:1px solid #AAAAAA;border-top:none;margin-top:-49px">&nbsp;</div>
                <div class="StandardBoxHeader" style="width: 878px;">
                  <span>You don't need an account to play ROBLOX</span>
                </div>
                <div class="StandardBox" style="width: 878px">
                  <div id="ctl00_cphRoblox_GuestMode" style="text-align: center;">
                    <p>
                      You can start playing right now, in guest mode! Just click on the game you want
                      to play.
                    </p>
                    <a id="ctl00_cphRoblox_PlayNow" tabindex="2" class="MediumButton" href="/games" style="text-decoration: none; color: #222222;
                      width: 20%;">Play as Guest</a>
                    </p>
                  </div>
                </div>
              </div>
              <div style="clear: both"></div>
              <script type="text/javascript">
                function CheckDate() {
                    $('#lblError').attr('style', 'display: none');
                    var year = parseInt($('#lstYears option:selected').val());
                    var month = parseInt($('#lstMonths option:selected').val());
                    var day = parseInt($('#lstDays option:selected').val());
                
                    if (year <= 0 || month <= 0 || day <= 0 || day > new Date(year, month, 0).getDate()) {
                        $('#lblError').attr('style', 'color: Red;');
                    }
                    else {
                        $('#ChooseBirthdate').slideToggle();
                        $('#ChooseGender').slideToggle();
                        $('#ExpandBorder').hide();
                        $('#newSignupBox').css("border","1px solid #AAAAAA");
                    }
                }
                function CheckGender() {
                        if ($('#MaleBtn:checked').length == 0 && $('#FemaleBtn:checked').length == 0) {
                            $('#genderError').show();
                            return false;
                        }
                        else {
                            $('#genderError').hide();
                        }
                }
              </script>
            </div>
            <div style="clear:both"></div>
          </div>
        </div>
      </div>
      </div>
      <div id="Footer" class="LanguageRedesign">
        <div class="FooterNav">
          <a href="/info/Privacy.aspx"><b>Privacy Policy</b></a>
          &nbsp;|&nbsp; 
          <a href="http://corp.roblox.com/advertise-on-roblox" class="roblox-interstitial">Advertise with Us</a>
          &nbsp;|&nbsp; 
          <a href="http://corp.roblox.com/roblox-press" class="roblox-interstitial">Press</a>
          &nbsp;|&nbsp; 
          <a href="http://corp.roblox.com/contact-us" class="roblox-interstitial">Contact Us</a>
          &nbsp;|&nbsp;
          <a href="http://corp.roblox.com/" class="roblox-interstitial">About Us</a>
          &nbsp;|&nbsp;
          <a href="http://blog.roblox.com/" class="roblox-interstitial">Blog</a>
          &nbsp;|&nbsp;
          <a href="http://corp.roblox.com/jobs" class="roblox-interstitial">Jobs</a>
          &nbsp;|&nbsp;
          <a href="/Parents.aspx">Parents</a>
          &nbsp;|&nbsp;
          <a href="http://shop.roblox.com/" class="roblox-interstitial">Shop</a>
          <span class="LanguageOptionElement">&nbsp;|&nbsp;</span> 
          <span runat="server" navigateurl="/Parents.aspx" ref="footer-parents" class="LanguageOptionElement LanguageTrigger" drop-down-nav-button="LanguageTrigger">
            English&nbsp;<span class="FooterArrow">▼</span>
            <div class="dropuplanguagecontainer" style="display:none;" drop-down-nav-container="LanguageTrigger">
              <div class="dropdownmainnav" style="z-index:1023">
                <a href="/UserLanguage/LanguageRedirect?languageCode=de&amp;relativePath=%2flogin%2findex.html" class="LanguageOption js-lang" data-js-langcode="de"><span class="notranslate">Deutsch</span>&nbsp;(German) </a>
              </div>
            </div>
          </span>
        </div>
        <div class="FooterNav">
          <div id="SEOGenreLinks" class="SEOGenreLinks">
            <a href="/all-games">All Games</a> 
            <span>|</span>
            <a href="/building-games">Building</a> 
            <span>|</span>
            <a href="/horror-games">Horror</a> 
            <span>|</span>
            <a href="/town-and-city-games">Town and City</a> 
            <span>|</span>
            <a href="/military-games">Military</a> 
            <span>|</span>
            <a href="/comedy-games">Comedy</a> 
            <span>|</span>
            <a href="/medieval-games">Medieval</a> 
            <span>|</span>
            <a href="/adventure-games">Adventure</a> 
            <span>|</span>
            <a href="/sci-fi-games">Sci-Fi</a> 
            <span>|</span>
            <a href="/naval-games">Naval</a> 
            <span>|</span>
            <a href="/fps-games">FPS</a> 
            <span>|</span>
            <a href="/rpg-games">RPG</a> 
            <span>|</span>
            <a href="/sports-games">Sports</a> 
            <span>|</span>
            <a href="/fighting-games">Fighting</a> 
            <span>|</span>
            <a href="/western-games">Western</a> 
          </div>
        </div>
        <div class="legal">
          <div class="left">
            <div id="a15b1695-1a5a-49a9-94f0-9cd25ae6c3b2">
              <a href="https://privacy.truste.com/privacy-seal/Roblox-Corporation/validation?rid=2428aa2a-f278-4b6d-9095-98c4a2954215" title="TRUSTe Children privacy certification" target="_blank">
              <img style="border: none" src="https://privacy-policy.truste.com/privacy-seal/Roblox-Corporation/seal?rid=2428aa2a-f278-4b6d-9095-98c4a2954215" alt="TRUSTe Children privacy certification"/>
              </a>
            </div>
          </div>
          <div class="right">
            <p class="Legalese">
              ROBLOX, "Online Building Toy", characters, logos, names, and all related indicia are trademarks of <a href="http://corp.roblox.com/" ref="footer-smallabout" class="roblox-interstitial">ROBLOX Corporation</a>, ©2013. Patents pending.
              ROBLOX is not sponsored, authorized or endorsed by any producer of plastic building bricks, including The LEGO Group, MEGA Brands, and K'Nex, and no resemblance to the products of these companies is intended. Use of this site signifies your acceptance of the <a href="/info/terms-of-service" ref="footer-terms">Terms and Conditions</a>.
            </p>
          </div>
          <div class="clear"></div>
        </div>
      </div>
      </div>
      <div id="ChatContainer" style="position:fixed;bottom:0;right:0;z-index:1000;">
      </div>
      <script src="https://ssl.google-analytics.com/urchin.js" type="text/javascript"></script>
      <script type="text/javascript">
        _uacct = "UA-486632-1";
        _udn = "roblox.com";
        _uccn = "rbx_campaign";
        _ucmd = "rbx_medium";
        _ucsr = "rbx_source";
        urchinTracker();
        __utmSetVar('Visitor/Anonymous');
      </script>
    </form>
    <form id="FacebookLoginForm" action="/login/dologin.aspx" method="post">
      <input type="hidden" id="username" name="username"/>
      <input type="hidden" id="password" name="password"/>
      <input type="hidden" id="IsSyncUp" name="IsSyncUp"/>
      <input type="hidden" id="FacebookAssociation" name="FacebookAssociation"/>
      <input type="hidden" id="SNAccessToken" name="SNAccessToken"/>
    </form>
    <div id="InstallationInstructions" class="modalPopup blueAndWhite" style="display:none;overflow:hidden">
      <a id="CancelButton2" onclick="return Roblox.Client._onCancel();" class="ImageButton closeBtnCircle_35h ABCloseCircle"></a>
      <div style="padding-bottom:10px;text-align:center">
        <br/><br/>
      </div>
    </div>
    <div id="pluginObjDiv" style="height:1px;width:1px;visibility:hidden;position: absolute;top: 0;"></div>
    <iframe id="downloadInstallerIFrame" style="visibility:hidden;height:0;width:1px;position:absolute"></iframe>
    <script type="text/javascript" src="https://s3.amazonaws.com/js.roblox.com/d2f5e8e03fc1c07754f3ea93867113a9.js"></script>
    <script type="text/javascript">
      Roblox.Client._skip = '/install/download.aspx';
      Roblox.Client._CLSID = '';
      Roblox.Client._installHost = '';
      Roblox.Client.ImplementsProxy = false;
      Roblox.Client._silentModeEnabled = false;
      Roblox.Client._bringAppToFrontEnabled = false;
      
           Roblox.Client._installSuccess = function() { urchinTracker('InstallSuccess'); };
      
      $(function () {
          Roblox.Client.Resources = {
              //<sl:translate>
              here: "here",
              youNeedTheLatest: "You need Our Plugin for this.  Get the latest version from ",
              plugInInstallationFailed: "Plugin installation failed!",
              errorUpdating: "Error updating: "
              //</sl:translate>
          };
      });
      
    </script>
    <div id="PlaceLauncherStatusPanel" style="display:none;width:300px">
      <div class="modalPopup blueAndWhite PlaceLauncherModal" style="min-height: 160px">
        <div id="Spinner" class="Spinner" style="margin:0 1em 1em 0; padding:20px 0;">
          <img src="https://s3.amazonaws.com/images.roblox.com/e998fb4c03e8c2e30792f2f3436e9416.gif" alt="Progress"/>
        </div>
        <div id="status" style="min-height:40px;text-align:center;margin:5px 20px">
          <div id="Starting" class="PlaceLauncherStatus MadStatusStarting" style="display:block">
            Starting Roblox...
          </div>
          <div id="Waiting" class="PlaceLauncherStatus MadStatusField">Connecting to Players...</div>
          <div id="StatusBackBuffer" class="PlaceLauncherStatus PlaceLauncherStatusBackBuffer MadStatusBackBuffer"></div>
        </div>
        <div style="text-align:center;margin-top:1em">
          <input type="button" class="Button CancelPlaceLauncherButton translate" value="Cancel"/>
        </div>
      </div>
    </div>
    <script type="text/javascript" src="https://s3.amazonaws.com/js.roblox.com/e9724bc11c59b5cc6f16b4f82f2d5269.js"></script>
    <div id="videoPrerollPanel" style="display:none">
      <div id="videoPrerollTitleDiv">
        Gameplay sponsored by:
      </div>
      <div id="videoPrerollMainDiv"></div>
      <div id="videoPrerollCompanionAd"></div>
      <div id="videoPrerollLoadingDiv">
        Loading <span id="videoPrerollLoadingPercent">0%</span> - <span id="videoPrerollMadStatus" class="MadStatusField">Starting game...</span><span id="videoPrerollMadStatusBackBuffer" class="MadStatusBackBuffer"></span>
        <div id="videoPrerollLoadingBar">
          <div id="videoPrerollLoadingBarCompleted">
          </div>
        </div>
      </div>
      <div id="videoPrerollJoinBC">
        <span>Get more with Builders Club!</span>
        <a href="/Upgrades/BuildersClubMemberships.aspx?ref=vpr" target="_blank" id="videoPrerollJoinBCButton"></a>
      </div>
    </div>
    <script type="text/javascript">
      Roblox.VideoPreRoll.showVideoPreRoll = false;
      Roblox.VideoPreRoll.loadingBarMaxTime = 30000;
      Roblox.VideoPreRoll.videoOptions.key = "robloxcorporation";
      Roblox.VideoPreRoll.videoOptions.categories = "NonBC,IsLoggedIn,AgeUnknown,GenderUnknown";
           Roblox.VideoPreRoll.videoOptions.id = "games";
      Roblox.VideoPreRoll.videoLoadingTimeout = 11000;
      Roblox.VideoPreRoll.videoPlayingTimeout = 23000;
      Roblox.VideoPreRoll.videoLogNote = "NotWindows";
      Roblox.VideoPreRoll.logsEnabled = true;
      Roblox.VideoPreRoll.excludedPlaceIds = "32373412";
          
              Roblox.VideoPreRoll.specificAdOnPlacePageEnabled = true;
              Roblox.VideoPreRoll.specificAdOnPlacePageId = 157382;
              Roblox.VideoPreRoll.specificAdOnPlacePageCategory = "stooges";
          
          
              Roblox.VideoPreRoll.specificAdOnPlacePage2Enabled = true;
              Roblox.VideoPreRoll.specificAdOnPlacePage2Id = 88419564;
              Roblox.VideoPreRoll.specificAdOnPlacePage2Category = "lego";
          
      $(Roblox.VideoPreRoll.checkEligibility);
    </script>
    <div id="GuestModePrompt_BoyGirl" class="Revised GuestModePromptModal" style="display:none;">
      <div class="simplemodal-close">
        <a class="ImageButton closeBtnCircle_20h" style="cursor: pointer; margin-left:455px;top:7px; position:absolute;"></a>
      </div>
      <div class="Title">
        Choose Your Character
      </div>
      <div style="min-height: 275px; background-color: white;">
        <div style="clear:both; height:25px;"></div>
        <div style="text-align: center;">
          <div class="VisitButtonsGuestCharacter VisitButtonBoyGuest" style="float:left; margin-left:45px;"></div>
          <div class="VisitButtonsGuestCharacter VisitButtonGirlGuest" style="float:right; margin-right:45px;"></div>
        </div>
        <div style="clear:both; height:25px;"></div>
        <div class="RevisedFooter">
          <div style="width:200px;margin:10px auto 0 auto;">
            <a href="#" onclick="redirectPlaceLauncherToRegister(); return false;">
              <div class="RevisedCharacterSelectSignup"></div>
            </a>
            <a class="HaveAccount" href="#" onclick="redirectPlaceLauncherToLogin();return false;">I have an account</a>
          </div>
        </div>
      </div>
    </div>
    <script type="text/javascript">
      function checkRobloxInstall() {
               window.location = '/install/download.aspx'; return false;
      }
          if (typeof MadStatus === "undefined") {
              MadStatus = {};
          }
      
          MadStatus.Resources = {
              //<sl:translate>
              accelerating: "Accelerating",
      aggregating: "Aggregating",
      allocating: "Allocating",
              acquiring: "Acquiring",
      automating: "Automating",
      backtracing: "Backtracing",
      bloxxing: "Bloxxing",
      bootstrapping: "Bootstrapping",
      calibrating: "Calibrating",
      correlating: "Correlating",
      denoobing: "De-noobing",
      deionizing: "De-ionizing",
      deriving: "Deriving",
              energizing: "Energizing",
      filtering: "Filtering",
      generating: "Generating",
      indexing: "Indexing",
      loading: "Loading",
      noobing: "Noobing",
      optimizing: "Optimizing",
      oxidizing: "Oxidizing",
      queueing: "Queueing",
      parsing: "Parsing",
      processing: "Processing",
      rasterizing: "Rasterizing",
      reading: "Reading",
      registering: "Registering",
      rerouting: "Re-routing",
      resolving: "Resolving",
      sampling: "Sampling",
      updating: "Updating",
      writing: "Writing",
              blox: "Blox",
      countzero: "Count Zero",
      cylon: "Cylon",
      data: "Data",
      ectoplasm: "Ectoplasm",
      encryption: "Encryption",
      event: "Event",
      farnsworth: "Farnsworth",
      bebop: "Bebop",
      fluxcapacitor: "Flux Capacitor",
      fusion: "Fusion",
      game: "Game",
      gibson: "Gibson",
      host: "Host",
      mainframe: "Mainframe",
      metaverse: "Metaverse",
      nerfherder: "Nerf Herder",
      neutron: "Neutron",
      noob: "Noob",
      photon: "Photon",
      profile: "Profile",
      script: "Script",
      skynet: "Skynet",
      tardis: "TARDIS",
      virtual: "Virtual",
              analogs: "Analogs",
      blocks: "Blocks",
      cannon: "Cannon",
      channels: "Channels",
      core: "Core",
      database: "Database",
      dimensions: "Dimensions",
      directives: "Directives",
      engine: "Engine",
      files: "Files",
      gear: "Gear",
      index: "Index",
      layer: "Layer",
      matrix: "Matrix",
      paradox: "Paradox",
      parameters: "Parameters",
      parsecs: "Parsecs",
      pipeline: "Pipeline",
      players: "Players",
      ports: "Ports",
      protocols: "Protocols",
      reactors: "Reactors",
      sphere: "Sphere",
      spooler: "Spooler",
      stream: "Stream",
      switches: "Switches",
      table: "Table",
      targets: "Targets",
      throttle: "Throttle",
      tokens: "Tokens",
      torpedoes: "Torpedoes",
      tubes: "Tubes"
              //</sl:translate>
          };
    </script>
    <script type="text/javascript" src="https://s3.amazonaws.com/js.roblox.com/343f343e39d4c0b3e4b3460d9a6af05c.js"></script>
    <div class="ConfirmationModal modalPopup unifiedModal smallModal" data-modal-handle="confirmation" style="display:none;">
      <a class="genericmodal-close ImageButton closeBtnCircle_20h"></a>
      <div class="Title"></div>
      <div class="GenericModalBody">
        <div class="TopBody">
          <div class="ImageContainer roblox-item-image" data-image-size="small" data-no-overlays data-no-click>
            <img class="GenericModalImage" alt="generic image"/>
          </div>
          <div class="Message"></div>
        </div>
        <div class="ConfirmationModalButtonContainer">
          <a href roblox-confirm-btn><span></span></a>
          <a href roblox-decline-btn><span></span></a>
        </div>
        <div class="ConfirmationModalFooter">
        </div>
      </div>
      <script type="text/javascript">
        //<sl:translate>
        Roblox.GenericConfirmation.Resources = { yes: "Yes", No: "No" }
        //</sl:translate>
      </script>
    </div>
  </body>
</html>
<!--
  FILE ARCHIVED ON 02:07:49 Oct 27, 2013 AND RETRIEVED FROM THE
  INTERNET ARCHIVE ON 00:26:23 Nov 03, 2018.
  JAVASCRIPT APPENDED BY WAYBACK MACHINE, COPYRIGHT INTERNET ARCHIVE.
  
  ALL OTHER CONTENT MAY ALSO BE PROTECTED BY COPYRIGHT (17 U.S.C.
  SECTION 108(a)(3)).
  -->
<!--
  playback timings (ms):
    LoadShardBlock: 160.428 (3)
    esindex: 0.007
    captures_list: 195.968
    CDXLines.iter: 20.439 (3)
    PetaboxLoader3.datanode: 94.292 (4)
    exclusion.robots: 0.259
    exclusion.robots.policy: 0.246
    RedisCDXSource: 1.578
    PetaboxLoader3.resolve: 98.752
    load_resource: 124.433
  -->