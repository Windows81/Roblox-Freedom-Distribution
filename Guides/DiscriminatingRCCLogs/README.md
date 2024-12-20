So we need to extract every valid FLog setting.

But we don't have the FFlags for 2018M available. But 16src has [this information](https://github.com/Jxys3rrV/roblox-2016-source-code/blob/4de2dc3a380e1babe4343c49a4341ceac749eddb/App/v8datamodel/FastLogSettings.cpp#L9) and more.

## Where to get the flags from?

So we're going to combine:

### FLogs from 16src

I've attached some of the flags to [a text file](./flogs-16src.txt). Flags are defined in code by a C++ macro called `LOGVARIABLE` or `DYNAMIC_LOGVARIABLE` and have a default value provided with them. So I've preserved the call syntax. The first 81 are copied from `FastLogSettings.cpp`, whereas [the rest are taken from other places in 16src](https://github.com/search?q=repo%3AJxys3rrV%2Froblox-2016-source-code+%28%2F%28%3F-i%29DYNAMIC_LOGVARIABLE%5C%28%2F+OR+%2F%28%3F-i%29LOGVARIABLE%5C%28%2F%29&type=code).

### The 2021E FFlags

Not very useful for RCC, as some important log flags such as `RCCServiceInit` are not included.

Flags were collected from [MaximumADHD/Roblox-FFlag-Tracker](https://github.com/MaximumADHD/Roblox-FFlag-Tracker/blob/50e7d23fb6723871b6f960b2ff530099e2485be0/PCDesktopClient.json).

Consult [this text file](./flogs-2021E.txt).

### The 2019 Sitetest4 deployment

Taken from [`Roblox.Settings.json`](https://github.com/FlarfGithub/RobloxLabs-Roblox.SiteTest4/blob/6286186bcf2adc898b7c9c04bf9d2fdc4ae69f81/Default/Roblox.Settings.json#L131). Processed to remove duplicates. But I also got rid of the various defaults.

Consult [this text file](./flogs-sitetest4.txt).

### Miscellaneous flags from my personal experience

I've also added FLog names such as `Output` and `RCCServiceJobs` since they show up a lot in my logs for 2021E servers.

Just to make sure, I kept track of which FFlags are used the most. This is done by counting how many times each FFlag appears in [a typical log file](./dev_20241211T185113Z_RCC_11372_last.log).

```py
import re, collections
with open('./dev_20241211T185113Z_RCC_11372_last.log', 'r') as log_file: # Replace with your log file path.
    log_entries = log_file.readlines()

log_entry_counts = collections.defaultdict(int)
for entry in log_entries:
    function_names = re.findall(r'(?<=FLog::)([^\]]+)', line)
    for name in function_names:
        log_entry_counts[name] += 1
```

The results are shown below:

| FLog Name      | Count |
| -------------- | ----- |
| RCCServiceInit | 1     |
| LocalStorage   | 2     |
| RCCServiceJobs | 5     |
| RCCExecuteInfo | 8     |
| Output         | 16    |
| NetworkAudit   | 95    |
| Error          | 8832  |

Not much variety in what FLogs are shown by default.

Notice how `[FLog::Output]` is always preceded by `6` and `[DFLog::NetworkAudit]` is preceded by `19`?

These are their default 'log levels'. FLogs with a log level below `6` do not display in the RCC log. The values `6` and `19` correspond to the default values for the `FLogNetworkAudit` and `FLogOutput` flags, respectively.

You can define these values in the following files:

- For 2018M: `./ClientSettings/RCCService.json`
- For 2021E: `./DevSettingsFile.json`

## What I did next

So I combined the files into [a single list](./flogs-all.txt) (inputs are ordered below) and removed duplicates from that.

- FLogs taken as-is from the table above.
- In [the 16src list](./flogs-16src.txt), I did regex replacement `.+\(([^,]+)(, .+)?\)` with `$1`.
- No modifications done from the [sitetest](./flogs-sitetest4.txt) list.
- In [the 2021E list](./flogs-2021E.txt), I did regex replacement `"D?FLog([^"]+)": .+` with `$1`.

Then...

```shell
awk '{print "\"FLog" $0 "\": " NR+100-1 ","}' "flogs-all.txt" > flogs-json-snippet.txt
```

We start with a value of 100 to ensure that each custom log levels will be unique and won't clash with any standard or predefined log levels.

I notice that for 2018M, the `RCCServiceInit` always sticks to 6. So we have to treat it specially. So 6 is reserved for `RCCServiceInit`. We also need to ensure that `RCCServiceInit` is not included in the list of custom log levels.
