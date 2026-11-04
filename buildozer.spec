[app]
title = DriverOS Local
package.name = driveroslocal
package.domain = com.driveros.local
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,kt,xml
version = 1.0.0
requirements = python3,flet,pyjnius

orientation = portrait
fullscreen = 0
android.permissions = INTERNET,SYSTEM_ALERT_WINDOW,BIND_ACCESSIBILITY_SERVICE
android.api = 34
android.minapi = 26
android.ndk = 25b
android.skip_update = False
android.accept_sdk_license = True
