## Asset Packs

Assets are automatically cached server-side in directory `./AssetCache`. To manually add assets, place the raw data in a file named with the iden number or string _without_ any extension.

The following are examples of asset idens resolving to cache files:

| Asset Iden                    | File Name          | Format |
| ----------------------------- | ------------------ | ------ |
| `rbxassetid://1818`           | `./00000001818`    | `%11d` |
| `rbxassetid://5950704`        | `./00005950704`    | `%11d` |
| `rbxassetid://97646706196482` | `./97646706196482` | `%11d` |
| `rbxassetid://custom-asset`   | `./custom-asset`   | `%s`   |
