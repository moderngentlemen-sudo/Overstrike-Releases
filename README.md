# Overstrike releases

Downloads and balance hotfixes for **Overstrike**, an original 6v6 hero shooter. The game's source is
private; this repository only holds what players' games fetch.

- **Download the game:** [latest release](https://github.com/moderngentlemen-sudo/Overstrike-Releases/releases/latest).
  Unzip it and run `Sixfold.exe`.
- **Balance hotfixes:** [`hotfix.txt`](hotfix.txt). Every Overstrike game reads it when it checks for
  updates (the **Updates** button on the main menu, and once at launch).

## Publishing a balance hotfix

1. Edit `hotfix.txt` (on github.com: open it, click the pencil).
2. Give it a new `@id` (for example the date, `2026-11-14a`). Players only see "Update ready" when
   the id changes.
3. Write one change per line: `path = value`. Times are in seconds.
4. Commit. The **Check hotfix** action checks the format; players get the hotfix on their next check
   (GitHub's cache can take up to about five minutes).

```text
@id = 2026-11-14a
@game = 0.9.0
@notes = Wisp: reload 0.5 s. Kestrel: Skyfall shells 120.
@latest = 0.9.0
@download = https://github.com/moderngentlemen-sudo/Overstrike-Releases/releases/latest

wisp.ReloadSeconds = 0.5
kestrel.Ultimate.OnStart.0.Damage = 120
status.marked.duration = 4
```

| Setting | Meaning |
|---|---|
| `@id` | Names this hotfix. Change it every time you publish. |
| `@notes` | Shown to players before they install. Repeat the line for more lines. |
| `@game` | Only games of this version install it (a hotfix for 0.9.0 would mis-tune 0.10.0). |
| `@latest` | The newest full build. Older games show "Version X is out" with a Download button. |
| `@download` | Where that build is (normally the latest release here). |

- **Paths** start at a hero id (`wisp`, `kestrel`, `warden`, ...) or `status.<id>`. Every path and its
  current number is listed in the game project's `Docs/TUNING_REFERENCE.txt` (made in the Unity editor
  with **Sixfold → Hotfix → Write Tuning Reference**). Before publishing, **Sixfold → Hotfix → Check
  Hotfix File...** confirms every path exists.
- A hotfix can only change existing numbers and on/off switches. New abilities, effects, maps and code
  fixes need a new build.
- A new hotfix replaces the previous one. To go back to the built-in balance, publish a new `@id`
  with no value lines.
- Every published hotfix is a commit: to roll back, revert the commit (it keeps its old `@id`, so
  change the id when you revert).
- In online play, the host's hotfix is used by everyone in the match.

## Publishing a new version

1. In the game project raise `GameVersion.Current`, build (**Sixfold → Build Windows Player**) and
   zip the build folder as `Overstrike-<version>-Windows64.zip` (or push a `v<version>` tag to have
   the game repository's Release workflow do the build and the next two steps).
2. Create a release here tagged `v<version>` and attach the zip.
3. In `hotfix.txt`: set `@latest` and `@game` to the new version, give it a new `@id`, and clear
   value lines meant for the old version.
