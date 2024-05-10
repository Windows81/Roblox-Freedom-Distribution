I had to patch 2018M to allow the web server to be open at any port.
The endpoints `/api.GetAllowedMD5Hashes/` and `/api.GetAllowedSecurityVersions/` wanted to remove the port number.
That's because there's a piece of compiled code in 2018M which would transform the host https://localhost:2006 to something which resolved to https://localhost/localhost:2006. Don't quote me. You can also see it works about the same per 16src. If you want to add a build from near 2016, keep this in mind.

My goal is to get the bootstrapping of clients to be as similar as possible between Rōblox versions. I also name my versions after their numbers. I use v348 (2018M) and v463 (2021E). I want my versions to be close to 100 apart.
